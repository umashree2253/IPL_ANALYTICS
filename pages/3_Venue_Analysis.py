import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Venue Analysis", layout="wide")

# ------------------ DARK CSS ------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}

.metric-card {
    background: #111827;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    border: 1px solid #1f2937;
}

.metric-title {
    color: #9ca3af;
    font-size: 14px;
}

.metric-value {
    font-size: 28px;
    font-weight: bold;
    color: white;
}

.section-title {
    color: #facc15;
    font-weight: bold;
    letter-spacing: 1px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------
st.sidebar.title("🏏 IPL Analytics")
st.sidebar.markdown("### Intelligence Platform")
st.sidebar.markdown("---")
st.sidebar.selectbox("Navigate", ["Venue Analysis"])
st.sidebar.markdown("---")
st.sidebar.info("Powered by\nXGBoost • K-Means • Random Forest • LogReg")

# ------------------ TITLE ------------------
st.markdown("## 🏟️ VENUE ANALYSIS")
st.markdown("Ground behaviour • Chasing vs defending • Historical trends")

# ------------------ LOAD DATA ------------------
matches = pd.read_csv("data/matches.csv")

# ------------------ VENUE SELECT ------------------
venues = matches['venue'].dropna().unique()
venue = st.selectbox("Select Venue", sorted(venues))

venue_df = matches[matches['venue'] == venue]

# ------------------ VENUE STATS ------------------
st.markdown('<p class="section-title">VENUE STATISTICS</p>', unsafe_allow_html=True)

total_matches = venue_df.shape[0]

# Chasing win logic
venue_df['chasing_win'] = venue_df.apply(
    lambda r: 1 if (
        (r['toss_decision'] == 'field' and r['toss_winner'] == r['winner']) or
        (r['toss_decision'] == 'bat' and r['toss_winner'] != r['winner'])
    ) else 0, axis=1
)

chasing_wins = venue_df['chasing_win'].sum()
defending_wins = total_matches - chasing_wins

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Matches</div>
        <div class="metric-value">{total_matches}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Chasing Wins</div>
        <div class="metric-value">{chasing_wins}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Defending Wins</div>
        <div class="metric-value">{defending_wins}</div>
    </div>
    """, unsafe_allow_html=True)

# ------------------ WIN TYPE DISTRIBUTION ------------------
st.markdown('<p class="section-title">WIN TYPE DISTRIBUTION</p>', unsafe_allow_html=True)

win_data = pd.DataFrame({
    "Type": ["Chasing", "Defending"],
    "Wins": [chasing_wins, defending_wins]
})

fig = px.bar(win_data, x="Type", y="Wins", color="Type")

fig.update_layout(
    plot_bgcolor='#0e1117',
    paper_bgcolor='#0e1117',
    font_color='white',
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)