import pandas as pd
import pybaseball as pyball


def get_pbp(first, last, start, end):

    #Get Player ID
    player_id = int(pyball.playerid_lookup(last, first)['key_mlbam'].values[0])

    #Get pitch by pitch data
    pbp_data = pyball.statcast_pitcher(start, end, player_id)

    #Regular Season games only!
    php_data = pbp_data[pbp_data['game_type'] == 'R']
    pbp_data['count'] = pbp_data['balls'].astype(str) + '-' + pbp_data['strikes'].astype(str)

    return pbp_data



#Filter data based on count
def count_filter(pbp_data, counts):
    #Count filters, can change later if needed.
    count_filters = {
    'Ahead' : ['1-0', '2-0', '3-1', '3-0'],
    'Behind': ['1-2', '0-2'],
    'Even' : ['0-0', '1-1']
    }
    print("hello")
    if counts == 'All':
        return pbp_data
    elif counts in count_filters:
        return pbp_data[pbp_data['count'].isin(count_filters[counts])]
    else:
        return pbp_data[pbp_data['count'] == counts]


def autopct_threshold(pct, threshold=2):
    return f'{pct:.1f}%' if pct > threshold else ''

def pitch_sums(pbp_data, stand = None):
    if stand is  not None:
        pitch_counts = pbp_data[pbp_data['stand'] == stand]
    return pbp_data['pitch_name'].value_counts().to_dict()


