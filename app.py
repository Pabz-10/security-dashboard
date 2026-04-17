from flask import Flask, render_template
import database

app = Flask(__name__)

@app.route('/')
def index():
    """Dashboard Overview."""
    stats = database.get_alert_stats()
    all_alerts = database.get_all_alerts()
    recent_alerts = all_alerts[:5]  # Last 5 alerts
    return render_template('index.html', stats=stats, recent_alerts=recent_alerts)

@app.route('/alerts')
def alerts():
    """Full Alerts Table."""
    all_alerts = database.get_all_alerts()
    return render_template('alerts.html', alerts=all_alerts)

@app.route('/report')
def report():
    """Security Report Summary."""
    all_alerts = database.get_all_alerts()
    
    # Calculate top 5 threat sources
    ip_counts = {}
    for alert in all_alerts:
        ip = alert['source_ip']
        ip_counts[ip] = ip_counts.get(ip, 0) + 1
    
    top_ips = sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Most common attack type
    type_counts = {}
    for alert in all_alerts:
        e_type = alert['event_type']
        type_counts[e_type] = type_counts.get(e_type, 0) + 1
    
    most_common_type = max(type_counts.items(), key=lambda x: x[1])[0] if type_counts else "N/A"
    
    return render_template('report.html', top_ips=top_ips, most_common_type=most_common_type, total_alerts=len(all_alerts))

if __name__ == "__main__":
    database.init_db()
    app.run(debug=True, port=5001)
