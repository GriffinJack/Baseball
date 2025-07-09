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
    hitters_count = ['1-0', '2-0', '3-1', '3-0']
    pitchers_count = ['1-2', '0-2']
    even_count = ['0-0', '1-1']

    print("hello")
    if counts == 'All':
        return pbp_data
    elif counts == 'Ahead':
        return pbp_data[pbp_data['count'].isin(pitchers_count)]
    elif counts == 'Behind':
        return pbp_data[pbp_data['count'].isin(hitters_count)]
    elif counts == 'Even':
        return pbp_data[pbp_data['count'].isin(even_count)]
    else:
        return pbp_data[pbp_data['count'] == counts]


