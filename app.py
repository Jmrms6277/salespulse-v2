import streamlit as st

st.set_page_config(
    page_title="SalesPulse",
    page_icon="💊",
    layout="wide",
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    from login import show_login
    show_login()
else:
    from dashboard import show_dashboard
    show_dashboard()