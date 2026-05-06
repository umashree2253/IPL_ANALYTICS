import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Head to Head", layout="wide")

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>

/* Main background */
body {
    background-color: #0b0f1a;
    color: white;
}

/* Header card */
.card {
    background: linear-gradient(145deg, #111827, #1f2937);
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #2d3748;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}

/* Section title */
.section {
    color: #facc15;
    font-weight: 600;
    margin-top: 25px;
}

/* Sidebar light */
section[data-testid="stSidebar"] {
    background-color: #f9fafb !important;
}

section[data-testid="stSidebar"] * {
    color: black !important;
}

</style>
""", unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------
st.sidebar.title("🏏 IPL Analytics")
st.sidebar.markdown("### Intelligence Platform")
st.sidebar.markdown("---")
st.sidebar.info("Powered by\nXGBoost • K-Means • Random Forest • Logistic Regression")

# ------------------ HEADER ------------------
st.markdown("""
<div class="card">
    <h2>⚔️ Head-to-Head Team Analysis</h2>
    <p style="color:#9ca3af;">Compare historical performance between IPL teams</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ------------------ LOAD DATA ------------------
matches = pd.read_csv("data/matches.csv")
teams = sorted(matches['team1'].dropna().unique())

# ------------------ TEAM SELECTION ------------------
col1, col2 = st.columns(2)

with col1:
    team1 = st.selectbox("Select Team 1", teams)

with col2:
    team2 = st.selectbox("Select Team 2", teams)

# ------------------ FILTER DATA ------------------
h2h = matches[
    ((matches['team1'] == team1) & (matches['team2'] == team2)) |
    ((matches['team1'] == team2) & (matches['team2'] == team1))
]

total_matches = h2h.shape[0]
team1_wins = h2h[h2h['winner'] == team1].shape[0]
team2_wins = h2h[h2h['winner'] == team2].shape[0]

# ------------------ HANDLE NO DATA ------------------
if total_matches == 0:
    st.warning("No matches found between selected teams.")
    st.stop()

# ------------------ CALCULATIONS ------------------
team1_pct = round((team1_wins / total_matches) * 100, 1)
team2_pct = round((team2_wins / total_matches) * 100, 1)

# ------------------ INSIGHT ------------------
if team1_wins > team2_wins:
    insight = f"🔥 {team1} dominates this rivalry"
elif team2_wins > team1_wins:
    insight = f"🔥 {team2} dominates this rivalry"
else:
    insight = "⚖️ This rivalry is evenly balanced"

st.markdown(f"### {insight}")

# ------------------ METRICS ------------------
st.markdown('<p class="section">HEAD-TO-HEAD RECORD</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

col1.metric(f"{team1} Wins", team1_wins, f"{team1_pct}%")
col2.metric(f"{team2} Wins", team2_wins, f"{team2_pct}%")
col3.metric("Total Matches", total_matches)

# ------------------ PROGRESS BARS ------------------
st.markdown("### 📊 Win Distribution")

st.write(f"{team1} ({team1_pct}%)")
st.progress(team1_pct / 100)

st.write(f"{team2} ({team2_pct}%)")
st.progress(team2_pct / 100)

# ------------------ BAR CHART ------------------
st.markdown("### 📈 Win Comparison")

win_data = pd.DataFrame({
    "Team": [team1, team2],
    "Wins": [team1_wins, team2_wins],
    "Win %": [team1_pct, team2_pct]
})

fig = px.bar(
    win_data,
    x="Team",
    y="Wins",
    text="Wins",
    color="Win %",
    color_continuous_scale="Blues"
)

fig.update_layout(
    plot_bgcolor='#0b0f1a',
    paper_bgcolor='#0b0f1a',
    font_color='white'
)

fig.update_traces(textposition='outside')

st.plotly_chart(fig, use_container_width=True)

# ------------------ FOOTER ------------------
st.markdown("---")
