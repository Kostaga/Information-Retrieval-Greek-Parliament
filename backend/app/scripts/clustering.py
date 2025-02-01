import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from scripts.dataCleaning import create_clean_data




def plot_inertia(data, max_clusters=10):
    # Calculate the inertia for a range of cluster counts
    inertias = []
    for k in range(1, max_clusters + 1):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(data)
        inertias.append(kmeans.inertia_)

    # Plot the inertia values
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, max_clusters + 1), inertias, marker='o', linestyle='--')
    plt.xlabel("Number of Clusters")
    plt.ylabel("Inertia")
    plt.title("Inertia Plot for K-Means Clustering")
    plt.grid(True)
    plt.show()


def kmeans():
    df = create_clean_data()
    kmeans = KMeans(n_clusters=5, random_state=42)
    kmeans.fit(df)
    plot_inertia(df)
    kmeans_labels = kmeans.labels_
    kmeans_centroids = kmeans.cluster_centers_
    print("here")
    plt.figure(figsize=(10, 8))
    
    unique_clusters = np.unique(kmeans_labels)
    cmap = plt.get_cmap('viridis', len(unique_clusters))
    for cluster_id in unique_clusters:
        cluster_data = df[kmeans_labels == cluster_id]

        # Use a consistent color for the cluster, but vary the markers for its subclusters
        cluster_color = cmap(cluster_id / len(unique_clusters))  # Assign color based on the cluster ID
    
    # Highlight K-Means centroids
    plt.scatter(
        kmeans_centroids[:, 0], kmeans_centroids[:, 1],
        marker='*', s=200, c='black', edgecolors='white', label='K-Means Centroids'
    )

    plt.title("K-Means Clustering on the Speeches Dataset")
    plt.savefig('static/kmeans_plot.png')  # Save the plot as an image file
    plt.show()