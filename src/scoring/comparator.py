import pandas as pd

WEIGHTS = {
    "PTS" : 1.0,
    "AST" : 0.8,
    "TRB" : 0.7,
    "STL" : 0.6,
    "BLK" : 0.7,
    "TOV" : -0.9
}

def compare_players(df, player1_name, player2_name):
    player1 = df[df["Player"] == player1_name].iloc[0]
    player2 = df[df["Player"] == player2_name].iloc[0]

    score1, score2 = 0, 0
    reasons = []

    for stat, weight in WEIGHTS.items():
        p1_val = float(player1[stat])
        p2_val = float(player2[stat])

        stat_diff = p1_val - p2_val
        weighted_diff = stat_diff * weight

        if weighted_diff > 0:
            reasons.append(f"{player1_name} leads in {stat} ({p1_val} vs {p2_val})")
        elif weighted_diff < 0:
            reasons.append(f"{player2_name} leads in {stat} ({p2_val} vs {p1_val})")

        score1 += p1_val * max(0, weight)
        score2 += p2_val * max(0, weight)
    
    total_score = score1 + score2
    prob = round(score1 / total_score, 2) if total_score > 0 else 0.5

    winner = player1_name if score1 > score2 else player2_name
    return {
        "winner": winner,
        "score": prob,
        "reasons": reasons
    }