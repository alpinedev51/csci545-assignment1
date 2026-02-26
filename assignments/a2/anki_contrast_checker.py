import tkinter as tk
from tkinter import messagebox
from typing import Tuple

# --- CSCI HCI 545/445 assignment 2 --
# -- Accessibility Improvement Python Script --
# -- For Anki --
# This script simulates a feature that would be embedded in Anki's card creator feature.
# This script provides feedback to prevent the user frmo creating cards that are
# inaccessible. Specifically, violations of WCAG 1.4.3 Minimum Contrast.

# You can run this script with Python 3.14. You shouldn't need anything else, as tkinter comes natively with Python.
# However, if it shows you don't have tkinter installed, it's probably because you used something like brew to install
# Python. Some managers strip tkinter from Python to make it more lightweight.
# In that case, you can make a virtual env and install Python 3.14 with something like uv, then use that virtual environment.

def hex_to_rgb(hex_color) -> Tuple:
    """Converts a hex color string to an RGB tuple."""
    hex_color = hex_color.lstrip('#') # remove the # symbol for the hex. Should be 6 hex digits following one # symbol.
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def get_luminance(r, g, b):
    """Calculates relative luminance using the WCAG formula. Source: https://www.w3.org/WAI/GL/wiki/Relative_luminance"""
    # normalize RGB values.
    a = [v / 255.0 for v in [r, g, b]]
    # use WCAG formula
    return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722
    # return sum(a)

def calculate_contrast():
    """Calculates contrast ratio and updates the UI with messages indicating compliance with accessibility standards."""
    try:
        # get user input
        fg_hex = fg_entry.get() # font color
        bg_hex = bg_entry.get() # background color

        # convert to RGB
        fg_rgb = hex_to_rgb(fg_hex)
        bg_rgb = hex_to_rgb(bg_hex)

        # calculate luminance
        l1 = get_luminance(*fg_rgb)
        l2 = get_luminance(*bg_rgb)

        # Ensure l1 is the lighter color for the ratio formula
        if l1 < l2:
            l1, l2 = l2, l1

        # WCAG Contrast Ratio formula: (L1 + 0.05) / (L2 + 0.05)
        ratio = (l1 + 0.05) / (l2 + 0.05)

        # Update the UI with result - shows compliance with WCAG standards
        result_text = f"Contrast Ratio: {ratio:.2f}:1\n"
        if ratio >= 7:
            result_text += "Passes WCAG AAA (Excellent!)"
            result_label.config(fg="#008800") # Medium green for
        elif ratio >= 4.5:
            result_text += "Passes WCAG AA (Good)"
            result_label.config(fg="#4444FF") # Bright blue/purple
        else:
            result_text += "Fails WCAG Standards (Do not use!)"
            result_label.config(fg="#CC0000") # Dark red

        result_label.config(text=result_text)

        # Show the user what their text will look like on the generated flashbard
        preview_label.config(fg=fg_hex, bg=bg_hex, text="Preview: Flashcard Text")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid Hex color codes (e.g., #FFFFFF).")

root = tk.Tk()
root.title("Anki Contrast Checker Prototype")
root.geometry("350x320")

# Input for text colors
tk.Label(root, text="Text Color (Hex):", font=("Arial", 10, "bold")).pack(pady=(15, 0))
fg_entry = tk.Entry(root, justify="center")
fg_entry.insert(0, "#FFFFFF")
fg_entry.pack(pady=5)

# Input for background color
tk.Label(root, text="Background Color (Hex):", font=("Arial", 10, "bold")).pack(pady=(10, 0))
bg_entry = tk.Entry(root, justify="center")
bg_entry.insert(0, "#2F2F31") # Default Anki dark mode background
bg_entry.pack(pady=5)

# evaluate contrast action button
check_btn = tk.Button(root, text="Evaluate Contrast", command=calculate_contrast, cursor="hand2")
check_btn.pack(pady=15)

# result display label
result_label = tk.Label(root, text="Enter colors and click evaluate.", font=("Arial", 11))
result_label.pack(pady=5)

# preview area label
preview_label = tk.Label(root, text="Preview Area", font=("Arial", 14), width=25, height=2, relief="solid", borderwidth=1)
preview_label.pack(pady=10)

# Run
root.mainloop()
