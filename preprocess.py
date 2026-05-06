import pandas as pd
import numpy as np

def load_data():
    matches = pd.read_csv("data/matches.csv")
    deliveries = pd.read_csv("data/deliveries.csv")
    return matches, deliveries

def create_match_features(matches, deliveries):
    first_innings = deliveries[deliveries['inning'] == 1].groupby(
        'match_id')['total_runs'].sum().reset_index()
    first_innings.columns = ['id', 'first_innings_score']

    df = matches.merge(first_innings, on='id', how='left')

    df['toss_win_bat'] = (
        (df['toss_winner'] == df['team1']) & 
        (df['toss_decision'] == 'bat')
    ).astype(int)

    df['team1_won'] = (df['winner'] == df['team1']).astype(int)

    return df

def create_live_features(target, current_score, wickets_lost, overs_done):
    runs_needed = target - current_score
    balls_remaining = int((20 - overs_done) * 6)
    required_rr = round((runs_needed / balls_remaining) * 6, 2) if balls_remaining > 0 else 99
    wickets_in_hand = 10 - wickets_lost
    current_rr = round((current_score / overs_done), 2) if overs_done > 0 else 0

    return pd.DataFrame([{
        'runs_needed': runs_needed,
        'balls_remaining': balls_remaining,
        'wickets_in_hand': wickets_in_hand,
        'required_run_rate': required_rr,
        'current_run_rate': current_rr,
        'overs_done': overs_done
    }])