# !pip install folium
# !pip install shapely_geojson
# !pip install geojson

import numpy as np
import folium
from shapely_geojson import Feature
from shapely.geometry.polygon import Polygon


def prepare_map(df_key):
    """
    The input must be a pandas dataframe. The function extracts for each unique station the coordinates (longitude and
    latitude)
    :param df_key: df_key must be a pandas dataframe with the following columns: station_name, station_longitude,
     station_latitude.
    :return: return 3 lists (in this order: stations, longitudes, latitudes), the coordinates for each unique station.
    """
    stations = df_key.station_name.unique()  # get the names of unique stations
    longitudes, latitudes = [], []  # initialize the lists
    for station in stations:  # loop over all stations
        longitudes.append(df_key[df_key.station_name == station]['station_longitude'].values[0])  # get longitude
        latitudes.append(df_key[df_key.station_name == station]['station_latitude'].values[0])  # get latitude
    return stations, longitudes, latitudes


def create_map(weights, latitudes, longitudes, save_title="map.html"):
    """
    Creates a folium map using coordinates (latitudes and longitudes) with the provided weights (as intensity).
    :param save_title: string, title of the output file (the saved map).
    :param weights: list of float (the intensities of each point).
    :param latitudes: list of float, latitude of each point.
    :param longitudes: list of float, longitude of each point.
    :return: a folium map and a list of cluster (based on the tercile of "weights").
    """
    dic_color = {np.quantile(weights, 0.33): 'green',
                 np.quantile(weights, 0.66): 'orange',
                 np.quantile(weights, 0.99) * 2: 'red'}
    dic_cluster = {'green': 1, 'orange': 2, 'red': 3}
    coordinates = (40.778152, -73.964083)  # center on manhattan
    final_map = folium.Map(location=coordinates, tiles='OpenStreetMap', zoom_start=12)
    l_cluster = []
    for i in range(len(latitudes)):  # loop over all points
        for key in dic_color:  # assign a cluster
            if not key < weights[i]:
                break
        folium.CircleMarker(location=(longitudes[i], latitudes[i]), radius=5, color=dic_color[key], opacity=100,
                            fill=True, fill_color=dic_color[key]).add_to(final_map)  # add the point on the map
        l_cluster.append(dic_cluster[dic_color[key]])  # save the cluster
    final_map.save(outfile=save_title)  # save the map
    return final_map, l_cluster


def save_geojson(df, df_demo, weight_feature="population"):
    """
    Creates features for a folium map using the neighborhoods (coordinates in df) and weights in df_demo.
    :param weight_feature: string, feature to color color the map with (column of df_demo).
    :param df: pandas dataframe, coordinates of the neighborhoods.
    :param df_demo: pandas dataframe, features to color the map with.
    :return: features to be used in addition with folium map.
    """
    features = []
    values = df_demo[weight_feature].fillna(df_demo[weight_feature].mean()).values
    dic_color = {np.quantile(values, 0.33): 'green',
                 np.quantile(values, 0.66): 'orange',
                 np.quantile(values, 0.99) * 2: 'red'}
    for col in df.columns:  # loop over all neighborhoods
        val = df_demo[df_demo['nta_code'] == col][weight_feature].values[0]  # get the feature for the neighborhood
        for key in dic_color:  # assign a cluster
            if not key < val:
                break
        values = df.loc[:, col].dropna().values  # get the coordinates
        polygon = [(values[i], values[i + 1]) for i in range(0, len(values) - 1, 2)]  # create the polygon
        features.append(Feature(geometry=Polygon(polygon), properties={'color': dic_color[key]}))  # save the result
    return features
