import datetime
import subprocess
import random
import sys

def main():
    # Start from 365 days ago up to today
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=365)
    
    current_date = start_date
    print(f"Generating backdated commits from {start_date} to {today}...")
    
    commit_count = 0
    # Loop through each day
    while current_date <= today:
        # We make between 1 and 4 commits per day to get a nice variation of green shades
        num_commits = random.randint(1, 4)
        date_str = current_date.strftime("%Y-%m-%d 12:00:00")
        
        for _ in range(num_commits):
            # Git command to make a backdated empty commit
            cmd = [
                "git", "commit", "--allow-empty", 
                f"--date={date_str}", 
                "-m", f"chore: active development {current_date.strftime('%Y-%m-%d')}"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error making commit for {date_str}: {result.stderr}")
                sys.exit(1)
            commit_count += 1
            
        current_date += datetime.timedelta(days=1)
        
    print(f"Done! Created {commit_count} backdated commits locally.")
    print("Run 'git push' to push them to GitHub and fill your profile calendar with green boxes!")

if __name__ == "__main__":
    main()
