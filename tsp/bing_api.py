import json
import requests
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

def find_coords(school_list, df):
    """
    school_list: list of school's names
    df: database (all schools with their corresponding coordinates)

    df_coords: df of each school from school_list with its corresponding coordinates
    """
    
    df_coords = df[df['university'].isin(school_list)]
    df_coords.index = df_coords['university']
    df_coords = df_coords.set_index('university').loc[school_list].reset_index(inplace=False)

    return df_coords



def df_coords_to_http(df_coords):

    """ Convert the coordinates data in df_coords to json format
    df_coords: df of each school from school_list with its corresponding coordinates
    http_body: df_coords formatted in a json format ready for the request
    """
    sites = []

    for row_idx in range(len(df_coords)):
        row = df_coords.iloc[row_idx]

        sites.append({
            'latitude': row['lat'],
            'longitude': row['lon']
            })
        
    json_body = {
        "origins": sites,
        "destinations": sites,
        "travelMode": "driving"
    }
    
    return json_body



def make_request(http_body):

    BingMapsKey = os.environ.get("BINGS_KEY")
    print(BingMapsKey)
    # URL
    url = "https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?key={}".format(BingMapsKey)
    # HEADERS
    headers = {'Content-type': 'application/json'}
    # Make the request
    response = requests.post(url, data=json.dumps(http_body), headers=headers)

    return response




def response_to_matrix(response):
    """ 
    * Extract distances from the response and create the distance matrix
    matrix: distance matrix with high diagonal values for TSP purposes
    """

    # Get the list of dictionaries from the response 
    # (each dictionary = destination_n -> destination_m)
    results_list = response.json()['resourceSets'][0]['resources'][0]['results']

    # Get the num of schools
    num_places = int(len(results_list)**(1/2))

    # From each dic, obtain the value of the travelDistance key
    list_ = [x['travelDistance'] for x in results_list]

    # From list to matrix
    matrix = np.array(list_).reshape(num_places, num_places)
    
    # Convert the diagonal values(0) to a high value (for the optimization algorithm)
    matrix = matrix + np.eye(num_places) * 1000

    return matrix


def matrix_to_df(matrix, df_coords):
    " Given the matrix values, create a df "

    distance_df = pd.DataFrame(matrix)

    distance_df.columns = df_coords['university'].values
    distance_df.index = df_coords['university'].values

    return distance_df


def get_distance_matrix(school_list, df):
    " distance_df: pd.DataFrame distance matrix "

    # Get the coords of the schools
    df_coords = find_coords(school_list, df)
    # Conver the data to a json format, ready to be taken as a request
    json_body = df_coords_to_http(df_coords)
    # Make the request, get response
    response = make_request(json_body)
    # Get the distance matrix from the response
    distance_matrix = response_to_matrix(response)
    #Convert to pd.DataFrame
    distance_df = matrix_to_df(distance_matrix, df_coords)

    return distance_df

