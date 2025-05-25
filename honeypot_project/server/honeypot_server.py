from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import datetime
import csv
import os
import smtplib
from email.message import EmailMessage
from urllib.parse import parse_qs

# === Configuration and File Paths ===

# Log file where all captured login attempts will be stored
LOG_FILE = "../data/honeypot_log.csv"

# Path to the fake login page served by the honeypot
LOGIN_PAGE_PATH = os.path.join(os.path.dirname(__file__), "website", "secret-login.html")

# Email credentials for sending alerts (ensure to use app passwords for security)
SENDER_EMAIL = "my.love.14356789@gmail.com"
SENDER_PASSWORD = "zpah cibd nluz scwe"
RECEIVER_EMAIL = "my.love.14356789@gmail.com"

# === Email Notification System ===

def send_email_alert(ip, timestamp, post_data, user_agent):
    """Sends an email alert when a fake login attempt is detected."""
    try:
        msg = EmailMessage()
        msg['Subject'] = '⚠️ Honeypot Alert: Fake Login Attempt Detected'
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL

        # Email body contains key metadata
        body = f"""🚨 Fake login attempt detected!

IP Address  : {ip}
Timestamp   : {timestamp}
User Agent  : {user_agent}
Login Data  : {post_data}
        """
        msg.set_content(body)

        # Send email securely using SMTP over SSL
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)

        print("[+] Email alert sent successfully.")
    except Exception as e:
        print(f"[!] Failed to send email alert: {e}")

# === HTTP Request Handler Class ===

class HoneypotHandler(BaseHTTPRequestHandler):
    """Custom HTTP handler for simulating a deceptive login endpoint."""

    def _set_headers(self, code=200, content_type='application/json'):
        """Sends HTTP response headers."""
        self.send_response(code)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        """Handles CORS preflight requests."""
        self._set_headers()

    def do_GET(self):
        """Handles GET requests — serves the fake login page."""
        if self.path == "/" or self.path == "/login":
            try:
                with open(LOGIN_PAGE_PATH, "rb") as file:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(file.read())
            except FileNotFoundError:
                self.send_error(404, "Login page not found.")
        else:
            self.send_error(404, "Page not found.")

    def do_POST(self):
        """Handles POST requests — logs login data and triggers alert."""
        if self.path == "/login":
            # Read POST request body
            content_length = int(self.headers.get('Content-Length', 0))
            post_data_raw = self.rfile.read(content_length).decode('utf-8')

            # Attempt to parse login credentials from JSON
            try:
                post_json = json.loads(post_data_raw)
                username = post_json.get('username', '')
                password = post_json.get('password', '')
                formatted_data = f"username={username}, password={password}"
            except json.JSONDecodeError:
                formatted_data = post_data_raw

            # Collect metadata
            ip = self.client_address[0]
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            path = self.path
            method = self.command
            user_agent = self.headers.get('User-Agent', '-')

            # Prepare log row
            new_row = [ip, timestamp, path, method, user_agent, formatted_data]

            # Append data to CSV log file
            file_exists = os.path.isfile(LOG_FILE)
            with open(LOG_FILE, 'a', newline='') as file:
                writer = csv.writer(file)
                if not file_exists or os.stat(LOG_FILE).st_size == 0:
                    writer.writerow(['IP', 'Timestamp', 'Path', 'Method', 'User-Agent', 'Data'])
                writer.writerow(new_row)

            print(f"[+] Logged request from {ip} to {path}")

            # Send real-time alert via email
            send_email_alert(ip, timestamp, formatted_data, user_agent)

            # Respond to attacker (deceptive success/failure message)
            self._set_headers(200)
            response = {"message": "Fake login recorded"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_error(404, "Not Found")

# === Server Initialization ===

if __name__ == "__main__":
    server_address = ('0.0.0.0', 8000)  # Listen on all interfaces, port 8000
    httpd = HTTPServer(server_address, HoneypotHandler)
    print("[*] Honeypot Server running on port 8000")
    httpd.serve_forever()
