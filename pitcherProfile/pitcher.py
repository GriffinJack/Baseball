import pandas as pd
import pybaseball as pyball
import matplotlib.pyplot as plt
from matplotlib.patches import Patch,Rectangle
import seaborn as sns
import pbp_data_prep as pbp
from constants import pitch_colors
import os


class Pitcher:

    def __init__(self, first, last, start, end):
        self.first = first
        self.last = last
        self.start = start
        self.end = end
        self.data = self.load_data()
        self.filtered_data = None
        self.active_filter = None

    def load_data(self):
        filename = f"data/{self.last}_{self.first}_{self.start}_{self.end}.csv"

        # avoid necessary api calls
        if os.path.exists(filename):
            print("Loading cached data...")
            return pd.read_csv(filename)

        # Get Player ID
        player_id = int(pyball.playerid_lookup(self.last, self.first)['key_mlbam'].values[0])

        # Get pitch by pitch data
        pbp_data = pyball.statcast_pitcher(self.start, self.end, player_id)

        # Regular Season games only!
        pbp_data = pbp_data[pbp_data['game_type'] == 'R']
        pbp_data['count'] = pbp_data['balls'].astype(str) + '-' + pbp_data['strikes'].astype(str)

        print("Pulling data from API...")
        pbp_data.to_csv(filename, index=False)
        return pbp_data

    def count_filter(self, counts="All"):

        count_filters = {
            'Behind': ['1-0', '2-0', '3-1', '3-0', '2-1'],
            'Ahead': ['1-2', '0-2', '0-1'],
            'Even': ['0-0', '1-1', '2-2']
        }
        self.active_filter = counts
        if counts == 'All':
            self.filtered_data = None
            self.active_filter = None
        elif counts in count_filters:
            self.filtered_data = self.data[self.data['count'].isin(count_filters[counts])]
        else:
            self.filtered_data =  self.data[self.data['count'] == counts]
        return self

    def pitch_dist(self, use_filter = False):
        if use_filter and self.filtered_data is not None:
            data = self.filtered_data
        else:
            data = self.data

        batter_splits = [pbp.pitch_sums(data, stand='L'), pbp.pitch_sums(data, stand='R')]
        count = self.active_filter if self.active_filter is not None else "All"

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

        main_title = f'{self.first} {self.last} - Pitch Usage vs LHB & RHB'
        fig.suptitle(main_title, fontsize=24, fontweight='bold')

        plt.savefig("static/images/pitch_dist.png", dpi=100, bbox_inches="tight")
        plt.close()

    def velo(self, use_filter = False):

        if use_filter and self.filtered_data is not None:
            data = self.filtered_data
        else:
            data = self.data

        plt.figure(figsize=(10, 6))

        # order pitches by avg velo
        order = data.groupby('pitch_name')['release_speed'].mean().sort_values(ascending=False).index.tolist()

        sns.violinplot(
            data=data,
            y='pitch_name',
            x='release_speed',
            hue='pitch_name',
            palette=pitch_colors,
            legend=False,
            order=order,
            cut=0,
            density_norm='area'
        )

        plt.title(f'{self.first} {self.last} - Velocity Distribution', fontsize=20, fontweight='bold')
        plt.ylabel('Pitch Type')
        plt.xlabel('MPH')
        plt.grid(axis='y', alpha=0.3)

        plt.savefig("static/images/velo.png", dpi=100, bbox_inches="tight")
        plt.close()

    def movement_profile(self, use_filter = False):

        if use_filter and self.filtered_data is not None:
            data = self.filtered_data
        else:
            data = self.data

        plt.rcParams['font.family'] = 'Arial'
        plt.figure(figsize=(6.5, 6.5))

        ax = plt.gca()

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

        plt.title(f"{self.first}  {self.last} - Movement Profile",
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

        plt.savefig("static/images/movement_profile.png", dpi=100, bbox_inches="tight")
        plt.close()

    def pitch_sample(self, use_filter = False ,sample_size=100):

        if use_filter and self.filtered_data is not None:
            data = self.filtered_data
        else:
            data = self.data

        sample_data = data.sample(n=sample_size, random_state=42)

        fig, ax = plt.subplots(figsize=(6, 6))

        avg_sz_top = data['sz_top'].mean()
        avg_sz_bot = data['sz_bot'].mean()

        strike_zone = Rectangle(
            (-0.97, 1.5),
            1.94,
            2.0,
            linewidth=1.5,
            edgecolor='black',
            facecolor='none'
        )

        sns.scatterplot(
            data=sample_data,
            x='plate_x',
            y='plate_z',
            hue='pitch_name',
            palette=pitch_colors,
            s=100,
            edgecolor='black'
        )

        plt.title(f"{self.first} {self.last} - {sample_size} Pitch Sample", fontsize=20, fontweight='bold')

        ax.add_patch(strike_zone)
        ax.set_xlim(-3, 3)
        ax.set_ylim(-1, 5)
        ax.set_aspect('equal')
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.get_legend().remove()

        plt.savefig("static/images/pitch_sample.png", dpi=100, bbox_inches="tight")
        plt.close()

if __name__ == '__main__':

    first = "Kevin"
    last = "Gausman"

    start = '2025-03-20'
    end = '2025-9-30'

    gausman = Pitcher(first, last, start, end)
    gausman.count_filter("Ahead")
    gausman.pitch_dist(use_filter=True)
    gausman.velo()
    gausman.movement_profile()
    gausman.pitch_sample()