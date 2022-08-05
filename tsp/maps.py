import pandas as pd


def find_coords(school_list, df):
    """
    school_list: list of school's names
    df: nancy's database (all schools with their corresponding coordinates)

    df_coords: df of each school from school_list with its corresponding coordinates
    """
    df_coords = df[df['university'].isin(school_list)]
    df_coords.index = df_coords['university']
    df_coords = df_coords.set_index('university').loc[school_list].reset_index(inplace=False)

    return df_coords

