import streamlit as st

def show_dashboard():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.main { background: #0f1117; }
                
/* Hide menu & footer */
#MainMenu, footer { visibility: hidden; }

/* 🔥 Remove header space completely */
header {
    visibility: hidden;
    height: 0px !important;
    margin: 0px !important;
    padding: 0px !important;
}

/* 🔥 Remove top spacing from main page */
.block-container {
    padding-top: 0rem !important;
}

/* KPI cards */
.kpi-card {
    background: linear-gradient(135deg, #1e2130 0%, #252840 100%);
    border: 1px solid #2e3250;
    border-radius: 16px;
    padding: 20px 24px;
    text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
}
.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(99,102,241,0.15);
}
.kpi-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #6b7280;
    margin-bottom: 6px;
}
.kpi-value {
    font-size: 28px;
    font-weight: 700;
    color: #f9fafb;
    font-family: 'DM Mono', monospace;
}
.kpi-sub {
    font-size: 12px;
    color: #10b981;
    margin-top: 4px;
}

/* Date banner */
.date-banner {
    background: linear-gradient(135deg, #1a1f35 0%, #1e2540 100%);
    border: 1px solid #2e3250;
    border-left: 4px solid #6366f1;
    border-radius: 12px;
    padding: 14px 24px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 40px;
}
.date-banner-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #6b7280;
    margin-bottom: 4px;
}
.date-banner-value {
    font-size: 16px;
    font-weight: 700;
    color: #a5b4fc;
    font-family: 'DM Mono', monospace;
}

/* Section headers */
.section-header {
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #6366f1;
    margin: 24px 0 12px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid #1e2130;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0d0f1a !important;
    border-right: 1px solid #1e2130;
}
</style>
""", unsafe_allow_html=True)

    full_name = st.session_state.get('full_name', 'User')
    role      = st.session_state.get('role', 'ASM')

    with st.sidebar:
        st.markdown("""
        <div style='text-align:center; padding:20px 0 16px;'>
            <div style='font-size:36px'>💊</div>
            <div style='font-size:20px; font-weight:800;
                background:linear-gradient(135deg,#818cf8,#c084fc);
                -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
                SalesPulse
            </div>
            <div style='font-size:10px; color:#374151; letter-spacing:1.5px; margin-top:2px;'>
                PHARMA INTELLIGENCE
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='user-badge'>
            <div style='font-size:10px; color:#6b7280; margin-bottom:2px; letter-spacing:1px;'>SIGNED IN AS</div>
            <div style='font-size:14px; font-weight:700; color:#e5e7eb;'>👤 {full_name}</div>
            <div style='font-size:11px; color:#6366f1; margin-top:2px; font-weight:600;'>{role}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='font-size:10px;color:#374151;letter-spacing:2px;font-weight:700;margin:14px 0 6px;padding-left:4px;'>MAIN MENU</div>", unsafe_allow_html=True)

        page = st.radio("nav", [
            "📊  Sales",
            "💊  CP Sales",
            "📅  FY Sales",
            "📈  Sales Metrics",
            "💰  Outstanding",
            "📉  L10D Trend",
            "🔍  GP Leakage",
            "💵  Cash Receipt",
        ], label_visibility="collapsed", key="main_nav")

        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()

        st.markdown("<div style='text-align:center;color:#1f2937;font-size:11px;margin-top:16px;'>SalesPulse v2.0<br>Entero Healthcare</div>", unsafe_allow_html=True)

    # ── Page Routing ──────────────────────────────────────────────────────────
    if page == "📊  Sales":
        from pages_.sales import show
        show()
    elif page == "💊  CP Sales":
        from pages_.cp_sales import show
        show()
    elif page == "📅  FY Sales":
        from pages_.fy_sales import show
        show()
    elif page == "📈  Sales Metrics":
        from pages_.sales_metrics import show
        show()
    elif page == "💰  Outstanding":
        from pages_.outstanding import show
        show()
    elif page == "📉  L10D Trend":
        from pages_.l10d_trend import show
        show()
    elif page == "🔍  GP Leakage":
        from pages_.gp_leakage import show
        show()
    elif page == "💵  Cash Receipt":
        from pages_.cash_receipt import show
        show()
