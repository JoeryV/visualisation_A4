import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from functions import *
import load_data
from copy import copy

speedup = True
vertical = True

# df_small = load_data.load_small_full_file()
# current_song = df_small.loc[df_small["Title"] == "Bohemian Rhapsody"] #TODO song has to be automatically updated based off the user's behaviour
# audio_sample_url = get_track_sample(current_song)

top_2000_img = html.Img(
    src='https://www.nporadio2.nl/templates/radio2/images/top2000/logo.png',
    className='one columns',
    style={
        'height': '15%',
        'width': '90%',
        'float': 'left',},
)

tabs = dcc.Tabs(
    id='tabs',
    children=
    [
        dcc.Tab(label='Pick your song', value=1),
        dcc.Tab(label='Fun Facts', value=2),
        dcc.Tab(label='Advanced analytics', value=3),
        dcc.Tab(label='Lyrics analysis', value=4),
    ],
    value=1,
    vertical=vertical,
    style=tab_style(vertical),
    className='custom-tabs-container'
)

# fun_facts_page = html.Div([
#                     html.Div([
#                         Header(),
#
#                         html.Div([
#
#                             html.Div([
#                                 get_subheader(title="Best artist", size=4, className="gs-header gs-text-header"),
#
#                                 html.Div([
#                                     html.H3(df_small.Artist.value_counts().index[0]),
#                                     html.Img(src='https://logonoid.com/images/thumbs/the-beatles-logo.png', height='40',
#                                              width='160'),
#                                 ],
#                                 className="six columns"),
#
#                                 html.H1(str(df_small.Artist.value_counts()[0])),
#                                 html.P("Times")
#                             ], className = "six columns"),
#
#                             html.Div([
#                                 get_subheader(title="Most on number 1", size=4, className="gs-header gs-text-header"),
#
#                                 html.H3(df_small.iloc[(df_small.iloc[:,4:24]==1).sum(axis=1).index[0]].Title + " - " + df_small.iloc[(df_small.iloc[:,4:24]==1).sum(axis=1).index[0]].Artist),
#                                 html.Img(src='https://upload.wikimedia.org/wikipedia/commons/b/bd/Bohemian_Rhapsody_by_Queen_US_vinyl_red_label.png', height='160', width='160'),
#                                 html.H1(str((df_small.iloc[:,4:24]==1).sum(axis=1)[0])),
#                                 html.P("Times")
#                                 ], className = "six columns"),
#                             ], className = "row "),
#
#                             html.Div([
#                                 html.Div([
#                                     get_subheader(title="Highest climber", size=4,
#                                                   className="gs-header gs-text-header"),
#
#                                     html.H3(df_small.iloc[df_small.iloc[:,4:24][(df_small.iloc[:,4:24].diff(axis=1) == df_small.iloc[:,4:24].diff(axis=1).min().min()).sum(axis=1)>0].index].Artist + "-" + df_small.iloc[df_small.iloc[:,4:24][(df_small.iloc[:,4:24].diff(axis=1) == df_small.iloc[:,4:24].diff(axis=1).min().min()).sum(axis=1)>0].index].Title),
#                                     html.Img(src='https://upload.wikimedia.org/wikipedia/it/a/a9/Adele%2C_Someone_Like_You_%28Jake_Nava%29.png', height='160', width='160'),
#                                     html.H2(str(int(abs(df_small.iloc[:,4:24].diff(axis=1).min().min())))),
#                                     html.P("Places")
#                                     ], className = "six columns"),
#
#                                 html.Div([
#                                     get_subheader(title="Biggest loser", size=4,
#                                                   className="gs-header gs-text-header"),
#
#                                     html.H3(df_small.iloc[df_small.iloc[:,4:24][(df_small.iloc[:,4:24].diff(axis=1) == df_small.iloc[:,4:24].diff(axis=1).max().max()).sum(axis=1)>0].index].Artist + "-" + df_small.iloc[df_small.iloc[:,4:24][(df_small.iloc[:,4:24].diff(axis=1) == df_small.iloc[:,4:24].diff(axis=1).max().max()).sum(axis=1)>0].index].Title),
#                                     html.Img(src='https://img.cdandlp.com/2018/04/imgL/119125064.png', height='160', width='160'),
#                                     html.H2(str(int(abs(df_small.iloc[:,4:24].diff(axis=1).max().max())))),
#                                     html.P("Places")
#                                     ], className = "six columns"),
#                                 ], className = "row ")
#
#                         ]),
#                 ], className="twelve columns")
#
# advanced_page = html.Div([
#     html.H3('Tab content 3'),
#     dcc.Graph(id='historical_plot', figure=generate_adv_analytic_1(df_small)),
#     dcc.Graph(id='other_plot', figure=generate_adv_analytic_2(df_small))
# ])
#
# if speedup == False:
#     df_lyrics = load_data.load_df_lyrics()
#     print('still loading data,  takes a while')
#     # df_lyrics_filtered = copy(df_lyrics)
#     df_audio_analysis = load_data.load_df_audio_analysis_feats()
#
#     markdown_text = '''## How many words sangs in each song title?
#     In this graph you can see that for each artist how many words are used in a song lyric. It excludes stopwords
#     '''
#
#     lyrics_page = html.Div([
#         dcc.Markdown(children=markdown_text),
#         dcc.Graph(
#             id='word-count-vs-year-all',
#             figure={
#                 'data': [
#                     go.Scatter(
#                         y=df_lyrics[df_lyrics['Artist'] == i]['lyrics_word_count'],
#                         x=df_lyrics[df_lyrics['Artist'] == i]['Year'],
#                         text=df_lyrics[df_lyrics['Artist'] == i]['Title'],
#                         mode='markers',
#                         opacity=0.6,
#                         marker={
#                             'size': 10,
#                             'line': {'width': 0.5, 'color': 'white'}
#                         },
#                         name=i
#                     ) for i in sorted(df_lyrics.Artist.unique())
#                 ],
#                 'layout': go.Layout(
#                     yaxis={'type': 'log', 'title': 'number of words in song'},
#                     xaxis={'title': 'song release year'},
#                     margin={'l': 100, 'b': 40, 't': 10, 'r': 10},
#                     legend={'x': 1, 'y': 1},
#                     hovermode='closest'
#                 )
#             }
#         ),
#     ])
#     landing_page_1 = html.Div([
#         html.H3('Takes a milly times to render'),
#         dcc.Graph(id='Vincent_plot', figure=update_plots(df_audio_analysis)),
#     ])
#
#
#
#
#
# landing_page_2 = html.Div([
#     Header("Pick your song", 3),
#
#     html.Div([
#         html.Div([html.H6(children="Song: ")], style={"padding": "20 0 0 100"}, className="one columns"),
#
#         html.Div([
#             dcc.Dropdown(
#                 id="dd_song",
#                 options=create_dd_options(df_small['Title']), #TODO use this as input for the songName id
#                 value=current_song,
#                 multi=True,
#                 style={"width": "80%"},
#                 ),
#         ],
#                  className="eleven columns"),
#
#
#     ], className="row"),
#
#     # html.Div(id="hidden_df_p1", style={'display': 'none'})),
#
#     html.Div([
#         html.Div([
#             get_subheader('Play Track Sample', size=4, className="gs-header gs-text-header"),
#
#             html.Div([
#                 html.Img(src=current_song["album_image"],
#                          style={
#                              'height': '30%',
#                              'width': '30%',
#                              'float': 'left',
#                          },
#                          className='twelve columns'
#                          ),
#
#                 html.H5(id="songName",
#                         children='{} - {}'.format(current_song['Title'], current_song['Artist']),
#                         className='seven columns'),
#
#                 html.A(
#                     id="playButton",
#                     href=audio_sample_url,
#                     children=html.Img(src="http://pluspng.com/img-png/play-button-png-play-button-png-picture-1024.png",
#                                       style={
#                                           "height": "100%",
#                                           "width": "100%",
#                                           "float": "left",
#                                       }),
#                     target="_blank",
#                     style={"margin": "0 0 0 100"},
#                     className="two columns"
#                 ),
#
#                 html.H4(id="song duration",
#                         children="{}:{}".format(int(current_song["duration_ms"] / 1000 / 60 // 1),
#                                                   int(current_song["duration_ms"] / 1000 / 60 % 1 * 60)),
#                         className="two columns",
#                         style={"position": "relative",
#                                "bottom": "0"}
#                         ),
#             ], className="row")
#
#         ], className="six columns"),
#
#         html.Div([
#             get_subheader("Text", size=4, className="gs-header gs-text-header"),
#             html.Div([
#                 dcc.Markdown('{}'.format('Placeholder text ' *20))
#                 ], style={"margin": "0 0 0 30"})
#         ], className='six columns',
#         ),
#
#     ], className='row twelve columns'),
#
#
# ])
