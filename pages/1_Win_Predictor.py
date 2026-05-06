import streamlit as st
import joblib
import pandas as pd

st.title("🏏 Live Match Win Probability")
st.markdown("Predict match outcome based on live match conditions")

# ------------------ TEAMS ------------------
st.markdown("## TEAMS")

teams = [
    "Royal Challengers Bangalore",
    "Mumbai Indians",
    "Chennai Super Kings",
    "Kolkata Knight Riders",
    "Delhi Capitals",
    "Rajasthan Royals"
]

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox("Batting Team", teams)

with col2:
    bowling_team = st.selectbox("Bowling Team", teams)

# ------------------ MATCH SITUATION ------------------
st.markdown("## MATCH SITUATION")

col1, col2, col3, col4 = st.columns(4)

with col1:
    target = st.number_input("Target Score", min_value=50, max_value=300, value=200)

with col2:
    current_score = st.number_input("Current Score", min_value=0, max_value=299, value=120)

with col3:
    balls_left = st.number_input("Balls Left", min_value=0, max_value=120, value=40)

with col4:
    wickets_left = st.number_input("Wickets Left", min_value=0, max_value=10, value=6)

# ------------------ LIVE METRICS ------------------
st.markdown("## LIVE METRICS")

runs_left = target - current_score
balls_bowled = 120 - balls_left
overs_completed = balls_bowled / 6

crr = round(current_score / overs_completed, 2) if overs_completed > 0 else 0
rrr = round((runs_left / balls_left) * 6, 2) if balls_left > 0 else 0

st.info(f"Runs Left: {runs_left}")
st.info(f"Current Run Rate (CRR): {crr}")
st.info(f"Required Run Rate (RRR): {rrr}")

# ------------------ LOAD MODEL ------------------
model = joblib.load("models/xgboost_model.pkl")

# ------------------ PREDICT ------------------
if st.button("Predict Win Probability"):

    input_df = pd.DataFrame([{
        "runs_left": runs_left,
        "balls_left": balls_left,
        "wickets": wickets_left,
        "first_innings_score": target,
        "crr": crr,
        "rrr": rrr
    }])

    result = model.predict_proba(input_df)

    batting_prob = round(result[0][1] * 100, 1)
    bowling_prob = round(100 - batting_prob, 1)

    st.markdown("## WIN PROBABILITY")

    # Simple bar (no fancy UI)
    st.progress(float(batting_prob / 100))

    st.write(f"🏏 {batting_team}: {batting_prob}%")
    st.write(f"🎯 {bowling_team}: {bowling_prob}%")

    st.success(f"Winning Probability: {batting_prob}%")