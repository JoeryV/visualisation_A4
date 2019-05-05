def get_min_max(attr):
    """Returns the minimum and maximum for quantities being plotted
    
    Arguments:
        attr: the musical attribute being plotted, provided by the dropdown widget
        
    Returns:
        min: the min value for the y-axis
        max: the max value for the y-axis
    
    """
    MIN_MAX_DICT = {
        'loudness_start': {
            'max': 0,
            'min': -60
        },
        'tempo': {
            'min': 0,
            'max': 200
        },
        'key': {
            'min': "C",
            'max': 'B'
        },
        'mode': {
            'min': 'Minor',
            'max': 'Major',
        },
        'time_signature': {
            'min': 'Complex',
            'max': '7/4'
        }
    }
    
    return MIN_MAX_DICT[attr]['min'], MIN_MAX_DICT[attr]['max']

def get_source(attr):
    """Returns the source (column) to use for fetching values
    
    Arguments:
        attr: the musical attribute being plotted, provided by the dropdown widget
        
    Returns:
        a string representing a column in the dataframe
    
    """
    SOURCE_DICT = {
        'loudness_start': 'segments',
        'tempo': 'sections',
        'key': 'sections',
        'mode': 'sections',
        'time_signature': 'sections'
    }
    
    return SOURCE_DICT[attr]

def map_vals(y_vals, attr):
    """Used to map categorical values represented as numbers back to their category
    
    Arguments:
        y_vals: a List of ints
        attr: the musical attribute to be mapped
        
    Returns:
        y_vals: a List of strings
    
    """
    KEY_MAPPING = {
        -1: None,
        0: 'C',
        1: 'C#',
        2: 'D',
        3: 'D#',
        4: 'E',
        5: 'F',
        6: 'F#',
        7: 'G',
        8: 'G#',
        9: 'A',
        10: 'A#',
        11: 'B'
    }
    
    MODE_MAPPING = {
        -1: None,
        0: 'Minor',
        1: 'Major'
    }
    
    TIME_SIGNATURE_MAPPING = {
        -1: None,
        1: 'Complex',
        3: '3/4',
        4: '4/4',
        5: '5/4',
        6: '6/4',
        7: '7/4'
    }
    
    if attr == 'key':
        y_vals = [KEY_MAPPING[val] for val in y_vals]
    elif attr == 'mode':
        y_vals = [MODE_MAPPING[val] for val in y_vals]
    elif attr == 'time_signature':
        y_vals = [TIME_SIGNATURE_MAPPING[val] for val in y_vals]
    
    return y_vals

def get_values(df, idx, source, attr):
    """Fetches values from dataframe according to source and attribute
    
    Arguments:
        idx: the row index of the track, provided as an int
        source: which column to fetch values from, provided by the get_source function
        attr: the musical attribute we are plotting, provided by the dropdown widget
        
    Returns:
        y_vals: a List of values (string xor numerical) that may have been mapped
        time: a List of time values in seconds
    
    """
    vals = eval(df[source][idx])    
    y_vals, time = zip(*[(d[attr],d['start']) for d in vals])
    y_vals = map_vals(y_vals, attr)
    
    return y_vals, time

def get_time_series_layout_params(attr, xdomain=None, ydomain=None):
    """Used to format the axes of the time series according to the quantity being plotted
    
    Arguments:
        attr: 'string', the attribute being plotted, provided by the dropdown widget
        
    Returns:
        xaxis: a dictionary containing the title and domain (positioning) of the x-axis
        yaxis: a dictionary containing the title, range, and domain of the y-axis
    
    """
    min, max = get_min_max(attr)
    xaxis = {
        'title': 'Time (s)'
    }
    
    if xdomain is not None:
        xaxis['domain'] = xdomain
        
    yaxis = {
        'title': get_yaxis_label(attr),
        'range': [min, max]
    }
    
    if ydomain is not None:
        yaxis['domain'] = ydomain
    
    if attr in ('key', 'mode', 'time_signature'):
        yaxis['categoryorder'] = "category ascending"
        yaxis['type'] = 'category'
    
    return xaxis, yaxis

def get_yaxis_label(attr):
    """Returns the proper y-axis label for the attribute being plotted
    
    Arguments:
        attr: 'string', the attribute being plotted, provided by the dropdown widget
        
    Returns:
        A string representation of the quantity being plotted
        
    """
    if attr == 'loudness_start':
        return 'decibel (dB)'
    elif attr == 'tempo':
        return 'Beats per Minute (bpm)'
    elif attr == 'key':
        return 'Pitch'
    elif attr == 'mode':
        return 'Modality'
    elif attr == 'time_signature':
        return 'Time Signature (beats per measure)'