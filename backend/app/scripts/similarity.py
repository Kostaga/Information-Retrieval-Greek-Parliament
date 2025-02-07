import pandas as pd  # to load the dataframe
import numpy as np
import spacy
from sklearn.metrics.pairwise import cosine_similarity
# Load spaCy's English language model
nlp = spacy.load("en_core_web_sm")
from scripts.dataCleaning import create_clean_data
from gensim import corpora
from gensim.models import LsiModel
from gensim.models.coherencemodel import CoherenceModel
import matplotlib.pyplot as plt



#Standardize the features
#Create an object of StandardScaler which is present in sklearn.preprocessing

df = create_clean_data()
# df_by_member= df.groupby('member_name')['clean_speech'].agg(' '.join).reset_index()
df_by_member= df.groupby('member_name')['clean_speech'].apply(list).reset_index()
# for token in df_by_member['clean_speech']:
print(df_by_member)
# Tokenize speeches using spaCy
def tokenize_with_spacy(speeches):
    return [[token.text for token in nlp(speech)] for speech in speeches]

# Apply tokenization
df_by_member['doc_clean'] = df_by_member['clean_speech'].apply(tokenize_with_spacy)

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

# Create Gensim LSA Model
def create_gensim_lsa_model(doc_clean, number_of_topics, words):
    dictionary, doc_term_matrix = prepare_corpus(doc_clean)
    lsamodel = LsiModel(doc_term_matrix, num_topics=number_of_topics, id2word=dictionary)
    
    # Extract topic distribution for the member
    topic_distribution = [lsamodel[doc] for doc in doc_term_matrix]

    # Aggregate topic vectors by averaging across all speeches
    avg_topic_vector = [np.mean([val for (_, val) in doc]) for doc in topic_distribution if doc]


    
    return avg_topic_vector

# Function to compute top 3 most similar members
def get_top_similar_members():
    topic_vectors = {}
    for _, row in df_by_member.iterrows():
        doc_clean = row['doc_clean']
        topic_vectors[row['member_name']] = create_gensim_lsa_model(doc_clean, 7, 10)

    members = list(topic_vectors.keys())
    vectors = np.array([topic_vectors[m] for m in members])
    vectors = np.array(vectors, dtype=float)  # Convert to NumPy array of floats
    # Compute cosine similarity
    print(f"Shape of vectors: {np.shape(vectors)}")

    similarity_matrix = cosine_similarity(vectors)

    # Get top 3 most similar pairs
    similarity_scores = []
    for i in range(len(members)):
        for j in range(i + 1, len(members)):  # Avoid duplicate pairs
            similarity_scores.append((members[i], members[j], similarity_matrix[i, j]))

    # Sort by similarity score
    top_3_similar = sorted(similarity_scores, key=lambda x: x[2], reverse=True)[:3]

    return [
        {"member_1": pair[0], "member_2": pair[1], "similarity": round(pair[2], 4)}
        for pair in top_3_similar
    ]