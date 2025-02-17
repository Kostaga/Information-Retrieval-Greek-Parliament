import numpy as np
import os
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from scripts.lsi_model import create_lsi_model, get_lsi_vectors


def plot_inertia(doc_term_matrix, max_clusters=10):
    data = np.array(doc_term_matrix, dtype=object)  # Ensure it's an array
    data = np.vstack(data)  # Stack it properly into a 2D array

    inertias = []
    for k in range(1, max_clusters + 1):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10, max_iter=100, algorithm="elkan")
        kmeans.fit(data)  # Ensure data is correctly shaped
        inertias.append(kmeans.inertia_)

    plt.figure(figsize=(8, 6))
    plt.plot(range(2, max_clusters + 1), inertias, marker='o')
    plt.xlabel("Number of Clusters")
    plt.ylabel("Inertia")
    plt.title("Elbow Method for Optimal Clusters")

    plot_path = "elbow_plot.png"
    plt.savefig(plot_path)
    plt.close('all')

   
#Converts sparse LSI vectors to a dense NumPy array.
def convert_lsi_vectors_to_dense(lsi_vectors, num_topics):
    dense_vectors = np.zeros((len(lsi_vectors), num_topics))  # Create a zero-filled matrix
    for i, doc in enumerate(lsi_vectors):
        for topic_id, value in doc:
            dense_vectors[i, topic_id] = value  # Assign topic value
    return dense_vectors

def kmeans():
   
    # Build the LSI model
    lsi_model, dictionary, doc_term_matrix = create_lsi_model(num_topics=2)


    # Transform speeches into LSI vectors
    lsi_vectors = get_lsi_vectors(lsi_model, doc_term_matrix)

    # Convert LSI vectors to a dense matrix
    num_topics = 2  # Set the number of topics
    lsi_vectors_dense = convert_lsi_vectors_to_dense(lsi_vectors, num_topics)

    kmeans = KMeans(n_clusters=2, random_state=42, n_init=10, max_iter=100, algorithm="elkan")  

    labels = np.array(kmeans.fit_predict(lsi_vectors_dense))

   
    # Step 5: Plot the Clusters
    plt.figure(figsize=(8, 6))
    plt.scatter(lsi_vectors_dense[:, 0], lsi_vectors_dense[:, 1], c=labels, cmap='viridis', edgecolors='k')


    plt.xlabel("LSI Topic 1")
    plt.ylabel("LSI Topic 2")
    plt.title("Speech Clustering using LSI & K-Means")
    
    plot_path = os.path.join(os.getcwd(), "cluster_plot.png")  # Use absolute path
    plt.savefig(plot_path)
    
    plt.close('all')  # Explicitly close the figure

    print(f"Cluster plot saved at {plot_path}")  # Debugging output

    return plot_path
    
