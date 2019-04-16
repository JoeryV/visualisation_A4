'''
Notes

I am still finding out why the buttons do not fill the entire div that they are contained in.
Next step: look at Dash HTML code


CSS in Dash: https://dash.plot.ly/external-resources
'''


import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.scripts.config.serve_locally = True
vertical = True


def tab_style(vertical):
    if vertical:
        style = {
            'height': '100vh',
            'width': '18vw',
            'borderRight': 'thin lightgrey solid',
            'textAlign': 'left',
            'float': 'left',
            # "border": "2px dashed lightgreen",
                 }
    else:
        style = {'width': '100vh'}
    return style


# @app.callback([Output('tab_id_1', 'style'),
#                Output('tab_id_2', 'style'),
#                Output('tab_id_3', 'style')],
#               [Input('tabs', 'value')])
# def display_content(tab_value):
#     print(tab_value)
#     style_update = {}
#     style_hidden = {
#         "display":"none",
#         # "border": "5px solid blue",
#     }
#
#     if tab_value ==1:
#         return style_update, style_hidden, style_hidden
#     if tab_value ==2:
#         return style_hidden, style_update, style_hidden
#     if tab_value ==3:
#         return style_hidden, style_hidden, style_update



if vertical:
    app.layout = html.Div(
        [
            html.Div(
                [
                    # JADS image
                    html.Div([
                        html.Img(
                            src='https://www.nporadio2.nl/templates/radio2/images/top2000/logo.png',
                            #"https://www.bigdata-alliance.org/wp-content/uploads/2017/02/JADS_logo_100_RGB_fc_CS6.png",
                            className='one columns',
                            style={
                                'height': '15%',
                                'width': '90%',
                                'float': 'left',
                                # 'position': 'relative',
                                # "border": "2px solid red",
                                # "clearfix": {"after": {"content": "","clear": "both", "display": "table",}},
                            },
                        ),
                    ]),

                    # Tabs element
                    html.Div(
                        [
                            dcc.Tabs(
                                id='tabs',
                                children=
                                [
                                    dcc.Tab(label='Currently playing',  value=1),
                                    dcc.Tab(label='Fun Facts',          value=2),
                                    dcc.Tab(label='Advanced analytics', value=3),
                                    dcc.Tab(label='Lyrics analysis',    value=4),
                                ],
                                value=1,
                                vertical=vertical,
                                style=tab_style(vertical),
                                className='custom-tabs-container'
                            ),
                        ],
                        style={
                            "float": "left",
                            "width":"100vw",
                            # "border": "2px dashed blue",
                            "margin": "0 0 0 0",
                        },
                        className="one columns",
                    ),
                ],
                style={'width': '20vw',
                       'float': 'left',
                       # "border": "2px solid green",
                       },
                className="two columns",
            ),

            # add the tabs to the dashboard as children
            html.Div(
                [
                    html.Div(id='tab-output'),
                ],
                style={'width': '75vw',
                       'float': 'right',
                       }
            ),

            # hidden component to store data
            html.Div(id='_filtered_df_stored', style={'display': 'none'}),
        ],
        style={
            'fontFamily': 'Sans-Serif',
            'margin-left': 'auto',
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
        return html.Div([
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
    elif tab == 2:
        return html.Div([
            html.H3('Tab content 2'),
            dcc.Graph(
                id='graph-2-tabs',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [5, 10, 6],
                        'type': 'bar'
                    }]
                }
            )
        ])


if __name__ == '__main__':
    app.run_server(debug=True)