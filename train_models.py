import pandas as pd
import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
import xgboost as xgb
from preprocess import load_data, create_match_features

matches, deliveries = load_data()
df = create_match_features(matches, deliveries)

# --- Model 1 & 2 & 3: Win prediction models ---
# Features for match-level prediction
# --- LIVE MATCH MODEL (FIXED VERSION) ---

# Create approximate live features
df['runs_left'] = df['first_innings_score']
df['balls_left'] = 120
df['wickets'] = 10
df['crr'] = df['first_innings_score'] / 20
df['rrr'] = df['crr']

features = ['runs_left', 'balls_left', 'wickets', 'first_innings_score', 'crr', 'rrr']
target = 'team1_won'

X = df[features].fillna(0)
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

xgb_model = xgb.XGBClassifier(n_estimators=100, eval_metric='logloss')
xgb_model.fit(X_train, y_train)

joblib.dump(xgb_model, "models/xgboost_model.pkl")



# --- Model 4: K-Means player clustering ---
batting = deliveries.groupby('batter').agg(
    runs=('batsman_runs', 'sum'),
    balls=('ball', 'count'),
    fours=('batsman_runs', lambda x: (x==4).sum()),
    sixes=('batsman_runs', lambda x: (x==6).sum())
).reset_index()
batting['strike_rate'] = (batting['runs'] / batting['balls']) * 100
batting = batting[batting['balls'] > 200]  # filter low-sample players

kmeans = KMeans(n_clusters=4, random_state=42)
batting['cluster'] = kmeans.fit_predict(batting[['runs', 'strike_rate', 'sixes']])
joblib.dump(kmeans, "models/kmeans_player.pkl")
batting.to_csv("data/player_clusters.csv", index=False)

print("All models trained and saved.")