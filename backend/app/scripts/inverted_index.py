import pandas as pd
from scripts.dataCleaning import clean_dataset, to_lowercase, remove_punctuation_and_numbers, stem_words
import pickle
import math
from collections import defaultdict
import os


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
        inverted_index = create_inverted_index(df)
        tf_idf = calculate_tf_idf(inverted_index, len(df['clean_speech']))
            
    else:
        # Otherwise, load the existing files
        with open('inverted_index.pkl', 'rb') as f:
            inverted_index = pickle.load(f)
        with open('tf_idf.pkl', 'rb') as f:
            tf_idf = pickle.load(f)

    return inverted_index, tf_idf
