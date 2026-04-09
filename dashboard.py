import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import io

# ── Navigation State ─────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Region"

# ── DB Connection ────────────────────────────────
@st.cache_resource
def get_engine():
    host     = "db31521.public.databaseasp.net"
    port     = 3306
    database = "db31521"
    username = "db31521"
    password = quote_plus(st.secrets["DB_PASSWORD"])
    return create_engine(
        f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}",
        pool_pre_ping=True, pool_recycle=3600,
    )

@st.cache_data(ttl=300)
def load_sales():
    engine = get_engine()
    df = pd.read_sql_table("sales_dashboard", engine)

    for col in ['Net_Cost','Net_Discount','Net_Sale','Net_Scheme']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    if 'Date' in df.columns:
        df['Date']  = pd.to_datetime(df['Date'], errors='coerce')
        df['Month'] = df['Date'].dt.to_period('M').astype(str)

    return df

def fmt(n):
    if abs(n) >= 1_000_000: return f"₹{n/1_000_000:.1f}M"
    if abs(n) >= 1_000:     return f"₹{n/1_000:.1f}K"
    return f"₹{n:.0f}"

# ── Load Data ───────────────────────────────────
df = load_sales()

# ── Sidebar ─────────────────────────────────────
with st.sidebar:
    st.markdown("## 💊 SalesPulse")

    st.markdown("### 📊 Navigation")
    pages = ["Region", "Unit", "ASM", "Customer", "Trend"]

    for p in pages:
        active = st.session_state.page == p
        if st.button(("👉 " if active else "") + p, use_container_width=True):
            st.session_state.page = p
            st.rerun()

    st.markdown("---")

    # Filters
    if 'Date' in df.columns:
        from_date = st.date_input("From Date", df['Date'].min())
        to_date   = st.date_input("To Date", df['Date'].max())

        df = df[(df['Date'] >= pd.to_datetime(from_date)) &
                (df['Date'] <= pd.to_datetime(to_date))]

# ── KPIs ────────────────────────────────────────
total_sale = df['Net_Sale'].sum()
total_cost = df['Net_Cost'].sum()
profit = total_sale - total_cost
gp_pct = (profit / total_sale * 100) if total_sale else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("💰 Sales", fmt(total_sale))
k2.metric("📦 Cost", fmt(total_cost))
k3.metric("📈 Profit", fmt(profit))
k4.metric("💹 GP %", f"{gp_pct:.2f}%")

st.markdown("---")

page = st.session_state.page

# ── REGION ──────────────────────────────────────
if page == "Region":
    st.title("🌍 Region Analysis")

    rdf = df.groupby('Region', as_index=False)['Net_Sale'].sum()

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(rdf, x='Region', y='Net_Sale', color='Region',
                     template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.pie(rdf, names='Region', values='Net_Sale')
        st.plotly_chart(fig, use_container_width=True)

# ── UNIT ────────────────────────────────────────
elif page == "Unit":
    st.title("🏢 Unit Analysis")

    udf = df.groupby('Unit', as_index=False)['Net_Sale'].sum()

    fig = px.bar(udf, x='Net_Sale', y='Unit', orientation='h',
                 template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

# ── ASM ─────────────────────────────────────────
elif page == "ASM":
    st.title("👤 ASM Analysis")

    adf = df.groupby('Area_Sales_Man', as_index=False)['Net_Sale'].sum()

    fig = px.bar(adf, x='Net_Sale', y='Area_Sales_Man',
                 orientation='h', template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

# ── CUSTOMER ────────────────────────────────────
elif page == "Customer":
    st.title("👥 Customer Analysis")

    cdf = df.groupby('Customer_Type', as_index=False)['Net_Sale'].sum()

    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(cdf, names='Customer_Type', values='Net_Sale')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(cdf, x='Customer_Type', y='Net_Sale',
                     color='Customer_Type')
        st.plotly_chart(fig, use_container_width=True)

# ── TREND ───────────────────────────────────────
elif page == "Trend":
    st.title("📅 Sales Trend")

    mdf = df.groupby('Month', as_index=False)['Net_Sale'].sum()

    fig = px.line(mdf, x='Month', y='Net_Sale', markers=True,
                  template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

# ── Footer ──────────────────────────────────────
st.markdown("---")
st.markdown(
    "<center style='color:gray'>SalesPulse v3 • Entero Healthcare</center>",
    unsafe_allow_html=True
)