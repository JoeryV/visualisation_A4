'''
Notes

* Turning everything into the same style
* Making sure the advanced analytics page and lyrics page are interactive
* In order to make things interactive we need to enable the callback within the same page
* Filters on genre, artist, year (top2000)

CSS in Dash: https://dash.plot.ly/external-resources
'''

import dash
import elements
import load_data


import pandas as pd
import dash_core_components as dcc

from functions import *
from textwrap import dedent
# from flask_caching import Cache
from dash.dependencies import Input, Output


df = load_data.load_file_100()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.scripts.config.serve_locally = True

# cache = Cache(app.server, config={
#     'CACHE_TYPE': 'filesystem',
#     'CACHE_DIR': 'cache-directory'
# })
#

# global variables
app.title = "Top 2000"
vertical = True
attributes = ['tempo', 'key', 'mode', 'time_signature'] #TODO loadness start is not in the new df. Does Vincent want it? If so, add it in,
genre_options = create_dd_options(df['primary_genre'].dropna().unique())
genre_options.append({"label": "all genres", "value": "all genres"})

artist_options = create_dd_options(df["Artist"].dropna().unique())
artist_options.append({"label": "all artists", "value": "all artists"})

releaseYear_options = create_dd_options(df["Year"].dropna().unique())
releaseYear_options.append({"label": "all release years", "value": "all release years"})

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
                id="dd_song",
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
                id="yearRange",
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
                get_subheader(title="Best artist", size=4, className="gs-header gs-text-header"),

                # Subrow contains the image + name + amount of times won
                html.Div([
                    # Image of Best Artist
                    html.Img(
                        id="bestArtistImg",
                        src='https://logonoid.com/images/thumbs/the-beatles-logo.png',
                        # height='20%',
                        # width='20%',
                        style={"margin": "0 0 50px 0"},
                        className="two columns",
                    ),

                    # IN THE BELOW TWO DIV'S I HARDCODED THE STYLE (LAYOUT). Hope this works out for other songs
                    # Name of best artist
                    html.H2(id="bestArtistName", children=getBestArtistName(df), ##TODO have to create a callback for this
                            style={
                                "margin": "0 0 0 0",
                            #     "bottom": "30%",
                            #     "left": "30%",
                            #     "margin": "0 0 0 10",
                            #     "position": "absolute"
                                    },
                            className="ten columns",
                            ),

                    # The amount of times the artist has won
                    html.H2(id="bestArtistWon", children="won {} times".format(getBestArtistWon(df)), ##TODO have to create a callback for this
                            style={
                                "margin": "0 0 0 0",
                            #     "bottom": "0",
                            #     "left": "30%",
                            #     "margin": "0 0 0 0",
                            #     "position": "absolute"
                            },
                                className="ten columns",
                            ),
                ],
                    className="row",
                ),
            ], className="six columns"),

            # Contains the best scoring song
            html.Div([
                get_subheader(title="Overall best rated song", size=4, className="gs-header gs-text-header"),

                # subrow contains the best song info
                html.Div([
                    html.Img(id="bestSongImg",  # TODO create a callback to update this
                             src='https://upload.wikimedia.org/wikipedia/commons/b/bd/Bohemian_Rhapsody_by_Queen_US_vinyl_red_label.png',
                             # height='160', width='160',
                             style={"margin": "0 0 0 0"},
                             className="two columns",
                             ),
                    html.H2(getBestSongTitle(df) + " - " + getBestSongArtist(df),
                            style={"margin": "0 0 0 0"},
                            className="ten columns"),
                    html.H2("won {} times".format(getBestSongWon(df)),
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
                html.H3(df.iloc[df.iloc[:,4:24][(df.iloc[:,4:24].diff(axis=1) == df.iloc[:,4:24].diff(axis=1).min().min()).sum(axis=1)>0].index].Artist + "-" + df.iloc[df.iloc[:,4:24][(df.iloc[:,4:24].diff(axis=1) == df.iloc[:,4:24].diff(axis=1).min().min()).sum(axis=1)>0].index].Title),
                html.Img(src='https://upload.wikimedia.org/wikipedia/it/a/a9/Adele%2C_Someone_Like_You_%28Jake_Nava%29.png', height='160', width='160'),
                html.H2(str(int(abs(df.iloc[:,4:24].diff(axis=1).min().min())))),
                html.P("Places")
            ], className="six columns"),

            # Contains the biggest lost
            html.Div([
                get_subheader(title="Biggest loser", size=4, className="gs-header gs-text-header"),
                html.H3(df.iloc[df.iloc[:,4:24][(df.iloc[:,4:24].diff(axis=1) == df.iloc[:,4:24].diff(axis=1).max().max()).sum(axis=1)>0].index].Artist + "-" + df.iloc[df.iloc[:,4:24][(df.iloc[:,4:24].diff(axis=1) == df.iloc[:,4:24].diff(axis=1).max().max()).sum(axis=1)>0].index].Title),
                html.Img(src='https://img.cdandlp.com/2018/04/imgL/119125064.png', height='160', width='160'),
                html.H2(str(int(abs(df.iloc[:,4:24].diff(axis=1).max().max())))),
                html.P("Places")
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

    html.Div([
        dcc.Graph(id='historical_plot', figure=generate_adv_analytic_1(df)),# className="six columns"),
        dcc.Graph(id='other_plot', figure=generate_adv_analytic_2(df)),#  className="six columns")
    ], className='row')

],
    id="tab_id_3",
    style={'display':"none"}
)

p4 = html.Div([],
              id="tab_id_4",
              style={'display':"none"}
              )

# external_css = [
#     "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
#     "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",  # this one contains the headers
#     "//fonts.googleapis.com/css?family=Raleway:400,300,600",
#     "https://codepen.io/bcd/pen/KQrXdb.css",
#     "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"
# ]

# for css in external_css:
#     app.css.append_css({"external_url": css})
#
# external_js = [
#     "https://code.jquery.com/jquery-3.2.1.min.js",
#     "https://codepen.io/bcd/pen/YaXojL.js"
# ]
#
# for js in external_js:
#     app.scripts.append_script({"external_url": js})
#


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
                 # children=df.to_json(date_format='iso', orient="split"),
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
              [Input("dd_song", "value")])
def updateCurrentSong(song_title):
    current_song = df.loc[df["Title"] == song_title[0]]
    return current_song.to_json(date_format="iso", orient="split")


@app.callback(Output("albumImg", "src"),
              [Input("_current_song_stored", "children")])
def getAlbumImg(current_song):
    current_song = pd.read_json(current_song, orient="split")
    return current_song["album_image"].iloc[0]

@app.callback([Output("bestArtistImg", "src")], #TODO Have to update this based on the filtered df rather than the _current_song_stored
              [Input("_current_song_stored", "children")])
def getArtistImg(current_song):
    current_song = pd.read_json(current_song, orient="split")
    return current_song["artist_image"].iloc[0]


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
               Input("dd_song", "value"),
               Input("yearRange", "value"),
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
              [Input("dd_song", "value"),
               Input("dd_attribute", "value"),
               ])
def update_attributePlot(songname, attribute):
    '''Not using filtered df here so we can cut the size of that df.
    This one will always be based on the songname anyway '''
    return create_attributePlot(df, songname, attribute)



# app.callback(Output("_filtered_df_stored", "children"),
#             [Input("ddGenre", "value"),
#              Input("ddArtist", "value"),
#              Input("ddReleaseYear", "value")])
# def filter_on_df(genres, artists, release_years):
#     if 'all genres' in genres: genres = df['primary_genre'].unique()
#     if 'all artists' in artists: artists = df['Artist'].unique()
#     if 'all release years' in release_years: release_years = df['Year'].unique()
#
#     columns = df.columns
#     columns.remove('segments')
#     columns.remove('sections')
#     df = df[columns]
#     df = df.loc[df["primary_genre"].isin(genres)]
#     df = df.loc[df["Artist"].isin(artists)]
#     df = df.loc[df["Year"].isin(release_years)]
#     return df.to_json(date_format="iso", orient="split")



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

