import os
import pickle
import numpy as np
import pandas as pd

data_location = "./Data/"

def load_small_full_file():
    '''This is the smallest df with all rows'''
    file_location = os.path.join(data_location, "corrected_data_small.csv")
    df = pd.read_csv(file_location)
    df.Year = df.Year.astype(str)
    year_list = ['1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010',
                 '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']
    df.loc[:, year_list] = df.loc[:, year_list].replace(0, np.nan)
    df['primary_key'] = pd.Series(list(zip(df.Title,df.Artist)))
    df['display_value'] = df.primary_key.apply(lambda x: '{} ({})'.format(x[0],x[1]))
    return df


def load_df_lyrics():
    file_location = os.path.join(data_location, "df_merged_have_lyrics.pkl")
    with open(file_location, "rb") as f:
        df = pickle.load(f)
    return df


def load_appearance_options():
    file_location = os.path.join(data_location, "all_words_lable_value.pkl")
    with open(file_location, "rb") as f:
        all_words_lable_value = pickle.load(f)
    return all_words_lable_value


def load_offensive_word_dict():
    ## load the offensive words dictionary
    file_location = os.path.join(data_location, "dict_offensive_words_with_genre.pkl")
    with open(file_location,'rb') as f:
        dict_offensive_words = pickle.load(f)

    file_location = os.path.join(data_location, "offensive_words_lable_value.pkl")
    with open(file_location,'rb') as f:
        offensive_word_options = pickle.load(f)

    return dict_offensive_words, offensive_word_options


# def load_wordcloud_data():
#     file_location = os.path.join(data_location, "dic_Artist_wordcloud_v5.pkl")
#     with open(file_location, 'rb') as f:
#         dic_Artist_wordcloud = pickle.load(f)
#
#     file_location = os.path.join(data_location, "all_artist_lable_value.pkl")
#     with open(file_location, 'rb') as f:
#         all_artist_lable_value = pickle.load(f)
#
#     file_location = os.path.join(data_location, "all_genre_lable_value.pkl")
#     with open(file_location, 'rb') as f:
#         all_genre_lable_value = pickle.load(f)
#
#     file_location = os.path.join(data_location, "all_year_lable_value.pkl")
#     with open(file_location, 'rb') as f:
#         all_year_lable_value = pickle.load(f)
#
#     file_location = os.path.join(data_location, "list_dictionary_keys.pkl")
#     with open(file_location, 'rb') as f:
#         list_dictionary_keys = pickle.load(f)
#
#     return (dic_Artist_wordcloud, all_artist_lable_value,
#             all_genre_lable_value, all_year_lable_value, list_dictionary_keys)