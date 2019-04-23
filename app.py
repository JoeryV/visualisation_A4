'''
Notes

* Turning everything into the same style
* Making sure the advanced analytics page and lyrics page are interactive
* In order to make things interactive we need to enable the callback within the same page
* Filters on genre, artist, year (top2000)

CSS in Dash: https://dash.plot.ly/external-resources
'''

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import elements

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.scripts.config.serve_locally = True
app.title = "Top 2000"
vertical = True

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


if vertical:
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
                                # "border": "2px dashed blue",
                                "margin": "0 0 0 0",
                                "clear": "both"
                            },
                            className="row one columns",
                        ),

                        html.Div([
                            html.H6(['Genre'], style={"margin":"1rem 0 0 0"}),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Korean Pop', 'value': 'KPOP'},
                                    {'label': 'Pop', 'value': 'POP'},
                                    {'label': 'Hip-Hop', 'value': 'HipHop'}
                                ],
                                value='HipHop',
                                multi=True,
                                style={
                                    "margin": "0 0 0 0",
                                    "width": "100%",
                                       },
                            ),

                            html.H6(['Artist'], style={"margin":"1rem 0 0 0"}),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Korean Pop', 'value': 'KPOP'},
                                    {'label': 'Pop', 'value': 'POP'},
                                    {'label': 'Hip-Hop', 'value': 'HipHop'}
                                ],
                                value='HipHop',
                                multi=True,
                                style={
                                    "margin": "0 0 0 0",
                                    "width": "100%",
                                },
                            ),

                            html.H6(['Top2000 Year'], style={"margin":"1rem 0 0 0"}),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Korean Pop', 'value': 'KPOP'},
                                    {'label': 'Pop', 'value': 'POP'},
                                    {'label': 'Hip-Hop', 'value': 'HipHop'}
                                ],
                                value='HipHop',
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
                                # "border": "2px dashed blue",
                                "margin": "0 0 75px 0",
                                "position": "fixed",
                                "bottom" : "10",
                                # "left":"0",
                                },
                            className="row one columns")

                    ], style={
                        'borderRight': 'thin lightgrey solid',
                        'height':'100vh'}
                    )

                ],
                style={'width': '20vw',
                       'float': 'left',
                       # "border": "2px solid green",
                       },
                className="two columns",
            ),

            # component which contains the 'tab output' aka the actual content
            html.Div(
                [
                    html.Div(id='tab-output'),
                ],
                style={'width': '78vw',
                       'float': 'right',
                       }
            ),

            # hidden component to store data
            html.Div(id='_filtered_df_stored', style={'display': 'none'}),
        ],
        # className='offsets-dis-by-one column',
        style={
            'fontFamily': 'Sans-Serif',
            'margin-left': '10px',
            'margin-right': 'auto',
        }
    )
else:
    app.layout = html.Div(
        [
            html.H1('Dash Tabs component demo'),
            dcc.Tabs(id="tabs", value=1,
                     children=[
                         dcc.Tab(label='Currently playing', value=1),
                         dcc.Tab(label='Fun Facts', value=2),
                         dcc.Tab(label='Advanced analytics', value=3),
                         dcc.Tab(label='Lyrics analysis', value=4),
                     ],
                     vertical=vertical,
                     style=tab_style(vertical),
                     ),
            html.Div(id='tab-output', style={"margin-left": "50px"}),
        ]
    )

@app.callback(Output('tab-output', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 1:
        # return placeholder
        return elements.landing_page
    elif tab == 2:
        return elements.fun_facts_page
    elif tab == 3:
        return elements.advanced_page
    elif tab == 4:
        # return placeholder
        return elements.lyrics_page


if __name__ == '__main__':
    app.run_server(debug=True)