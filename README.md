# SalesPulse Streamlit App

This repository contains the Entero Healthcare SalesPulse dashboard built with Streamlit.

## Run locally

1. Create and activate the virtual environment:
   - Windows PowerShell:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```

2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

3. Run the app:
   ```powershell
   streamlit run app.py
   ```

4. Open the app in your browser:
   - http://localhost:8501

## Streamlit Cloud deployment

To host this app on Streamlit Cloud:

1. Push the repository to a GitHub repository.
2. Create a new Streamlit Cloud app and connect it to the GitHub repo.
3. Set the `Python` branch to the branch you pushed.
4. Add the following secret in Streamlit Cloud:
   - `DB_PASSWORD`

## Secrets

- Do not commit `.streamlit/secrets.toml` to source control.
- On Streamlit Cloud, configure `DB_PASSWORD` in the Secrets section.
