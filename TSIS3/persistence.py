import json
import os

def load_data(filename, default):
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        with open(filename, 'w') as f:
            json.dump(default, f, indent=4)
        return default
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return default

def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def update_leaderboard(name, score):
    lb = load_data('leaderboard.json', [])
    lb.append({"name": name, "score": score})
    # Sort by score descending and keep top 10
    lb = sorted(lb, key=lambda x: x['score'], reverse=True)[:10]
    save_data('leaderboard.json', lb)