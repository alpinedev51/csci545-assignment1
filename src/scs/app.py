import sqlite3
import time
from datetime import datetime

import pandas as pd
import streamlit as st
import torch
from PIL import Image
from torchvision import models, transforms

from scs.database import DB_FILE, init_db


def log_meal(food, weight, macros):
    """Insert a new entry into the local database."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.execute(
        "INSERT INTO food_logs (date, food_item, weight_g, calories, protein, carbs, fats) VALUES (?,?,?,?,?,?,?)",
        (timestamp, food, weight, *macros),
    )
    conn.commit()
    conn.close()


def get_logs():
    """Fetch logs to display in the GUI."""
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM food_logs ORDER BY id DESC", conn)
    conn.close()
    return df


@st.cache_resource
def load_model():
    weights = models.MobileNet_V2_Weights.DEFAULT
    model = models.mobilenet_v2(weights=weights)
    model.eval()

    preprocess = transforms.Compose(
        [
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    return model, preprocess, weights.meta["categories"]


def predict_image(image, model, preprocess, categories):
    start_time = time.time()

    input_tensor = preprocess(image)
    input_batch = input_tensor.unsqueeze(0)

    with torch.no_grad():
        output = model(input_batch)

    end_time = time.time()

    inference_time_ms = (end_time - start_time) * 1000

    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    top5_prob, top5_catid = torch.topk(probabilities, 5)

    debug_preds = []
    for i in range(5):
        raw_class_name = categories[top5_catid[i]]
        confidence = top5_prob[i].item() * 100
        debug_preds.append(f"{raw_class_name} ({confidence:.2f}%)")

    top1_prob, top1_catid = torch.topk(probabilities, 1)

    top1_raw_label = categories[top1_catid]

    label_map = {
        "broccoli": "Broccoli",
        "cucumber": "Cucumber",
        "mushroom": "Mushroom",
        "bell pepper": "Bell Pepper",
        "strawberry": "Strawberry",
        "lemon": "Lemon",
        "saltshaker": "Salt",
        "bagel": "Bagel",
        "Guacamole": "Guacamole",
    }

    mapped_label = "Unknown"
    for key, value in label_map.items():
        if key in top1_raw_label.lower():
            mapped_label = value
            break

    debug_info = {
        "inference_time": f"{inference_time_ms:.2f} ms",
        "top_1_raw": top1_raw_label,
        "top_1_prob": top1_prob,
        "top_5_list": debug_preds,
    }

    return mapped_label, debug_info


def main():
    st.set_page_config(page_title="Sovereign Prep Station", page_icon="🥗")
    st.title("Sovereign Whole-Health Station")
    st.caption("Offline - Local Compute - Privacy First")

    init_db()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("1. The 'Cutting Board'")
        uploaded_file = st.file_uploader(
            "Place Item on Scale (Upload Image)", type=["jpg", "png", "jpeg"]
        )

        if uploaded_file is not None:
            image = Image.open(uploaded_file).convert("RGB")
            st.image(image, caption="Live Camera Feed", width="stretch")

            model, preprocess, categories = load_model()
            with st.spinner("Running Local Inference..."):
                detected_food, debug_info = predict_image(
                    image, model, preprocess, categories
                )

            with st.expander("🔍 See Computer Vision Logs"):
                st.write(f"**Inference Time:** {debug_info['inference_time']}")
                st.write(f"**Raw ImageNet Class:** `{debug_info['top_1_raw']}`")
                st.write("**Top 5 Probabilities:**")
                st.json(debug_info["top_5_list"])

            if detected_food == "Unknown":
                st.error(f"Could not map '{debug_info['top_1_raw']}' to inventory.")
            else:
                st.success(f"Detected: **{detected_food}**")

                st.markdown("---")
                st.subheader("2. The Scale")
                weight = st.number_input(
                    "Weight reading (grams)", min_value=0.0, value=150.0, step=10.0
                )

                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM inventory WHERE name=?", (detected_food,))
                data = cursor.fetchone()
                conn.close()

                if data:
                    factor = weight / 100.0
                    macros = (
                        round(data[1] * factor, 1),  # Cals
                        round(data[2] * factor, 1),  # Protein
                        round(data[3] * factor, 1),  # Carbs
                        round(data[4] * factor, 1),  # Fat
                    )

                    st.metric(label="Estimated Calories", value=f"{macros[0]} kcal")
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Protein", f"{macros[1]}g")
                    m2.metric("Carbs", f"{macros[2]}g")
                    m3.metric("Fats", f"{macros[3]}g")

                    if st.button("Log Portion"):
                        log_meal(detected_food, weight, macros)
                        st.toast(f"Logged {weight}g of {detected_food}!", icon="✅")
                else:
                    st.warning("Item not found in local inventory.")

    with col2:
        st.subheader("3. Local Database Logs")
        st.markdown("Existing entries in `nutrition_logs.db`")
        df = get_logs()
        st.dataframe(df, width=True)

        if not df.empty:
            st.bar_chart(df, x="food_item", y="calories")


if __name__ == "__main__":
    main()
