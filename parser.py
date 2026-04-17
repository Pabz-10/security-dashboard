import re
from datetime import datetime

# Regex pattern for SSH auth logs
# Example: Jan 15 06:23:12 server sshd[1234]: Failed password for root from 192.168.1.105 port 4444 ssh2
SSH_LOG_PATTERN = r'(?P<timestamp>\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2})\s+\S+\s+sshd\[\d+\]:\s+(?P<event_type>Failed|Accepted)\s+password\s+for\s+(?P<username>\S+)\s+from\s+(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+port\s+(?P<port>\d+)'

def parse_auth_log(file_path):
    """Parses an SSH auth log file and returns a list of structured dictionaries."""
    parsed_entries = []
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                match = re.search(SSH_LOG_PATTERN, line)
                if match:
                    entry = match.groupdict()
                    parsed_entries.append(entry)
    except FileNotFoundError:
        print(f"Error: Log file not found at {file_path}")
    
    return parsed_entries

if __name__ == "__main__":
    # Test with a dummy line
    test_line = "Jan 15 06:23:12 server sshd[1234]: Failed password for root from 192.168.1.105 port 4444 ssh2"
    match = re.search(SSH_LOG_PATTERN, test_line)
    if match:
        print("Regex test successful:")
        print(match.groupdict())
    else:
        print("Regex test failed.")
