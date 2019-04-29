import plotly.graph_objs as go
import dash_html_components as html

from time_series import get_source, get_values, get_time_series_layout_params


def tab_style(vertical=True):
    if vertical:
        style = {
            'width': '19.9vw',
            'textAlign': 'left',
            'float': 'left',
            # "border": "2px dashed lightgreen",
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

def generate_year_options(df, col='Year'):
    years = df[col].astype(int)
    # year_range = list(range(years.min(), years.max()+1, 10)) + [2018]
    year_range = list([1924] + list(range(1930, 2020, 10)) + [2018])
    year_range = ['1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006',
                  '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014',
                  '2015', '2016', '2017', '2018']
    year_dict = {year: year for year in year_range}
    return year_dict


# Casper functions
def generate_adv_analytic_1(df):
    years = [str(i) for i in range(1999,2019)]
    data = [go.Bar(visible=False,
                 name = 'Year = '+str(year),
                x = list(df[df[year] > 0].Year.value_counts()[df[df[year] > 0].Year.value_counts()>1].index),
                y = list(df[df[year] > 0].Year.value_counts()[df[df[year] > 0].Year.value_counts()>1].values)
                    ) for year in years]
    data[19]['visible'] = True

    steps = []
    for i in range(len(data)):
        step = dict( method = 'restyle',  args = ['visible', [False] * len(data)],  label= i+1999 )
        step['args'][1][i] = True # Toggle i'th trace to "visible"
        steps.append(step)

    sliders = [dict( active = 19, currentvalue = {"prefix": "Year: "}, pad = {"t": 50}, steps = steps )]
    layout = go.Layout(sliders=sliders,  xaxis=dict(range=[1938,2020]), yaxis=dict(range=[0,100]), title='Number of songs per Publication Year')
    fig = dict(data=data, layout=layout)
    return(fig)

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

    layout = dict(title='Publication year averages', showlegend=False,
                  updatemenus=updatemenus)

    fig = dict(data=data, layout=layout)
    return (fig)


# Vincent functions
#TODO vincent's functions need to be updated by song (radar), song & years (rank_plot), song & attribute & years
# (attribute vs time), additionally it should work with comparing multiple songs
def create_attributePlot(df, song, attribute):
    '''Function updates the attribute vs time plot on the first page of the dashboard'''
    song = song[0]
    idx = df.index[df['Title'] == song].tolist()[0]
    source = get_source(attribute)
    print(idx, attribute, source)
    y_vals, time = get_values(df, idx, source, attribute)


    data = []
    attribute_trace = go.Scatter(
        x = time,
        y = y_vals
    )
    data.append(attribute_trace)
    layout = go.Layout(
        title="{} vs. Time".format(attribute.capitalize()),
        paper_bgcolor='#FAFAFA',
        plot_bgcolor='#FAFAFA'
    )
    fig = go.Figure(data=data, layout=layout)
    return fig


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
        # margin=
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


# spotify functions
import spotipy
import spotipy.util as util
import token_files as tf

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
