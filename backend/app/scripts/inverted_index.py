import pandas as pd
from scripts.dataCleaning import clean_dataset, remove_punctuation_and_numbers
import math
from collections import defaultdict
import os
from sqlalchemy import create_engine, inspect
from scripts.database import engine, table_exists


def create_inverted_index(df) -> dict:
    '''Creates an inverted index for the cleaned data and saves it to the database'''
  
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

            # Initialize the tfidf[index] if not present
            if index not in tfidf:
                tfidf[index] = {}

            # Add the tf-idf value for the word
            if word not in tfidf[index]:
                tfidf[index][word] = tf * idf
            else:
                tfidf[index][word] += tf * idf

    
    # Normalize the TF-IDF values so they sum to 1 for each document
    for index, terms in tfidf.items():
        total_tfidf = sum(terms.values())  # Sum of all TF-IDF values in the document
        if total_tfidf > 0:  # Avoid division by zero
            for word in terms:
                terms[word] /= (total_tfidf * 1.0)

    save_tf_idf_to_sql(tfidf, engine)
    return tfidf




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
    # Query the database directly and load the necessary columns
    query = """
    SELECT word, document_id, term_frequency
    FROM inverted_index
    """
    # Load data from SQL into a DataFrame
    df = pd.read_sql(query, con=engine)
    
    # Create the inverted index using pandas groupby (to minimize loops)
    inverted_index = df.groupby('word').apply(
        lambda x: dict(zip(x['document_id'], x['term_frequency']))
    ).to_dict()

    
    return inverted_index


def load_tf_idf_from_sql(engine):
    # Query the database directly and load the necessary columns
    query = """
    SELECT word, document_id, tf_idf
    FROM tf_idf
    """
    # Load data from SQL into a DataFrame (you can optionally add chunking here for very large datasets)
    df = pd.read_sql(query, con=engine)
    
    # Create the tf-idf dictionary using pandas groupby
    tf_idf_dict = df.groupby('document_id').apply(
        lambda x: dict(zip(x['word'], x['tf_idf']))
    ).to_dict()

    
    return tf_idf_dict