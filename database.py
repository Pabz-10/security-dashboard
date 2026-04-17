import sqlite3
import os

DB_PATH = "security_monitor.db"

def init_db():
    """Initializes the SQLite database and creates the alerts table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            source_ip TEXT NOT NULL,
            event_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            description TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

def write_alert(source_ip, event_type, severity, description):
    """Inserts a new alert into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO alerts (source_ip, event_type, severity, description)
        VALUES (?, ?, ?, ?)
    ''', (source_ip, event_type, severity, description))
    
    conn.commit()
    conn.close()

def get_all_alerts():
    """Retrieves all alerts from the database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM alerts ORDER BY timestamp DESC')
    alerts = cursor.fetchall()
    conn.close()
    return alerts

def get_alert_stats():
    """Retrieves summary statistics for the dashboard."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    stats = {}
    
    # Total alerts
    cursor.execute('SELECT COUNT(*) FROM alerts')
    stats['total'] = cursor.fetchone()[0]
    
    # Severity counts
    cursor.execute('SELECT severity, COUNT(*) FROM alerts GROUP BY severity')
    stats['severity_counts'] = dict(cursor.fetchall())
    
    # Unique IPs
    cursor.execute('SELECT COUNT(DISTINCT source_ip) FROM alerts')
    stats['unique_ips'] = cursor.fetchone()[0]
    
    conn.close()
    return stats

if __name__ == "__main__":
    init_db()
