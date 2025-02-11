import pandas as pd  # to load the dataframe
import numpy as np
import spacy
import json
from sklearn.metrics.pairwise import cosine_similarity
# Load spaCy's English language model
nlp = spacy.load("el_core_news_sm", disable=["parser", "ner", "tok2vec", "tagger", "attribute_ruler", "lemmatizer"])
from scripts.dataCleaning import create_clean_data
from gensim import corpora
from gensim.models import LsiModel
from gensim.models.coherencemodel import CoherenceModel
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from itertools import combinations
from sklearn.feature_extraction.text import TfidfVectorizer




#Standardize the features
#Create an object of StandardScaler which is present in sklearn.preprocessing

df = create_clean_data()

# df_by_member= df.groupby('member_name')['clean_speech'].apply(list).reset_index()
df_by_member= df.groupby('member_name')['clean_speech']
# for token in df_by_member['clean_speech']:

# Tokenize speeches using spaCy
# def tokenize_with_spacy(speeches):
#     tokens_list = [[token.text for token in nlp(speech)] for speech in speeches]
#     # print(tokens_list)
#     return tokens_list
# # Apply tokenization
# df_by_member['doc_clean'] = df_by_member['clean_speech'].apply(tokenize_with_spacy)

# Prepare corpus function
def prepare_corpus(doc_clean):
    """
    Input  : clean document
    Purpose: Create term dictionary and Document Term Matrix
    Output : term dictionary and Document Term Matrix
    """
    dictionary = corpora.Dictionary(doc_clean)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
    return dictionary, doc_term_matrix

# # Create Gensim LSA Model
# def create_gensim_lsa_model(doc_clean, number_of_topics, words):
#     dictionary, doc_term_matrix = prepare_corpus(doc_clean)
#     lsamodel = LsiModel(doc_term_matrix, num_topics=number_of_topics, id2word=dictionary)
    
#     # Extract topic distribution for the member
#     topic_distribution = [lsamodel[doc] for doc in doc_term_matrix]

#     # Aggregate topic vectors by averaging across all speeches
#     avg_topic_vector = [np.mean([val for (_, val) in doc]) for doc in topic_distribution if doc]

#     # Ensure consistent length of avg_topic_vector
#     if len(avg_topic_vector) < number_of_topics:
#         avg_topic_vector.extend([0] * (number_of_topics - len(avg_topic_vector)))
#     elif len(avg_topic_vector) > number_of_topics:
#         avg_topic_vector = avg_topic_vector[:number_of_topics]
    
#     return avg_topic_vector
# Convert text data to TF-IDF vectors


def get_top_similar_members():
    # Group speeches by member and combine them into a single text entry per member
    df_by_member = df.groupby('member_name')['clean_speech'].apply(lambda x: ' '.join(x))
    
    # Reset index to allow index-based access
    df_by_member = df_by_member.reset_index()
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df_by_member['clean_speech'].tolist())

    # Compute cosine similarity
    similarity_matrix = cosine_similarity(tfidf_matrix)

    # Find the top N most similar pairs
    similarity_scores = []
    for i, j in combinations(range(len(df_by_member)), 2):
        similarity_scores.append({
            "member_1": df_by_member.iloc[i, 0],  # Access member_name
            "member_2": df_by_member.iloc[j, 0],  # Access member_name
            "score": round(similarity_matrix[i, j], 4)  # Keep 4 decimal places
        })
    
    # Sort by similarity score in descending order
    similarity_scores.sort(key=lambda x: x["score"], reverse=True)

    # Get top 3 pairs
    top_similar_pairs = similarity_scores[:3]

    # Print results
    for pair in top_similar_pairs:
        print(f"Similar pair: {pair['member_1']} & {pair['member_2']} with similarity score: {pair['score']:.4f}")

    return top_similar_pairs  # Convert to JSON format


# Function to compute top 3 most similar members
# def get_top_similar_members():
#     topic_vectors = {}
    
#     with ThreadPoolExecutor() as executor:
#         futures = {executor.submit(create_gensim_lsa_model, row['doc_clean'], 20, 10): row['member_name'] for _, row in df_by_member.iterrows()}
#         for future in futures:
#             member_name = futures[future]
#             topic_vectors[member_name] = future.result()
#     print(topic_vectors)
#     members = list(topic_vectors.keys())
#     vectors = np.array([topic_vectors[m] for m in members])
#     vectors = np.array(vectors, dtype=float)  # Convert to NumPy array of floats
#     # Compute cosine similarity
#     print(f"Shape of vectors: {np.shape(vectors)}")

#     similarity_matrix = cosine_similarity(vectors)

#     # Get top 3 most similar pairs
#     similarity_scores = []
#     for i in range(len(members)):
#         for j in range(i + 1, len(members)):  # Avoid duplicate pairs
#             similarity_scores.append((members[i], members[j], similarity_matrix[i, j]))

#     # Sort by similarity score
#     top_3_similar = sorted(similarity_scores, key=lambda x: x[2], reverse=True)[:3]

#     return [
#         {"member_1": pair[0], "member_2": pair[1], "similarity": round(pair[2], 4)}
#         for pair in top_3_similar
#     ]