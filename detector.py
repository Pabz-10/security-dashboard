from database import write_alert
from collections import Counter

SUSPICIOUS_PORTS = ['23', '3389', '445', '4444']

def detect_brute_force(entries, threshold=5):
    """Detects multiple failed logins from the same IP (MITRE T1110)."""
    failed_attempts = [entry['ip'] for entry in entries if entry['event_type'] == 'Failed']
    counts = Counter(failed_attempts)
    
    for ip, count in counts.items():
        if count >= threshold:
            description = f"Potential SSH Brute Force: {count} failed attempts detected from {ip}."
            write_alert(ip, "Brute Force", "HIGH", description)
            print(f"[ALERT] HIGH: {description}")

def detect_suspicious_ports(entries):
    """Detects connection attempts on high-risk ports."""
    for entry in entries:
        if entry['port'] in SUSPICIOUS_PORTS:
            description = f"Connection attempt on suspicious port {entry['port']} from {entry['ip']}."
            write_alert(entry['ip'], "Suspicious Port", "MEDIUM", description)
            print(f"[ALERT] MEDIUM: {description}")

def detect_root_login_attempts(entries):
    """Detects failed login attempts targeting the 'root' user."""
    for entry in entries:
        if entry['username'] == 'root' and entry['event_type'] == 'Failed':
            description = f"Failed root login attempt from {entry['ip']}."
            write_alert(entry['ip'], "Root Login Attempt", "MEDIUM", description)
            print(f"[ALERT] MEDIUM: {description}")

def run_detection(entries):
    """Runs all detection rules on the provided log entries."""
    if not entries:
        return
    
    detect_brute_force(entries)
    detect_suspicious_ports(entries)
    detect_root_login_attempts(entries)
