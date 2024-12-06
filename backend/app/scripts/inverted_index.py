import pandas as pd
import os
from dataCleaning import clean_dataset, to_lowercase, remove_punctuation_and_numbers, stem_words
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import math
from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Determine the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'cleaned_data.csv')

if not os.path.exists(csv_path):
    print("cleaned_data.csv not found. Creating the file...")
    df = pd.read_csv("data_sample.csv")
    clean_dataset(df)
    print("File created!")
    df = pd.read_csv(csv_path)
else:
    df = pd.read_csv(csv_path)



def create_inverted_index() -> dict:
    '''Creates an inverted index for the cleaned data and saves it to a pickle file'''
  
    print("Creating the inverted index...")
    inverted_index = {}

    for index, row in df.iterrows():
        words = row['clean_speech'].split()
        
        for word in words:
            if word not in inverted_index:
                # maps words to a list of indexes containing the word and their term frequency.
                inverted_index[word] = {index: 1}
            else:
                if index in inverted_index[word]:
                    inverted_index[word][index] += 1
                else:
                    inverted_index[word][index] = 1


    
    print("Inverted index created!")

    with open('inverted_index.pkl', 'wb') as f:
        pickle.dump(inverted_index, f)
    
    return inverted_index



def calculate_tf_idf(inverted_index: dict, total_documents: int) -> dict:
    '''Calculates the term frequency-inverse document frequency for the cleaned data'''
    tfidf = {}
   
    for word, indexes in inverted_index.items():
        # calculate the idf
        idf = math.log(total_documents / (1 + len(indexes)))

        for index, term_count in indexes.items():
            # calculate the tf
            tf = 1 + math.log(term_count)
            if index not in tfidf:
                tfidf[index] = {word: tf * idf}
            else:
                tfidf[index][word] = tf * idf

    with open('tf_idf.pkl', 'wb') as f:
        pickle.dump(tfidf, f)


    return tfidf


def find_keyword(matching_docs, value: str, inverted_index: dict) -> set:
    # Preprocess and find keyword matches
    processed_keywords = [
        stem_words(remove_punctuation_and_numbers(word))
        for word in value
    ]
    print(f"Processed keywords: {processed_keywords}")
    # Find the indexes of the keywords in the inverted index
    keyword_indexes = [
        set(inverted_index[word].keys()) for word in processed_keywords if word in inverted_index
    ]
    print(keyword_indexes)
    # Intersect all keyword matches
    if keyword_indexes:
        matching_docs &= set.intersection(*keyword_indexes)
    
    return matching_docs


def create_table(df: pd.DataFrame):
    # Create inverted index and TF-IDF values if they do not exist
    if not os.path.exists("inverted_index.pkl" or "tf_idf.pkl"):
        print("Creating the inverted_index and tf_idf tables...")
        inverted_index = create_inverted_index()
        tf_idf = calculate_tf_idf(inverted_index, len(df['clean_speech']))
            
    else:
        # Otherwise, load the existing files
        with open('inverted_index.pkl', 'rb') as f:
            inverted_index = pickle.load(f)
        with open('tf_idf.pkl', 'rb') as f:
            tf_idf = pickle.load(f)

    return inverted_index, tf_idf

def search(
    df: pd.DataFrame,
    name: str = None,
    date: str = None,
    political_party: str = None,
    keywords: str = None
) -> list:
    """
    Searches the cleaned data for the query fields provided by the user.
    
    Args:
        df (pd.DataFrame): DataFrame containing the cleaned speeches.
        name (str): Name to search for.
        date (str): Date to search for.
        political_party (str): Political party to search for.
        keywords (str): String of comma-separated keywords to search for.
        
    Returns:
        list: A ranked list of document IDs and their TF-IDF scores.
    """
    
    # Create inverted index and TF-IDF values if they do not exist
    _ , tf_idf = create_table(df)

    # Combine fields into a dictionary for dynamic processing
    query_fields = {
        "member_name": name.lower() if name else None,
        "sitting_date": date if date else None,
        "political_party": political_party.lower() if political_party else None,
        "keywords": [k.strip() for k in keywords.split(",")] if keywords else None
    }

    
    

    # Initialize the result set with all possible document IDs
    all_docs = set(tf_idf.keys())
    matching_docs = all_docs  # Start with the broadest match
    
    # Preprocess and find keyword matches
    processed_keywords = [
        stem_words(remove_punctuation_and_numbers(word))
        for word in query_fields["keywords"]
    ]

    # Process each field
    for field, value in query_fields.items():
        if not value:
            continue

        if field == "keywords":
            # For keyword fields, calculate the cosine similarity
            similar_docs = find_cosine_similarity(tf_idf, matching_docs, processed_keywords)
            matching_docs = set(doc_id for doc_id, _ in similar_docs)
        else:
            # For single-value fields like name, date, and political_party
            field_indexes = df[df[field] == value].index.tolist()
            matching_docs &= set(field_indexes)
        
        print(f"Matching documents for {field}: {len(matching_docs)}")

    print(f"Final matching documents: {len(matching_docs)}")
    
    # Find the cosine similarity between the query and the documents and get top-5 results
    # top_docs = find_cosine_similarity(tf_idf, matching_docs, query_fields["keywords"])

    # Sort the results by similarity score and return the top-5 documents
    return matching_docs
    

def find_cosine_similarity(tf_idf: dict, matching_docs: set, keywords: list) -> list:
    '''Finds the cosine similarity between the query keywords and the documents'''
  
    # Create a vector for the query keywords
    query_vector = defaultdict(float)
    for keyword in keywords:
        for doc_id in matching_docs:
            if keyword in tf_idf[doc_id]:
                query_vector[keyword] += tf_idf[doc_id][keyword]
    
    # Normalize the query vector
    query_vector = np.array(list(query_vector.values()))
    query_vector = query_vector / np.linalg.norm(query_vector)

    print(f"Query vector: {query_vector}")
    
    # Calculate cosine similarity for each document
    similarities = []
    for doc_id in matching_docs:
        doc_vector = np.array([tf_idf[doc_id].get(keyword, 0) for keyword in keywords])
        if np.linalg.norm(doc_vector) == 0:
            continue
        doc_vector = doc_vector / np.linalg.norm(doc_vector)
        similarity = cosine_similarity([query_vector], [doc_vector])[0][0]
        similarities.append((doc_id, similarity))
    
    # Sort documents by similarity score in descending order
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    return similarities



    


# inverted_index = create_inverted_index()
# print(inverted_index)
# tf_idf = calculate_tf_idf(inverted_index, len(df['clean_speech']))


print(search(df,"σκρεκας θεοδωρου κωνσταντινος", "", "", "αγία,σοφία"))
print("-----------------")
# def calculate_tf_idf2():
#     '''Calculates the term frequency-inverse document frequency for the cleaned data'''
#     # create object
#     tfidf = TfidfVectorizer()
    
#     # get tf-df values
#     tfidf.fit_transform(df['clean_speech'])
#     # get idf values
#     print('\nidf values:')
#     for ele1, ele2 in zip(tfidf.get_feature_names_out(), tfidf.idf_):
#         print(ele1, ':', ele2)
# create_inverted_index()
# calculate_tf_idf2()