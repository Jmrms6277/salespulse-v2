import streamlit as st

st.set_page_config(
    page_title="Ent Retail Sales dashboard",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Hide sidebar collapse button
st.markdown("""
<style>
[data-testid="collapsedControl"] { display: none !important; }
span[data-testid="stIconMaterial"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None

if not st.session_state.logged_in:
    from login import show_login
    show_login()
else:
    from dashboard import show_dashboard
    show_dashboard()
