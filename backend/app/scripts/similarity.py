import pandas as pd  # to load the dataframe
import gensim # to create the LSA model
import spacy

# Load spaCy's English language model
nlp = spacy.load("en_core_web_sm")
from scripts.dataCleaning import create_clean_data
from gensim import corpora
from gensim.models import LsiModel
from gensim.models.coherencemodel import CoherenceModel
import matplotlib.pyplot as plt

#Standardize the features
#Create an object of StandardScaler which is present in sklearn.preprocessing

df = create_clean_data()
# df_by_member= df.groupby('member_name')['clean_speech'].agg(' '.join).reset_index()
df_by_member= df.groupby('member_name')['clean_speech'].apply(list).reset_index()
# for token in df_by_member['clean_speech']:
print(df_by_member)
# Tokenize speeches using spaCy
def tokenize_with_spacy(speeches):
    return [[token.text for token in nlp(speech)] for speech in speeches]

# Apply tokenization
df_by_member['doc_clean'] = df_by_member['clean_speech'].apply(tokenize_with_spacy)

# Prepare corpus function
def prepare_corpus(doc_clean):
    """
    Input  : clean document
    Purpose: Create term dictionary and Document Term Matrix
    Output : term dictionary and Document Term Matrix
    """
    dictionary = corpora.Dictionary(doc_clean)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
    return dictionary, doc_term_matrix

# Create Gensim LSA Model
def create_gensim_lsa_model(doc_clean, number_of_topics, words):
    """
    Input  : clean document, number of topics, number of words per topic
    Purpose: Create LSA model using Gensim
    Output : LSA model
    """
    dictionary, doc_term_matrix = prepare_corpus(doc_clean)
    lsamodel = LsiModel(doc_term_matrix, num_topics=number_of_topics, id2word=dictionary)
    topics = lsamodel.print_topics(num_topics=number_of_topics, num_words=words)
    for topic in topics:
        print(topic)
    return lsamodel

# Generate LSA model for each speaker
for _, row in df_by_member.iterrows():
    print(f"Topics for {row['member_name']}:\n")
    doc_clean = [doc for doc in row['doc_clean']]  # Tokenized speeches for the speaker
    create_gensim_lsa_model(doc_clean, number_of_topics=7, words=10)
    print("\n" + "="*50 + "\n")

