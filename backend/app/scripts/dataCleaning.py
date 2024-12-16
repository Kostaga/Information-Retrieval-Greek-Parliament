import pandas as pd
import re
from stopwords import STOPWORDS
import spacy
from greek_stemmer import stemmer
import os
import unicodedata
# Load the spaCy model
try:
    nlp = spacy.load("el_core_news_sm")
except Exception as e:
    print("Please run this: python -m spacy download el_core_news_sm")
    exit(1)

# Determine the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'data_sample.csv')



# Transform to lowercase every speech
def to_lowercase(text):
    return text.lower()

# Remove punctuation and numerical values
def remove_punctuation_and_numbers(word: str) -> str:
    # remove unwanted characters such as numbers, punctuation, etc.
    # include the greek alphabet with and without accents
    word = word.lower()


    word = ''.join(
        c for c in unicodedata.normalize('NFD', word) 
        if unicodedata.category(c) != 'Mn'
    )

    cleaned_word = re.sub(r'[^α-ω]', '', word)
    if (cleaned_word == " " or len(cleaned_word) == 1 or cleaned_word in STOPWORDS):
        return ""

    return cleaned_word
        


def stem_words(word: str) -> str:
    """Stem the word based on its POS tag and return the stemmed word"""
    doc = nlp(word)
    tag = doc[0].pos_
    if tag == "NOUN":
        return stemmer.stem_word(word, "NNM").lower()

    elif tag == "VERB":
        return stemmer.stem_word(word, "VB").lower()

    elif tag == "PROPN":
        return stemmer.stem_word(word, "PRP").lower()

    elif tag == "ADJ" or tag == "ADV":
        return stemmer.stem_word(word, "JJM").lower()

    else:
        return stemmer.stem_word(word, "NNM").lower()

# Clean the speeches
def clean_dataset(dataframe):
    """Clean the speeches and return the updated DataFrame"""
    
    dataframe.drop(columns=['government', 'parliamentary_period', 'member_region', 'roles','parliamentary_sitting','parliamentary_session'], inplace=True)
    dataframe.dropna(subset=['member_name', ], inplace=True)
    dataframe['clean_speech'] = dataframe['speech'].apply(to_lowercase)

    # Remove punctuation and numerical values
    dataframe['clean_speech'] = dataframe['clean_speech'].apply(lambda x: ' '.join([remove_punctuation_and_numbers(word) for word in x.split()]))
    dataframe['clean_speech'] = dataframe['clean_speech'].apply(lambda x: ' '.join([stem_words(word) for word in x.split()]))
    

    # Remove clean speech null values
    dataframe['clean_speech'].replace('', pd.NA, inplace=True)
    dataframe.dropna(subset=['clean_speech'], inplace=True)

    # Clean the data and display the cleaned DataFrame
    df.to_csv('cleaned_data.csv', index=False)
    

    return dataframe



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

# Read the CSV file
# df = pd.read_csv(csv_path)
# clean_dataset(df)



