import streamlit as st

st.set_page_config(
    page_title="IPL Analytics Platform",
    page_icon="🏏",
    layout="wide"
)

st.title("🏏 IPL Cricket Analytics Platform")
st.markdown("16 seasons of IPL data — powering real-time match insights.")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info("🎯 **Win Predictor**\n\nLive win probability using XGBoost")

with col2:
    st.success("📊 **Player Analytics**\n\nSeason trends and player clusters")

with col3:
    st.warning("🗺️ **Venue Analysis**\n\nGround statistics and heatmaps")

with col4:
    st.error("⚔️ **Head to Head**\n\nTeam history and top performers")

st.markdown("---")