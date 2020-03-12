### import the data
def prepare_map(df_key):
    """
    df like dataset_1.csv
    output just the stations, latitudes, longitudes
    """
    stations = df_key.station_name.unique()
    longitudes = []
    latitudes = []
    for station in stations:
        longitudes.append(df_key[df_key.station_name == station]['station_longitude'].values[0])
        latitudes.append(df_key[df_key.station_name == station]['station_latitude'].values[0])
    return stations, longitudes, latitudes

def creat_map(weights, stations, latitudes, longitudes):
    dic_color = {np.quantile(weights, 0.33): 'green', np.quantile(weights, 0.66): 'orange',
                 np.quantile(weights, 0.99) * 2: 'red'}
    dic_cluster = {'green': 1, 'orange': 2, 'red': 3}
    coords = (40.778152, -73.964083)
    mapp = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=12)
    l_cluster = []
    for i in range(len(latitudes)):
        for key in dic_color:
            if not key < weights[i]:
                break
        folium.CircleMarker(location=(longitudes[i], latitudes[i]), radius=5,
                            color=dic_color[key], opacity=100, fill=True, fill_color=dic_color[key]
                            ).add_to(mapp)
        l_cluster.append(dic_cluster[dic_color[key]])
    mapp.save(outfile='map.html')
    return mapp, l_cluster

def save_geojson(df, df_demo):
    """
    df like dataset_9.csv
    """
    features = []
    values = df_demo['population'].fillna(df_demo['population'].mean()).values
    dic_color = {np.quantile(values, 0.33): 'green', np.quantile(values, 0.66): 'orange',
                 np.quantile(values, 0.99) * 2: 'red'}
    for col in df.columns:
        val = df_demo[df_demo['nta_code'] == col]['population'].values[0]
        for key in dic_color:
            if not key < val:
                break
        values = df.loc[:, col].dropna().values
        polygon = [(values[i], values[i + 1]) for i in range(0, len(values) - 1, 2)]
        features.append(Feature(geometry=Polygon(polygon), properties={'color': dic_color[key]}))
    return features