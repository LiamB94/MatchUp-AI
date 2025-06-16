import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

import pandas as pd
from scoring.comparator import compare_players


csv_path = project_root / "data" / "per_game_2025.csv"

df = pd.read_csv(csv_path)
result = compare_players(df, "LeBron James", "Jahlil Okafor")

print(f"🏆 Winner: {result['winner']}")
print(f"🔢 Score: {result['score']}")
print("🧠 Reasons:")
for reason in result["reasons"]:
    print(f"- {reason}")
