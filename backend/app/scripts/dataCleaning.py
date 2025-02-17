import pandas as pd
import regex as re
from scripts.stopwords import STOPWORDS
import spacy
from greek_stemmer import stemmer
import os
import unicodedata
import time
import multiprocessing as mp

FILE = "app/parliament.csv"
OUTPUT_FILE = "cleaned_data.csv"
ROWS = 100000 # Adjust this value as needed for the number of rows to process

# Load the spaCy model
try:
    nlp = spacy.load("el_core_news_sm", disable=["parser", "ner", "tok2vec", "tagger", "attribute_ruler", "lemmatizer"])

except Exception as e:
    print("Please run this: python -m spacy download el_core_news_sm")
    exit(1)



# Remove punctuation and numerical values
def remove_punctuation_and_numbers(word: str) -> str:
    word = word.lower()
    cleaned_word = re.sub(r'[^\wάέήίόύώα-ω]', '', word)
    if (cleaned_word == ' ' or len(cleaned_word) == 1 or cleaned_word in STOPWORDS):
        return ""
    
    return cleaned_word


def stem_words(words: list) -> list:
    doc = nlp(' '.join(words))  # Process the whole sentence at once
    return [
        stemmer.stem_word(token.text, "NNM").lower() for token in doc if token.is_alpha
    ]


# Process the dataset
def clean_dataset(df):
    df = df.dropna(subset=['member_name'],ignore_index=True)
    df = df.dropna(subset=['speech'],ignore_index=True)
    speeches = df['speech'].tolist()
    df['clean_speech'] = parallel_process(speeches)
    df['clean_speech'] = df['clean_speech'].replace('', pd.NA)
    df = df.dropna(subset=['clean_speech'],ignore_index=True)
    return df


def process_batch(batch):
    # Process a batch of records
    return clean_speech_bulk(batch)


def parallel_process(data, num_workers=4):
    pool = mp.Pool(num_workers)
    chunk_size = len(data) // num_workers
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    results = pool.map(process_batch, chunks)
    return [item for sublist in results for item in sublist]

# Clean speeches in bulk
def clean_speech_bulk(speeches: list) -> list:
    regex = re.compile(r'[^\p{Greek}\w]')
    def process_speech(speech: str) -> str:
        # Remove punctuation and numbers, and split into words
        words = regex.split(speech.lower())
        # Filter and clean words in one step
        cleaned_words = [
            word for word in words
            if word and len(word) > 1 and word not in STOPWORDS
        ]
        # Stem words in bulk
        stemmed_words = stem_words(cleaned_words)
        return ' '.join(stemmed_words)

    start = time.time()
    results = [process_speech(speech) for speech in speeches]
    print(f"Time taken: {time.time() - start:.2f} seconds")
    return results



def create_clean_data():
    '''Creates the cleaned data CSV file if it does not exist'''
    if not os.path.exists(OUTPUT_FILE):
        print(f"{OUTPUT_FILE} not found. Creating the file...")
        df = pd.read_csv(FILE, nrows=ROWS, usecols=['member_name', 'speech', 'political_party','sitting_date'])
        cleaned_dataset = clean_dataset(df)
        print("File created!")
        cleaned_dataset.to_csv(OUTPUT_FILE, index=False)
        return cleaned_dataset
    else:
        print(f"{OUTPUT_FILE} already exists. Loading file...")
        return pd.read_csv(OUTPUT_FILE)
