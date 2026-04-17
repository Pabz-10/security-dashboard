import random
import time
from datetime import datetime
import os

LOG_FILE = "logs/sample_auth.log"

IPS = ["192.168.1.10", "10.0.0.5", "172.16.0.20", "192.168.1.50"]
ATTACKER_IPS = ["45.33.22.11", "185.220.101.5", "203.0.113.42"]
USERNAMES = ["admin", "root", "user1", "guest", "test", "webmaster"]
SUSPICIOUS_PORTS = [23, 3389, 445, 4444]

def generate_log_line(ip=None, user=None, event="Failed", port=None):
    timestamp = datetime.now().strftime("%b %d %H:%M:%S")
    ip = ip or random.choice(IPS)
    user = user or random.choice(USERNAMES)
    port = port or random.randint(1024, 65535)
    
    return f"{timestamp} server sshd[1234]: {event} password for {user} from {ip} port {port} ssh2\n"

def simulate_brute_force(attacker_ip):
    lines = []
    # 10 failed attempts in quick succession
    for _ in range(10):
        lines.append(generate_log_line(ip=attacker_ip, user="root", event="Failed"))
    return lines

def simulate_suspicious_port(attacker_ip):
    return [generate_log_line(ip=attacker_ip, port=random.choice(SUSPICIOUS_PORTS))]

def main():
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    print(f"Generating simulated logs in {LOG_FILE}...")
    
    with open(LOG_FILE, "w") as f:
        # Generate some legitimate traffic
        for _ in range(50):
            f.write(generate_log_line(event="Accepted"))
        
        # Inject Brute Force attacks
        for attacker in ATTACKER_IPS:
            for line in simulate_brute_force(attacker):
                f.write(line)
        
        # Inject Suspicious Port connections
        for attacker in ATTACKER_IPS:
            for line in simulate_suspicious_port(attacker):
                f.write(line)
        
        # Some more random failures
        for _ in range(20):
            f.write(generate_log_line(event="Failed"))

    print("Log generation complete.")

if __name__ == "__main__":
    main()
