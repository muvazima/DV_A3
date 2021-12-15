import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
import pathlib
from folium import plugins
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
#st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
# STREAMLIT_STATIC_PATH = pathlib.Path(st.__path__[0]) / 'static'
# DOWNLOADS_PATH = (STREAMLIT_STATIC_PATH / "downloads")

@st.cache(persist=True)
def load_csv():
    #df=pd.read_csv(str(DOWNLOADS_PATH / "moby_data_nov.csv"))
    df=pd.read_csv("Moby_November.csv")
    df=df[df['HarvestTime'] == df.groupby('BikeID')['HarvestTime'].transform('max')]
    return df

def circle_color(battery):
    if(battery<=20):
        return 'red'
    elif(battery>20 and battery<=60):
        return 'orange'
    else:
        return 'green'

def main():
    df=load_csv()
    st.title("Moby Bikes Accessibility")
#st.title('Select')
    radius=st.sidebar.text_input('Enter radius in m')
    option = st.sidebar.radio('Select Bike Type',list(df['BikeTypeName'].unique()))

    m = folium.Map(location=[53.350140, -6.266155], zoom_start=12)
#folium.TileLayer('cartodbpositron').add_to(m)
    colordict = {1: 'red', 2: 'blue', 3: 'black', 4: 'purple', 5:'lightgray'}
    bike_state_dict={1:'Warning - is in move and not rented',2:'Normal',3:'Switched Off',4:'Firmware Upgrade',5:'Laying on the ground'}
    marker_cluster = plugins.MarkerCluster().add_to(m)
    if(option!=''):
        bike_type_df=df[df.BikeTypeName==option]
        for lat, lon, battery,bike_id, bike_type, bike_state in zip(bike_type_df['Latitude'], bike_type_df['Longitude'], bike_type_df['Battery'],bike_type_df['BikeID'], bike_type_df['BikeTypeName'], bike_type_df['EBikeStateID']):
            folium.Marker(location=[lat, lon], popup = ('Battery: ' + str(battery) + '<br>'
                    'Bike ID: ' + str(bike_id) + '<br>'
                    'Bike State: ' + bike_state_dict[bike_state]
                    ), icon=folium.Icon(color=colordict[bike_state],icon='bicycle', prefix='fa')).add_to(marker_cluster)
            if(radius!=''):
                folium.Circle(location=[lat, lon], radius=int(radius), fill=True, fill_color=circle_color(battery),weight=0,opacity=0.001*battery).add_to(m)

    folium_static(m)

if __name__== "__main__":
    main()