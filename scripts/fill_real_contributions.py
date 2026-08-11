import datetime
import json
import os
import random
import subprocess
import sys

# Default configuration
USERNAME = os.environ.get("GH_PROFILE_USER", "Arjun-coder-ops")
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "contributions.json")

def compute_current_streak(days):
    idx = len(days) - 1
    if days[idx]["count"] == 0:
        idx -= 1  # today isn't over yet -- don't break the streak on it
    streak = 0
    end_idx = idx
    while idx >= 0 and days[idx]["count"] > 0:
        streak += 1
        idx -= 1
    start_idx = idx + 1
    if streak == 0:
        return 0, None, None
    return streak, days[start_idx]["date"], days[end_idx]["date"]


def compute_longest_streak(days):
    longest = run = 0
    longest_start = longest_end = None
    run_start_idx = None
    for i, d in enumerate(days):
        if d["count"] > 0:
            if run == 0:
                run_start_idx = i
            run += 1
            if run > longest:
                longest = run
                longest_start = days[run_start_idx]["date"]
                longest_end = days[i]["date"]
        else:
            run = 0
    return longest, longest_start, longest_end


def build_data(days):
    total = sum(d["count"] for d in days)
    active_days = sum(1 for d in days if d["count"] > 0)
    best = max(days, key=lambda d: d["count"])
    cur_len, cur_start, cur_end = compute_current_streak(days)
    long_len, long_start, long_end = compute_longest_streak(days)

    monthly = {}
    for d in days:
        key = d["date"][:7]
        monthly[key] = monthly.get(key, 0) + d["count"]
    monthly_list = [{"month": k, "total": v} for k, v in sorted(monthly.items())]

    return {
        "username": USERNAME,
        "generated_at": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "range": {"start": days[0]["date"], "end": days[-1]["date"]},
        "total_contributions": total,
        "active_days": active_days,
        "avg_per_active_day": round(total / active_days, 1) if active_days else 0,
        "current_streak": {"length": cur_len, "start": cur_start, "end": cur_end},
        "longest_streak": {"length": long_len, "start": long_start, "end": long_end},
        "best_day": {"date": best["date"], "count": best["count"]},
        "monthly": monthly_list,
        "days": days,
    }


def main():
    random.seed(42)  # Fixed seed for deterministic behavior
    
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=365)
    
    current_date = start_date
    days = []
    
    print(f"Generating backdated commits stats from {start_date} to {today}...")
    
    # 1. Prepare deterministic stats first
    while current_date <= today:
        date_str = current_date.strftime("%Y-%m-%d")
        
        is_active = random.random() < 0.55  # ~55% probability of activity
        if is_active:
            count = random.randint(2, 4)
        else:
            count = 0
            
        days.append({"date": date_str, "count": count})
        current_date += datetime.timedelta(days=1)
        
    # Write the contributions.json data
    data = build_data(days)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        
    print(f"Wrote stats to {OUT_PATH}.")
    print(f"Computed stats: {data['total_contributions']} contributions across {data['active_days']} active days.")
    
    # 2. Make the local commits
    print("Now executing git commits (this might take a few seconds)...")
    commit_count = 0
    for d in days:
        if d["count"] == 0:
            continue
            
        date_str = d["date"] + " 12:00:00"
        for _ in range(d["count"]):
            cmd = [
                "git", "commit", "--allow-empty", 
                f"--date={date_str}", 
                "-m", f"chore: active development {d['date']}"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error making commit for {date_str}: {result.stderr}")
                sys.exit(1)
            commit_count += 1
            
    print(f"Finished! Created {commit_count} backdated commits locally.")
    print("Next step: force-push your repository to apply changes on GitHub!")

if __name__ == "__main__":
    main()
