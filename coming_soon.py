import streamlit as st

def coming_soon(page_name, icon, description):
    st.markdown(f"""
    <div style='
        display:flex; flex-direction:column;
        align-items:center; justify-content:center;
        min-height:60vh; text-align:center; padding:40px;
    '>
        <div style='font-size:64px; margin-bottom:20px;'>{icon}</div>
        <div style='font-size:32px; font-weight:800; color:#f9fafb;
            margin-bottom:10px; letter-spacing:-0.5px;'>{page_name}</div>
        <div style='font-size:15px; color:#4b5563; max-width:400px;
            margin-bottom:32px; line-height:1.6;'>{description}</div>
        <div style='
            background:linear-gradient(135deg,#1e1f4b,#1a1035);
            border:1px solid #6366f1; border-radius:16px;
            padding:16px 32px; font-size:14px; font-weight:600;
            color:#818cf8; letter-spacing:1px;
        '>🚧 DASHBOARD COMING SOON</div>
    </div>
    """, unsafe_allow_html=True)
