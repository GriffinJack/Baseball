import pybaseball as pyball
import pandas as pd
import os

from pandas.core.interchange.dataframe_protocol import DataFrame


def get_pbp(first, last, start, end):
    filename = f"data/{last}_{first}_{start}_{end}.csv"

    #avoid necessary api calls
    if os.path.exists(filename):
        print("Loading cached data...")
        return pd.read_csv(filename)

    #Get Player ID
    player_id = int(pyball.playerid_lookup(last, first)['key_mlbam'].values[0])

    #Get pitch by pitch data
    pbp_data = pyball.statcast_pitcher(start, end, player_id)

    #Regular Season games only!
    pbp_data = pbp_data[pbp_data['game_type'] == 'R']
    pbp_data['count'] = pbp_data['balls'].astype(str) + '-' + pbp_data['strikes'].astype(str)


    print("Pulling data from API...")
    pbp_data.to_csv(filename, index=False)
    return pbp_data



#Filter data based on count
def count_filter(pbp_data, counts):
    #Count filters, can change later if needed.
    count_filters = {
    'Behind' : ['1-0', '2-0', '3-1', '3-0', '2-1'],
    'Ahead': ['1-2', '0-2', '0-1'],
    'Even' : ['0-0', '1-1', '2-2']
    }
    if counts == 'All':
        return pbp_data
    elif counts in count_filters:
        return pbp_data[pbp_data['count'].isin(count_filters[counts])]
    else:
        return pbp_data[pbp_data['count'] == counts]


def autopct_threshold(pct, threshold=2):
    return f'{pct:.1f}%' if pct > threshold else ''

def pitch_sums(pbp_data, stand = None):
    if stand is not None:
        pbp_data = pbp_data[pbp_data['stand'] == stand]
    return pbp_data['pitch_name'].value_counts().to_dict()


if __name__ == '__main__':

    first = "Paul"
    last = "Skenes"

    start = '2025-03-20'
    end = '2025-9-30'

    data = get_pbp(first, last, start, end)
    count_filter(data, "Behind")