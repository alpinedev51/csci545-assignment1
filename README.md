# Sovereign Whole-Health Station

**An offline-first, privacy-centric meal preparation assistant.**

This prototype demonstrates a "Sovereign Tech" approach to health tracking. Unlike commercial smart kitchen devices that rely on cloud APIs, subscription models, and data mining, this workstation runs entirely on `localhost`. It uses edge-computing (simulated via local Python scripts) to identify whole food ingredients and log nutritional density without a single packet of data leaving your machine.

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
    cd scs
    ```

2.  **Run the Streamlit Server:**
    Use `uv` to execute the `streamlit` module within the context of the project dependencies.
    ```bash
    uv run streamlit run src/scs/app.py
    ```

3.  **Access the Interface:**
    The application will automatically open in your default browser at `http://localhost:8501`.

## Project Structure

```text
scs/
├── README.md               # You are here
├── pyproject.toml          # Dependency definitions
├── uv.lock                 # Lock file for reproducible builds
└── src/
    └── scs/
        ├── app.py          # Main GUI and CV Logic
        └── database.py     # SQLite init and connection logic
```
