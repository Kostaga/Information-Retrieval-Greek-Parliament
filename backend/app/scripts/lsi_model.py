from gensim import corpora, models
import numpy as np
from scripts.dataCleaning import create_clean_data
import os

# Builds an LSI model for topic extraction.
def create_lsi_model(num_topics):

    documents = create_clean_data()[["clean_speech"]]

    documents = documents["clean_speech"].tolist()
    processed_docs = [doc.split() for doc in documents] # Tokenizes text documents
   
    # Create a dictionary representation of the documents.
    dictionary = corpora.Dictionary(processed_docs)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in processed_docs]
    
    # Train LSI model
    lsi_model = models.LsiModel(doc_term_matrix, id2word=dictionary, num_topics=num_topics)
    
    return lsi_model, dictionary, doc_term_matrix
    
# Converts each document into an LSI topic vector.
def get_lsi_vectors(lsi_model, doc_term_matrix):
    lsi_vectors = [lsi_model[doc] for doc in doc_term_matrix]
    return lsi_vectors



