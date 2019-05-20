## This stuff are old functions

def generate_adv_analytic_1_old(df):
    years = [str(i) for i in range(1999,2019)]
    data = [go.Bar(visible=False,
                   name='Year = '+str(year),
                   x=list(df[df[year] > 0].Year.value_counts()[df[df[year] > 0].Year.value_counts()>1].index),
                   y=list(df[df[year] > 0].Year.value_counts()[df[df[year] > 0].Year.value_counts()>1].values)
                   ) for year in years]
    data[19]['visible'] = True

    steps = []
    for i in range(len(data)):
        step = dict(method='restyle',  args=['visible', [False] * len(data)],  label=i+1999)
        step['args'][1][i] = True # Toggle i'th trace to "visible"
        steps.append(step)

    # sliders = [dict( active = 19, currentvalue = {"prefix": "Year: "}, pad = {"t": 50}, steps = steps )]
    layout = go.Layout(#sliders=sliders,
                       # xaxis=dict(range=[1938,2020]),
                       # yaxis=dict(range=[0,100]),
                       # title='Number of songs per Publication Year',
                       paper_bgcolor='#FAFAFA',
                       plot_bgcolor='#FAFAFA',
                       )
    fig = dict(data=data, layout=layout)
    return(fig)


def update_plots(df, song="Bohemian Rhapsody", attribute="loudness_start", years=("1999", "2018")):
    attributes = ['loudness_start', 'tempo', 'key', 'mode', 'time_signature']
    features = ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence']
    year_list = ['1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010',
                 '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']


    idx = df.index[df['Title'] == song].tolist()[0]
    start, stop = year_list.index(years[0]), year_list.index(years[1])
    rankings = df.loc[idx, year_list].values[start:stop + 1]

    source = get_source(attribute)
    y_vals, time = get_values(df, idx, source, attribute)

    # Create a trace
    attribute_trace = go.Scatter(
        x=time,
        y=y_vals
    )

    # Create a trace
    rank_trace = go.Scatter(
        x=year_list[start: stop + 1],
        y=rankings,
        mode='lines+markers',
        xaxis='x2',
        yaxis='y2'
    )

    radar_trace = go.Scatterpolar(
        r=df.loc[idx, features].values,
        theta=features,
        fill='toself'
    )

    data = [attribute_trace, rank_trace, radar_trace]

    xaxis, yaxis = get_time_series_layout_params(attribute, xdomain=[0, 1], ydomain=[0, 0.25])

    layout = dict(
        showlegend=False,
        autosize=False,  # Allows for custom-sized plot
        width=900,  # Control width of OVERALL plot
        height=1000,  # Control height of OVERALL plot

        # Axes for Attribute plot (time series), defined in line 32
        xaxis=xaxis,
        yaxis=yaxis,

        # Axes for Rank plot
        xaxis2=dict(
            title='Year',
            domain=[0, 1],
            anchor='y2'
        ),
        yaxis2=dict(
            title='Ranking',
            #             range=[2000, 1],
            domain=[0.4, 0.65]),

        # Axes for Radar Plot
        polar=dict(

            # This domain controls the position of the radar plot.  Vals must be between 0 and 1
            domain=dict(
                x=[0, 0.45],
                y=[0.7, 0.95]
            ),

            # Controls min and max values for radar plot
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            ),

            angularaxis=dict(
                thetaunit="radians"
            )
        ),

        annotations=[
            dict(
                x=0.5,
                y=0.275,
                text='Attribute vs. Time',
                xref="paper",
                yref="paper",
                xanchor="center",
                yanchor="bottom",
                showarrow=False,
                font={
                    'size': 16
                }
            ),
            dict(
                x=0.5,
                y=0.675,
                text='Rank by Year',
                xref="paper",
                yref="paper",
                xanchor="center",
                yanchor="bottom",
                showarrow=False,
                font={
                    'size': 16
                }
            ),
            dict(
                x=0.45 / 2,
                y=1,
                text='Audio Features',
                xref="paper",
                yref="paper",
                xanchor="center",
                yanchor="bottom",
                showarrow=False,
                font={
                    'size': 16
                }
            )
        ]
    )

    fig = dict(data=data, layout=layout)
    return fig


def generate_adv_analytic_2(df):
    var_dic = {}
    columns = ['danceability', 'energy', 'key', 'loudness', 'duration_ms',
               'speechiness', 'acousticness', 'instrumentalness', 'liveness',
               'valence', 'tempo']
    # old code for columns: [i for i in df.columns[24:28].append(df.columns[40:41]).append(df.columns[29:35])]

    for column in columns:
        df['AVG_' + column] = df.groupby('Year')[column].transform('mean')
        #     df['AVG_'+column] = round(df['AVG_'+column] / 1000)
        temp = df.groupby(['Year', 'AVG_' + column]).size().reset_index().rename(columns={0: 'count'})
        if column == columns[0]:
            var_dic['trace_' + column] = go.Bar(x=list(temp.Year.values),
                                                y=list(temp['AVG_' + column].values),
                                                visible=True,
                                                name=column)  ############ color='#ff474c', alpha=0.5
        else:
            var_dic['trace_' + column] = go.Bar(x=list(temp.Year.values),
                                                y=list(temp['AVG_' + column].values),
                                                visible=False,
                                                name=column)  ############ color='#ff474c', alpha=0.5

    data = [var_dic['trace_' + column] for column in columns]

    abc = []
    for i in range(len(columns)):
        a = [False for i in range(len(columns))]
        a[i] = True
        abc.append(a)

    updatemenus = list([
        dict(buttons=list([
            dict(label=columns[i],
                 method='update',
                 args=[{'visible': abc[i]},
                       {'title': 'Publication year averages for {}'.format(columns[i]),
                        'annotations': []}]) for i in range(len(columns))]))])

    layout = dict(#title='Publication year averages',
                  showlegend=False,
                  updatemenus=updatemenus,
                  paper_bgcolor='#FAFAFA',
                  plot_bgcolor='#FAFAFA',
                  )

    fig = dict(data=data, layout=layout)
    return (fig)

# SJOERD FUNCTIONS
def getBestArtistName(df):
    return df.Artist.value_counts().index[0]

def getBestArtistWon(df):
    return str(df.Artist.value_counts()[0])

def getBestSongTitle(df):
    return df.iloc[(df.iloc[:, 4:24] == 1).sum(axis=1).index[0]].Title

def getBestSongArtist(df):
    return df.iloc[(df.iloc[:,4:24]==1).sum(axis=1).index[0]].Artist

def getBestSongWon(df):
    return str((df.iloc[:,4:24]==1).sum(axis=1)[0])

def getHighestClimberName(df):
    return df.iloc[df.iloc[:, 4:24][
        (df.iloc[:, 4:24].diff(axis=1) == df.iloc[:, 4:24].diff(axis=1).min().min())
            .sum(axis=1) > 0].index].Artist + "-" + df.iloc[df.iloc[:, 4:24][
        (df.iloc[:, 4:24].diff(axis=1) == df.iloc[:, 4:24].diff(axis=1).min().min())
            .sum(axis=1) > 0].index].Title

def getHighestClimberNr(df):
    return str(int(abs(df.iloc[:, 4:24].diff(axis=1).min().min())))

def getBiggestLosterName(df):
    return df.iloc[df.iloc[:, 4:24][
        (df.iloc[:, 4:24].diff(axis=1) == df.iloc[:, 4:24].diff(axis=1).max().max())
            .sum(axis=1) > 0].index].Artist + "-" + df.iloc[df.iloc[:, 4:24][
        (df.iloc[:, 4:24].diff(axis=1) == df.iloc[:, 4:24].diff(axis=1).max().max())
            .sum(axis=1) > 0].index].Title

def getBiggestLosterNr(df):
    return str(int(abs(df.iloc[:, 4:24].diff(axis=1).max().max())))




## All this stuff is from elements
fun_facts_page = html.Div([
                    html.Div([
                        Header(),

                        html.Div([

                            html.Div([
                                get_subheader(title="Best artist", size=4, className="gs-header gs-text-header"),

                                html.Div([
                                    html.H3(df_small.Artist.value_counts().index[0]),
                                    html.Img(src='https://logonoid.com/images/thumbs/the-beatles-logo.png', height='40',
                                             width='160'),
                                ],
                                className="six columns"),

                                html.H1(str(df_small.Artist.value_counts()[0])),
                                html.P("Times")
                            ], className = "six columns"),

                            html.Div([
                                get_subheader(title="Most on number 1", size=4, className="gs-header gs-text-header"),

                                html.H3(df_small.iloc[(df_small.iloc[:,4:24]==1).sum(axis=1).index[0]].Title + " - " + df_small.iloc[(df_small.iloc[:,4:24]==1).sum(axis=1).index[0]].Artist),
                                html.Img(src='https://upload.wikimedia.org/wikipedia/commons/b/bd/Bohemian_Rhapsody_by_Queen_US_vinyl_red_label.png', height='160', width='160'),
                                html.H1(str((df_small.iloc[:,4:24]==1).sum(axis=1)[0])),
                                html.P("Times")
                                ], className = "six columns"),
                            ], className = "row "),

                            html.Div([
                                html.Div([
                                    get_subheader(title="Highest climber", size=4,
                                                  className="gs-header gs-text-header"),

                                    html.H3(df_small.iloc[df_small.iloc[:,4:24][(df_small.iloc[:,4:24].diff(axis=1) == df_small.iloc[:,4:24].diff(axis=1).min().min()).sum(axis=1)>0].index].Artist + "-" + df_small.iloc[df_small.iloc[:,4:24][(df_small.iloc[:,4:24].diff(axis=1) == df_small.iloc[:,4:24].diff(axis=1).min().min()).sum(axis=1)>0].index].Title),
                                    html.Img(src='https://upload.wikimedia.org/wikipedia/it/a/a9/Adele%2C_Someone_Like_You_%28Jake_Nava%29.png', height='160', width='160'),
                                    html.H2(str(int(abs(df_small.iloc[:,4:24].diff(axis=1).min().min())))),
                                    html.P("Places")
                                    ], className = "six columns"),

                                html.Div([
                                    get_subheader(title="Biggest loser", size=4,
                                                  className="gs-header gs-text-header"),

                                    html.H3(df_small.iloc[df_small.iloc[:,4:24][(df_small.iloc[:,4:24].diff(axis=1) == df_small.iloc[:,4:24].diff(axis=1).max().max()).sum(axis=1)>0].index].Artist + "-" + df_small.iloc[df_small.iloc[:,4:24][(df_small.iloc[:,4:24].diff(axis=1) == df_small.iloc[:,4:24].diff(axis=1).max().max()).sum(axis=1)>0].index].Title),
                                    html.Img(src='https://img.cdandlp.com/2018/04/imgL/119125064.png', height='160', width='160'),
                                    html.H2(str(int(abs(df_small.iloc[:,4:24].diff(axis=1).max().max())))),
                                    html.P("Places")
                                    ], className = "six columns"),
                                ], className = "row ")

                        ]),
                ], className="twelve columns")

advanced_page = html.Div([
    html.H3('Tab content 3'),
    dcc.Graph(id='historical_plot', figure=generate_adv_analytic_1(df_small)),
    dcc.Graph(id='other_plot', figure=generate_adv_analytic_2(df_small))
])

if speedup == False:
    df_lyrics = load_data.load_df_lyrics()
    print('still loading data,  takes a while')
    # df_lyrics_filtered = copy(df_lyrics)
    df_audio_analysis = load_data.load_df_audio_analysis_feats()

    markdown_text = '''## How many words sangs in each song title?
    In this graph you can see that for each artist how many words are used in a song lyric. It excludes stopwords
    '''

    lyrics_page = html.Div([
        dcc.Markdown(children=markdown_text),
        dcc.Graph(
            id='word-count-vs-year-all',
            figure={
                'data': [
                    go.Scatter(
                        y=df_lyrics[df_lyrics['Artist'] == i]['lyrics_word_count'],
                        x=df_lyrics[df_lyrics['Artist'] == i]['Year'],
                        text=df_lyrics[df_lyrics['Artist'] == i]['Title'],
                        mode='markers',
                        opacity=0.6,
                        marker={
                            'size': 10,
                            'line': {'width': 0.5, 'color': 'white'}
                        },
                        name=i
                    ) for i in sorted(df_lyrics.Artist.unique())
                ],
                'layout': go.Layout(
                    yaxis={'type': 'log', 'title': 'number of words in song'},
                    xaxis={'title': 'song release year'},
                    margin={'l': 100, 'b': 40, 't': 10, 'r': 10},
                    legend={'x': 1, 'y': 1},
                    hovermode='closest'
                )
            }
        ),
    ])

    landing_page_1 = html.Div([
        html.H3('Takes a milly times to render'),
        dcc.Graph(id='Vincent_plot', figure=update_plots(df_audio_analysis)),
    ])





landing_page_2 = html.Div([
    Header("Pick your song", 3),

    html.Div([
        html.Div([html.H6(children="Song: ")], style={"padding": "20 0 0 100"}, className="one columns"),

        html.Div([
            dcc.Dropdown(
                id="dd_song",
                options=create_dd_options(df_small['Title']), #TODO use this as input for the songName id
                value=current_song,
                multi=True,
                style={"width": "80%"},
                ),
        ],
                 className="eleven columns"),


    ], className="row"),

    # html.Div(id="hidden_df_p1", style={'display': 'none'})),

    html.Div([
        html.Div([
            get_subheader('Play Track Sample', size=4, className="gs-header gs-text-header"),

            html.Div([
                html.Img(src=current_song["album_image"],
                         style={
                             'height': '30%',
                             'width': '30%',
                             'float': 'left',
                         },
                         className='twelve columns'
                         ),

                html.H5(id="songName",
                        children='{} - {}'.format(current_song['Title'], current_song['Artist']),
                        className='seven columns'),

                html.A(
                    id="playButton",
                    href=audio_sample_url,
                    children=html.Img(src="http://pluspng.com/img-png/play-button-png-play-button-png-picture-1024.png",
                                      style={
                                          "height": "100%",
                                          "width": "100%",
                                          "float": "left",
                                      }),
                    target="_blank",
                    style={"margin": "0 0 0 100"},
                    className="two columns"
                ),

                html.H4(id="song duration",
                        children="{}:{}".format(int(current_song["duration_ms"] / 1000 / 60 // 1),
                                                  int(current_song["duration_ms"] / 1000 / 60 % 1 * 60)),
                        className="two columns",
                        style={"position": "relative",
                               "bottom": "0"}
                        ),
            ], className="row")

        ], className="six columns"),

        html.Div([
            get_subheader("Text", size=4, className="gs-header gs-text-header"),
            html.Div([
                dcc.Markdown('{}'.format('Placeholder text ' *20))
                ], style={"margin": "0 0 0 30"})
        ], className='six columns',
        ),

    ], className='row twelve columns'),


])



## from app layout

html.Div([
    html.Div([dcc.Markdown(dedent('''Add introductory text'''))]),

    # html.Div([
    #     html.Div([
              dcc.Graph(id='historical_plot', figure=generate_adv_analytic_1(df))],
    #         ],
    #         className="five columns",
    #         # style={'width': '45%', 'display': 'inline-block', 'float': 'left',
    #         #        'border': 'thin lightgrey solid'}),  # , 'padding': '10 10 10 10'
    #
    #     ),
    #
    # ], ),

], className="row twelve columns"),

html.Div([
    dcc.Graph(id='other_plot', figure=generate_adv_analytic_2(df))],
    className="five columns",
    # style={'width': '45%', 'display': 'inline-block', 'float': 'right',
    #        'border': 'thin lightgrey solid', 'padding': '10 10 10 10'}),  # className="six columns"
)

# p3_old = html.Div([
#     Header("Advanced Analytics"),
#
#     html.Div([
#         dcc.Graph(id='historical_plot', figure=generate_adv_analytic_1(df)),# className="six columns"),
#         dcc.Graph(id='other_plot', figure=generate_adv_analytic_2(df)),#  className="six columns")
#     ], className='row')
#
# ],
#     id="tab_id_3",
#     style={'display':"none"}
# )

## from styling stuff
external_css = [
    "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",  # this one contains the headers
    "//fonts.googleapis.com/css?family=Raleway:400,300,600",
    "https://codepen.io/bcd/pen/KQrXdb.css",
    "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"
]

for css in external_css:
    app.css.append_css({"external_url": css})

external_js = [
    "https://code.jquery.com/jquery-3.2.1.min.js",
    "https://codepen.io/bcd/pen/YaXojL.js"
]

for js in external_js:
    app.scripts.append_script({"external_url": js})

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

# p3 = html.Div([
#     Header("Advanced Analytics"),
#
#     # Header left & Header right
#     html.Div([
#         html.Div([get_subheader("Number of songs per publication year", size=3, className="gs-header gs-text-header")],
#                  style={"width": "47%"}, className="six columns"),
#         html.Div([get_subheader("Publication year averages", size=3, className="gs-header gs-text-header")],
#                  style={"width": "48%", 'float': 'right'}, className="six_columns"),
#     ], className="row twelve columns"),
#
#     # Slider & Dropdown
#     html.Div([
#         # year slider
#         html.Div([
#             html.Div([html.H6(children="Top2000 Year: ")], style={"padding": "20 0 0 20"}, className="three columns"),
#
#             # The RangeSlider to select the years
#             html.Div([
#                 dcc.Slider(
#                     id="yearSlider",
#                     min=1999,
#                     max=2018,
#                     marks={k: v for k, v in generate_year_options(df).items() if int(k) % 2 == 1},
#                     ## select only odd years
#                     step=1,
#                     value=2018,
#                     updatemode='drag',
#                 )
#             ], style={"width": "71%"}, className="nine columns")
#         ], className="six columns"),  #### row twelve columns
#
#         # dropdown menu
#         html.Div([
#             html.Div([html.H6(children="Inspect attribute: ")], className="three columns"),
#
#             html.Div([
#                 dcc.Dropdown(
#                     id="dd_song_p3",
#                     options=create_dd_options(p3_col_options),
#                     value="danceability",
#                     multi=False,
#                     style={"width": "80%"},
#                 ),
#             ], className="nine columns"),
#         ], className="six columns"),  ##### row twelve columns
#     ]),
#
#     # Historical & Other plot
#     html.Div([
#         html.Div([
#             dcc.Graph(id='historical_plot',
#                       figure=generate_adv_analytic_1(df, 2018),
#                       config=config,
#                       style={
#                           "margin": "0 0 0 0",
#                           # "width": "100%"
#                       },
#                       )
#         ], className="six columns"),
#         html.Div([
#             dcc.Graph(id='other_plot',
#                       figure=generate_adv_analytic_2(df, 'danceability'),
#                       config=config,
#                       style={
#                           "margin": "0 0 10 0",
#                           # 'width': '100%'
#                       },
#                       )
#         ], className="six columns"),
#     ], className="row twelve columns"),
#
#     # pattern analysis title + markdown text
#     html.Div([
#         get_subheader('Pattern Analysis', size=4, className="gs-header gs-text-header"),
#
#         html.Div([dcc.Markdown(dedent('''
#
#
#
#         Introduction/exlpanation to come. Possibly also add input for number of clusters
#
#
#                                         '''))]),
#
#     ], className="row twelve columns"),
#
#     # row contains left and right plot for the second row of visualisations
#     html.Div([
#         # the left plot
#         html.Div([
#             dcc.Graph(id='left_plot',
#                       figure=generate_left_plot(df3),
#                       style={
#                           "margin": "0 0 0 0",
#                           # 'width': '100%'
#                       },
#                       ),
#         ], className="six columns"),
#         # style={'width': '45%', 'display': 'inline-block', 'float': 'left',
#         #        'border': 'thin lightgrey solid', 'padding': '10 10 1=0 10'}
#
#         # the right plot
#         html.Div([
#             dcc.Graph(id='right_plot',
#                       figure=generate_right_plot(df, df3),
#                       style={
#                           "margin": "0 0 10 0",
#                           # 'width': '100%'
#                       },
#                       )
#         ], className="six columns")
#         # style={'width': '45%', 'display': 'inline-block', 'float': 'right',
#         #            'border': 'thin lightgrey solid'}),  # , 'padding': '10 10 10 10'
#
#     ], className="row twelve columns"),
#
# ],
#     id="tab_id_3",
#     style={'display':"none"}
# )

# p4 = html.Div([
#     Header("Lyric Analysis"),
#
#     html.Div([
#         html.Div([
#             get_subheader("Appearance of Offensive Words", size=3, className="gs-header gs-text-header"),
#
#             html.Div([
#                 html.Div([html.H6(children="Offensive words: ")], className="three columns"),
#
#                 html.Div([
#                     dcc.Dropdown(
#                         id='ddOffensiveWords',
#                         options=offensive_word_options,
#                         value=['dirty', 'shit', 'sex'],
#                         multi=True,
#                         style={"width": "80%"},
#                     ),
#                 ], className="nine columns"),
#             ], className="six columns"),
#
#             dcc.Graph(
#                 id='offensiveWordsPlot',
#                 figure=create_offensive_words_plot(dict_offensive_words, ['dirty', 'shit', 'sex'], xaxis_type_value="Year"),
#                 config=config,
#                 style={
#                     "margin": "0 0 0 0",
#                     # "width": "100%"
#                 },)
#         ], className="six columns"),
#
#         html.Div([
#             get_subheader("First Appearance of Words", size=3, className="gs-header gs-text-header"),
#
#             html.Div([
#                 html.Div([html.H6(children="Words to search: ")], className="three columns"),
#
#                 html.Div([
#                     dcc.Dropdown(
#                         id='ddWordSearch',
#                         options=all_words_lable_value,
#                         value=['honey', 'heart', 'love'],
#                         multi=True,
#                         style={"width": "80%"},
#                     ),
#                 ], className="nine columns"),
#             ], className="six columns"),
#
#             dcc.Graph(
#                 id='firstAppearance',
#                 figure=create_search_words_plot(df_merged_have_lyrics, ['honey', 'heart','love']),
#                 config=config,
#                 style={
#                     "margin": "0 0 0 0",
#                     # "width": "100%"
#                 },)
#         ], className="six columns"),
#
#         # get_subheader("Word cloud", size=3, className="gs-header gs-text-header"),
#         # html.Div(id='my-div'),
#
#     ], className="row twelve columns")
#
#
#
# ## THIS WAS THE VERY EXTENSIVE PLOT
#     # dcc.Markdown(children=markdown_text),
#     # dcc.Graph(
#     #     id='word-count-vs-year-all',
#     #     figure={
#     #         'data': [
#     #             go.Scatter(
#     #                 y=df_lyrics[df_lyrics['Artist'] == i]['lyrics_word_count'],
#     #                 x=df_lyrics[df_lyrics['Artist'] == i]['Year'],
#     #                 text=df_lyrics[df_lyrics['Artist'] == i]['Title'],
#     #                 mode='markers',
#     #                 opacity=0.6,
#     #                 marker={
#     #                     'size': 10,
#     #                     'line': {'width': 0.5, 'color': 'white'}
#     #                 },
#     #                 name=i
#     #             ) for i in sorted(df_lyrics.Artist.unique())
#     #         ],
#     #         'layout': go.Layout(
#     #             yaxis={'type': 'log', 'title': 'number of words in song'},
#     #             xaxis={'title': 'song release year'},
#     #             margin={'l': 100, 'b': 40, 't': 10, 'r': 10},
#     #             legend={'x': 1, 'y': 1},
#     #             hovermode='closest'
#     #         )
#     #     }
#     # ),
# ],
#     id="tab_id_4",
#     style={'display':"none"}
# )


# @app.callback(Output("rankPlot", "figure"),
#               [#Input("_filtered_df_stored", "children"),
#                Input("dd_song_p1", "value"),
#                Input("yearRange_p1", "value"),
#                ])
# def update_rankplot(songname, years): #df,
#     # df = pd.read_json(df, orient="split")
#     return create_rank_plot(df, songname, years)
#
#
# @app.callback(Output("radarPlot", "figure"),
#               [Input("_current_song_stored", "children")])
# def update_radarplot(current_song):
#     current_song = pd.read_json(current_song, orient="split")
#     return create_radar(current_song)
#
#
# @app.callback(Output("attributePlot", "figure"),
#               [Input("dd_song_p1", "value"),
#                Input("dd_attribute", "value"),
#                ])
# def update_attributePlot(songname, attribute):
#     '''Not using filtered df here so we can cut the size of that df.
#     This one will always be based on the songname anyway '''
#     return create_attributePlot(df, songname, attribute)
#


# @app.callback(
#     Output(component_id='my-div', component_property='children'),
#     [Input(component_id='ddArtist', component_property='value'),
#      Input(component_id='ddGenre', component_property='value'),
#      Input(component_id='releaseYearSlider', component_property='value')]
# )
# ## create the visualization based on the input value and pass it as output children component for my_div
#
# def update_output_div(input_artist, input_genre, input_year):
#     ## create a tuple from input values to be used as key for the dictionary of word clouds
#     temp_tuple_input = tuple(list(item for item in [input_artist, input_year, input_genre] if item != None))
#
#     ## convert one input from tuple to format that is acceptable for dictionary of word clouds keys
#     if len(temp_tuple_input) == 1:
#
#         if type(temp_tuple_input[0]) == int:
#             temp_tuple_input = int(temp_tuple_input[0])
#
#         elif type(temp_tuple_input[0]) == str:
#             temp_tuple_input = temp_tuple_input[0]
#
#     if temp_tuple_input in list_dictionary_keys:
#
#         ## get the values related to plot the wordcloud
#
#         word_cloud = dic_Artist_wordcloud[temp_tuple_input][1]
#         length = dic_Artist_wordcloud[temp_tuple_input][2]
#         colors = dic_Artist_wordcloud[temp_tuple_input][3]
#         weights = dic_Artist_wordcloud[temp_tuple_input][4]
#
#     else:
#         temp_tuple_input = ('pink', 'blues')
#         word_cloud = dic_Artist_wordcloud[temp_tuple_input][1]
#         length = dic_Artist_wordcloud[temp_tuple_input][2]
#         colors = dic_Artist_wordcloud[temp_tuple_input][3]
#         weights = dic_Artist_wordcloud[temp_tuple_input][4]
#
#     return (html.Div([
#
#         dcc.Markdown(children="""## words cloud
#     In this graph you can see that higher frequncy words apeear in bigger font size"""),
#
#         dcc.Graph(
#             id='word-cloud',
#             figure={
#                 'data':
#                     [
#                         go.Scatter(
#                             x=[random.random() for i in range(length)],
#                             y=[random.random() for i in range(length)],
#                             mode='text',
#                             text=list(word_cloud.words_.keys()),
#                             hoverinfo='text',
#                             marker={'opacity': 0.3},
#                             textfont={'size': weights,
#                                       'color': colors}
#                         )],
#
#                 # 'color':  colors,
#                 'layout': go.Layout(
#                     xaxis={'showgrid': False, 'showticklabels': False, 'zeroline': False},
#                     yaxis={'showgrid': False, 'showticklabels': False, 'zeroline': False}
#                 )
#             }
#         )
#     ]))
