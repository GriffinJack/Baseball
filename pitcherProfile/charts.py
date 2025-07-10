import pandas as pd
import pybaseball as pyball
import matplotlib.pyplot as plt
from PIL.ImageChops import constant
from matplotlib.patches import Patch,Rectangle
import seaborn as sns
import pbp_data_prep as pbp
from constants import pitch_colors


def plot_pitchDist(data, count = "All"):
    data = pbp.count_filter(pbp_data=data, counts=count)
    batter_splits = [pbp.pitch_sums(data, stand='L'), pbp.pitch_sums(data, stand='R')]

    last, first = data.player_name.iloc[0].split(', ')

    titles = ['Pitch Distribution vs LHB', 'Pitch Distributions vs RHB']

    # change font for fun
    plt.rcParams['font.family'] = 'Arial'

    fig, axes = plt.subplots(1, 2, figsize=(14, 7))

    for ax, pitch_data, title in zip(axes, batter_splits, titles):
        labels = list(pitch_data.keys())
        colours = [pitch_colors.get(pitch, pitch_colors) for pitch in labels]

        ax.pie(
            pitch_data.values(),
            startangle=140,
            autopct=lambda pct: pbp.autopct_threshold(pct, threshold=3),
            labeldistance=1.1,
            colors=colours,
            pctdistance=0.75,
            wedgeprops=dict(width=0.5),
            shadow=True
        )
        ax.set_title(title, fontsize=14, fontweight='bold')

    # Display count
    fig.text(
        0.5,
        0.88,
        f"{count} counts",
        ha='center',
        fontsize=18,
        fontweight='bold'
    )

    # Get all unique pitch types used across both LHB and RHB
    all_pitches = set(batter_splits[0].keys()) | set(batter_splits[1].keys())
    legend_elements = [
        Patch(facecolor=pitch_colors.get(pitch, pitch_colors), label=pitch)
        for pitch in all_pitches
    ]

    # Add the legend to the figure (not one of the axes)
    fig.legend(
        handles=legend_elements,
        loc='lower center',
        ncol=4,
        fontsize=12,
        frameon=False
    )

    main_title = f'{first} {last} - Pitch Usage vs LHB & RHB'
    fig.suptitle(main_title, fontsize=24, fontweight='bold')
    plt.show()

def plot_velo(data):
    plt.figure(figsize=(10, 6))
    last, first = data.player_name.iloc[0].split(', ')
    #order pitches by avg velo
    order = data.groupby('pitch_name')['release_speed'].mean().sort_values(ascending=False).index.tolist()

    sns.violinplot(
        data = data,
        y = 'pitch_name',
        x = 'release_speed',
        hue = 'pitch_name',
        palette = pitch_colors,
        legend = False,
        order = order,
        cut = 0,
        density_norm='area'
    )

    plt.title(f'{first} {last} - Velocity Distribution', fontsize=20, fontweight='bold' )
    plt.ylabel('Pitch Type')
    plt.xlabel('MPH')
    plt.grid(axis='y', alpha=0.3)

    plt.show()


if __name__ == '__main__':

    first = "Paul"
    last = "Skenes"

    start = '2025-03-20'
    end = '2025-9-30'

    pbp_data = pbp.get_pbp(first, last, start, end)
    plot_pitchDist(pbp_data, "Behind")