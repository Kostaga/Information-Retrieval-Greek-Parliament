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


# Load the cleaned data
df = create_clean_data()

# Group speeches by member and combine them into a single text entry per member
df_by_member= df.groupby('member_name')['clean_speech']



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


