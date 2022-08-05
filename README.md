# Traveling Salesman Problem
Compute the optimal route for a salesman given locations that must be visited.

## Steps
* Receive the request with the selected locations that must be visited.
* Given the lat & lon of each location, create a distance matrix using the Bing API.
* With the distance matrix, implement the Nearest Neighbor heuristic to compute the optimal visit order.
