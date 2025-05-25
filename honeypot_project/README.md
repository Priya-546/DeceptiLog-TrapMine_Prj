# 🛡️ DeceptiLog-TrapMine: Low-Interaction Web-Based Honeypot with AI/ML Log Analysis and Real-Time Email Alerts
 
## 📌 Overview
**DeceptiLog-TrapMine** is a custom-built, low-interaction honeypot designed to simulate a vulnerable login portal for detecting and analyzing unauthorized access attempts. It logs attacker metadata such as IP addresses, credentials, and headers. The captured data is analyzed using machine learning (KMeans) to uncover behavioral patterns, and visualized using `matplotlib`. Additionally, the system supports **real-time email alerts** for immediate incident notification.
 
---
 
## 🚀 Features
- Deceptive HTML-based fake login page to lure attackers
- Python-based logging server capturing IP, credentials, timestamps, and headers
- Structured CSV logging for easy analysis
- KMeans clustering to detect behavioral anomalies
- Visualizations for:
  - Most frequent attacker IPs
  - Time-based attack trends
  - Clustered attacker behavior
- **📧 Real-time email alerts** when login attempts occur
- Designed to run securely in a virtual environment (e.g., Kali Linux on VMware)
 
---
 
## 🧰 Technologies Used
- **Python 3.x**
- **pandas** – for CSV handling and preprocessing
- **matplotlib** – for visual insights (PNG graphs)
- **scikit-learn** – for KMeans clustering
- **collections** – for IP frequency analysis
- **smtplib / email** – for sending email alerts
- **HTML/CSS** – for the fake login page
- **CSV** – for structured logging
- **VMware + Kali Linux** – for safe, sandboxed deployment
 
---
 
## 📁 Folder Structure
 
```
 
honeypot\_project/
├── .venv/                  # Python virtual environment
├── website/                # Fake login interface (HTML/CSS)
├── server/
│   └── honeypot\_server.py  # HTTP server + real-time logger + email alert trigger
├── data/
│   └── honeypot\_log.csv    # CSV file storing captured intrusion attempts
├── analysis/
│   ├── analyze\_logs.py     # ML-based analysis
│   ├── top\_ips.png         # Output graph
│   ├── attack\_frequency.png
│   └── kmeans\_clusters.png
└── README.md               # Project documentation
 
````
 
---
 
## 💻 Usage Instructions
 
### 1. Install Dependencies
Set up your virtual environment and install required packages:
 
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pandas matplotlib scikit-learn
````
---
 
### 2. Start the Honeypot Server
 
```bash
python server/honeypot_server.py
```
 
This will:
 
* Start a local HTTP server
* Capture attacker inputs
* Append logs to `data/honeypot_log.csv`
* Send **real-time email alerts** on each login attempt
 
> ✉️ **Note:** Configure your email settings (`EMAIL_ADDRESS`, `PASSWORD`, `TO_ADDRESS`) inside `honeypot_server.py` before use.
 
---
 
### 3. Simulate an Attack
 
Open the honeypot in your browser:
 
```
website/secret-login.html
```
 
Enter any dummy credentials to simulate an attack.
 
---
 
### 4. Run Log Analysis
 
Analyze the attacker logs using the KMeans clustering script:
 
```bash
python analysis/analyze_logs.py
```
 
---
 
### 📊 Output Visualizations
 
The following PNG graphs are generated inside the `analysis/` folder:
 
* `top_ips.png` – Top attacking IPs
* `attack_frequency.png` – Trend of attacks over time
* `kmeans_clusters.png` – Behavioral clusters of attackers
 
---
 
## ⚠️ Security Note
 
**Important:**
Deploy this honeypot **only within a sandboxed environment** like a local virtual machine (Kali Linux on VMware/VirtualBox).
**Do NOT expose this honeypot to the public internet**, as it is intentionally designed to appear vulnerable.
 
---
 
## 🔮 Future Enhancements
 
* 🌍 GeoIP integration for attacker location mapping
* 🔐 Admin panel simulation to capture post-login behavior
* 📊 Real-time dashboard for live monitoring
 
---
 
## 👨‍💻 Author
 
** Name:- Priya Kumari **
Final-Year B.voc. Computer Application Student ( B.H.U )
Project Title: *DeceptiLog-TrapMine: A Low-Interaction Honeypot for Behavior-Based Threat Analysis*
 
---
 
## 📬 Contact
 
Feel free to reach out for collaborations or suggestions.
 
```
Email: gunjan.87gn.89@gmail.com
GitHub: https://github.com/Priya-546
```
 
---
 
```
 

