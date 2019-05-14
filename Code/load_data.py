import os
import json
import pickle
import numpy as np
import pandas as pd

data_location = "./Data/"

def load_df_audio_feats():
    file_location = os.path.join(data_location, "top_2000_with_audio_features.csv")
    df_audio_feats = pd.read_csv(file_location)
    df_audio_feats.drop("Unnamed: 0",axis=1,inplace=True)
    df_audio_feats.Year = df_audio_feats.Year.astype(str)
    df_audio_feats.replace(0,2001,inplace=True)
    return df_audio_feats

def load_df_audio_analysis_feats():
    file_location = os.path.join(data_location, "audio_analysis_plus_features.csv")
    df = pd.read_csv(file_location)
    year_list = ['1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010',
                 '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']
    for year in year_list:
        df.loc[df[year_list][year] == 0, year] = None
    return df

def load_full_file():
    file_location = os.path.join(data_location, "corrected_data.csv")
    df = pd.read_csv(file_location)
    df.Year = df.Year.astype(str)
    df.replace(0, 2001, inplace=True)
    return df


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
    # df.replace(0, 2001, inplace=True)
    return df


def load_smaller_full_file():
    '''This ones is smaller than full, but larger than small'''
    file_location = os.path.join(data_location, "corrected_data_smaller.csv")
    df = pd.read_csv(file_location)
    df.Year = df.Year.astype(str)
    year_list = ['1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010',
                 '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']
    df.loc[:, year_list] = df.loc[:, year_list].replace(0, np.nan)
    # df.replace(0, 2001, inplace=True)
    return df

def load_file_1000():
    file_location = os.path.join(data_location, "corrected_data_smaller_1000.csv")
    df = pd.read_csv(file_location)
    df.Year = df.Year.astype(str)
    year_list = ['1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010',
                 '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']
    df.loc[:, year_list] = df.loc[:, year_list].replace(0, np.nan)
    # df.replace(0, 2001, inplace=True)
    df['primary_key'] = pd.Series(list(zip(df.Title,df.Artist)))
    df['display_value'] = df.primary_key.apply(lambda x: '{} ({})'.format(x[0],x[1]))
    return df

def load_file_100():
    file_location = os.path.join(data_location, "corrected_data_smaller_100.csv")
    df = pd.read_csv(file_location)
    df.Year = df.Year.astype(str)
    year_list = ['1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010',
                 '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']
    df.loc[:, year_list] = df.loc[:, year_list].replace(0, np.nan)
    df['primary_key'] = pd.Series(list(zip(df.Title,df.Artist)))
    df['display_value'] = df.primary_key.apply(lambda x: '{} ({})'.format(x[0],x[1]))
    # df.replace(0, 2001, inplace=True)
    df.loc[:, 'album_image_meta'] = df['album_image_meta'].str.replace("'", '"').apply(lambda x: json.loads(x))
    df.loc[:, 'artist_image_meta'] = df['artist_image_meta'].str.replace("'", '"').apply(lambda x: json.loads(x))
    return df

def load_offensive_word_dict():
    ## load the offensive words dictionary
    file_location = os.path.join(data_location, "dict_offensive_words_with_genre.pkl")
    with open(file_location,'rb') as f:
        dict_offensive_words = pickle.load(f)

    file_location = os.path.join(data_location, "offensive_words_lable_value.pkl")
    with open(file_location,'rb') as f:
        offensive_word_options = pickle.load(f)

    return dict_offensive_words, offensive_word_options

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