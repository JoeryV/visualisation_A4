import pickle
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

