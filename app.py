'''
Notes

* Turning everything into the same style
* Making sure the advanced analytics page and lyrics page are interactive
* In order to make things interactive we need to enable the callback within the same page
* Filters on genre, artist, year (top2000)

CSS in Dash: https://dash.plot.ly/external-resources
'''

import dash
from Code import elements, load_data

import pandas as pd
import dash_core_components as dcc

from Code.functions import *
from textwrap import dedent
# from flask_caching import Cache
from dash.dependencies import Input, Output


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
config= {'displayModeBar': False, 'showLink' : False}
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.scripts.config.serve_locally = True

# global variables
app.title = "Top 2000"
vertical = True


df = load_data.load_file_100()
df_lyrics = load_data.load_df_lyrics()
df3 = pattern_clustering(df)
dict_offensive_words, offensive_word_options = load_data.load_offensive_word_dict()
df_merged_have_lyrics = load_data.load_df_lyrics()
all_words_lable_value = load_data.load_appearance_options()


attributes = ['tempo', 'key', 'mode', 'time_signature'] #TODO loadness start is not in the new df. Does Vincent want it? If so, add it in,
genre_options = create_dd_options(df['primary_genre'].dropna().unique())
genre_options.append({"label": "all genres", "value": ""})
artist_options = create_dd_options(df["Artist"].dropna().unique())
artist_options.append({"label": "all artists", "value": ""})

releaseYear_options = create_dd_options(df["Year"].dropna().unique())
releaseYear_options.append({"label": "all release years", "value": ""})

p3_col_options = ['danceability', 'energy', 'key', 'loudness', 'duration_ms',
                  'speechiness', 'acousticness', 'instrumentalness', 'liveness',
                  'valence', 'tempo']

markdown_text = '''## How many words sangs in each song title?
In this graph you can see that for each artist how many words are used in a song lyric. It excludes stopwords
'''


placeholder = html.Div([
    html.H3('Tab content 1'),
    dcc.Graph(
        id='graph-1-tabs',
        figure={
            'data': [{
                'x': [1, 2, 3],
                'y': [3, 1, 2],
                'type': 'bar'
            }]
        }
    )
])

p1 = html.Div([
    Header("Pick your song", 3),

    # This row contains the dropdown where you choose your song
    html.Div([
        html.Div([html.H6(children="Song: ")], className="one columns"),

        # The dropdown to select the song
        #TODO update this dropdown based on the global params
        html.Div([
            dcc.Dropdown(
                id="dd_song_p1",
                options=create_dd_options(df['Title']),
                value=["Bohemian Rhapsody"],
                multi=True,
                style={"width": "80%"},
                ),
        ], className="eleven columns"),

    ], className="row twelve columns"),

    # This row contains the Attribute Dropdown
    #TODO update this dropdown based on the global params
    html.Div([
        html.Div([html.H6(children="Attribute: ")], className="one columns"),

        # The dropdown to select the attribute
        html.Div([
            dcc.Dropdown(
                id="dd_attribute",
                options=create_dd_options(attributes),
                value="tempo",
                multi=False,
                style={"width": "80%"},
            ),
        ], className="eleven columns"),

    ], className="row twelve columns"),

    # This row contains the RangeSlider for the years
    html.Div([
        html.Div([html.H6(children="Years: ")], style={"padding": "20 0 0 100"}, className="one columns"),

        # The RangeSlider to select the years
        html.Div([
            dcc.RangeSlider(
                id="yearRange_p1",
                min=1999,
                max=2018,
                marks=generate_year_options(df),
                step=1,
                value=[1999, 2018],
                allowCross=False,
            )
        ], style={"width": "60%"}, className="eleven columns")
    ], className="row twelve columns"),

    # This row contains the song title, description of the song and so forth
    html.Div([

        # div containing the song name and sample
        html.Div([
            get_subheader('Play Track Sample', size=4, className="gs-header gs-text-header"),

            html.Div([
                html.Img(
                    id="albumImg",
                    src="https://i.scdn.co/image/beae4292c3214147a7201ef48f855b4ed40ff84e",
                    style={
                        "height": "30%",
                        "width": "30%",
                        "float": "left"
                    },
                    className="twelve columns"
                ),

                html.H5(id="songName",
                        children="Bohemian Rhapsody - Queen",
                        className="seven columns"),

                html.A(
                    id="playButton",
                    href=["https://p.scdn.co/mp3-preview/d1ff0ba5c5538ca2c50b808aab2278253c98b038?cid=3c49fddc0db74e098cf098070532f4b5"],
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

                html.H4(
                    id="songDuration",
                    children="{}:{}".format(5, 54),
                    className="two columns",
                    style={"position": "relative",
                           "bottom": "0"}
                ),
            ], className="row")

        ], className="six columns"),

        # div containing the song description/ text
        html.Div([
            get_subheader("Text", size=4, className="gs-header gs-text-header"),
            html.Div([
                dcc.Markdown(dedent('''Unfortunately, we do not have any information on this song yet. 
                We are working hard to realise descriptions for every song.
                We hope we will have a description ready by your next visit!

Thank you for your understanding, \n
The Top 2000 Team''')),
                ], style={"margin-left": "10px"})
        ], className='six columns',
        ),

    ], className='row twelve columns'),

    # this row contains the graphs
    html.Div([
        get_subheader('Visualisations', size=4, className="gs-header gs-text-header"),

        dcc.Graph(
            id="rankPlot",
            figure=create_rank_plot(df, ["Bohemian Rhapsody"], (1999, 2018)),
            style={"margin": "0 0 0 0"},
            className="four columns"
        ),

        dcc.Graph(
            id="radarPlot",
            figure=create_radar(pd.DataFrame(df.loc[0]).T),
            style={"margin": "0 0 0 0"},
            className="four columns"
        ),

        dcc.Graph(
            id="attributePlot",
            figure=create_attributePlot(df, ["Bohemian Rhapsody"], "tempo"),
            style={"margin": "0 0 0 0"},
            className="four columns"
        ),

    ], className='row twelve columns')


],
id="tab_id_1",)


p2 = html.Div([
    html.Div([
        Header(),

        # Row contains best artist and best song
        html.Div([
            # Contains the Best artist block
            html.Div([
                get_subheader(title="Most frequent artist", size=4, className="gs-header gs-text-header"),

                # Subrow contains the image + name + amount of times won
                html.Div([
                    # Image of Best Artist
                    html.Img(
                        id="Best_artist_image",
                        src=df.loc[df["Artist"] == best_artist_name(df)]["artist_image"].iloc[0],
                        style={"margin": "0 0 50px 0"},
                        className="two columns",
                    ),

                    # Name of best artist
                    html.H3(id="best_artist_name_change", children=best_artist_name(df), ##TODO have to create a callback for this
                            style={"margin": "0 0 0 0",},
                            className="ten columns",
                            ),

                    # The amount of times the artist has won
                    html.H3(id="best_artist_count", children="won {} times".format(best_artist_count(df)), ##TODO have to create a callback for this
                            style={"margin": "0 0 0 0",},
                            className="ten columns",
                            ),
                ],
                    className="row",
                ),
            ], className="six columns"),

            # Contains the best scoring song
            html.Div([
                get_subheader(title="Best rated song", size=4, className="gs-header gs-text-header"),

                # subrow contains the best song info
                html.Div([
                    html.Img(id="Best_rated_image",  # TODO create a callback to update this
                             src=df.loc[df["Title"] == best_rated_song2(df)]["album_image"].iloc[0],
                             # height='160', width='160',
                             style={"margin": "0 0 0 0"},
                             className="two columns",
                             ),
                    html.H3(id="best_rated_song",
                            children=best_rated_song(df), #getBestSongTitle(df) + " - " + getBestSongArtist(df),
                            style={"margin": "0 0 0 0"},
                            className="ten columns"),
                    html.H3(id="best_rated_count",
                            children="won {} times".format(best_rated_count(df)),
                            style={"margin": "0 0 0 0"},
                            className="ten columns"),
                ], className="row"),
            ], className = "six columns"),

        ], className="row"),

            # Row contains the highest climber and biggest lost
        html.Div([

            # Contains the highest climber
            html.Div([
                get_subheader(title="Highest climber", size=4, className="gs-header gs-text-header"),

                html.Div([
                    html.Img(
                        id="highest_climb",
                        src=df.loc[df["Title"] == highest_climber_title(df).values[0]]["album_image"].iloc[0],
                        # height='160', width='160',
                        style={"margin": "0 0 50px 0"},
                        className="two columns",
                    ),

                    html.H3(
                        id="highest_climber",
                        children=highest_climber(df),
                        style={"margin": "0 0 0 0",},
                        className="ten columns",
                            ),

                    html.H3(
                        id="highest_climber_count",
                        children=highest_climber_count(df),
                        style={"margin": "0 0 0 0"},
                        className="ten columns"),
                ], className="row")
            ], className="six columns"),

            # Contains the biggest lost
            html.Div([
                get_subheader(title="Biggest loser", size=4, className="gs-header gs-text-header"),

                html.Div([
                    html.Img(
                        id="biggest_los",
                        src=df.loc[df["Title"] == loser_title(df).values[0]]["album_image"].iloc[0],
                        # height='160', width='160',
                        style={"margin": "0 0 50px 0"},
                        className="two columns",
                        ),


                    html.H3(
                        id="biggest_loser",
                        children=biggest_loser(df),
                        style={"margin": "0 0 0 0", },
                        className="ten columns",
                            ),

                    html.H3(
                        id="biggest_loser_count",
                        children=biggest_loser_count(df),
                        style={"margin": "0 0 0 0"},
                        className="ten columns"),
                ], className="row")
            ], className="six columns"),

        ], className="row")
    ]),
],
    className="twelve columns",
    id="tab_id_2",
    style={'display': "none"}
)


p3 = html.Div([
    Header("Advanced Analytics"),

    # dropdown menu
    html.Div([
        html.Div([html.H6(children="Inspect attribute: ")], className="three columns"),

        # TODO set proper default value
         html.Div([
             dcc.Dropdown(
                 id="dd_song_p3",
                 options=create_dd_options(p3_col_options),
                 value="danceability",
                 multi=False,
                 style={"width": "80%"},
             ),
         ], className="nine columns"),
    ], className="row twelve columns"),

    # year slider
    html.Div([
        html.Div([html.H6(children="Top2000 Year: ")], style={"padding": "20 0 0 100"}, className="three columns"),

        # TODO adapt this to the proper years
        # The RangeSlider to select the years
        html.Div([
            dcc.Slider(
                id="yearSlider",
                min=1999,
                max=2018,
                marks=generate_year_options(df),
                step=1,
                value=2018,
                updatemode='drag',
            )
        ], style={"width": "60%"}, className="nine columns")
    ], className="row twelve columns"),

    # row contains nr songs plot and attribute averages plot
    html.Div([
        # Number of songs per publication year
        html.Div([
            get_subheader("Number of songs per publication year", size=3, className="gs-header gs-text-header"),

            html.Div([
                dcc.Graph(id='historical_plot', #TODO Have to update this figure based on the slider on same page
                          figure=generate_adv_analytic_1(df, 2018),
                          config=config,
                          style={"margin": "0 0 0 0", "width": "100%"},
                )
            ]),
        ], className="six columns"),

        # Publication year averages
        html.Div([
                get_subheader("Publication year averages", size=3, className="gs-header gs-text-header"),

                html.Div([
                    dcc.Graph(id='other_plot',
                              figure=generate_adv_analytic_2(df, 'danceability'),
                              config=config,
                              style={"margin": "0 0 0 0", 'width': '100%'},
                              )
                ]),
            ], className="six columns")

    ], className="row twelve columns"),

    # pattern analysis title + markdown text
    html.Div([
        get_subheader('Pattern Analysis', size=4, className="gs-header gs-text-header"),

        html.Div([dcc.Markdown(dedent('''Introduction/exlpanation to come. Possibly also add input for number of clusters'''))]),

    ], className='row twelve columns'),

    # row contains left and right plot for the second row of visualisations
    html.Div([
            # the left plot
            html.Div([
                dcc.Graph(id='left_plot',
                          figure=generate_left_plot(df3),
                          style={"margin": "0 0 0 0", 'width': '100%'},
                          ),
            ], className="six columns"),
                # style={'width': '45%', 'display': 'inline-block', 'float': 'left',
                #        'border': 'thin lightgrey solid', 'padding': '10 10 1=0 10'}

            # the right plot
            html.Div([
                dcc.Graph(id='right_plot',
                          figure=generate_right_plot(df, df3),
                          style={"margin": "0 0 0 0", 'width': '100%'},
                          )
            ], className="six columns")
            # style={'width': '45%', 'display': 'inline-block', 'float': 'right',
            #            'border': 'thin lightgrey solid'}),  # , 'padding': '10 10 10 10'

        ], className="row twelve columns"),

    html.Div([dcc.Markdown(dedent('''Also here to-do: add table which shows songs from the in the left image selected cluster(s)''')), ],
             style={'display': 'inline-block', 'float': 'bottom'})
],
    id="tab_id_3",
    style={'display':"none"}
)


p4 = html.Div([
    Header("Lyric Analysis"),

    html.Div([
        html.Div([html.H6(children="Offensive words: ")], className="three columns"),

        html.Div([
            dcc.Dropdown(
                id='ddOffensiveWords',
                options=offensive_word_options,
                value=['dirty', 'shit', 'sex'],
                multi=True,
                style={"width": "80%"},
            ),
        ], className="nine columns"),
    ], className="row twelve columns"),

    html.Div([
        html.Div([html.H6(children="Words to search: ")], className="three columns"),

        html.Div([
            dcc.Dropdown(
                id='ddWordSearch',
                options=all_words_lable_value,
                value=['honey', 'heart','love'],
                multi=True,
                style={"width": "80%"},
            ),
        ], className="nine columns"),
    ], className="row twelve columns"),


    html.Div([
        html.Div([
            get_subheader("Appearance of Offensive Words", size=3, className="gs-header gs-text-header"),

            dcc.Graph(
                id='offensiveWordsPlot',
                figure=create_offensive_words_plot(dict_offensive_words, ['dirty', 'shit', 'sex']),
                style={"margin": "0 0 0 0", "width": "100%"},
            )
        ], className="six columns"),

        html.Div([
            get_subheader("First Appearance of Words", size=3, className="gs-header gs-text-header"),

            dcc.Graph(
                id='firstAppearance',
                figure=create_search_words_plot(df_merged_have_lyrics, ['honey', 'heart','love']),
                style={"margin": "0 0 0 0", "width": "100%"},
            )
        ], className="six columns")
    ], className="row twelve columns")


## THIS WAS THE VERY EXTENSIVE PLOT
    # dcc.Markdown(children=markdown_text),
    # dcc.Graph(
    #     id='word-count-vs-year-all',
    #     figure={
    #         'data': [
    #             go.Scatter(
    #                 y=df_lyrics[df_lyrics['Artist'] == i]['lyrics_word_count'],
    #                 x=df_lyrics[df_lyrics['Artist'] == i]['Year'],
    #                 text=df_lyrics[df_lyrics['Artist'] == i]['Title'],
    #                 mode='markers',
    #                 opacity=0.6,
    #                 marker={
    #                     'size': 10,
    #                     'line': {'width': 0.5, 'color': 'white'}
    #                 },
    #                 name=i
    #             ) for i in sorted(df_lyrics.Artist.unique())
    #         ],
    #         'layout': go.Layout(
    #             yaxis={'type': 'log', 'title': 'number of words in song'},
    #             xaxis={'title': 'song release year'},
    #             margin={'l': 100, 'b': 40, 't': 10, 'r': 10},
    #             legend={'x': 1, 'y': 1},
    #             hovermode='closest'
    #         )
    #     }
    # ),
],
    id="tab_id_4",
    style={'display':"none"}
)




app.layout = html.Div(
    [
        # components which contains the tab structure
        html.Div(
            [
                # image
                html.Div([elements.top_2000_img]),

                # everything underneath the image
                html.Div([

                    # Tabs element
                    html.Div(
                        [elements.tabs],
                        style={
                            "float": "left",
                            "width": "100vw",
                            "margin": "0 0 0 0",
                            "clear": "both"
                        },
                        className="row one columns",
                    ),

                    # This Div contains the global parameters.
                    # Position is currently fixed so that it floats with scrolling.
                    html.Div([
                        html.H6(['Genre'], style={"margin": "1rem 0 0 0"}),
                        dcc.Dropdown(
                            id="ddGenre",
                            options=genre_options,
                            value=["all genres"],
                            multi=True,
                            style={
                                "margin": "0 0 0 0",
                                "width": "100%",
                            },
                        ),

                        html.H6(['Artist'], style={"margin": "1rem 0 0 0"}),
                        dcc.Dropdown(
                            id="ddArtist",
                            options=artist_options,
                            value=["all artists"],
                            multi=True,
                            style={
                                "margin": "0 0 0 0",
                                "width": "100%",
                            },
                        ),

                        html.H6(["Release Year"], style={"margin": "1rem 0 0 0"}),
                        dcc.Dropdown(
                            id="ddReleaseYear",
                            options=releaseYear_options,
                            value=["all release years"],
                            multi=True,
                            style={
                                "margin": "0 0 0 0",
                                "width": "100%",
                            },
                        )
                    ],
                        style={
                            "float": "left",
                            "width": "18vw",
                            "clear": "both",
                            "margin": "0 0 75px 0",
                            "position": "fixed",
                            "bottom": "10",
                            # "left":"0",
                        },
                        className="row one columns"),

                ], style={
                    'borderRight': 'thin lightgrey solid',
                    'height': '100vh'}
                )

            ],
            style={'width': '20vw',
                   'float': 'left',
                   # "border": "2px solid green",
                   },
            className="two columns",
        ),

        # tab_ouput
        html.Div(
            html.Div(id='tab-output',
                     children=[p1,
                               p2,
                               p3,
                               p4]
                     ),
            style={'width': '78vw',
                   'float': 'right', }
        ),

        # # component which contains the 'tab output' aka the actual content
        # html.Div(
        #     [
        #         html.Div(id='tab-output'),
        #     ],
        #     style={'width': '78vw',
        #            'float': 'right',
        #            }
        # ),

        # hidden component to store data
        html.Div(id='_filtered_df_stored',
                 children=df.to_json(date_format='iso', orient="split"),
                 style={'display': 'none'}),

        # hidden component to store data
        html.Div(id='_current_song_stored', style={'display': 'none'}),
    ],
    className='offsets-dis-by-one column',
    style={
        'fontFamily': 'Sans-Serif',
        'margin-left': '10px',
        'margin-right': 'auto',
    }
)


@app.callback(Output("_current_song_stored", "children"),
              [Input("dd_song_p1", "value")])
def updateCurrentSong(song_title):
    current_song = df.loc[df["Title"] == song_title[0]]
    return current_song.to_json(date_format="iso", orient="split")


@app.callback(Output("albumImg", "src"),
              [Input("_current_song_stored", "children")])
def getAlbumImg(current_song):
    current_song = pd.read_json(current_song, orient="split")
    return current_song["album_image"].iloc[0]

# @app.callback([Output("bestArtistImg", "src")], #TODO Have to update this based on the filtered df rather than the _current_song_stored
#               [Input("_current_song_stored", "children")])
# def getArtistImg(current_song):
#     current_song = pd.read_json(current_song, orient="split")
#     return current_song["artist_image"].iloc[0]


@app.callback(Output("songName", "children"),
              [Input("_current_song_stored", "children")])
def getSongTitle(current_song):
    current_song = pd.read_json(current_song, orient="split")
    return "{} - {}".format(current_song["Title"].iloc[0], current_song["Artist"].iloc[0])


@app.callback(Output("songDuration", "children"),
              [Input('_current_song_stored', 'children')])
def getSongDuration(current_song):
    current_song = pd.read_json(current_song, orient='split')
    minutes = int(current_song["duration_ms"] / 1000 / 60 // 1)
    seconds = int(current_song["duration_ms"] / 1000 / 60 % 1 * 60)
    return "{}:{}".format(minutes, seconds)


@app.callback(Output("playButton", "href"),
              [Input('_current_song_stored', 'children')])
def playSong(current_song):
    current_song = pd.read_json(current_song, orient='split')
    return get_track_sample(current_song)


@app.callback(Output("rankPlot", "figure"),
              [#Input("_filtered_df_stored", "children"),
               Input("dd_song_p1", "value"),
               Input("yearRange_p1", "value"),
               ])
def update_rankplot(songname, years): #df,
    # df = pd.read_json(df, orient="split")
    return create_rank_plot(df, songname, years)


@app.callback(Output("radarPlot", "figure"),
              [Input("_current_song_stored", "children")])
def update_radarplot(current_song):
    current_song = pd.read_json(current_song, orient="split")
    return create_radar(current_song)


@app.callback(Output("attributePlot", "figure"),
              [Input("dd_song_p1", "value"),
               Input("dd_attribute", "value"),
               ])
def update_attributePlot(songname, attribute):
    '''Not using filtered df here so we can cut the size of that df.
    This one will always be based on the songname anyway '''
    return create_attributePlot(df, songname, attribute)



@app.callback(Output("_filtered_df_stored", "children"),
            [Input("ddGenre", "value"),
             Input("ddArtist", "value"),
             Input("ddReleaseYear", "value")])
def filter_on_df(genres, artists, release_years):
    if (not genres) or ('all genres' in genres):
        genres = df['primary_genre'].unique()
    if (not artists) or ('all artists' in artists):
        artists = df['Artist'].unique()
    if (not release_years) or ('all release years' in release_years):
        release_years = df['Year'].unique()

    columns = df.columns.tolist()
    columns.remove('segments')
    columns.remove('sections')
    loc_df = df[columns]
    loc_df = loc_df.loc[df["primary_genre"].isin(genres)]
    loc_df = loc_df.loc[df["Artist"].isin(artists)]
    loc_df = loc_df.loc[df["Year"].isin(release_years)]
    return loc_df.to_json(date_format="iso", orient="split")


@app.callback([Output("Best_artist_image", "src"),
             Output("Best_rated_image", "src"),
             Output("highest_climb", "src"),
             Output("biggest_los", "src")],
              [Input("_filtered_df_stored", "children")])
def getArtistImage(df):
    df = pd.read_json(df, orient="split")
    best_artist = df.loc[df["Artist"] == best_artist_name(df)]
    title_best_rated_song = df.loc[df["Title"] == best_rated_song2(df)]
    title_highest_climber = df.loc[df["Title"] == highest_climber_title(df).values[0]]
    title_loser = df.loc[df["Title"] == loser_title(df).values[0]]
    return best_artist["artist_image"].iloc[0], title_best_rated_song["album_image"].iloc[0], title_highest_climber["album_image"].iloc[0], title_loser["album_image"].iloc[0]

@app.callback([Output("highest_climber", "children"),
              Output("highest_climber_count", "children"),
              Output("biggest_loser", "children"),
              Output("biggest_loser_count", "children"),
              Output("best_rated_count", "children"),
              Output("best_rated_song", "children"),
              Output("best_artist_count", "children"),
              Output("best_artist_name_change", "children")],
              [Input("_filtered_df_stored", "children")])
def highest_climber_(df):
    df = pd.read_json(df, orient="split")
    return highest_climber(df),highest_climber_count(df), biggest_loser(df), biggest_loser_count(df), best_rated_count(df), best_rated_song(df), best_artist_count(df), best_artist_name(df)


@app.callback(Output("historical_plot", "figure"),
              [Input("yearSlider", "value")])
def update_historical_plot(year_value):
    return generate_adv_analytic_1(df, year_value)

@app.callback(Output("other_plot", "figure"),
              [Input("dd_song_p3", "value")])
def update_historical_plot(attribute_value):
    return generate_adv_analytic_2(df, attribute_value)


@app.callback(Output('offensiveWordsPlot', 'figure'),
              [Input('ddOffensiveWords', 'value')])
def update_output_div(input_value):
    return create_offensive_words_plot(dict_offensive_words, input_value)


@app.callback(Output('firstAppearance', 'figure'),
              [Input('ddWordSearch', 'value')])
def update_output_div(input_value):
    return create_search_words_plot(df_merged_have_lyrics, input_value)


@app.callback([Output("tab_id_1", "style"),
               Output("tab_id_2", "style"),
               Output("tab_id_3", "style"),
               Output("tab_id_4", "style")],
              [Input("tabs", "value")])
def display_content(tab_value):
    style_update = {}
    style_hidden = {"display":"none"}

    if tab_value ==1:
        return style_update, style_hidden, style_hidden, style_hidden
    if tab_value ==2:
        return style_hidden, style_update, style_hidden, style_hidden
    if tab_value ==3:
        return style_hidden, style_hidden, style_update, style_hidden
    if tab_value ==4:
        return style_hidden, style_hidden, style_hidden, style_update

if __name__ == '__main__':
    app.run_server(debug=True)

