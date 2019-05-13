import dash_core_components as dcc
from Code.functions import *

speedup = True
vertical = True

# df_small = load_data.load_small_full_file()
# current_song = df_small.loc[df_small["Title"] == "Bohemian Rhapsody"]
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
        dcc.Tab(label='Pick your song', value=1     ), #style={"font-size": "20px"}),
        dcc.Tab(label='Fun Facts', value=2          ), #style={"font-size": "20px"}),
        dcc.Tab(label='Advanced analytics', value=3 ), #),
        dcc.Tab(label='Lyrics analysis', value=4    ), #),
    ],
    value=1,
    vertical=vertical,
    style=tab_style(vertical),
    className='custom-tabs-container'
)



