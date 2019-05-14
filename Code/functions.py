import spotipy
import pandas as pd
import spotipy.util as util
import plotly.graph_objs as go
import dash_html_components as html

from copy import copy
from operator import itemgetter
from sklearn.cluster import KMeans
from Code import token_files as tf
from Code.time_series import get_source, get_values

import numpy as np

def tab_style(vertical=True):
    if vertical:
        style = {
            'width': '19.9vw',
            'textAlign': 'left',
            'float': 'left',
            # "border": "2px dashed lightgreen",
            "font-size": "15px"
                 }
    else:
        style = {'width': '100vh'}
    return style

# style functions
def Header(title='Fun facts top 2000', size=3):
    return html.Div([
        get_header(title, size),
        html.Br([])
    ])

def get_header(title, size):

    title_element = get_subheader(title, size, header=True)
    header = html.Div([
        html.Div([title_element], className="twelve columns padded")
    ], className="row gs-header gs-text-header")

    return header

def get_subheader(title, size=3, className="", header=False):
    if size==1:
        title_element = html.H1(title, className=className)
    elif size==2:
        title_element = html.H2(title, className=className)
    elif size == 3:
        title_element = html.H3(title, className=className)
    elif size == 4:
        title_element = html.H4(title, className=className)
    elif size == 5:
        title_element = html.H5(title, className=className)
    elif size == 6:
        title_element = html.H6(title, className=className)

    if header:
        return html.Div([title_element])
    else:
        return html.Div([title_element, html.Br([])]) #title_element

def create_dd_options(list_of_values):
    options = []
    for value in list_of_values:
        options.append({"label": value, "value": value})
    return options

def generate_year_options(df, col='Year', top2000year=True):
    years = df[col].astype(int)
    # year_range = list(range(years.min(), years.max()+1, 10)) + [2018]
    year_range = list([1924] + list(range(1950, 2000, 20)) + [2018])
    if top2000year:
        year_range = ['1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006',
                      '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014',
                      '2015', '2016', '2017', '2018']
    year_dict = {year: year for year in year_range}
    return year_dict


# # Casper functions
# def generate_adv_analytic_1(df, year):
#     year = str(year)
#     count_per_publ_year = df.loc[df[year] > 0, "Year"].value_counts().sort_index()
#
#     data = [go.Bar(
#         name="Based on Top2000 year {}".format(year),
#         x=list(count_per_publ_year[count_per_publ_year > 0].index),
#         y=list(count_per_publ_year[count_per_publ_year > 0].values))
#     ]
#
#     layout = go.Layout(
#         # xaxis=dict(range=[1938,2018]),
#         # yaxis=dict(range=[0,100]),
#         # title='Number of songs per Publication Year',
#         paper_bgcolor='#FAFAFA',
#         plot_bgcolor='#FAFAFA',
#         margin=go.layout.Margin(
#             l=10,
#             r=10,
#             b=20,
#             t=0
#         )
#     )
#
#     fig = dict(data=data, layout=layout)
#     return fig
#
#
# def generate_adv_analytic_2(df, attribute):
#     df['AVG_' + attribute] = df.groupby('Year')[attribute].transform('mean')
#     temp = df.groupby(['Year', 'AVG_' + attribute]).size().reset_index().rename(columns={0: 'count'})
#     data = [go.Bar(x=list(temp.Year.values),
#                    y=list(temp['AVG_' + attribute].values),
#                    visible=True,
#                    name=attribute)
#             ]
#     layout = dict(  # title='Publication year averages',
#         showlegend=False,
#         paper_bgcolor='#FAFAFA',
#         plot_bgcolor='#FAFAFA',
#         margin=go.layout.Margin(
#             l=10,
#             r=30,
#             b=20,
#             t=0
#         )
#     )
#
#     fig = dict(data=data, layout=layout)
#     return (fig)
#
# def pattern_clustering(dataframe, n_clusters=10):
#     """ Clusters patterns, adds column to the dataframe containing the cluster number of the respective row"""
#     ## Clean dataframe
#     years = [str(i) for i in range(1999, 2019)]
#     tmp_df = copy(dataframe)
#     for year in years:
#         tmp_df.loc[tmp_df[year] == 0, year] = 2500
#         tmp_df.loc[tmp_df[year].isnull(), year] = 2500
#     tmp_df = tmp_df[years]
#
#     kmeans = KMeans(n_clusters=n_clusters)
#     kmeans.fit(tmp_df)
#     y_kmeans = kmeans.predict(tmp_df)
#     tmp_df.loc[:, 'cluster'] = y_kmeans
#     return (tmp_df)
#
#
# def generate_left_plot(dataframe, n_clusters=10):
#     means = {}
#     for cluster in range(n_clusters):
#         temp = dataframe[dataframe['cluster'] == cluster].drop('cluster', axis=1)
#
#         ## Keuze: 2500 voor NaN values
#         means[cluster] = temp.mean()
#
#     data = [go.Scatter(x=means[0].keys(), y=means[cluster].values, name='Cluster {}'.format(cluster),
#                        ) for cluster in range(n_clusters)]
#     layout = go.Layout(
#         yaxis=dict(autorange='reversed'),
#         paper_bgcolor='#FAFAFA',
#         plot_bgcolor='#FAFAFA',
#     )
#     fig = go.Figure(data=data, layout=layout)
#     return (fig)
#
#
# def generate_right_plot(df, dataframe, n_clusters=10):
#     temp = df[df.index.isin(dataframe.index)][
#         ['speechiness', 'energy', 'danceability', 'valence', 'liveness', 'instrumentalness', 'acousticness']]
#
#     result = pd.concat([dataframe['cluster'], temp], axis=1, join='inner')
#
#     means_spider = {}
#     for cluster in range(n_clusters):
#         temp = result[result['cluster'] == cluster].drop('cluster', axis=1)
#         means_spider[cluster] = temp.mean()
#     dataframe = pd.DataFrame(means_spider).T
#
#     features = ['danceability', 'energy', 'speechiness', 'acousticness',
#                 'instrumentalness', 'liveness', 'valence']
#
#     data = [go.Scatterpolar(
#         r=dataframe.iloc[i][features].values,
#         theta=features, name='Cluster {}'.format(i),
#         fill='toself') for i in range(len(dataframe))]
#     layout = go.Layout(
#         paper_bgcolor='#FAFAFA',
#         plot_bgcolor='#FAFAFA',
#     )
#
#
#     #     layout = go.Layout( polar=dict( radialaxis=dict( visible=True, range=[0, 1]  )  ),  paper_bgcolor='#FAFAF, plot_bgcolor='#FAFAFA', showlegend=False )
#
#     fig = go.Figure(data=data, layout=layout)
#     return fig

# Casper functions
def generate_adv_analytic_1(df, year):
    year = str(year)
    count_per_publ_year = df.loc[df[year] > 0, "Year"].value_counts().sort_index()

    data = [go.Bar(
        name="Based on Top2000 year {}".format(year),
        x=list(count_per_publ_year[count_per_publ_year > 0].index),
        y=list(count_per_publ_year[count_per_publ_year > 0].values))
    ]

    layout = go.Layout(xaxis=dict(title='Song Publication Year', range=[1938,2018]),
                       yaxis=dict(title='Number of Songs'),
        # xaxis=dict(range=[1938,2018]),
        # yaxis=dict(range=[0,100]),
        # title='Number of songs per Publication Year',
        paper_bgcolor='#FAFAFA',
        plot_bgcolor='#FAFAFA',
#         margin=go.layout.Margin(
#             l=10,
#             r=10,
#             b=20,
#             t=0
#         )
    )

    fig = dict(data=data, layout=layout)
    return fig


def generate_adv_analytic_2(df, attribute):
    df['AVG_' + attribute] = df.groupby('Year')[attribute].transform('mean')
    temp = df.groupby(['Year', 'AVG_' + attribute]).size().reset_index().rename(columns={0: 'count'})
    data = [go.Bar(x=list(temp.Year.values),
                   y=list(temp['AVG_' + attribute].values),
                   visible=True,
                   name=attribute)
            ]
    layout = dict(  # title='Publication year averages',
                xaxis=dict(title='Song Publication Year'),
                yaxis=dict(title='Score on attribute'),
        showlegend=False,
        paper_bgcolor='#FAFAFA',
        plot_bgcolor='#FAFAFA',
#         margin=go.layout.Margin(
#             l=10,
#             r=30,
#             b=20,
#             t=0
#         )
    )

    fig = dict(data=data, layout=layout)
    return (fig)

def pattern_clustering(dataframe, n_clusters=10):
    """ Clusters patterns, adds column to the dataframe containing the cluster number of the respective row"""
    ## Clean dataframe
    years = [str(i) for i in range(1999, 2019)]
    tmp_df = copy(dataframe)
    for year in years:
        tmp_df.loc[tmp_df[year] == 0, year] = 2500
        tmp_df.loc[tmp_df[year].isnull(), year] = 2500
    tmp_df = tmp_df[years]

    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(tmp_df)
    y_kmeans = kmeans.predict(tmp_df)
    tmp_df.loc[:, 'cluster'] = y_kmeans
    return tmp_df

def generate_left_plot(dataframe, n_clusters=10):
    means = {}
    #################################
    count = 1
    for cluster in range(n_clusters):
        temp = dataframe[dataframe['cluster'] == cluster].drop('cluster', axis=1)
        if temp.mean().min() < 2000:
            ## Keuze: 2500 voor NaN values
            means[count] = temp.mean()
            count += 1

    data = [go.Scatter(x=means[1].keys(), y=means[cluster].values, name='Group {}'.format(cluster),
                       ) for cluster in range(1, count)]

    #################################

    layout = go.Layout(xaxis=dict(title='Year'),
                       yaxis=dict(title='Average rank in Top 2000', range=[2000, 1]),
                       hovermode=False,
                       paper_bgcolor='#FAFAFA',
                       plot_bgcolor='#FAFAFA',
                       )
    fig = go.Figure(data=data, layout=layout)
    return (fig)


def generate_right_plot(df, dataframe, n_clusters=10):
    temp = df[df.index.isin(dataframe.index)][
        ['speechiness', 'energy', 'danceability', 'valence', 'liveness', 'instrumentalness', 'acousticness']]

    result = pd.concat([dataframe['cluster'], temp], axis=1, join='inner')
    means_spider = {}
    #################################
    count = 1
    for cluster in range(n_clusters):
        temp = result[result['cluster'] == cluster].drop('cluster', axis=1)
        if temp.mean().min() < 2000:
            means_spider[count] = temp.mean()
            count += 1
    #################################

    dataframe = pd.DataFrame(means_spider).T

    features = ['danceability', 'energy', 'speechiness', 'acousticness',
                'instrumentalness', 'liveness', 'valence']

    data = [go.Scatterpolar(
        r=dataframe.iloc[i][features].values,
        theta=features, name='Group {}'.format(i + 1),
        fill='toself') for i in range(len(dataframe))]
    data = data[:-1]
    layout = go.Layout(
        paper_bgcolor='#FAFAFA',
        plot_bgcolor='#FAFAFA',
    )

    #     layout = go.Layout( polar=dict( radialaxis=dict( visible=True, range=[0, 1]  )  ),  paper_bgcolor='#FAFAF, plot_bgcolor='#FAFAFA', showlegend=False )

    fig = go.Figure(data=data, layout=layout)
    return fig


# def generate_left_plot(dataframe, n_clusters=10):
#     means = {}
#     for cluster in range(n_clusters):
#         temp = dataframe[dataframe['cluster'] == cluster].drop('cluster', axis=1)
#
#         ## Keuze: 2500 voor NaN values
#         means[cluster] = temp.mean()
#
#     data = [go.Scatter(x=means[0].keys(), y=means[cluster].values,
#                        name='Group {}'.format(cluster),
#                        ) for cluster in range(n_clusters)]
#     layout = go.Layout(xaxis=dict(title='Year'),
#                        yaxis=dict(title='Average rank in Top 2000', range=[2000, 1]),
#         paper_bgcolor='#FAFAFA',
#         plot_bgcolor='#FAFAFA',
#     )
#     fig = go.Figure(data=data, layout=layout)
#     return fig
#
#
# def generate_right_plot(df, dataframe, n_clusters=10):
#     temp = df[df.index.isin(dataframe.index)][
#         ['speechiness', 'energy', 'danceability', 'valence', 'liveness', 'instrumentalness', 'acousticness']]
#
#     result = pd.concat([dataframe['cluster'], temp], axis=1, join='inner')
#
#     means_spider = {}
#     for cluster in range(n_clusters):
#         temp = result[result['cluster'] == cluster].drop('cluster', axis=1)
#         means_spider[cluster] = temp.mean()
#     dataframe = pd.DataFrame(means_spider).T
#
#     features = ['danceability', 'energy', 'speechiness', 'acousticness',
#                 'instrumentalness', 'liveness', 'valence']
#
#     data = [go.Scatterpolar(
#         r=dataframe.iloc[i][features].values,
#         theta=features, name='Group {}'.format(i),
#         fill='toself') for i in range(len(dataframe))]
#     layout = go.Layout(
#         paper_bgcolor='#FAFAFA',
#         plot_bgcolor='#FAFAFA',
#     )
#
#     #     layout = go.Layout( polar=dict( radialaxis=dict( visible=True, range=[0, 1]  )  ),  paper_bgcolor='#FAFAF, plot_bgcolor='#FAFAFA', showlegend=False )
#
#     fig = go.Figure(data=data, layout=layout)
#     return fig


# Vincent functions
#TODO vincent's functions need to be updated by song (radar), song & years (rank_plot), song & attribute & years
# (attribute vs time), additionally it should work with comparing multiple songs


## VINCENT FUNCTIONS
def get_color(idx):
    "Fetches a color for a plot"
    colors = ['rgb(31, 119, 180)', 'rgb(255, 127, 14)',
             'rgb(44, 160, 44)', 'rgb(214, 39, 40)',
             'rgb(148, 103, 189)', 'rgb(140, 86, 75)',
             'rgb(227, 119, 194)', 'rgb(127, 127, 127)',
             'rgb(188, 189, 34)', 'rgb(23, 190, 207)']
    return colors[idx]

# Add these two to the function script
def create_plots(df, songs, years): #, attribute):
    year_list = ['1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006',
                 '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014',
                 '2015', '2016', '2017', '2018']

    features = ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence']

    get_primary_key = lambda x: (x[:x.rfind('(') - 1], x[x.rfind('(') + 1:-1])
    primary_keys = [get_primary_key(song) for song in songs]
    idxs = df[df["primary_key"].isin(primary_keys)].index
    start, stop = year_list.index(str(years[0])), year_list.index(str(years[1]))
    rankings = df.loc[idxs, year_list].values[:,start:stop+1]

    data = []
    for trace_nr, ranking in enumerate(rankings):
        rank_trace = go.Scatter(
            name = '{} ({})'.format(primary_keys[trace_nr][0], primary_keys[trace_nr][1]),
            x = year_list[start: stop+1],
            y = ranking,
            mode = 'lines+markers',
            xaxis='x2',
            yaxis='y2',
            legendgroup = str(trace_nr),
            marker = {'color': get_color(trace_nr), 'symbol': 'circle'},
            showlegend = True
        )
        data.append(rank_trace)

    for trace_nr, idx in enumerate(idxs):
        radar_trace = go.Scatterpolar(
            r = df.loc[idx, features].values,
            name='{} ({})'.format(primary_keys[trace_nr][0], primary_keys[trace_nr][1]),
            theta = features,
            fill = 'toself',
            legendgroup = str(trace_nr),
            mode = 'lines',
            marker = {'color': get_color(trace_nr), 'symbol': 'circle'},
            showlegend = False
        )
        data.append(radar_trace)

    # source = get_source(attribute)
    # values, times = [], []
    # for idx in idxs:
    #     y_vals, time = get_values(df, idx, source, attribute)
    #     values.append(y_vals)
    #     times.append(time)

    # for trace_nr, (vals, time) in enumerate(zip(values, times)):
    #     attribute_trace = go.Scatter(
    #         x = time,
    #         y = vals,
    #         legendgroup = str(trace_nr),
    #         mode = 'lines',
    #         marker = {'color': get_color(trace_nr), 'symbol': 'circle'},
    #         showlegend=False
    #     )
    #     data.append(attribute_trace)

    # xaxis, yaxis = get_time_series_layout_params(attribute, xdomain=[0.75,1], ydomain=[0,1])

    xaxis2 = dict(
        title='Year',
        domain = [0,0.5],
        anchor='y2'
    )

    yaxis2 = dict(
        title='Ranking',
        autorange='reversed',
        domain = [0, 1],
        anchor='x2'
    )

    if stop-start <5:
        xaxis2['nticks'] = stop-start+1
    # if rankings.max()-rankings.min() < 5:
    #     yaxis2['nticks'] = int(rankings.max()-rankings.min()+1)

    layout = go.Layout(

        paper_bgcolor='#FAFAFA',
        plot_bgcolor='#FAFAFA',
        # legend=dict(x=0, y=1.4, orientation='h'),

        # # Axes for Attribute plot (time series), defined in line 32
        # xaxis=xaxis,
        # yaxis=yaxis,

        # Axes for Rank plot
        xaxis2 = xaxis2,
        yaxis2 = yaxis2,

         # Axes for Radar Plot
        polar = dict(

          # This domain controls the position of the radar plot.  Vals must be between 0 and 1
          domain = dict(
            x = [0.5, 1.0],
            y = [0, 1]
          ),

          # Controls min and max values for radar plot
          radialaxis = dict(
            visible = True,
            range = [0, 1]
          ),

          angularaxis = dict(
            thetaunit = "radians"
          )
        ),

        # annotations = [
        #     # dict(
        #     # x=0.875,
        #     # y=1.1,
        #     # text='{} vs. Time'.format(attribute.capitalize()),
        #     # xref= "paper",
        #     # yref= "paper",
        #     # xanchor= "center",
        #     # yanchor= "bottom",
        #     # showarrow= False,
        #     # font = {
        #     #     'size': 16
        #     # }
        # # ),
        #     dict(
        #     x=0.125,
        #     y=1.1,
        #     text='Rank of Song by Year',
        #     xref= "paper",
        #     yref= "paper",
        #     xanchor= "center",
        #     yanchor= "bottom",
        #     showarrow= False,
        #     font = {
        #         'size': 16
        #     }
        # ),
        #     dict(
        #     x=0.5,
        #     y=1.1,
        #     text='Audio Features',
        #     xref= "paper",
        #     yref= "paper",
        #     xanchor= "center",
        #     yanchor= "bottom",
        #     showarrow= False,
        #     font = {
        #         'size': 16
        #     }
        # )
        # ]
        )

    fig = go.Figure(data=data, layout=layout)
    return fig



# def create_attributePlot(df, song, attribute):
#     '''Function updates the attribute vs time plot on the first page of the dashboard'''
#     song = song[0]
#     idx = df.index[df['Title'] == song].tolist()[0]
#     source = get_source(attribute)
#     y_vals, time = get_values(df, idx, source, attribute)
#
#
#     data = []
#     attribute_trace = go.Scatter(
#         x = time,
#         y = y_vals
#     )
#     data.append(attribute_trace)
#     layout = go.Layout(
#         title="{} vs. Time".format(attribute.capitalize()),
#         paper_bgcolor='#FAFAFA',
#         plot_bgcolor='#FAFAFA'
#     )
#     fig = go.Figure(data=data, layout=layout)
#     return fig


def create_radar(currentSong):
    features = ['danceability', 'energy', 'speechiness', 'acousticness',
                'instrumentalness', 'liveness', 'valence']


    trace = go.Scatterpolar(
        r=currentSong.iloc[0][features].values,
        theta=features,
        fill='toself')
    data = [trace]

    layout = go.Layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        paper_bgcolor='#FAFAFA',
        plot_bgcolor='#FAFAFA',
        showlegend=False
    )

    fig = go.Figure(data=data, layout=layout)
    return fig


def create_rank_plot(df, song, years):
    year_list = ['1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006',
                 '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014',
                 '2015', '2016', '2017', '2018']
    print(song)
    song = song[0]
    idx = df.index[df['Title'] == song].tolist()[0]
    start, stop = year_list.index(str(years[0])), year_list.index(str(years[1]))
    rankings = df.loc[idx, year_list].values[start:stop + 1]

    trace = go.Scatter(
        x=year_list[start: stop + 1],
        y=rankings
    )

    xaxis=dict()
    yaxis=dict()

    if stop-start <5:
        xaxis=dict(nticks=stop-start+1)
    if rankings.max()-rankings.min() < 5:
        yaxis=dict(nticks=int(rankings.max()-rankings.min()+1))

    layout = go.Layout(title='Rank of Song by Year',
                       xaxis=xaxis,
                       yaxis=yaxis,
                       paper_bgcolor='#FAFAFA',
                       plot_bgcolor='#FAFAFA',
                       # margin=go.layout.Margin(
                       #     l=10,
                       #     r=10,
                       #     b=10,
                       #     t=10,
                       # ),

                       )  # , yaxis=dict(range=[2000, 1]))
    data = [trace]
    fig = go.Figure(data=data, layout=layout)
    return fig


# spotify functions
def get_track_sample(current_song):
    client_id = tf.SPOTIPY_CLIENT_ID
    client_secret = tf.SPOTIPY_CLIENT_SECRET
    redirect_uri = 'http://localhost/'
    spotify_user = 'Joery de Vos'

    token = util.prompt_for_user_token(spotify_user, 'user-read-recently-played',
                                       client_id = client_id,
                                       client_secret = client_secret,
                                       redirect_uri = redirect_uri)
    sp = spotipy.Spotify(auth=token)
    sample = sp.track(current_song['uri'].iloc[0])
    return sample['preview_url']


########################################################################################################################################
############################################################# Fun facts ################################################################
########################################################################################################################################
def clean(df):
    year_list = ['1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010',
                 '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']
    df.loc[:, year_list] = df.loc[:, year_list].replace(0, np.nan)
    df.loc[:, year_list] = df.loc[:, year_list].astype(float)
    return df

def best_artist_name(df,number):
    df = clean(df)
    return df.Artist.value_counts().index[number]

def best_artist_count(df,number):
    df = clean(df)
    return str(df.Artist.value_counts()[number])

def best_rated_song(df,number):
    df = clean(df)
    df_temp = df.copy()
    if number > 0:
        df_temp = df_temp.drop((df_temp.iloc[:,5:24]==df_temp['Highest position'].sort_values().tolist()[0]).sum(axis=1).sort_values(ascending=False).index[0]).copy()
    if number == 2:
        df_temp = df_temp.drop((df_temp.iloc[:,5:24]==df_temp['Highest position'].sort_values().tolist()[0]).sum(axis=1).sort_values(ascending=False).index[0]).copy()
    return df_temp.loc[(df_temp.iloc[:,5:24]==df_temp['Highest position'].sort_values().tolist()[0]).sum(axis=1).sort_values(ascending=False).index[0]].Artist + " - " + df_temp.loc[(df_temp.iloc[:,5:24]==df_temp['Highest position'].sort_values().tolist()[0]).sum(axis=1).sort_values(ascending=False).index[0]].Title

def best_rated_song2(df,number):
    df = clean(df)
    df_temp = df.copy()
    if number > 0:
        df_temp = df_temp.drop((df_temp.iloc[:,5:24]==df_temp['Highest position'].sort_values().tolist()[0]).sum(axis=1).sort_values(ascending=False).index[0]).copy()
    if number == 2:
        df_temp = df_temp.drop((df_temp.iloc[:,5:24]==df_temp['Highest position'].sort_values().tolist()[0]).sum(axis=1).sort_values(ascending=False).index[0]).copy()
    return df_temp.loc[(df_temp.iloc[:,5:24]==df_temp['Highest position'].sort_values().tolist()[0]).sum(axis=1).sort_values(ascending=False).index[0]].Title

def best_rated_count(df,number):
    df = clean(df)
    word = ' time'
    if int((df[df.Title==best_rated_song2(df,number)].iloc[:,5:24]==df[df.Title==best_rated_song2(df,number)].iloc[:,5:24].min().min()).sum().sum()) > 1:
        word = ' times'
    return "Number " + str(int(df[df.Title==best_rated_song2(df,number)].iloc[:,5:24].min().min())) + " for " + str(int((df[df.Title==best_rated_song2(df,number)].iloc[:,5:24]==df[df.Title==best_rated_song2(df,number)].iloc[:,5:24].min().min()).sum().sum())) + word

def highest_climber(df,number):
    df = clean(df)
    return df[(df.iloc[:,5:24].replace(np.NaN,2001).diff(axis=1).iloc[:,1:]==sorted([x for y in df.iloc[:,5:25].replace(np.NaN,2001).diff(axis=1).iloc[:,1:].values for x in y])[number]).sum(axis=1)>=1].Artist.tolist()[0] + ' - ' +  df[(df.iloc[:,5:24].replace(np.NaN,2001).diff(axis=1).iloc[:,1:]==sorted([x for y in df.iloc[:,5:25].replace(np.NaN,2001).diff(axis=1).iloc[:,1:].values for x in y])[number]).sum(axis=1)>=1].Title.tolist()[0]

def highest_climber_count(df,number):
    df = clean(df)
    return "Climbed with "  + str(int(abs(sorted([x for y in df.iloc[:,5:24].replace(np.NaN,2001).diff(axis=1).iloc[:,1:].values for x in y])[number]))) + " places"

def highest_climber_title(df,number):
    df = clean(df)
    return df[(df.iloc[:,5:24].replace(np.NaN,2001).diff(axis=1).iloc[:,1:]==sorted([x for y in df.iloc[:,5:25].replace(np.NaN,2001).diff(axis=1).iloc[:,1:].values for x in y])[number]).sum(axis=1)>=1].Title.tolist()[0]

def biggest_loser(df,number):
    df = clean(df)
    return df[(df.iloc[:,5:24].replace(np.NaN,2001).diff(axis=1).iloc[:,1:]==sorted([x for y in df.iloc[:,5:25].replace(np.NaN,2001).diff(axis=1).iloc[:,1:].values for x in y],reverse=True)[number]).sum(axis=1)>=1].Artist.tolist()[0] + ' - ' +  df[(df.iloc[:,5:24].replace(np.NaN,2001).diff(axis=1).iloc[:,1:]==sorted([x for y in df.iloc[:,5:25].replace(np.NaN,2001).diff(axis=1).iloc[:,1:].values for x in y],reverse=True)[number]).sum(axis=1)>=1].Title.tolist()[0]

def biggest_loser_count(df,number):
    df = clean(df)
    return "Lost "  + str(int(sorted([x for y in df.iloc[:,5:24].replace(np.NaN,2001).diff(axis=1).iloc[:,1:].values for x in y], reverse=True)[number])) + " places"

def loser_title(df,number):
    df = clean(df)
    return df[(df.iloc[:,5:24].replace(np.NaN,2001).diff(axis=1).iloc[:,1:]==sorted([x for y in df.iloc[:,5:25].replace(np.NaN,2001).diff(axis=1).iloc[:,1:].values for x in y],reverse=True)[number]).sum(axis=1)>=1].Title.tolist()[0]

########################################################################################################################################
########################################################################################################################################
########################################################################################################################################

## NIMA FUNCTIONS
# def create_offensive_words_plot(dict_offensive_words, input_value, xaxis_type_value):
#     data = []
#
#     for off_word in input_value:
#         trace = go.Bar(x=[item[2] for item in dict_offensive_words[off_word]],
#                        y=[item[3] for item in dict_offensive_words[off_word]],
#                        name=off_word)
#         data.append(trace)
#         # data.append({'x': [item[2] for item in dict_offensive_words[off_word]],
#         #                            'y': [item[3] for item in dict_offensive_words[off_word]], 'type': 'bar',
#         #                            'name': off_word})
#
#     layout = go.Layout(
#         paper_bgcolor='#FAFAFA',
#         plot_bgcolor='#FAFAFA',
#         # showlegend=False,
#         margin=go.layout.Margin(
#             l=25,
#             r=10,
#             b=25,
#             t=0
#         )
#     )
#
#     fig = {"data":data, "layout":layout}
#     return fig

def create_offensive_words_plot(dict_offensive_words, input_value, xaxis_type_value):
    data = []

    if xaxis_type_value == "Year":
        for off_word in input_value:
            artist_list = [item[0] for item in dict_offensive_words[off_word]]
            year_list = [item[2] for item in dict_offensive_words[off_word]]
            frequency_list = [item[3] for item in dict_offensive_words[off_word]]
            title_list = [item[1] for item in dict_offensive_words[off_word]]

            sum_frequency_list = []
            for name in set(year_list):
                inx_list = [i for i, x in enumerate(year_list) if x == name]
                sum_frequency = sum([frequency_list[number] for number in inx_list])
                sum_frequency_list.append(sum_frequency)

            all_titles_list = []
            for name in set(year_list):
                inx_list = [i for i, x in enumerate(year_list) if x == name]
                all_titles_list.append(
                    " // ".join(['(' + artist_list[number] + ') ' + title_list[number] for number in inx_list]))

            trace = go.Bar(x=year_list, y=sum_frequency_list,
                           text=all_titles_list,
                           name=off_word)
            data.append(trace)

    else:
        for off_word in input_value:
            artist_list = [item[0] for item in dict_offensive_words[off_word]]
            genre_list = [item[4] for item in dict_offensive_words[off_word]]
            frequency_list = [item[3] for item in dict_offensive_words[off_word]]
            title_list = [item[1] for item in dict_offensive_words[off_word]]

            sum_frequency_list = []
            for name in set(genre_list):
                inx_list = [i for i, x in enumerate(genre_list) if x == name]
                sum_frequency = sum([frequency_list[number] for number in inx_list])
                sum_frequency_list.append(sum_frequency)

            all_titles_list = []
            for name in set(genre_list):
                inx_list = [i for i, x in enumerate(genre_list) if x == name]
                all_titles_list.append(
                    " // ".join(['(' + artist_list[number] + ') ' + title_list[number] for number in inx_list]))


            trace = go.Bar(x=genre_list, y=sum_frequency_list,
                           text=all_titles_list,
                           name=off_word)
            data.append(trace)

    layout = go.Layout(
        paper_bgcolor='#FAFAFA',
        plot_bgcolor='#FAFAFA',
        # showlegend=False,
        margin=go.layout.Margin(
            l=25,
            r=10,
            b=25,
            t=0
        )
    )

    fig = {"data":data, "layout":layout}
    return fig


def create_search_words_plot(df_merged_have_lyrics, input_value):
    data = []
    list_of_artists = df_merged_have_lyrics.Artist.unique().tolist()

    for element in input_value:
        list_of_apperance = []

        for name in list_of_artists:
            temp_df = df_merged_have_lyrics[df_merged_have_lyrics.Artist == name]
            for item in temp_df[['Lyrics_cleaned', 'Title', 'Year']].values:
                if element.lower() in item[0].lower():
                    list_of_apperance.append([element, item[2], name, item[1], item[0].lower().count(element.lower())])
        list_of_apperance.sort(key=itemgetter(1))

        find_word_appearance_list = [item[1:] for item in list_of_apperance]
        data.append({'x': [item[0] for item in find_word_appearance_list],
                                   'y': [item[3] for item in find_word_appearance_list], 'type': 'bar', 'name': element}
                                  )
    layout = go.Layout(
        paper_bgcolor='#FAFAFA',
        plot_bgcolor='#FAFAFA',
        # showlegend=False,
        margin=go.layout.Margin(
            l=25,
            r=10,
            b=25,
            t=0
        )
    )

    figure = {'data': data, "layout": layout}
    return figure
