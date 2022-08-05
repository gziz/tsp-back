from tsp.bing_api import get_distance_matrix, find_coords
from tsp.TSP_NN import run_tsp, altered_nn_tsp
import pandas as pd

def tsp(json_locations):
    
    df = pd.DataFrame(json_locations)
    school_list = list(df['university'].values)

    dist_matrix = get_distance_matrix(school_list, df)
    tour, [tour_length, hours, minutes] = run_tsp(altered_nn_tsp, dist_matrix)
    tour_df = find_coords(tour, df).values.tolist()

    return tour_df, [tour_length, hours, minutes]