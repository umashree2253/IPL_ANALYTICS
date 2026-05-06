import streamlit as st
import pandas as pd
import plotly.express as px

st.title("👤 PLAYER PERFORMANCE DASHBOARD")
st.markdown("Career statistics • Season trends • Strike rates")

# ------------------ LOAD DATA ------------------
deliveries = pd.read_csv("data/deliveries.csv")
matches = pd.read_csv("data/matches.csv")

# Merge data
df = deliveries.merge(matches[['id', 'season']], left_on='match_id', right_on='id')

# ------------------ PLAYER SELECTION ------------------
players = df['batter'].value_counts().head(30).index.tolist()
player = st.selectbox("Select Player", players)

player_df = df[df['batter'] == player]

# ------------------ CAREER SUMMARY ------------------
st.markdown("### CAREER SUMMARY")

col1, col2, col3, col4 = st.columns(4)

# Total Runs
total_runs = player_df['batsman_runs'].sum()

# Balls faced
total_balls = player_df.shape[0]

# Strike rate
strike_rate = round((total_runs / total_balls) * 100, 2) if total_balls > 0 else 0

# Dismissals (approx using is_wicket)
dismissals = player_df['is_wicket'].sum()

# Batting average
batting_avg = round(total_runs / dismissals, 2) if dismissals > 0 else total_runs

# Matches played
matches_played = player_df['match_id'].nunique()

col1.metric("Total Runs", total_runs)
col2.metric("Strike Rate", strike_rate)
col3.metric("Batting Average", batting_avg)
col4.metric("Matches Played", matches_played)

# ------------------ RUNS PER MATCH ------------------
st.markdown("### RUNS PER MATCH — SEASON TIMELINE")

runs_per_match = player_df.groupby('match_id')['batsman_runs'].sum().reset_index()

fig = px.line(
    runs_per_match,
    x='match_id',
    y='batsman_runs',
    markers=True,
    title=f"{player} — Runs per Match"
)

st.plotly_chart(fig, use_container_width=True)

# ------------------ RUNS BY SEASON ------------------
st.markdown("### RUNS BY SEASON")

season_stats = player_df.groupby('season').agg(
    runs=('batsman_runs', 'sum'),
    balls=('ball', 'count')
).reset_index()

season_stats['strike_rate'] = (season_stats['runs'] / season_stats['balls'] * 100).round(1)

fig2 = px.bar(
    season_stats,
    x='season',
    y='runs',
    color='strike_rate',
    title=f"{player} — Runs by Season",
    color_continuous_scale='RdYlGn'
)

st.plotly_chart(fig2, use_container_width=True)

# ------------------ PLAYER CLUSTERS ------------------
st.markdown("### PLAYER PERFORMANCE CLUSTERS")

clusters = pd.read_csv("data/player_clusters.csv")

cluster_names = {
    0: "Anchor",
    1: "Power Hitter",
    2: "Finisher",
    3: "All-rounder"
}

clusters['role'] = clusters['cluster'].map(cluster_names)

fig3 = px.scatter(
    clusters,
    x='strike_rate',
    y='runs',
    color='role',
    hover_data=['batter'],
    title="Player Performance Clusters"
)

st.plotly_chart(fig3, use_container_width=True)