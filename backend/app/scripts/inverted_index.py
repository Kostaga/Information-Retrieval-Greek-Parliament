import pandas as pd
from scripts.dataCleaning import clean_dataset, to_lowercase, remove_punctuation_and_numbers, stem_words
import pickle
import math
from collections import defaultdict
import os
from sqlalchemy import create_engine, inspect
from scripts.database import engine

def table_exists(engine, table_name):
    inspector = inspect(engine)
    return table_name in inspector.get_table_names()



def create_inverted_index(df) -> dict:
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


    save_inverted_index_to_sql(inverted_index, engine)
    
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


    save_tf_idf_to_sql(tfidf, engine)
    

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


def ensure_table(df: pd.DataFrame, table_name: str) -> dict:
    """Ensures the table exists in the database and returns its data."""
    if not table_exists(engine, table_name):
        print(f"Table '{table_name}' does not exist. Creating...")
        if table_name == 'inverted_index':
            data = create_inverted_index(df)  # Creates and saves the inverted index
        elif table_name == 'tf_idf':
            inverted_index = ensure_table(df, 'inverted_index')  # Ensures the inverted index exists
            data = calculate_tf_idf(inverted_index, len(df))  # Calculates and saves TF-IDF
        else:
            raise ValueError("Invalid table name. Must be 'inverted_index' or 'tf_idf'")
    else:
        print(f"Loading table '{table_name}' from database...")
        if table_name == 'inverted_index':
            data = load_inverted_index_from_sql(engine)
        elif table_name == 'tf_idf':
            data = load_tf_idf_from_sql(engine)
        else:
            raise ValueError("Invalid table name. Must be 'inverted_index' or 'tf_idf'")
            
    return data




def save_inverted_index_to_sql(inverted_index, engine):
    # Convert the inverted index dictionary to a DataFrame
    data = []
    for word, doc_dict in inverted_index.items():
        for doc_id, term_freq in doc_dict.items():
            data.append({'word': word, 'document_id': doc_id, 'term_frequency': term_freq})
    df = pd.DataFrame(data)
    # Save the DataFrame to SQL
    df.to_sql('inverted_index', con=engine, if_exists='replace', index=False)



def save_tf_idf_to_sql(tf_idf, engine):
    # Convert the tf_idf dictionary to a DataFrame
    data = []
    for doc_id, word_dict in tf_idf.items():
        for word, tf_idf_value in word_dict.items():
            data.append({'document_id': doc_id, 'word': word, 'tf_idf': tf_idf_value})
    df = pd.DataFrame(data)
    # Save the DataFrame to SQL
    df.to_sql('tf_idf', con=engine, if_exists='replace', index=False)


def load_inverted_index_from_sql(engine):
    # Load the DataFrame from SQL
    df = pd.read_sql('inverted_index', con=engine)
    # Convert the DataFrame back to a dictionary
    inverted_index = {}
    for _, row in df.iterrows():
        word = row['word']
        doc_id = row['document_id']
        term_freq = row['term_frequency']
        if word not in inverted_index:
            inverted_index[word] = {}
        inverted_index[word][doc_id] = term_freq
    return inverted_index



def load_tf_idf_from_sql(engine):
    # Load the DataFrame from SQL
    df = pd.read_sql('tf_idf', con=engine)
    # Convert the DataFrame back to a dictionary
    tf_idf = {}
    for _, row in df.iterrows():
        doc_id = row['document_id']
        word = row['word']
        tf_idf_value = row['tf_idf']
        if doc_id not in tf_idf:
            tf_idf[doc_id] = {}
        tf_idf[doc_id][word] = tf_idf_value
    return tf_idf