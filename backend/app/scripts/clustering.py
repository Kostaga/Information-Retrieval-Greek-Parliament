import numpy as np
import os
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from flask import Flask, send_file
import matplotlib.pyplot as plt
from scripts.dataCleaning import create_clean_data
from scripts.stopwords import STOPWORDS
from scripts.similarity import tokenize_with_spacy, create_gensim_lsa_model




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
    data = create_clean_data()[["clean_speech"]]
    doc_clean = data.apply(tokenize_with_spacy)
    df = create_gensim_lsa_model(doc_clean, number_of_topics=7, words=10)

    plot_inertia(df, max_clusters=10)

    kmeans = KMeans(n_clusters=5)
    kmeans.fit(df)
    df["cluster"] = kmeans.labels_

    # Scatter plot
    plt.scatter(df["x"], df["y"], c=df["cluster"])

    # Save the plot in a static folder
    plot_path = os.path.join("static", "cluster_plot.png")
    plt.savefig(plot_path)
    plt.close()  # Close plot to prevent memory issues

    print(f"Cluster plot saved at {plot_path}")
    return plot_path


# def kmeans():
#     speeches = create_clean_data()[["clean_speech"]]
#     # Step 2: Convert text to TF-IDF vectors
#     vectorizer = TfidfVectorizer(stop_words=STOPWORDS)
#     X_tfidf = vectorizer.fit_transform(speeches)

#     # Step 3: Apply LSA (Dimensionality Reduction)
#     lsa = TruncatedSVD(n_components=2)
#     X_lsa = lsa.fit_transform(X_tfidf)

#     # Step 4: Apply K-Means Clustering
#     num_clusters = 10  # Change as needed
#     kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
#     labels = kmeans.fit_predict(X_lsa)

#     # Step 5: Create and Save the Cluster Plot
#     plt.figure(figsize=(8, 6))
#     colors = ['blue', 'red', 'green', 'purple', 'orange']
#     for i in range(len(X_lsa)):
#         plt.scatter(X_lsa[i, 0], X_lsa[i, 1], color=colors[labels[i]], label=f'Cluster {labels[i]}' if f'Cluster {labels[i]}' not in plt.gca().get_legend_handles_labels()[1] else "")
#     plt.xlabel("LSA Component 1")
#     plt.ylabel("LSA Component 2")
#     plt.title("Speech Clustering using LSA & K-Means")
#     plt.legend()
#     plt.savefig("cluster_plot.png")
#     plt.close()

# if __name__ == "__main__":
#     kmeans()