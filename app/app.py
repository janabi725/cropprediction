import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import pandas as pd

st.title("Ertragsprognose Baden-Württemberg")

# dummy data
data = {
    'Landkreis_ID': ['08111', '08115', '08116'], # Beispiel-IDs für Stuttgart, Böblingen, Esslingen
    'Prognose_dt_ha': [75.5, 82.1, 68.9]
}
df_predictions = pd.DataFrame(data)

# read geo jason
gdf = gpd.read_file("landkreise_bawu_sauber.geojson")

# clean data
for col in df_predictions.select_dtypes(include=['datetime64', 'datetimetz']).columns:
    df_predictions[col] = df_predictions[col].astype(str)

for col in gdf.select_dtypes(include=['datetime64', 'datetimetz']).columns:
    gdf[col] = gdf[col].astype(str)

df_predictions['Landkreis_ID'] = df_predictions['Landkreis_ID'].astype(str)
gdf['ARS'] = gdf['ARS'].astype(str)

# map creation    
m = folium.Map(location=[48.5, 9.0], zoom_start=8, tiles=None)

folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Satellitenbild',
    overlay=False,
    control=True
).add_to(m)

folium.Choropleth(
    geo_data=gdf,
    name='Ertragsprognose',
    data=df_predictions,
    columns=['Landkreis_ID', 'Prognose_dt_ha'],
    key_on='feature.properties.ARS',
    fill_color='YlGn',              
    fill_opacity=0.6,               
    line_opacity=0.5,
    legend_name='Prognostizierter Ertrag (dt/ha)'
).add_to(m)

st_folium(m, width=700, height=500)
