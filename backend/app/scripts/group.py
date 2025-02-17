import pandas as pd
from scripts.dataCleaning import create_clean_data
from scripts.inverted_index import ensure_table
from scripts.database import engine, table_exists


# Group by member_name and the most important keyword in the speech
def group_by_member_name():
    df = create_clean_data()
    tf_idf = ensure_table(df, "tf_idf")
    
    if table_exists(engine, 'keyword_per_member'):
        return pd.read_sql('keyword_per_member', con=engine)

    # For every member_name get the word with the maximum TF-IDF value and the tf_idf value
    max_tf_idf = {}
    for doc_id, word_dict in tf_idf.items():
        max_word = max(word_dict, key=word_dict.get)
        max_tf_idf[doc_id] = (max_word,round(word_dict[max_word],2))
    

    
    # Get the rows present in the max_tf_idf dictionary
    df_max_tf_idf = pd.DataFrame(max_tf_idf.items(), columns=['document_id', 'max_tf_idf'])
    df_max_tf_idf[['Keyword', 'Tf_idf_value']] = pd.DataFrame(df_max_tf_idf['max_tf_idf'].tolist(), index=df_max_tf_idf.index)
    df_max_tf_idf.drop(columns=['max_tf_idf'], inplace=True)

    # Merge the two DataFrames on the document_id and keep only doc_id,member_name and keyword
    df_filtered = pd.merge(df, df_max_tf_idf, left_index=True, right_on='document_id')
    df_filtered = df_filtered[['member_name', 'Keyword', 'Tf_idf_value']]
    df_filtered = df_filtered.groupby('member_name').agg({'Keyword': 'first', 'Tf_idf_value': 'first'}).reset_index()

    
    # Save to sql table for further use
    df_filtered.to_sql('keyword_per_member', con=engine, if_exists='replace', index=False)
    

    return df_filtered
    


def group_by_speech() -> pd.DataFrame:
    df = create_clean_data()
    tf_idf = ensure_table(df, "tf_idf")

    if table_exists(engine, 'keyword_per_speech'):
        return pd.read_sql('keyword_per_speech', con=engine)

    # For every document, get the word with the maximum TF-IDF value and the tf_idf value
    max_tf_idf = {}
    for doc_id, word_dict in tf_idf.items():
        max_word = max(word_dict, key=word_dict.get)
        max_tf_idf[doc_id] = (max_word,round(word_dict[max_word],2))

    
    # Create a DataFrame with the maximum TF-IDF values
    df_max_tf_idf = pd.DataFrame(max_tf_idf.items(), columns=['document_id', 'max_tf_idf'])
    df_max_tf_idf[['Keyword', 'Tf_idf_value']] = pd.DataFrame(df_max_tf_idf['max_tf_idf'].tolist(), index=df_max_tf_idf.index)
    df_max_tf_idf.drop(columns=['max_tf_idf'], inplace=True)

    df_filtered = pd.merge(df, df_max_tf_idf, left_index=True, right_on='document_id')
    df_filtered = df_filtered[['speech', 'Keyword', 'Tf_idf_value']]

    # Save to sql table for further use
    df_filtered.to_sql('keyword_per_speech', con=engine, if_exists='replace', index=False)

    return df_filtered


def group_by_party() -> pd.DataFrame:
    df = create_clean_data()
    tf_idf = ensure_table(df, "tf_idf")

    if table_exists(engine, 'keyword_per_party'):
        return pd.read_sql('keyword_per_party', con=engine)

    # For every document, get the word with the maximum TF-IDF value and the tf_idf value
    max_tf_idf = {}
    for doc_id, word_dict in tf_idf.items():
        max_word = max(word_dict, key=word_dict.get)
        max_tf_idf[doc_id] = (max_word,round(word_dict[max_word],2))

    
    # Create a DataFrame with the maximum TF-IDF values
    df_max_tf_idf = pd.DataFrame(max_tf_idf.items(), columns=['document_id', 'max_tf_idf'])
    df_max_tf_idf[['Keyword', 'Tf_idf_value']] = pd.DataFrame(df_max_tf_idf['max_tf_idf'].tolist(), index=df_max_tf_idf.index)
    df_max_tf_idf.drop(columns=['max_tf_idf'], inplace=True)

    # Merge the two DataFrames on the document_id and keep only doc_id,party and keyword
    df_filtered = pd.merge(df, df_max_tf_idf, left_index=True, right_on='document_id')
    df_filtered = df_filtered[['political_party', 'Keyword', 'Tf_idf_value']]
    df_filtered = df_filtered.groupby('political_party').agg({'Keyword': 'first', 'Tf_idf_value': 'first'}).reset_index()

    # Save to sql table for further use
    df_filtered.to_sql('keyword_per_party', con=engine, if_exists='replace', index=False)

    return df_filtered



def group_by_date() -> pd.DataFrame:
    df = create_clean_data()
    tf_idf = ensure_table(df, "tf_idf")

    if table_exists(engine, 'keyword_per_date'):
        return pd.read_sql('keyword_per_date', con=engine)

    # For every document, get the word with the maximum TF-IDF value and the tf_idf value
    max_tf_idf = {}
    for doc_id, word_dict in tf_idf.items():
        max_word = max(word_dict, key=word_dict.get)
        max_tf_idf[doc_id] = (max_word,round(word_dict[max_word],2))

    
    # Create a DataFrame with the maximum TF-IDF values
    df_max_tf_idf = pd.DataFrame(max_tf_idf.items(), columns=['document_id', 'max_tf_idf'])
    df_max_tf_idf[['Keyword', 'Tf_idf_value']] = pd.DataFrame(df_max_tf_idf['max_tf_idf'].tolist(), index=df_max_tf_idf.index)
    df_max_tf_idf.drop(columns=['max_tf_idf'], inplace=True)

    # Merge the two DataFrames on the document_id and keep only doc_id,date and keyword
    df_filtered = pd.merge(df, df_max_tf_idf, left_index=True, right_on='document_id')
    df_filtered = df_filtered[['sitting_date', 'Keyword', 'Tf_idf_value']]
    df_filtered = df_filtered.groupby('sitting_date').agg({'Keyword': 'first', 'Tf_idf_value': 'first'}).reset_index()

    # Save to sql table for further use
    df_filtered.to_sql('keyword_per_date', con=engine, if_exists='replace', index=False)

    return df_filtered


