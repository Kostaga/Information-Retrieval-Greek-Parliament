import pandas as pd
import os
from dataCleaning import clean_dataset
import pickle


if not os.path.exists("cleaned_data.csv"):
    print("cleaned_data.csv not found. Creating the file...")
    df = pd.read_csv("data_sample.csv")
    clean_dataset(df)
    print("File created!")


def create_inverted_index():
    # Read the cleaned data
    df = pd.read_csv("cleaned_data.csv")
    print("Creating the inverted index...")
    inverted_index = {}

    for index, row in df.iterrows():
        words = row['clean_speech'].split()
        for word in words:
            if word not in inverted_index:
                # The inverse index catalogue maps words to a list of indexes containing the word and their term frequency.
                inverted_index[word] = {index: 1}
            else:
                if index in inverted_index[word]:
                    inverted_index[word][index] += 1
                else:
                    inverted_index[word][index] = 1


    
    print("Inverted index created!")
    print(inverted_index)

    with open('inverted_index.pkl', 'wb') as f:
        pickle.dump(inverted_index, f)


create_inverted_index()