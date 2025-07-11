import pandas as pd
import pybaseball as pyball
import matplotlib.pyplot as plt
from IPython.core.pylabtools import figsize
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

def movement_profile(data):
    plt.rcParams['font.family'] = 'Arial'
    plt.figure(figsize=(6.5,6.5))

    ax = plt.gca()

    last, first = data.player_name.iloc[0].split(', ')

    for spine in ax.spines.values():
        spine.set_visible(False)

    # Add concentric rings
    for radius in [0.5, 1.0, 1.5, 2.0, 2.5]:
        circle = plt.Circle(
            (0, 0),
            radius,
            color='gray',
            fill=False,
            linestyle='dotted',
            linewidth=0.8,
            alpha=0.4,
            zorder=0
        )
        ax.add_patch(circle)

    sns.scatterplot(
        data=data,
        x='pfx_x',
        y='pfx_z',
        hue='pitch_name',
        palette=pitch_colors,
        s=50,
        edgecolor='black'
    )

    plt.title(first + ' ' + last + ' - Movement Profile',
              fontsize=20,
              fontweight='bold',
              pad=20)

    # Center axis
    plt.axhline(0, color='gray', linestyle='--', linewidth=1)
    plt.axvline(0, color='gray', linestyle='--', linewidth=1)
    plt.xlim(-2.5, 2.5)
    plt.ylim(-2.5, 2.5)
    plt.gca().set_aspect('equal', adjustable='box')
    ax.get_legend().remove()

    plt.show()


def pitch_sample(data, sample_size = 100):
    sample_data = data.sample(n=sample_size, random_state=42)

    fig, ax = plt.subplots(figsize = (6,6))

    strike_zone = Rectangle((-0.95, 1.5), 1.9, 2.0, linewidth=1.5, edgecolor='black', facecolor='none')

    sns.scatterplot(
        data=sample_data,
        x='plate_x',
        y='plate_z',
        hue='pitch_name',
        palette=pitch_colors,
        s=50,
        edgecolor='black'
    )

    last, first = data.player_name.iloc[0].split(', ')
    plt.title(f"{first} {last} - {sample_size} Pitch Sample", fontsize=20, fontweight='bold')

    ax.add_patch(strike_zone)
    ax.set_xlim(-4.5, 4.5)
    ax.set_ylim(-2, 6.25)
    ax.set_aspect('equal')
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.get_legend().remove()

    plt.show()



if __name__ == '__main__':

    first = "Paul"
    last = "Skenes"

    start = '2025-03-20'
    end = '2025-9-30'

    pbp_data = pbp.get_pbp(first, last, start, end)
    pitch_sample(pbp_data)