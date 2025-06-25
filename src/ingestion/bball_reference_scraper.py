import pandas as pd

def get_nba_per_game_stats(season):
    url = f"https://www.basketball-reference.com/leagues/NBA_{season}_per_game.html"

    tables = pd.read_html(url)
    df = tables[0]
    df = df[df["Player"] != "Player"]

    if "Rk" in df.columns:
        df = df.drop(columns=["Rk"])
    
    df = df.reset_index(drop=True)
    
    return df


if __name__ == "__main__":
    print("starting")
    season = "2025"
    df = get_nba_per_game_stats(season)
    df.to_csv(f"data/per_game_{season}.csv", index=False)
    print(f"NBA per-game stats saved to data/processed/per_game_{season}.csv")