import streamlit as st
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

@st.cache_resource
def get_engine():
    return create_engine(
        f"mysql+pymysql://db31521:{quote_plus(st.secrets['DB_PASSWORD'])}"
        "@db31521.public.databaseasp.net:3306/db31521",
        pool_pre_ping=True,
        pool_recycle=3600,
    )

def verify_user(username, password):
    try:
        engine = get_engine()
        with engine.connect() as conn:
            row = conn.execute(
                text("SELECT * FROM users WHERE username=:u AND password=:p"),
                {"u": username, "p": password}
            ).fetchone()
        return dict(row._mapping) if row else None
    except Exception as e:
        st.error(f"DB error: {e}")
        return None

def show_login():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = verify_user(username, password)

        if user:
            st.session_state.logged_in = True
            st.session_state.full_name = user.get("full_name", username)
            st.session_state.role = user.get("role", "ASM")
            st.session_state.region = user.get("region", "ALL")
            st.session_state.unit = user.get("unit", "ALL")
            st.session_state.asm_code = user.get("asm_code", "ALL")

            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")