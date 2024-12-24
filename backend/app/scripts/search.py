import pandas as pd
import os
import numpy as np
from scripts.inverted_index import calculate_tf_idf, create_inverted_index, ensure_table
from collections import defaultdict
from scripts.dataCleaning import clean_dataset, remove_punctuation_and_numbers, stem_words, create_clean_data
from sklearn.metrics.pairwise import cosine_similarity






def search(
    name: str = None,
    date: str = None,
    political_party: str = None,
    keywords: str = None,
    limit: int = 100
) -> set:
    """
    Searches the cleaned data for the query fields provided by the user. 
    
    Args:
        df (pd.DataFrame): DataFrame containing the cleaned speeches.
        name (str): Name to search for.
        date (str): Date to search for.
        political_party (str): Political party to search for.
        keywords (str): String of comma-separated keywords to search for.
        limit (int): Maximum number of results to return.
        
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
        query_fields["keywords"] = stem_words([remove_punctuation_and_numbers(word) for word in query_fields["keywords"]])


    # Process each field
    for field, value in query_fields.items():
        if not value:
            continue

        if field == "keywords":
            # For keyword fields, calculate the cosine similarity
            similar_docs = find_cosine_similarity(tf_idf, matching_docs, value,limit=limit)
            matching_docs = set(doc_id for doc_id, _ in similar_docs)
        else:
            # For partial matching of text fields
            if field == "sitting_date":
                # Exact match for dates
                field_matches = df[df[field] == value].index.tolist()
            else:
                # Partial match for strings (case insensitive)
                field_matches = df[df[field].str.contains(value, na=False, case=False)].index.tolist()

            matching_docs &= set(field_matches)
        
        print(f"Matching documents for {field}: {len(matching_docs)}")

    print(f"Final matching documents: {len(matching_docs)}")
    
    # Return the rows of the matching documents
    rows = df.loc[list(matching_docs)[:limit]]
    return rows
    
    

def find_cosine_similarity(tf_idf: dict, matching_docs: set, keywords: list, limit: int) -> list:
    '''Finds the cosine similarity between the query keywords and the documents'''
  
    # Create a vector for the query keywords
    query_vector = defaultdict(float)
    for keyword in keywords:
        for doc_id in matching_docs:
            if keyword in tf_idf[doc_id]:
                query_vector[keyword] += tf_idf[doc_id][keyword]
    
    # Normalize the query vector
    query_vector = np.array(list(query_vector.values()))
    if np.linalg.norm(query_vector) == 0:
        return []
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
    similarities = sorted(similarities, key=lambda x: x[1], reverse=True)[:limit]
    
    return similarities


