import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import io

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
        pool_pre_ping=True, pool_recycle=3600,
    )

@st.cache_data(ttl=300, show_spinner=False)
def load_sales(role, region, unit, asm_code):
    engine = get_engine()
    df = pd.read_sql_table("sales_dashboard", engine)
    for col in ['Net_Cost','Net_Discount','Net_Sale','Net_Scheme']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    if 'Date' in df.columns:
        df['Date']  = pd.to_datetime(df['Date'], errors='coerce')
        df['Month'] = df['Date'].dt.to_period('M').astype(str)
        df['Year']  = df['Date'].dt.year.astype(str)
    # Row-level security
    if role != 'Admin':
        if region != 'ALL' and 'Region' in df.columns:
            df = df[df['Region'] == region]
        if unit != 'ALL' and 'Unit' in df.columns:
            df = df[df['Unit'] == unit]
        if asm_code != 'ALL' and 'ASM_Code' in df.columns:
            df = df[df['ASM_Code'] == asm_code]
    return df

def fmt(n):
    if abs(n) >= 1_000_000_000: return f"₹{n/1_000_000_000:.1f}B"
    if abs(n) >= 1_000_000:     return f"₹{n/1_000_000:.1f}M"
    if abs(n) >= 1_000:         return f"₹{n/1_000:.1f}K"
    return f"₹{n:.0f}"

COLORS = px.colors.qualitative.Vivid

# ── CSS ─────────────────────────────────────────────────────────────────────────
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=DM+Mono&display=swap');
    * { font-family: 'Outfit', sans-serif !important; }
    .stApp { background: #060818; }
    #MainMenu, footer { visibility: hidden; }

    /* Sidebar */
    section[data-testid="collapsedControl"] {
        background: #0a0d1a !important;
        border-right: 1px solid #1a1f35 !important;
    }
    section[data-testid="collapsedControl"] * { color: #e5e7eb !important; }

    /* Nav buttons */
    .nav-btn {
        display: flex; align-items: center; gap: 12px;
        padding: 12px 16px; border-radius: 12px;
        margin-bottom: 4px; cursor: pointer;
        transition: all 0.2s; color: #6b7280;
        font-size: 14px; font-weight: 500;
        border: 1px solid transparent;
    }
    .nav-btn:hover { background: #1a1f35; color: #e5e7eb; }
    .nav-btn.active {
        background: linear-gradient(135deg, #1e1f4b, #1a1035);
        border-color: #6366f1;
        color: #818cf8 !important;
    }

    /* KPI cards */
    .kpi-card {
        background: linear-gradient(145deg, #0d1117, #111827);
        border: 1px solid #1f2937;
        border-radius: 20px;
        padding: 22px 24px;
        text-align: left;
        transition: transform 0.2s, box-shadow 0.2s;
        position: relative;
        overflow: hidden;
    }
    .kpi-card::before {
        content: '';
        position: absolute; top: 0; left: 0;
        width: 4px; height: 100%;
        background: linear-gradient(180deg, #6366f1, #8b5cf6);
        border-radius: 4px 0 0 4px;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(99,102,241,0.15);
        border-color: #374151;
    }
    .kpi-icon { font-size: 22px; margin-bottom: 10px; }
    .kpi-label {
        font-size: 11px; font-weight: 600;
        letter-spacing: 1.5px; text-transform: uppercase;
        color: #6b7280; margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 26px; font-weight: 800; color: #f9fafb;
        font-family: 'DM Mono', monospace !important;
        letter-spacing: -0.5px;
    }
    .kpi-sub { font-size: 12px; color: #10b981; margin-top: 6px; font-weight: 500; }
    .kpi-sub.red { color: #ef4444; }

    /* Date banner */
    .period-banner {
        background: linear-gradient(135deg, #0d1117, #111827);
        border: 1px solid #1f2937;
        border-radius: 16px;
        padding: 16px 24px;
        margin-bottom: 24px;
        display: flex; gap: 40px; align-items: center;
        border-left: 4px solid #6366f1;
    }
    .pb-label { font-size: 11px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; color: #6b7280; margin-bottom: 4px; }
    .pb-value { font-size: 15px; font-weight: 700; color: #a5b4fc; font-family: 'DM Mono', monospace !important; }

    /* Section header */
    .sec-header {
        font-size: 12px; font-weight: 700; letter-spacing: 2px;
        text-transform: uppercase; color: #6366f1;
        margin: 28px 0 14px; padding-bottom: 10px;
        border-bottom: 1px solid #1a1f35;
    }

    /* Page header */
    .page-header {
        font-size: 24px; font-weight: 800; color: #f9fafb;
        margin-bottom: 4px; letter-spacing: -0.3px;
    }
    .page-sub { font-size: 13px; color: #4b5563; margin-bottom: 24px; }

    /* User badge */
    .user-badge {
        background: linear-gradient(135deg, #1e1f4b, #1a1035);
        border: 1px solid #6366f1;
        border-radius: 12px; padding: 12px 16px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)


def show_dashboard():
    load_css()

    user      = st.session_state.get('user', {})
    full_name = st.session_state.get('full_name', 'User')
    role      = st.session_state.get('role', 'ASM')
    region    = st.session_state.get('region', 'ALL')
    unit      = st.session_state.get('unit', 'ALL')
    asm_code  = st.session_state.get('asm_code', 'ALL')

    # ── Sidebar ──────────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align:center; padding: 20px 0 10px;'>
            <div style='font-size:36px'>💊</div>
            <div style='font-size:20px; font-weight:800;
                background: linear-gradient(135deg, #818cf8, #c084fc);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                SalesPulse
            </div>
            <div style='font-size:10px; color:#4b5563; letter-spacing:1px; margin-top:2px;'>
                PHARMA INTELLIGENCE
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='user-badge'>
            <div style='font-size:12px; color:#6b7280; margin-bottom:2px;'>SIGNED IN AS</div>
            <div style='font-size:15px; font-weight:700; color:#e5e7eb;'>👤 {full_name}</div>
            <div style='font-size:11px; color:#6366f1; margin-top:2px;'>{role}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**NAVIGATION**", )
        page = st.radio("", [
            "🏠  Dashboard",
            "🌍  Region",
            "🏢  Unit",
            "👤  ASM",
            "👥  Customer",
            "📅  Trend",
        ], label_visibility="collapsed")

        st.markdown("---")
        st.markdown("**FILTERS**")

        # Load data for filter options
        with st.spinner("Loading..."):
            df_full = load_sales(role, region, unit, asm_code)

        if 'Date' in df_full.columns:
            min_d = df_full['Date'].min().date()
            max_d = df_full['Date'].max().date()
            from_date = st.date_input("📅 From Date", value=min_d, min_value=min_d, max_value=max_d)
            to_date   = st.date_input("📅 To Date",   value=max_d, min_value=min_d, max_value=max_d)
        else:
            from_date = to_date = None

        if 'Region' in df_full.columns and role == 'Admin':
            sel_regions = st.multiselect("Region", df_full['Region'].dropna().unique().tolist(),
                                         default=df_full['Region'].dropna().unique().tolist())
        else:
            sel_regions = []

        if 'Unit' in df_full.columns:
            sel_units = st.multiselect("Unit", sorted(df_full['Unit'].dropna().unique().tolist()),
                                       default=sorted(df_full['Unit'].dropna().unique().tolist()))
        else:
            sel_units = []

        if 'Customer_Type' in df_full.columns:
            sel_cx = st.multiselect("Customer Type", df_full['Customer_Type'].dropna().unique().tolist(),
                                    default=df_full['Customer_Type'].dropna().unique().tolist())
        else:
            sel_cx = []

        st.markdown("---")
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()

    # ── Apply Filters ─────────────────────────────────────────────────────────
    df = df_full.copy()
    if from_date and to_date and 'Date' in df.columns:
        df = df[(df['Date'].dt.date >= from_date) & (df['Date'].dt.date <= to_date)]
    if sel_regions and 'Region' in df.columns:
        df = df[df['Region'].isin(sel_regions)]
    if sel_units and 'Unit' in df.columns:
        df = df[df['Unit'].isin(sel_units)]
    if sel_cx and 'Customer_Type' in df.columns:
        df = df[df['Customer_Type'].isin(sel_cx)]

    # ── KPIs ──────────────────────────────────────────────────────────────────
    total_sale     = df['Net_Sale'].sum()     if 'Net_Sale'     in df.columns else 0
    total_cost     = df['Net_Cost'].sum()     if 'Net_Cost'     in df.columns else 0
    total_discount = df['Net_Discount'].sum() if 'Net_Discount' in df.columns else 0
    total_scheme   = df['Net_Scheme'].sum()   if 'Net_Scheme'   in df.columns else 0
    profit  = total_sale - total_cost
    gp_pct  = (profit / total_sale * 100)         if total_sale else 0
    dis_pct = (total_discount / total_sale * 100)  if total_sale else 0

    def kpi_row():
        k = st.columns(6)
        items = [
            ("💰", "NET SALES",    fmt(total_sale),     "", ""),
            ("📦", "NET COST",     fmt(total_cost),     "", ""),
            ("🏷️", "DISCOUNT",    fmt(total_discount), f"{dis_pct:.2f}%", ""),
            ("🎁", "SCHEME",       fmt(total_scheme),   "", ""),
            ("📈", "GROSS PROFIT", fmt(profit),         "", ""),
            ("💹", "GP %",         f"{gp_pct:.2f}%",   "", ""),
        ]
        for col, (icon, label, val, sub, _) in zip(k, items):
            col.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">{icon}</div>
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{val}</div>
                {'<div class="kpi-sub">' + sub + '</div>' if sub else ''}
            </div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    def period_banner():
        if from_date and to_date:
            st.markdown(f"""
            <div class="period-banner">
                <div><div class="pb-label">📅 Period</div>
                <div class="pb-value">{from_date.strftime('%d %b %Y')} → {to_date.strftime('%d %b %Y')}</div></div>
                <div><div class="pb-label">👤 User</div>
                <div class="pb-value">{full_name} ({role})</div></div>
                <div><div class="pb-label">📋 Records</div>
                <div class="pb-value">{len(df):,}</div></div>
            </div>""", unsafe_allow_html=True)

    def export_btn(dataframe, filename):
        buf = io.BytesIO()
        dataframe.to_excel(buf, index=False)
        st.download_button("📥 Export to Excel", buf.getvalue(),
                           file_name=filename, mime="application/vnd.ms-excel")

    # ════════════════════════════════════════════════════════════════════════════
    # PAGE: DASHBOARD
    # ════════════════════════════════════════════════════════════════════════════
    if page == "🏠  Dashboard":
        st.markdown(f"<div class='page-header'>👋 Welcome back, {full_name}</div>", unsafe_allow_html=True)
        st.markdown("<div class='page-sub'>Here's what's happening with your sales today.</div>", unsafe_allow_html=True)
        period_banner()
        kpi_row()

        c1, c2 = st.columns(2)
        with c1:
            if 'Region' in df.columns:
                rdf = df.groupby('Region', as_index=False)['Net_Sale'].sum().sort_values('Net_Sale', ascending=False)
                fig = px.bar(rdf, x='Region', y='Net_Sale', color='Region',
                             title='Region-wise Net Sales', color_discrete_sequence=COLORS,
                             template='plotly_dark', text_auto='.2s')
                fig.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)',
                                  paper_bgcolor='rgba(0,0,0,0)', title_font_size=14)
                st.plotly_chart(fig, use_container_width=True)

        with c2:
            if 'Customer_Type' in df.columns:
                ctdf = df.groupby('Customer_Type', as_index=False)['Net_Sale'].sum()
                fig2 = px.pie(ctdf, names='Customer_Type', values='Net_Sale',
                              title='Customer Type Share', hole=0.45,
                              color_discrete_sequence=COLORS, template='plotly_dark')
                fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', title_font_size=14)
                st.plotly_chart(fig2, use_container_width=True)

        if 'Month' in df.columns:
            mdf = df.groupby('Month', as_index=False)['Net_Sale'].sum().sort_values('Month')
            fig3 = px.area(mdf, x='Month', y='Net_Sale', title='Monthly Sales Trend',
                           template='plotly_dark', color_discrete_sequence=['#6366f1'])
            fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                               title_font_size=14)
            fig3.update_traces(fill='tozeroy', fillcolor='rgba(99,102,241,0.1)')
            st.plotly_chart(fig3, use_container_width=True)

    # ════════════════════════════════════════════════════════════════════════════
    # PAGE: REGION
    # ════════════════════════════════════════════════════════════════════════════
    elif page == "🌍  Region":
        st.markdown("<div class='page-header'>🌍 Region Analysis</div>", unsafe_allow_html=True)
        st.markdown("<div class='page-sub'>Sales performance by region.</div>", unsafe_allow_html=True)
        period_banner()
        kpi_row()

        c1, c2 = st.columns(2)
        with c1:
            if 'Region' in df.columns:
                rdf = df.groupby('Region', as_index=False)['Net_Sale'].sum().sort_values('Net_Sale', ascending=False)
                fig = px.bar(rdf, x='Region', y='Net_Sale', color='Region',
                             title='Region-wise Net Sales', color_discrete_sequence=COLORS,
                             template='plotly_dark', text_auto='.2s')
                fig.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)',
                                  paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
        with c2:
            if 'Region' in df.columns:
                fig2 = px.pie(rdf, names='Region', values='Net_Sale', title='Region Share',
                              hole=0.45, color_discrete_sequence=COLORS, template='plotly_dark')
                fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig2, use_container_width=True)

        if 'State' in df.columns:
            sdf = df.groupby('State', as_index=False)['Net_Sale'].sum().sort_values('Net_Sale', ascending=False).head(15)
            fig3 = px.bar(sdf, x='Net_Sale', y='State', orientation='h',
                          color='Net_Sale', color_continuous_scale='Purples',
                          title='Top 15 States', template='plotly_dark', text_auto='.2s')
            fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                               yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig3, use_container_width=True)

        if 'Region' in df.columns:
            st.markdown("<div class='sec-header'>Region Summary</div>", unsafe_allow_html=True)
            rtbl = df.groupby('Region').agg(
                Sales=('Net_Sale','sum'), Discount=('Net_Discount','sum'),
                Cost=('Net_Cost','sum'), Scheme=('Net_Scheme','sum')
            ).reset_index()
            rtbl['Profit'] = rtbl['Sales'] - rtbl['Cost']
            rtbl['GP %']   = (rtbl['Profit'] / rtbl['Sales'] * 100).round(2)
            rtbl['Dis %']  = (rtbl['Discount'] / rtbl['Sales'] * 100).round(2)
            export_btn(rtbl, "region_summary.xlsx")
            for c in ['Sales','Discount','Cost','Scheme','Profit']:
                rtbl[c] = rtbl[c].apply(lambda x: f"₹{x:,.0f}")
            st.dataframe(rtbl, use_container_width=True, hide_index=True)

    # ════════════════════════════════════════════════════════════════════════════
    # PAGE: UNIT
    # ════════════════════════════════════════════════════════════════════════════
    elif page == "🏢  Unit":
        st.markdown("<div class='page-header'>🏢 Unit Analysis</div>", unsafe_allow_html=True)
        st.markdown("<div class='page-sub'>Sales performance by unit.</div>", unsafe_allow_html=True)
        period_banner()
        kpi_row()

        if 'Unit' in df.columns:
            udf = df.groupby('Unit', as_index=False)['Net_Sale'].sum().sort_values('Net_Sale', ascending=False).head(20)
            fig = px.bar(udf, x='Net_Sale', y='Unit', orientation='h',
                         color='Net_Sale', color_continuous_scale='Blues',
                         title='Unit-wise Net Sales (Top 20)', template='plotly_dark', text_auto='.2s')
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                              yaxis={'categoryorder':'total ascending'}, height=600)
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("<div class='sec-header'>Unit Summary</div>", unsafe_allow_html=True)
            utbl = df.groupby('Unit').agg(
                Sales=('Net_Sale','sum'), Discount=('Net_Discount','sum'),
                Cost=('Net_Cost','sum'), Scheme=('Net_Scheme','sum')
            ).reset_index().sort_values('Sales', ascending=False)
            utbl['Profit'] = utbl['Sales'] - utbl['Cost']
            utbl['GP %']   = (utbl['Profit'] / utbl['Sales'] * 100).round(2)
            utbl['Dis %']  = (utbl['Discount'] / utbl['Sales'] * 100).round(2)
            export_btn(utbl, "unit_summary.xlsx")
            for c in ['Sales','Discount','Cost','Scheme','Profit']:
                utbl[c] = utbl[c].apply(lambda x: f"₹{x:,.0f}")
            st.dataframe(utbl, use_container_width=True, hide_index=True)

    # ════════════════════════════════════════════════════════════════════════════
    # PAGE: ASM
    # ════════════════════════════════════════════════════════════════════════════
    elif page == "👤  ASM":
        st.markdown("<div class='page-header'>👤 ASM Analysis</div>", unsafe_allow_html=True)
        st.markdown("<div class='page-sub'>Sales performance by Area Sales Manager.</div>", unsafe_allow_html=True)
        period_banner()
        kpi_row()

        if 'Area_Sales_Man' in df.columns:
            adf = df.groupby('Area_Sales_Man', as_index=False)['Net_Sale'].sum().sort_values('Net_Sale', ascending=False).head(20)
            fig = px.bar(adf, x='Net_Sale', y='Area_Sales_Man', orientation='h',
                         color='Net_Sale', color_continuous_scale='Greens',
                         title='ASM-wise Net Sales (Top 20)', template='plotly_dark', text_auto='.2s')
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                              yaxis={'categoryorder':'total ascending'}, height=600)
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("<div class='sec-header'>ASM Summary</div>", unsafe_allow_html=True)
            atbl = df.groupby(['Area_Sales_Man','Unit'], as_index=False).agg(
                Sales=('Net_Sale','sum'), Discount=('Net_Discount','sum'),
                Cost=('Net_Cost','sum')
            ).sort_values('Sales', ascending=False)
            atbl['Profit'] = atbl['Sales'] - atbl['Cost']
            atbl['GP %']   = (atbl['Profit'] / atbl['Sales'] * 100).round(2)
            atbl['Dis %']  = (atbl['Discount'] / atbl['Sales'] * 100).round(2)
            export_btn(atbl, "asm_summary.xlsx")
            for c in ['Sales','Discount','Cost','Profit']:
                atbl[c] = atbl[c].apply(lambda x: f"₹{x:,.0f}")
            st.dataframe(atbl, use_container_width=True, hide_index=True)

    # ════════════════════════════════════════════════════════════════════════════
    # PAGE: CUSTOMER
    # ════════════════════════════════════════════════════════════════════════════
    elif page == "👥  Customer":
        st.markdown("<div class='page-header'>👥 Customer Analysis</div>", unsafe_allow_html=True)
        st.markdown("<div class='page-sub'>Sales performance by customer.</div>", unsafe_allow_html=True)
        period_banner()
        kpi_row()

        c1, c2 = st.columns(2)
        with c1:
            if 'Customer_Type' in df.columns:
                ctdf = df.groupby('Customer_Type', as_index=False)['Net_Sale'].sum().sort_values('Net_Sale', ascending=False)
                fig = px.pie(ctdf, names='Customer_Type', values='Net_Sale',
                             title='Customer Type Share', hole=0.4,
                             color_discrete_sequence=COLORS, template='plotly_dark')
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
        with c2:
            if 'Customer_Type' in df.columns:
                fig2 = px.bar(ctdf, x='Customer_Type', y='Net_Sale', color='Customer_Type',
                              title='Customer Type Sales', color_discrete_sequence=COLORS,
                              template='plotly_dark', text_auto='.2s')
                fig2.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)',
                                   plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig2, use_container_width=True)

        if 'Customer' in df.columns:
            st.markdown("<div class='sec-header'>Top 50 Customers</div>", unsafe_allow_html=True)
            cust = df.groupby(['Customer','Customer_Type'], as_index=False).agg(
                Sales=('Net_Sale','sum'), Discount=('Net_Discount','sum')
            ).sort_values('Sales', ascending=False).head(50)
            cust['Dis %'] = (cust['Discount'] / cust['Sales'] * 100).round(2)
            export_btn(cust, "customer_summary.xlsx")
            cust['Sales']    = cust['Sales'].apply(lambda x: f"₹{x:,.0f}")
            cust['Discount'] = cust['Discount'].apply(lambda x: f"₹{x:,.0f}")
            st.dataframe(cust, use_container_width=True, hide_index=True)

    # ════════════════════════════════════════════════════════════════════════════
    # PAGE: TREND
    # ════════════════════════════════════════════════════════════════════════════
    elif page == "📅  Trend":
        st.markdown("<div class='page-header'>📅 Sales Trend</div>", unsafe_allow_html=True)
        st.markdown("<div class='page-sub'>Month-wise and year-wise sales trends.</div>", unsafe_allow_html=True)
        period_banner()
        kpi_row()

        if 'Month' in df.columns:
            mdf = df.groupby('Month', as_index=False).agg(
                Net_Sale=('Net_Sale','sum'), Net_Discount=('Net_Discount','sum'),
                Net_Cost=('Net_Cost','sum')
            ).sort_values('Month')
            mdf['Profit'] = mdf['Net_Sale'] - mdf['Net_Cost']

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=mdf['Month'], y=mdf['Net_Sale'], mode='lines+markers',
                                     name='Net Sale', line=dict(color='#6366f1', width=3), marker=dict(size=8)))
            fig.add_trace(go.Scatter(x=mdf['Month'], y=mdf['Profit'], mode='lines+markers',
                                     name='Profit', line=dict(color='#10b981', width=2, dash='dot'), marker=dict(size=6)))
            fig.add_trace(go.Bar(x=mdf['Month'], y=mdf['Net_Discount'], name='Discount',
                                 marker_color='#f59e0b', opacity=0.5, yaxis='y2'))
            fig.update_layout(
                title='Month-wise Sales Trend', template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                yaxis2=dict(overlaying='y', side='right', showgrid=False),
                legend=dict(orientation='h', yanchor='bottom', y=1.02),
            )
            st.plotly_chart(fig, use_container_width=True)

            if 'Region' in df.columns:
                mrdf = df.groupby(['Month','Region'], as_index=False)['Net_Sale'].sum().sort_values('Month')
                fig2 = px.line(mrdf, x='Month', y='Net_Sale', color='Region',
                               title='Month-wise Sales by Region', markers=True,
                               color_discrete_sequence=COLORS, template='plotly_dark')
                fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig2, use_container_width=True)

            if 'Unit' in df.columns:
                mudf = df.groupby(['Month','Unit'], as_index=False)['Net_Sale'].sum().sort_values('Month')
                fig3 = px.line(mudf, x='Month', y='Net_Sale', color='Unit',
                               title='Month-wise Sales by Unit', markers=True,
                               color_discrete_sequence=COLORS, template='plotly_dark')
                fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig3, use_container_width=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    <p style='text-align:center; color:#1f2937; font-size:12px'>
        SalesPulse v2.0 • Entero Healthcare • Powered by Streamlit
    </p>""", unsafe_allow_html=True)