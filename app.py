from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import tempfile
import os
import requests
import subprocess

app = Flask(__name__)
CORS(app)

# ClamAV executable path
CLAMAV_PATH = r"C:\Users\BADAL ROY\Downloads\clamav-1.4.2-r1-winxp-x86\clamav-1.4.2-r1-winxp-x86\clamscan.exe"

# Home page route (root URL)
@app.route('/')
def index():
    return render_template('index.html')

# Other page routes
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/monitor')
def monitor():
    return render_template('monitor.html')

@app.route('/file')
def file():
    return render_template('file.html')

@app.route('/phishing')
def phishing():
    return render_template('phishing.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# File malware scan route
@app.route('/scan/file', methods=['POST'])
def scan_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400
    
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file.save(temp_file.name)
        temp_file_path = temp_file.name

    result = scan_file_with_clamav(temp_file_path)

    try:
        os.unlink(temp_file_path)
    except Exception as e:
        print("Temporary file delete error:", e)

    return jsonify({"status": result})

# Function to scan file using ClamAV
def scan_file_with_clamav(file_path):
    try:
        result = subprocess.run([CLAMAV_PATH, file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "Infected files: 1" in result.stdout:
            return "malicious"
        elif "Infected files: 0" in result.stdout:
            return "clean"
        else:
            return f"error: {result.stdout.strip()} {result.stderr.strip()}"
    except Exception as e:
        return f"error: {str(e)}"

# URL phishing/malware scan route
@app.route('/scan/url', methods=['POST'])
def scan_url():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    status = check_url_safety("AIzaSyBCvXsBmFSxUEsbD3nV_-lmAqBjZYhUKuo", url)
    return jsonify({"status": status})

# Google Safe Browsing API URL check
def check_url_safety(api_key, url_to_check):
    api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}"
    payload = {
        "client": {
            "clientId": "yourcompanyname",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": url_to_check}
            ]
        }
    }
    response = requests.post(api_url, json=payload)
    if response.status_code == 200:
        if response.json().get('matches'):
            return "malicious"
        else:
            return "safe"
    else:
        return "error"

# Fake login detector route
@app.route('/scan/fake-login', methods=['POST'])
def detect_fake_login():
    data = request.get_json()
    html_content = data.get("html", "").lower()
    if "login" in html_content and ("action=" not in html_content or "example.com" in html_content):
        return jsonify({"status": "fake"})
    return jsonify({"status": "safe"})

if __name__ == '__main__':
    app.run(debug=True)
