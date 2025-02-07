from gensim import corpora, models
import numpy as np
from scripts.dataCleaning import create_clean_data
import os

def preprocess_documents(documents):
    """
    Tokenizes and cleans text documents.
    """
    return [[word.lower() for word in doc.split()] for doc in documents]

def create_lsi_model( num_topics=10):
    """
    Builds an LSI model for topic extraction.
    """
    documents = create_clean_data()[["clean_speech"]]
    processed_docs = preprocess_documents(documents)
    dictionary = corpora.Dictionary(processed_docs)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in processed_docs]

    # Train LSI model
    lsi_model = models.LsiModel(doc_term_matrix, id2word=dictionary, num_topics=num_topics)
    return lsi_model, dictionary, doc_term_matrix

def get_lsi_vectors(lsi_model, doc_term_matrix):
    """
    Converts each document into an LSI topic vector.
    """
    return [lsi_model[doc] for doc in doc_term_matrix]

def avg_lsi_vector(lsi_vectors):
    """
    Computes the average LSI topic vector.
    """
    return np.mean([np.array([val for _, val in vec]) for vec in lsi_vectors if vec], axis=0)

