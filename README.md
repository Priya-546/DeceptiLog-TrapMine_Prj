# DeceptiLog-TrapMine_Prj
 An Intelligent Framework for Visual Analytics and Behavioral Segmentation of Honeypot Attack Patterns.

Overview

This project simulates a fake login page to trap unauthorized users. All interactions are logged and analyzed using Python, Pandas, and basic Machine Learning (K-Means).
Usage

    Run the honeypot server:

python server/honeypot_server.py

    Open website/secret-login.html and submit fake login data.
    Run analysis:

python analysis/analyze_logs.py
Output

    top_ips.png: Shows most aggressive IPs.
    attack_frequency.png: Shows attack trends over time.
    kmeans_clusters.png: Clustering of attacks.

Security Note
Run only in isolated environment (VM). Do not expose to the internet.
