import pandas as pd
import re
from stopwords import STOPWORDS
import spacy
from greek_stemmer import stemmer

# Load the spaCy model
try:
    nlp = spacy.load("el_core_news_sm")
except Exception as e:
    print("Please run this: python -m spacy download el_core_news_sm")
    exit(1)

# Read the CSV file
df = pd.read_csv('data_sample.csv')

# Transform to lowercase every speech
def to_lowercase(text):
    return text.lower()

# Remove punctuation and numerical values
def remove_punctuation_and_numbers(word: str) -> str:
    # remove unwanted characters such as numbers, punctuation, etc.
    cleaned_word = re.sub(r'[^α-ωΑ-Ω]', '', word)
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
    
    dataframe.drop(columns=['government', 'member_region', 'roles','parliamentary_sitting','parliamentary_session'], inplace=True)
    dataframe.dropna(subset=['member_name',], inplace=True)

    dataframe['speech'] = dataframe['speech'].apply(to_lowercase)

    # Remove punctuation and numerical values
    dataframe['speech'] = dataframe['speech'].apply(lambda x: ' '.join([remove_punctuation_and_numbers(word) for word in x.split()]))
    dataframe['speech'] = dataframe['speech'].apply(lambda x: ' '.join([stem_words(word) for word in x.split()]))

    

    return dataframe




# Clean the data and display the cleaned DataFrame
cleaned_data = clean_dataset(df)
cleaned_data.to_csv('cleaned_data.csv', index=False)

