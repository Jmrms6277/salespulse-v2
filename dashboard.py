import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# ── DB ─────────────────────────────
@st.cache_resource
def get_engine():
    return create_engine(
        f"mysql+pymysql://db31521:{quote_plus(st.secrets['DB_PASSWORD'])}"
        "@db31521.public.databaseasp.net:3306/db31521",
        pool_pre_ping=True,
        pool_recycle=3600,
    )

@st.cache_data(ttl=300)
def load_data():
    df = pd.read_sql_table("sales_dashboard", get_engine())
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Month'] = df['Date'].dt.to_period('M').astype(str)
    return df

# ── CSS FIXED ──────────────────────
def load_css():
    st.markdown("""
    <style>
    .stApp { background: #060818; }
    #MainMenu, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# ── MAIN DASHBOARD ─────────────────
def show_dashboard():

    load_css()

    full_name = st.session_state.get("full_name", "User")

    st.title(f"📊 Sales Dashboard")
    st.caption(f"Welcome {full_name}")

    df = load_data()

    # Sidebar
    with st.sidebar:
        st.header("Filters")

        from_date = st.date_input("From", df['Date'].min())
        to_date   = st.date_input("To", df['Date'].max())

    df = df[(df['Date'] >= pd.to_datetime(from_date)) &
            (df['Date'] <= pd.to_datetime(to_date))]

    # KPIs
    total_sale = df['Net_Sale'].sum()
    total_cost = df['Net_Cost'].sum()
    profit = total_sale - total_cost

    c1, c2, c3 = st.columns(3)
    c1.metric("Sales", f"₹{total_sale:,.0f}")
    c2.metric("Cost", f"₹{total_cost:,.0f}")
    c3.metric("Profit", f"₹{profit:,.0f}")

    st.markdown("---")

    # Tabs
    tab1, tab2 = st.tabs(["Region", "Trend"])

    with tab1:
        rdf = df.groupby("Region", as_index=False)["Net_Sale"].sum()
        fig = px.bar(rdf, x="Region", y="Net_Sale", color="Region")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        mdf = df.groupby("Month", as_index=False)["Net_Sale"].sum()
        fig = px.line(mdf, x="Month", y="Net_Sale", markers=True)
        st.plotly_chart(fig, use_container_width=True)