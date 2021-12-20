import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
import branca
from PIL import Image
image = Image.open('state_legend_white.png')
from folium import plugins
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
@st.cache(persist=True)
def load_csv():
    df=pd.read_csv("Moby_November.csv")
    df=df[df['HarvestTime'] == df.groupby('BikeID')['HarvestTime'].transform('max')]
    return df

def main():
    df=load_csv()
    st.title("Moby Bikes Accessibility")
    st.write("A visualization that helps to determine how much area of Dublin has accessibility to Moby bikes based on the walking distance selected by the user. It also helps in determining the battery level of the cycle using the colour of the radius around the cycle and the state of the cycle is represented by the marker colour. The opacity of each circle also indicates the number of bikes present within that circle.")
    radius=st.sidebar.text_input('Enter Walking distance in m:')
    option = st.sidebar.radio('Select Bike Type',list(df['BikeTypeName'].unique()))
    m = folium.Map(location=[53.350140, -6.266155], zoom_start=12)
    colordict = {1: 'red', 2: 'blue', 3: 'black', 4: 'purple', 5:'lightgray'}
    bike_state_dict={1:'Warning - is in move and not rented',2:'Normal',3:'Switched Off',4:'Firmware Upgrade',5:'Laying on the ground'}
    colormap = branca.colormap.LinearColormap(['red', 'yellow', 'green'])
    colormap = colormap.to_step(index=[0,20,40,60,80,100])
    colormap.caption = 'Battery'
    colormap.add_to(m)
    marker_cluster = plugins.MarkerCluster().add_to(m)
    
    if(option!=''):
        bike_type_df=df[df.BikeTypeName==option]
        for lat, lon, battery,bike_id, bike_type, bike_state in zip(bike_type_df['Latitude'], bike_type_df['Longitude'], bike_type_df['Battery'],bike_type_df['BikeID'], bike_type_df['BikeTypeName'], bike_type_df['EBikeStateID']):
            folium.Marker(location=[lat, lon], popup = ('Battery: ' + str(battery) + '<br>'
                    'Bike ID: ' + str(bike_id) + '<br>'
                    'Bike State: ' + bike_state_dict[bike_state]
                    ), icon=folium.Icon(color=colordict[bike_state],icon='bicycle', prefix='fa')).add_to(marker_cluster)
            
            if(radius!=''):
                folium.Circle(location=[lat, lon], radius=int(radius), fill=True, fill_color=colormap(battery),weight=0,opacity=0.001*battery).add_to(m)
    
    folium_static(m)
    st.image(image, caption='Bike State',use_column_width=True)

if __name__== "__main__":
    main()