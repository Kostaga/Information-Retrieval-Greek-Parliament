import numpy as np
import os
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from scripts.lsi_model import create_lsi_model, get_lsi_vectors


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
    plt.savefig("inertia_plot.png")
   
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

    labels = kmeans.fit_predict(lsi_vectors_dense)

   
    # Step 5: Plot the Clusters
    plt.figure(figsize=(8, 6))
    for i in range(len(lsi_vectors_dense)):
       plt.scatter(lsi_vectors_dense[i, 0], lsi_vectors_dense[i, 1], c=f"C{labels[i]}")

    plt.xlabel("LSI Topic 1")
    plt.ylabel("LSI Topic 2")
    plt.title("Speech Clustering using LSI & K-Means")
    
    plot_path = os.path.join(os.getcwd(), "cluster_plot.png")  # Use absolute path
    plt.savefig(plot_path)
    plt.close()
    print(f"Cluster plot saved at {plot_path}")  # Debugging output

    return plot_path
    
