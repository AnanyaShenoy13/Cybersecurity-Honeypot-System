from flask import Flask, render_template, jsonify, request, redirect, url_for, send_file
from flask_socketio import SocketIO, emit
from threading import Thread
from datetime import datetime
import random
import socket
import struct
import json
import os
from fpdf import FPDF

app = Flask(__name__)
socketio = SocketIO(app)

# Global variables
recent_activity = []
threshold_value = 10  # Initial threshold value for demo purposes

# Sample data for demonstration purposes
attack_frequency_data = {
    "labels": ["SQL Injection", "XSS", "Brute Force", "DDoS", "Phishing"],
    "datasets": [{
        "label": "Frequency of Attack Types",
        "data": [12, 19, 3, 5, 2],
        "backgroundColor": [
            "rgba(255, 99, 132, 0.2)",
            "rgba(54, 162, 235, 0.2)",
            "rgba(255, 206, 86, 0.2)",
            "rgba(75, 192, 192, 0.2)",
            "rgba(153, 102, 255, 0.2)"
        ],
        "borderColor": [
            "rgba(255, 99, 132, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(255, 206, 86, 1)",
            "rgba(75, 192, 192, 1)",
            "rgba(153, 102, 255, 1)"
        ],
        "borderWidth": 1
    }]
}

attack_trend_data = {
    "labels": ["January", "February", "March", "April", "May", "June", "July"],
    "datasets": [{
        "label": "Attack Trends Over Time",
        "data": [3, 2, 2, 1, 5, 3, 4],
        "backgroundColor": "rgba(153, 102, 255, 0.2)",
        "borderColor": "rgba(153, 102, 255, 1)",
        "borderWidth": 1
    }]
}

attack_geo_data = {
    "labels": ["North America", "Europe", "Asia", "South America", "Africa"],
    "datasets": [{
        "label": "Geographic Distribution of Attacks",
        "data": [10, 5, 8, 2, 3],
        "backgroundColor": [
            "rgba(255, 99, 132, 0.2)",
            "rgba(54, 162, 235, 0.2)",
            "rgba(255, 206, 86, 0.2)",
            "rgba(75, 192, 192, 0.2)",
            "rgba(153, 102, 255, 0.2)"
        ],
        "borderColor": [
            "rgba(255, 99, 132, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(255, 206, 86, 1)",
            "rgba(75, 192, 192, 1)",
            "rgba(153, 102, 255, 1)"
        ],
        "borderWidth": 1
    }]
}

# Function to log attacks to a file
def log_attack_to_file(timestamp, ip_address, attack_type):
    log_entry = {
        "timestamp": timestamp,
        "ip_address": ip_address,
        "attack_type": attack_type
    }
    log_file = os.path.join(os.path.dirname(__file__), "additional_logs.json")
    
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            data = json.load(f)
    else:
        data = []
    
    data.append(log_entry)
    
    with open(log_file, "w") as f:
        json.dump(data, f, indent=4)

# Route to handle logging of attacks from logs.html
@app.route('/api/log_additional_attack', methods=['POST'])
def log_additional_attack():
    data = request.get_json()
    timestamp = data.get('timestamp')
    ip_address = data.get('ip_address')
    attack_type = data.get('attack_type')
    
    if not (timestamp and ip_address and attack_type):
        return jsonify({'error': 'Invalid data format'}), 400
    
    log_attack_to_file(timestamp, ip_address, attack_type)
    return jsonify({'message': 'Additional attack logged successfully'}), 200

@app.route('/')
def home():
    return render_template('index.html', recent_activity=recent_activity)

@app.route('/logs')
def logs():
    log_file = os.path.join(os.path.dirname(__file__), "additional_logs.json")
    with open(log_file, "r") as f:
        additional_logs = json.load(f)
    return render_template('logs.html', attack_logs=recent_activity, additional_logs=additional_logs)

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    global threshold_value
    if request.method == 'POST':
        threshold = int(request.form['threshold'])
        # Dummy logic to simulate saving settings
        threshold_value = threshold
        return redirect(url_for('settings'))
    return render_template('settings.html', threshold=threshold_value)

@app.route('/api/attack_frequency')
def api_attack_frequency():
    return jsonify(attack_frequency_data)

@app.route('/api/attack_trend')
def api_attack_trend():
    return jsonify(attack_trend_data)

@app.route('/api/attack_geo')
def api_attack_geo():
    return jsonify(attack_geo_data)

@app.route('/api/log_alerts_to_file', methods=['GET'])
def log_alerts_to_file():
    try:
        # Example: Log alert to a file
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ip_address = request.remote_addr
        
        with open('honeypot_alerts.log', 'a') as log_file:
            log_file.write(f"Alert logged: Device IP: {ip_address} - Timestamp: {timestamp}\n")
        
        return 'Alert logged successfully', 200
    except Exception as e:
        return str(e), 500

# Route to download logs as a PDF
@app.route('/download_logs')
def download_logs():
    log_file = os.path.join(os.path.dirname(__file__), "additional_logs.json")
    with open(log_file, "r") as f:
        additional_logs = json.load(f)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add a title
    pdf.cell(200, 10, txt="Attack Logs - Additional Logs", ln=True, align='C')

    # Add table headers
    pdf.cell(60, 10, txt="Timestamp", border=1, align='C')
    pdf.cell(50, 10, txt="IP Address", border=1, align='C')
    pdf.cell(80, 10, txt="Type of Attack", border=1, align='C')
    pdf.ln()

    # Add table rows
    for log in additional_logs:
        pdf.cell(60, 10, txt=log["timestamp"], border=1)
        pdf.cell(50, 10, txt=log["ip_address"], border=1)
        pdf.cell(80, 10, txt=log["attack_type"], border=1)
        pdf.ln()

    pdf_output = os.path.join(os.path.dirname(__file__), "attack_logs.pdf")
    pdf.output(pdf_output)

    return send_file(pdf_output, as_attachment=True)

def simulate_attacks():
    global threshold_value
    while True:
        simulate_attack()
        # Check against threshold and send alert if needed
        if len(recent_activity) >= threshold_value:
            # Dummy function call for email alert (removed actual email sending)
            pass
        socketio.sleep(5)

def simulate_attack():
    mock_attack = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'ip_address': generate_random_ip(),
        'attack_type': random.choice(['SQL Injection', 'XSS', 'Brute Force', 'DDoS', 'Phishing'])
    }
    recent_activity.append(mock_attack)
    
    # Log attack to file
    log_attack_to_file(mock_attack['timestamp'], mock_attack['ip_address'], mock_attack['attack_type'])
    
    socketio.emit('update_activity', recent_activity)

def generate_random_ip():
    return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

if __name__ == '__main__':
    attack_thread = Thread(target=simulate_attacks, daemon=True)
    attack_thread.start()
    socketio.run(app, debug=True)
