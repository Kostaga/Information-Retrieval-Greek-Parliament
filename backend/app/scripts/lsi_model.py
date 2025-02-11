from gensim import corpora, models
import numpy as np
from scripts.dataCleaning import create_clean_data
import os

def preprocess_documents(documents):
    """
    Tokenizes and cleans text documents.
    """
    print("Preprocessing documents...")  # Debugging statement
    return [doc.split() for doc in documents]

def create_lsi_model(num_topics=10):
    """
    Builds an LSI model for topic extraction.
    """
    documents = create_clean_data()[["clean_speech"]]
   
    print("Documents:", documents.head())  # Debugging statement 
    documents = documents["clean_speech"].tolist()
    processed_docs = preprocess_documents(documents)
    print("Processed Docs:", processed_docs[:5])  # Debugging statement
    dictionary = corpora.Dictionary(processed_docs)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in processed_docs]
    print("Doc Term Matrix:", doc_term_matrix[:5])  # Debugging statement
    # Train LSI model
    lsi_model = models.LsiModel(doc_term_matrix, id2word=dictionary, num_topics=num_topics)
    return lsi_model, dictionary, doc_term_matrix
def get_lsi_vectors(lsi_model, doc_term_matrix):
    """
    Converts each document into an LSI topic vector.
    """
    lsi_vectors = [lsi_model[doc] for doc in doc_term_matrix]
    return lsi_vectors



