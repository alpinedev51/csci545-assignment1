# Sovereign Whole-Health Station

**An offline-first, privacy-centric meal preparation assistant.**

This prototype demonstrates a "Sovereign Tech" approach to health tracking. Unlike commercial smart kitchen devices that rely on cloud APIs, subscription models, and data mining, this workstation runs entirely on `localhost`. It uses edge-computing (simulated via local Python scripts) to identify whole food ingredients and log nutritional density without a single packet of data leaving your machine.

---

## 🚀 Features

* **Local Computer Vision:** Identifies whole ingredients (Broccoli, Steak, etc.) using an on-device neural network.
* **Privacy-First Logging:** All data is stored in a local SQLite database (`nutrition_logs.db`).
* **Simulated Hardware Integration:**
    * **"The Camera":** Upload an image to simulate the overhead camera feed.
    * **"The Scale":** Manual input simulates the load-cell reading.
* **Modular Architecture:** Decoupled inventory management and logging systems.

---

## 🛠️ Installation & Usage

This project is managed using `uv`, a distinctively fast Python package manager.

### Prerequisites
* [uv](https://github.com/astral-sh/uv) installed on your system.
* Python 3.10+

### Running the App
You do not need to manually create a virtual environment; `uv` handles dependencies on the fly.

1.  **Clone/Navigate to the directory:**
    ```bash
    cd csci545-assignment1
    ```

2.  **Run the Streamlit Server:**
    Use `uv` to execute the `streamlit` module within the context of the project dependencies.
    ```bash
    uv run streamlit run src/csci545_assignment1/app.py
    ```

3.  **Access the Interface:**
    The application will automatically open in your default browser at `http://localhost:8501`.

---

## 🧠 The AI Model & Dataset

To maintain the "offline" requirement, this project utilizes a lightweight Convolutional Neural Network (CNN) rather than a heavy cloud-based API (like GPT-4 Vision).

### The Model: MobileNetV2
We utilize **MobileNetV2**, a model architecture optimized for mobile and embedded vision applications.
* **Why this model?** It uses inverted residual blocks with linear bottlenecks, significantly reducing the parameter count and computational complexity. This allows it to run inference efficiently on standard CPUs (or potential edge devices like a Raspberry Pi) without needing a dedicated GPU or internet connection.
* **Inference Speed:** Typical inference time on a standard laptop CPU is <50ms per image.

### The Dataset: ImageNet-1K
The model was pre-trained on the **ImageNet (ILSVRC-2012-CLS)** dataset.
* **Scale:** Approximately 1.28 million training images.
* **Classes:** The model can distinguish between **1,000 distinct classes**.
* **Classes of Interest:** While ImageNet contains many non-food items (e.g., "Golden Retriever", "Aircraft Carrier"), it includes specific whole-food classes utilized by this application:
    * `937: broccoli`
    * `943: cucumber, cuke`
    * `947: mushroom`
    * `945: bell pepper`

### The "Sovereign" Gap
Since ImageNet is a general-purpose dataset, this application implements a **mapping layer**. The raw output from the neural network (e.g., `Class 937`) is intercepted and mapped to the user's local `inventory` table (e.g., `Broccoli`). In a production version of this device, a custom model (YOLO) would be fine-tuned specifically on the user's pantry items to improve accuracy and remove the need for this translation layer.

---

## 📂 Project Structure

```text
csci545-assignment1/
├── README.md               # You are here
├── pyproject.toml          # Dependency definitions
├── uv.lock                 # Lock file for reproducible builds
└── src/
    └── csci545_assignment1/
        ├── app.py          # Main GUI and CV Logic
        └── database.py     # SQLite init and connection logic
```
