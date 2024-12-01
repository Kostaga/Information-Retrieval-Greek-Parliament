import pandas as pd
import os
from dataCleaning import clean_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import math


if not os.path.exists("cleaned_data.csv"):
    print("cleaned_data.csv not found. Creating the file...")
    df = pd.read_csv("data_sample.csv")
    clean_dataset(df)
    print("File created!")
else:
    df = pd.read_csv("cleaned_data.csv")



def create_inverted_index() -> dict:
    '''Creates an inverted index for the cleaned data and saves it to a pickle file'''
    # Read the cleaned data
   
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

    return tfidf

inverted_index = create_inverted_index()
tf_idf = calculate_tf_idf(inverted_index, len(df['clean_speech']))
print(tf_idf)
print("-----------------")
def calculate_tf_idf2():
    '''Calculates the term frequency-inverse document frequency for the cleaned data'''
    # create object
    tfidf = TfidfVectorizer()
    
    # get tf-df values
    tfidf.fit_transform(df['clean_speech'])
    # get idf values
    print('\nidf values:')
    for ele1, ele2 in zip(tfidf.get_feature_names_out(), tfidf.idf_):
        print(ele1, ':', ele2)
# create_inverted_index()
# calculate_tf_idf2()