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

# html.Div([
#     html.Div([dcc.Markdown(dedent('''Add introductory text'''))]),
#
#     # html.Div([
#     #     html.Div([
#               dcc.Graph(id='historical_plot', figure=generate_adv_analytic_1(df))],
#     #         ],
#     #         className="five columns",
#     #         # style={'width': '45%', 'display': 'inline-block', 'float': 'left',
#     #         #        'border': 'thin lightgrey solid'}),  # , 'padding': '10 10 10 10'
#     #
#     #     ),
#     #
#     # ], ),
#
# ], className="row twelve columns"),

# html.Div([
#     dcc.Graph(id='other_plot', figure=generate_adv_analytic_2(df))],
#     className="five columns",
#     # style={'width': '45%', 'display': 'inline-block', 'float': 'right',
#     #        'border': 'thin lightgrey solid', 'padding': '10 10 10 10'}),  # className="six columns"
# )

