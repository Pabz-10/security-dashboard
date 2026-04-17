# Security Monitoring Dashboard

## Project Overview
NetWatch is a lightweight Security Information and Event Management (SIEM) prototype designed to demonstrate core concepts of log analysis, threat detection, and security visualization. It parses SSH authentication logs to identify common attack patterns and displays them on a centralized dashboard.

## Features
- **Automated Log Parsing**: Uses regular expressions to extract structured data from raw Linux auth logs.
- **Threat Detection Engine**: Implements rules to identify malicious activity based on real-world attack patterns.
- **Security Dashboard**: A clean, dark-themed UI providing a high-level overview of security events.
- **Data Persistence**: Stores alerts in a SQLite database for recurring analysis and reporting.

## Detection Rules (MITRE ATT&CK Mapping)
The following detection rules are implemented in `detector.py`:

1. **SSH Brute Force (T1110)**: 
   - **Logic**: Flags any IP address with more than 5 failed login attempts in the analyzed log period.
   - **Severity**: HIGH
2. **Suspicious Port Connection (T1046)**:
   - **Logic**: Monitors for connection attempts on high-risk ports like 23 (Telnet), 3389 (RDP), and 4444 (Metasploit).
   - **Severity**: MEDIUM
3. **Unauthorized Root Login Attempt (T1078.003)**:
   - **Logic**: Specifically flags failed login attempts targeting the 'root' administrative account.
   - **Severity**: MEDIUM

## Tech Stack
- **Backend**: Python, Flask
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3 (Vanilla)
- **Log Processing**: Regular Expressions (Regex)

## How to Run
1. **Install Dependencies**:
   ```bash
   pip install flask
   ```
2. **Initialize and Run**:
   ```bash
   python3 main.py
   ```
   This script will:
   - Initialize the local database.
   - Generate a simulated `auth.log` file with embedded attack patterns.
   - Parse the logs and populate the dashboard with alerts.
   - Start the Flask web server.

3. **Access the Dashboard**:
   Open your browser and navigate to `http://127.0.0.1:5001`.

## Future Improvements
- **Real-time Monitoring**: Implementing `tail -f` logic or a file watcher (like `watchdog`) to process logs as they are written.
- **Geolocation**: Integrating an IP geolocation API to map the physical origin of threats.
- **Advanced Visualization**: Adding charts (e.g., Chart.js) to show attack trends over time.
- **Alerting**: Email or Slack notifications for HIGH severity alerts.
