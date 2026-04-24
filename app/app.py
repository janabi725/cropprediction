import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import pandas as pd
import joblib


@st.cache_resource
def load_rf_model():
    return joblib.load('../ml-pipeline/rf_ertragsmodell.pkl')

@st.cache_data
def get_predictions():
    gdf = gpd.read_file("landkreise_bawu_sauber.geojson")
    
    input_data = pd.read_csv('../ml-pipeline/features_2024_für_app.csv')

    for col in gdf.select_dtypes(include=['datetime64', 'datetimetz']).columns:
        gdf[col] = gdf[col].astype(str)
            
    for col in input_data.select_dtypes(include=['datetime64', 'datetimetz']).columns:
        input_data[col] = input_data[col].astype(str)
    
    model = load_rf_model()
    feature_cols = ['NDVI', 'Temp', 'Niederschlag']
    input_data['Prognose_dt_ha'] = model.predict(input_data[feature_cols])
    
    input_data['Kreis-Id'] = input_data['Kreis-Id'].astype(str).str.zfill(5)
    gdf['ARS'] = gdf['ARS'].astype(str).str.zfill(5)
    
    gdf_final = gdf.merge(input_data[['Kreis-Id', 'Prognose_dt_ha']], left_on='ARS', right_on='Kreis-Id', how='left')
    
    gdf_final['geometry'] = gdf_final['geometry'].simplify(tolerance=0.001, preserve_topology=True)
    
    return gdf_final

st.title("Ertragsprognose Baden-Württemberg")

gdf = get_predictions()

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
    data=gdf,
    columns=['Kreis-Id', 'Prognose_dt_ha'],
    key_on='feature.properties.ARS',
    fill_color='YlGn',              
    fill_opacity=0.6,               
    line_opacity=0.5,
    legend_name='Prognostizierter Ertrag (dt/ha)'
).add_to(m)

st_data = st_folium(
    m, 
    width=800, 
    height=600,
    returned_objects=["last_active_drawing"],
    zoom=8
)
