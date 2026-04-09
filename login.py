import streamlit as st
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

# ── DB Connection ───────────────────────────────────────────────────────────────
@st.cache_resource
def get_engine():
    host     = "db31521.public.databaseasp.net"
    port     = 3306
    database = "db31521"
    username = "db31521"
    password = quote_plus(st.secrets["DB_PASSWORD"])
    return create_engine(
        f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}",
        pool_pre_ping=True,
        pool_recycle=3600,
    )


def verify_user(username: str, password: str):
    try:
        engine = get_engine()
        with engine.connect() as conn:
            row = conn.execute(
                text("SELECT * FROM users WHERE username=:u AND password=:p"),
                {"u": username, "p": password}
            ).fetchone()
        if row:
            return dict(row._mapping)
        return None
    except Exception as e:
        st.error(f"DB error: {e}")
        return None


def show_login():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

    * { font-family: 'Outfit', sans-serif !important; box-sizing: border-box; }

    .stApp {
        background: linear-gradient(135deg, #060818 0%, #0d1117 50%, #060818 100%);
        min-height: 100vh;
    }

    /* Hide streamlit default elements */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 0 !important; max-width: 100% !important; }

    /* Animated background dots */
    .bg-dots {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background-image: radial-gradient(circle, #1e2130 1px, transparent 1px);
        background-size: 40px 40px;
        opacity: 0.4;
        z-index: 0;
        pointer-events: none;
    }

    /* Login container */
    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        padding: 20px;
        position: relative;
        z-index: 1;
    }

    .login-box {
        background: linear-gradient(145deg, #0d1117 0%, #111827 100%);
        border: 1px solid #1f2937;
        border-radius: 28px;
        padding: 52px 44px;
        width: 100%;
        max-width: 440px;
        box-shadow:
            0 25px 60px rgba(0,0,0,0.6),
            0 0 0 1px rgba(99,102,241,0.1),
            inset 0 1px 0 rgba(255,255,255,0.05);
        animation: fadeInUp 0.6s ease;
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    .brand-wrap {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 14px;
        margin-bottom: 10px;
    }

    .brand-logo {
        width: 52px; height: 52px;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        border-radius: 16px;
        display: flex; align-items: center; justify-content: center;
        font-size: 26px;
        box-shadow: 0 8px 20px rgba(99,102,241,0.3);
    }

    .brand-name {
        font-size: 32px;
        font-weight: 800;
        background: linear-gradient(135deg, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
    }

    .brand-tagline {
        text-align: center;
        color: #4b5563;
        font-size: 13px;
        font-weight: 500;
        letter-spacing: 0.5px;
        margin-bottom: 40px;
    }

    .input-label {
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        color: #6b7280;
        margin-bottom: 8px;
        display: block;
    }

    /* Input styling */
    .stTextInput > div > div > input {
        background: #161b2e !important;
        border: 1.5px solid #1f2937 !important;
        border-radius: 14px !important;
        color: #f9fafb !important;
        padding: 14px 18px !important;
        font-size: 15px !important;
        font-family: 'Outfit', sans-serif !important;
        transition: all 0.2s !important;
        height: 52px !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
        background: #1a1f35 !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #374151 !important;
    }

    /* Button */
    .stButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 16px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        font-family: 'Outfit', sans-serif !important;
        letter-spacing: 0.3px !important;
        cursor: pointer !important;
        transition: all 0.3s !important;
        height: 54px !important;
        margin-top: 8px !important;
        box-shadow: 0 4px 15px rgba(99,102,241,0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(99,102,241,0.45) !important;
    }
    .stButton > button:active {
        transform: translateY(0) !important;
    }

    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #1f2937, transparent);
        margin: 28px 0;
    }

    .footer-text {
        text-align: center;
        color: #1f2937;
        font-size: 12px;
        margin-top: 32px;
    }

    /* Error/success */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
    }
    </style>

    <div class="bg-dots"></div>
    """, unsafe_allow_html=True)

    # Center the login form
    _, col, _ = st.columns([1, 1.4, 1])

    with col:
        st.markdown("<div style='height: 60px'></div>", unsafe_allow_html=True)

        # Brand
        st.markdown("""
        <div class="brand-wrap">
            <div class="brand-logo">💊</div>
            <div class="brand-name">SalesPulse</div>
        </div>
        <div class="brand-tagline">PHARMA SALES INTELLIGENCE PLATFORM</div>
        """, unsafe_allow_html=True)

        # Input fields
        st.markdown("<span class='input-label'>Username</span>", unsafe_allow_html=True)
        username = st.text_input("", placeholder="Enter your username", key="username_input",
                                 label_visibility="collapsed")

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        st.markdown("<span class='input-label'>Password</span>", unsafe_allow_html=True)
        password = st.text_input("", placeholder="Enter your password", type="password",
                                 key="password_input", label_visibility="collapsed")

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # Login button
        if st.button("Sign In →", use_container_width=True):
            if not username or not password:
                st.error("⚠️ Please enter both username and password.")
            else:
                with st.spinner("Authenticating..."):
                    user = verify_user(username.strip(), password.strip())
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user      = user
                    st.session_state.username  = user['username']
                    st.session_state.full_name = user.get('full_name', username)
                    st.session_state.role      = user.get('role', 'ASM')
                    st.session_state.region    = user.get('region', 'ALL')
                    st.session_state.unit      = user.get('unit', 'ALL')
                    st.session_state.asm_code  = user.get('asm_code', 'ALL')
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password. Please try again.")

        st.markdown("""
        <div class="divider"></div>
        <div class="footer-text">
            © 2026 SalesPulse • Entero Healthcare • All rights reserved
        </div>
        """, unsafe_allow_html=True)