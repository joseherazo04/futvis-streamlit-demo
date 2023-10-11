import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch
from scipy.ndimage import gaussian_filter

def juego_de_posicion(df):
    pitch = VerticalPitch(
        pitch_type='statsbomb', 
        line_zorder=2
        )

    fig, ax = pitch.draw(figsize=(6.6, 4.125))

    bin_statistic = pitch.bin_statistic_positional(
        df['y'], 
        df['x'], 
        statistic='count',
        positional='full', 
        normalize=True
        )

    pitch.heatmap_positional(
        bin_statistic, 
        ax=ax,
        edgecolors='gray',
        cmap='coolwarm'
        )

    labels = pitch.label_heatmap(
        bin_statistic, 
        color='black', 
        fontsize=9,
        ax=ax, 
        ha='center', 
        va='center',
        str_format='{:.0%}'
        )
    return fig

def three_zones_positioning(df, vertical_bins=3):
    pitch = VerticalPitch(
        pitch_type='statsbomb', 
        line_zorder=2
    )
    fig, ax = pitch.draw(figsize=(6.6, 4.125))

    bin_statistic = pitch.bin_statistic(
        df['y'], 
        df['x'], 
        statistic='count', 
        bins=(vertical_bins, 1), 
        normalize=True
        )

    pitch.heatmap(
        bin_statistic, 
        ax=ax, 
        cmap='coolwarm', 
        edgecolor='gray'
    )

    labels = pitch.label_heatmap(
        bin_statistic, 
        color='black', 
        fontsize=17,
        ax=ax, 
        ha='center', 
        va='center',
        str_format='{:.0%}')
    return fig

def position_heatmap_grids(df):
    pitch = VerticalPitch(
        pitch_type='statsbomb',
        line_zorder=2,
        line_color='#efefef'
    )

    fig, ax = pitch.draw(figsize=(6.6, 4.125))
    
    bin_statistic = pitch.bin_statistic(
        df['y'], 
        df['x'], 
        statistic='count', 
        normalize=True,
        bins=(32, 24))
    
    bin_statistic['statistic'] = gaussian_filter(bin_statistic['statistic'], 1)

    pcm = pitch.heatmap(
        bin_statistic, 
        ax=ax, 
        cmap='hot', 
        edgecolors='#22312b')
    
    return fig

def convexhull_plot(df):
    pitch = VerticalPitch()

    fig, ax = pitch.draw(figsize=(6.6, 4.125))
    hull = pitch.convexhull(
        df['y'], 
        df['x'])

    poly = pitch.polygon(
        hull, 
        ax=ax, 
        edgecolor='red', 
        facecolor='red', 
        alpha=0.3)

    scatter = pitch.scatter(
        df['y'], 
        df['x'], 
        ax=ax, 
        edgecolor='black', 
        facecolor='red'
        )
    return fig

def get_pos_by_min_plot(df):
    labels = [i for i in range(0,df['minute'].max() + 1)]
    att_points = df[df.zone_played=='attacking']['percentage'].to_list()
    mid_points = df[df.zone_played=='middle']['percentage'].to_list()
    def_points = df[df.zone_played=='defensive']['percentage'].to_list()

    mid_def_points = [x + y for x, y in zip(mid_points, def_points)]

    width = 0.6       # the width of the bars: can also be len(x) sequence

    fig, ax = plt.subplots(figsize=(8,3.125))

    ax.bar(labels, att_points, width, 
           label='attacking', bottom = mid_def_points, 
           edgecolor = "black", linewidth = 2, 
           color='blue')
    
    ax.bar(labels, mid_points, width, 
           label='middle', bottom = def_points, 
           edgecolor = "black", linewidth = 2)
    
    ax.bar(labels, def_points, width, 
           label='defensive', edgecolor = "black", 
           linewidth = 2, color='red')
    
    ax.legend(loc='upper right', bbox_to_anchor=(1.23, 1))
    ax.set_xlabel('minute')

    # Labels
    for bar in ax.patches:
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() / 2 + bar.get_y(),
                str(bar.get_height())+'%', ha = 'center',
                color = 'w', size = 9)

    return fig