import streamlit as st
import pandas as pd
import utils.visuals as vs

@st.cache_data
def load_data(path='src/data.csv'):
    df =  pd.read_csv(path)

    df_count_by_zone = df.groupby(['zone_played','minute']).count()
    df_total_count = df.groupby(['minute']).count()

    df_positional = df_count_by_zone/df_total_count
    df_positional = (df_positional['y']*100).round(0).astype(int)
    df_positional = df_positional.reset_index()
    df_positional.columns = ['zone_played','minute','percentage']

    return df, df_positional

@st.cache_data
def load_video(path='src/video.mp4'):
    video_file = open('src/video.mp4', 'rb') 
    video_bytes = video_file.read() 
    return video_bytes

@st.cache_data
def get_position_vis(df):
    return vs.juego_de_posicion(df)

@st.cache_data
def get_heatmap_vis(df):
    return vs.position_heatmap_grids(df)

@st.cache_data
def get_convexhull_vis(df):
    return vs.convexhull_plot(df)

@st.cache_data
def get_three_part_vis(df):
    return vs.three_zones_positioning(df)

@st.cache_data
def get_pos_by_min(df):
    return vs.get_pos_by_min_plot(df)

df, df_pos = load_data()
total_mins = df['minute'].max() 

st.image('src/logo.png')
st.sidebar.write('## About')
st.sidebar.write(
    '''
    Hello everyone. I'm building FUTVIS, a platform for every soccer fan 
    to collect advanced statistics from their soccer match videos.
    ''')
st.sidebar.write(
    '''
    To play with this demo you just have to interact with the filters to choose different 
    periods of time, try it, and see how the visuals change.
    ''')
st.sidebar.write(
    '''
    At the bottom of the page, you have the original video match if you want to check 
    the source of the analysis.
    ''')
st.sidebar.write(
    '''
    This analysis was completely done by artificial intelligence, 
    if you are interested in trying this software please fill this form: 
    https://forms.gle/U8UeeTwrWiMjiUzZA
    ''')

st.title('Match analysis')
st.write('Advanced soccer video analysis')

st.divider()
st.markdown("### Filters")

minutes_range = st.slider(
    'Minute of match', 
    min_value=0, 
    max_value=total_mins, 
    value=(0,total_mins))

second = st.slider(
    'Second of minute ' + str(minutes_range[0]), 
    min_value=0, 
    max_value=59)

min_time_str = f'{str.zfill(str(minutes_range[0]),2)}:00 - {str.zfill(str(minutes_range[1]),2)}:00'
time_sec_str = f'{str.zfill(str(minutes_range[0]),2)}:{str.zfill(str(second),2)}'

sel_min_msec = minutes_range[0]*60000
sel_max_msec = minutes_range[1]*60000
sel_msec = sel_min_msec+second*1000

mask = (df['millisecond']>=sel_min_msec) & (df['millisecond']<=sel_max_msec)
df_sample = df[mask]

col_left, col_right = st.columns(2)

with col_left:
    st.write('### Players position')
    st.write(f'Position of every player detected at {time_sec_str}')
    st.info('This plot can be updated using the second filter')
    st.pyplot(get_convexhull_vis(df[df['millisecond'] == sel_msec]), use_container_width=True)

with col_right:
    st.write('### Most played zones')
    st.write(f'General overview of the most played zone during ' + min_time_str + ' period.')
    st.pyplot(get_heatmap_vis(df_sample), use_container_width=True)

with col_left:
    st.divider()
    st.write('### Juego de posición')
    st.write(f'Tactical analysis of different zones covered during the ' + min_time_str + ' period.')
    st.pyplot(get_position_vis(df_sample), use_container_width=True)

with col_right:
    st.divider()
    st.write('### Most played zones')
    st.write(f'Covered zones during the ' + min_time_str + ' period.')
    st.write(
        '''
        The pitch is divided into 3 different zones: attacking, middle, defensive
        ''')
    
    st.pyplot(get_three_part_vis(df_sample), use_container_width=True)

st.divider()
st.write('### Played zone through time')
st.write('Minute-by-minute analysis of the most played zones (defensive, middle, and attacking).')
st.pyplot(get_pos_by_min(df_pos))

st.divider()
st.write('### Match video')

st.video(load_video()) 