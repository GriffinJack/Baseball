import pandas as pd
import pybaseball as pyball
import matplotlib.pyplot as plt
from matplotlib.patches import Patch,Rectangle
import seaborn as sns
import pbp_data_prep as pbp
from constants import pitch_colors


def plot_pitchDist(data, count):
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

if __name__ == '__main__':

    first = "Jordan"
    last = "Romano"

    start = '2025-03-20'
    end = '2025-9-30'

    pbp_data = pbp.get_pbp(first, last, start, end)
    plot_pitchDist(pbp_data, "Ahead")