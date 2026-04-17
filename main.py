import os
import subprocess
import time
from parser import parse_auth_log
from detector import run_detection
import database

def main():
    # 1. Initialize DB
    database.init_db()
    
    # 2. Generate Logs (Simulate activity)
    print("Step 1: Generating simulated logs...")
    subprocess.run(["python3", "scripts/generate_logs.py"])
    
    # 3. Parse and Detect
    print("Step 2: Parsing logs and running detection...")
    log_file = "logs/sample_auth.log"
    entries = parse_auth_log(log_file)
    run_detection(entries)
    
    print("Step 3: Starting dashboard...")
    print("Go to http://127.0.0.1:5001 to view the dashboard.")
    subprocess.run(["python3", "app.py"])

if __name__ == "__main__":
    main()
