import datetime
import numpy as np


def get_time_start_stop(df):
    """
    Get the delta time in minutes (truncated) between start and stop.
    :param df: pandas dataframe, must have the columns: stoptime, starttime.
    :return: pandas dataframe, df with one added columns: trip_duration_min.
    """

    def to_datetime(x): return datetime.datetime.strptime(x, '%m/%d/%y %H:%M')  # transform into datetime format

    delta = df.stoptime.apply(to_datetime) - df.starttime.apply(to_datetime)  # get the delta time
    delta = delta.apply(lambda x: int(x.total_seconds() // 60))  # transform in minutes
    df['trip_duration_min'] = delta  # save results
    return df


def adjacency_matrix(df):
    """
    Given a graph with n vertices and m nodes, the adjacency matrix is a square n*n matrix with the property:
    A[i][j] = 1 if there is an edge between node i and node j, 0 otherwise.
    :param df: pandas dataframe, it must contains the following columns: start_station_id, end_station_id.
    :return: adj_matrix (numpy array) and a mapping station2id.
    """
    unique_station = set(df.start_station_id.unique()).union(set(df.end_station_id.unique()))  # unique stations
    station2id = {key: i for i, key in enumerate(unique_station)}  # mapping station to number (id)
    vertices = [(start, end) for start, end in zip(df.start_station_id.values, df.end_station_id.values)]  # vertices
    adj_matrix = np.zeros((len(unique_station), len(unique_station)))  # initialize the adjacency matrix
    for station_a, station_b in vertices:  # loop over all vertices
        adj_matrix[station2id[station_a], station2id[station_b]] = 1  # 1 if there is a link between the 2 stations
    adj_matrix = (adj_matrix + adj_matrix.T)  # apply transformation 1 (the adjacency matrix is symmetric)
    adj_matrix[adj_matrix > 0] = 1  # apply transformation 2 (the adjacency matrix is symmetric)
    return adj_matrix, station2id


def degree_matrix_new(df):
    """
    The degree matrix is a n*n diagonal matrix with the property: d[i][i] = the number of adjacent edges in node i or
     the degree of node i and d[i][j] = 0.
    :param df: pandas dataframe, see adjacency_matrix function.
    :return: numpy array.
    """
    adj_matrix, _ = adjacency_matrix(df)
    return np.diag(adj_matrix.sum(axis=1))


def laplacian_matrix(df):
    """"
    The laplacian matrix is a n*n matrix defined as: L = degree_matrix_new - adjacency_matrix.
    :param df: pandas dataframe, see adjacency_matrix function.
    :return: numpy array.
    """
    adj_matrix, _ = adjacency_matrix(df)
    def_matrix = np.diag(adj_matrix.sum(axis=1))
    return def_matrix - adj_matrix

# def degree_matrix_new(df):
#     """
#     The degree matrix is a n*n diagonal matrix with the property: d[i][i] = the number of adjacent edges in node i or
#      the degree of node i and d[i][j] = 0.
#     :param df: pandas dataframe, it must contains the columns: start_station_id, end_station_id.
#     :return:
#     """
#     vertices = [(start, end) for start, end in zip(df.start_station_id.values, df.end_station_id.values)]
#     dic = {}
#     for vertex in vertices:
#         if vertex in dic:
#             dic[vertex] += 1
#         else:
#             dic[vertex] = 1
#
#     return dic
