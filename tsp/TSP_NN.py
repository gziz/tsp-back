def distance(A,B, df):
    a_to_b = df.loc[A][B]
    b_to_a = df.loc[B][A]

    avg = (a_to_b + b_to_a) /2
    return avg

def first(schools):
    # Tomar el primer el primer valor de una lista
    return next(iter(schools))



def run_tsp(algorithm, df):

    schools_list = list(df.columns)

    tour = algorithm(schools_list, df)
    total_length = round(tour_length(tour, df), 1)
    # Suponiendo que va a 60km/hr or 1km/min. Para pasar de total_length a minutos multiplicar por 1.
    total_minutes = total_length 
    hours = total_minutes // 60
    minutes = round(total_minutes % 60)
    minutes = minutes if len(str(minutes)) > 1 else '0' + str(minutes)    
    
    return tour, [round(total_length,1), hours, minutes]

def valid_tour(tour, cities):
    "Is tour a valid tour for these cities?"
    return set(tour) == set(cities) and len(tour) == len(cities)

def tour_length(tour, df=None):
    # Regresar la distancia acumulada en la ruta
    return sum(distance(tour[i], tour[i-1], df)
               for i in range(len(tour)))



def nn_tsp(cities, df):
    """Start the tour at the first city; at each step extend the tour 
    by moving from the previous city to the nearest neighboring city, C,
    that has not yet been visited."""
    start = first(cities)

    tour = [start]
    
    unvisited = cities.copy()
    unvisited.remove(start)
    
    while unvisited:
        next_school = nearest_neighbor(tour[-1], unvisited, df)
        tour.append(next_school)
        unvisited.remove(next_school)

    return tour


def nearest_neighbor(last_visited_school, unvisited_schools, df):
    "Find the school from the unvisited_schools that's closest to the last_visited_school"
    return min(unvisited_schools, key=lambda x: distance(x, last_visited_school, df))


def reverse_segment_if_better(tour, i, j, df):
    """
    Given a pair (i=start, j=end), 
    if reversing tour=[...(i-1),(i)...j...] into tour=[...(i-1), (j)...(i)...] minimizes the distance, we reverse it.

    how to know if tour[i-1]->tour[i] + to be continued
    """
    # Given tour [...A-B...C-D...], consider reversing B...C to get [...A-C...B-D...]
    A, B, C, D = tour[i-1], tour[i], tour[j-1], tour[j % len(tour)]
    
    # Are old edges (AB + CD) longer than new ones (AC + BD)? If so, reverse segment.
    if distance(A, B, df) + distance(C, D, df) > distance(A, C, df) + distance(B, D, df):
        tour[i:j] = reversed(tour[i:j])

def alter_tour(tour, df):
    "Try to alter tour for the better by reversing segments."
    original_length = tour_length(tour, df)

    for (start, end) in all_segments(len(tour)):
        reverse_segment_if_better(tour, start, end, df)
    # If we made an improvement, then try again; else stop and return tour.
    if tour_length(tour, df) < original_length:
        return alter_tour(tour, df)
    return tour

def all_segments(len_tour):
    """
    * We want pairs (start, end) of indexes where there's a value difference of at least 2 btw start & end
    * why the difference? -> When performing reversed(tour[start, end]), we need reversed at least 2 values
    * hence the minimum 2 value difference btw start & end
        * end - start >= 2
        * end <= len_tour
        * min(start) = 0
    """
    segments = []
    for x in range(len_tour+1):
        for y in range(x+2, len_tour+1):
            segments.append((x, y))

    return segments


def altered_nn_tsp(cities, df):
    "Run nearest neighbor TSP algorithm, and alter the results by reversing segments."
    return alter_tour(nn_tsp(cities, df), df)