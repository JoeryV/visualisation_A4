import json
import pickle
import numpy as np
import pandas as pd

def load_df_audio_feats():
    df_audio_feats = pd.read_csv("./Data/top_2000_with_audio_features.csv")
    df_audio_feats.drop("Unnamed: 0",axis=1,inplace=True)
    df_audio_feats.Year = df_audio_feats.Year.astype(str)
    df_audio_feats.replace(0,2001,inplace=True)
    return df_audio_feats

def load_df_lyrics():
    with open("./Data/df_merged_have_lyrics.pkl", "rb") as f:
        df = pickle.load(f)
    return df

def load_df_audio_analysis_feats():
    df = pd.read_csv('./Data/audio_analysis_plus_features.csv')
    year_list = ['1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010',
                 '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']
    for year in year_list:
        df.loc[df[year_list][year] == 0, year] = None
    return df

def load_full_file():
    df = pd.read_csv('./Data/corrected_data.csv')
    df.Year = df.Year.astype(str)
    df.replace(0, 2001, inplace=True)
    return df


def load_small_full_file():
    df = pd.read_csv('./Data/corrected_data_small.csv')
    df.Year = df.Year.astype(str)
    year_list = ['1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010',
                 '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']
    df.loc[:, year_list].replace(0, np.nan, inplace=True)
    # df.replace(0, 2001, inplace=True)
    return df


def load_smaller_full_file():
    df = pd.read_csv('./Data/corrected_data_smaller.csv')
    df.Year = df.Year.astype(str)
    year_list = ['1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010',
                 '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']
    df.loc[:, year_list].replace(0, np.nan, inplace=True)
    # df.replace(0, 2001, inplace=True)
    return df

def load_file_1000():
    df = pd.read_csv('./Data/corrected_data_smaller_1000.csv')
    df.Year = df.Year.astype(str)
    year_list = ['1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010',
                 '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']
    df.loc[:, year_list].replace(0, np.nan, inplace=True)
    # df.replace(0, 2001, inplace=True)
    return df

def load_file_100():
    df = pd.read_csv('./Data/corrected_data_smaller_100.csv')
    df.Year = df.Year.astype(str)
    year_list = ['1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010',
                 '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']
    df.loc[:, year_list].replace(0, np.nan, inplace=True)
    # df.replace(0, 2001, inplace=True)
    df.loc[:, 'album_image_meta'] = df['album_image_meta'].str.replace("'", '"').apply(lambda x: json.loads(x))
    df.loc[:, 'artist_image_meta'] = df['artist_image_meta'].str.replace("'", '"').apply(lambda x: json.loads(x))
    return df
