import geopandas as gpd

gdf = gpd.read_file("VG250_KRS.shp") 

# get BW data
bawu_gdf = gdf[gdf['SN_L'] == '08'] 

bawu_gdf.to_file("landkreise_bawu_sauber.geojson", driver="GeoJSON")
