import pandas as pd
import os
import numpy as np
from scripts.inverted_index import find_keyword, calculate_tf_idf, create_inverted_index, ensure_table
from collections import defaultdict
from scripts.dataCleaning import clean_dataset, to_lowercase, remove_punctuation_and_numbers, stem_words
from sklearn.metrics.pairwise import cosine_similarity


def create_clean_data():
    '''Creates the cleaned data CSV file if it does not exist'''
    # Determine the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'cleaned_data.csv')

    if not os.path.exists(csv_path):
        print("cleaned_data.csv not found. Creating the file...")
        df = pd.read_csv("data_sample.csv")
        clean_dataset(df)
        print("File created!")
        return pd.read_csv(csv_path)
    else:
        return pd.read_csv(csv_path)



def search(
    name: str = None,
    date: str = None,
    political_party: str = None,
    keywords: str = None
) -> set:
    """
    Searches the cleaned data for the query fields provided by the user.
    
    Args:
        df (pd.DataFrame): DataFrame containing the cleaned speeches.
        name (str): Name to search for.
        date (str): Date to search for.
        political_party (str): Political party to search for.
        keywords (str): String of comma-separated keywords to search for.
        
    Returns:
        set: A ranked set of document IDs and their TF-IDF scores.
    """
    df = create_clean_data()
    # Create inverted index and TF-IDF values if they do not exist
    tf_idf = ensure_table(df, "tf_idf")

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
    

    # Remove punctuation from name field for every word in splitted name and then join them
    if query_fields["member_name"]:
        query_fields["member_name"] = ' '.join([remove_punctuation_and_numbers(word) for word in query_fields["member_name"].split()])
    
    if query_fields["political_party"]:
        query_fields["political_party"] = ' '.join([remove_punctuation_and_numbers(word) for word in query_fields["political_party"].split()])
    
    # Preprocess and find keyword matches
    if query_fields["keywords"]:
        query_fields["keywords"] = [stem_words(remove_punctuation_and_numbers(word)) for word in query_fields["keywords"]]


    # Process each field
    for field, value in query_fields.items():
        if not value:
            continue

        if field == "keywords":
            # For keyword fields, calculate the cosine similarity
            similar_docs = find_cosine_similarity(tf_idf, matching_docs, value)
            matching_docs = set(doc_id for doc_id, _ in similar_docs)
        else:
            # For single-value fields like name, date, and political_party
            field_indexes = df[df[field] == value].index.tolist()
            matching_docs &= set(field_indexes)
        
        print(f"Matching documents for {field}: {len(matching_docs)}")

    print(f"Final matching documents: {len(matching_docs)}")
    
    # Return the rows of the matching documents without the clean speech column
    rows = df.loc[list(matching_docs)].drop(columns=["clean_speech"])
    return rows
    
    

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


