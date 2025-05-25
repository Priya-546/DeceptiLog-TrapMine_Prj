# Import required libraries
import pandas as pd                  # For data manipulation and analysis
import matplotlib.pyplot as plt      # For plotting graphs
from collections import Counter      # For counting occurrences (not used in current code, but often helpful)
from sklearn.cluster import KMeans   # For clustering analysis (unsupervised ML)
import numpy as np                   # For numerical operations

# ================================
# STEP 1: Load and Clean the Log Data
# ================================

# Load honeypot log CSV file
df = pd.read_csv('../data/honeypot_log.csv')

# Convert 'Timestamp' column to datetime format; invalid entries become NaT
df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')

# Drop rows where timestamp conversion failed (NaT)
df = df.dropna(subset=['Timestamp'])

# Print the total number of requests recorded
print("Total requests logged:", len(df))

# ================================
# STEP 2: Identify Top 5 Attacker IPs
# ================================

# Count frequency of each IP and get top 5 attacker IPs
top_ips = df['IP'].value_counts().head(5)

# Display the top 5 IPs
print("\nTop 5 Attacker IPs:")
print(top_ips)

# ================================
# STEP 3: Visualization - Top IPs
# ================================

try:
    # Create a bar chart for the top 5 IPs
    plt.figure(figsize=(8, 5))
    plt.bar(top_ips.index, top_ips.values, color='orange')
    plt.title("Top Attacker IPs")
    plt.xlabel("IP Address")
    plt.ylabel("Request Count")
    plt.xticks(rotation=45)  # Rotate IP labels for better readability
    plt.tight_layout()
    plt.savefig("top_ips.png")  # Save the figure as an image
    print("✅ Saved: top_ips.png")
except Exception as e:
    print("❌ Failed to save top_ips.png:", e)

# ================================
# STEP 4: Visualization - Attack Frequency Over Time
# ================================

try:
    # Set Timestamp as index for resampling
    df.set_index('Timestamp', inplace=True)

    # Resample the data to get number of attacks per hour
    hourly_attacks = df.resample('H').size()

    # Plot the attack frequency over time
    plt.figure(figsize=(10, 4))
    plt.plot(hourly_attacks.index, hourly_attacks.values, color='blue', marker='o')
    plt.title("Attack Frequency Over Time")
    plt.xlabel("Time")
    plt.ylabel("Requests per Hour")
    plt.tight_layout()
    plt.savefig("attack_frequency.png")  # Save the figure
    print("✅ Saved: attack_frequency.png")
except Exception as e:
    print("❌ Failed to save attack_frequency.png:", e)

# ================================
# STEP 5: KMeans Clustering - Attack Timing Pattern
# ================================

try:
    # Reset index to get Timestamp back as a column
    df_reset = df.reset_index()

    # Extract hour and minute from the timestamp
    df_reset['Hour'] = df_reset['Timestamp'].dt.hour
    df_reset['Minute'] = df_reset['Timestamp'].dt.minute

    # Prepare data for clustering based on hour and minute
    X = df_reset[['Hour', 'Minute']]

    # Apply KMeans clustering to group attacks based on time
    kmeans = KMeans(n_clusters=2, random_state=0)  # You can tune n_clusters
    df_reset['Cluster'] = kmeans.fit_predict(X)

    # Visualize the clusters
    plt.figure(figsize=(6, 6))
    colors = ['red', 'green']
    for i in range(2):
        cluster_data = df_reset[df_reset['Cluster'] == i]
        plt.scatter(cluster_data['Hour'], cluster_data['Minute'], 
                    label=f'Cluster {i}', color=colors[i])

    plt.xlabel("Hour")
    plt.ylabel("Minute")
    plt.title("KMeans Clustering of Attack Times")
    plt.legend()
    plt.tight_layout()
    plt.savefig("kmeans_clusters.png")  # Save the cluster plot
    print("✅ Saved: kmeans_clusters.png")
except Exception as e:
    print("❌ Failed to save kmeans_clusters.png:", e)
