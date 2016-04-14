from collections import deque
from copy import deepcopy

from board import get_scoring
from classes import Path

# Maximum number of iterations for finding paths.
MAX_PATH_ITER = 1000

MAX_NUM_PATH = 20


def connected(city1, city2, city_edges, edge_claims, player):
    """
    Perform a depth-first search to determine if 2 cities are connected by a route from a given player.

    :param city1: The first city.
    :param city2: The second city.
    :param city_edges: A dictionary of which cities, as keys, have which edges.
    :param edge_claims: A dictionary with edges as keys of which edges are claimed by which players.
    :param player: The player who owns the route being checked.
    :return: True if connected, false otherwise.
    """
    stack = [city1]
    visited = set()

    while stack:
        city = stack.pop()

        # Don't visit the same city twice.
        if city in visited:
            continue

        for edge in city_edges[city]:
            if edge_claims[edge] == player.name:
                other_city = edge.other_city(city)

                # We're done if this is the city we're trying to connect to.
                if other_city == city2:
                    return True

                stack.append(other_city)

        visited.add(city)

    return False


def find_paths_for_destinations(destinations, city_edges, max_cost, scoring=get_scoring(), player=None,
                                edge_claims=None, sort_paths=True):
    """
    Finds all paths that connect all destinations for less than the max_cost.

    :param destinations: A list of the destinations to connect.
    :param city_edges: All of the edges that make up the map.
    :param max_cost: The maximum cost of all paths returned.
    :param scoring: The scoring dictionary for the game.
    :param player: Optional parameter for a player.  If included, all edges owned by the player have 0 cost.
    :param edge_claims: Optional parameter for edge_claims.  If included, all edges owned by the player have 0 cost.
    :param sort_paths: Optional boolean to sort the paths.  By default, will sort paths by cost.
    :return: A list of paths, ordered with sort method.  Paths may not be continuous.
    """
    dest_paths = {}
    all_paths = []

    # First step: get candidate paths.
    for dest in destinations:
        # Perform breadth first search to get all paths below the max_cost.
        dest_paths[dest] = find_paths(dest.city1, dest.city2, city_edges, max_cost, scoring, player, edge_claims)

    # Second step: Combine paths to get a list of all possible paths that hit everything for less than the max_cost.
    for dest in dest_paths:
        # For the first destination, just dump in all the paths currently found.
        if not all_paths:
            all_paths = dest_paths[dest]
        # For any destination past the first, combine with the existing paths to create new ones, only counting
        # duplicates once in the new path, thus possibly reducing cost.
        else:
            working_paths = all_paths
            all_paths = []
            for path1 in working_paths:
                for path2 in dest_paths[dest]:
                    # Combine the paths and add them to all_paths if they're still below max_cost.
                    combined_path = Path(path1.edges.union(path2.edges), scoring, player, edge_claims)

                    if combined_path.cost <= max_cost:
                        all_paths.append(combined_path)

    # Third step: Sort by path cost in ascending order.
    if sort_paths:
        return sorted(all_paths, key=Path.default_sort_method)
    else:
        return all_paths


def find_paths(city1, city2, city_edges, max_cost, scoring, player=None, edge_claims=None):
    """
    Find all paths that connect two cities for less than the max_cost.

    :param city1: The first city to connect.
    :param city2: The second city to connect.
    :param city_edges: All of the edges that make up the map.
    :param max_cost: The maximum cost of all paths returned.
    :param scoring: The scoring dictionary for the game.
    :param player: Optional parameter for a player.  If included, all edges owned by the player have 0 cost.
    :param edge_claims: Optional parameter for edge_claims.  If included, all edges owned by the player have 0 cost.
    :return: A list of paths.
    """

    queue = deque()
    result = []

    # Put the first city into the queue.
    queue.append((city1, set(city1), Path(set(), scoring, player, edge_claims)))

    iteration = 0

    while queue and iteration < MAX_PATH_ITER and len(result) < MAX_NUM_PATH:
        city, visited, path = queue.popleft()
        iteration += 1

        # Add all neighbors to the queue.
        for outgoing_edge in city_edges[city]:
            other_city = outgoing_edge.other_city(city)

            # First line makes sure the edge isn't already in the path and it's below max cost.
            # Second and third line make sure it's not claimed by another player, if that matters.
            if other_city not in visited and path.cost + outgoing_edge.cost <= max_cost \
                    and ((edge_claims is None and player is None)
                         or edge_claims[outgoing_edge] is None or edge_claims[outgoing_edge] == player.name):
                # Create a copy of the path thus far with the new edge added.
                updated_path = deepcopy(path)
                updated_path.add_edge(outgoing_edge, scoring, player, edge_claims)

                if other_city == city2:
                    # The updated path is a valid path between the two cities.
                    result.append(updated_path)
                else:
                    # Add the updated path and new city to the queue.
                    queue.append((other_city, visited.union(set(other_city)), updated_path))

    return result


"""
get the city and edges which are adjacent from a city, (follows player claim type)
"""


def get_adjacent_cities(city, routes, player):
    # print 'In get adjacent'
    # print city
    city_edges = list()
    for route in routes:
        if (str(routes.get(route) or 'unclaimed') is str(player)):
            if (str(route.city1) == str(city)):
                city_edges.append([route.city2, route])
            if (str(route.city2) == str(city)):
                city_edges.append([route.city1, route])
    # print'Returning city edges'
    # print city_edges
    return city_edges


"""
Brushfire algorithm from city: returns cities and depths as list

param: start_city = where brushfire starts from
param: depth = maximum depth of brushfire
param: player = which claim type the brushfire can expand over
param: allow_loop_back = wheather or not 
"""


def brushfire_from(start_city, player, allow_loop_back, routes):
    actual_depth = 0
    burned_cities = list()
    burning_cities = list()
    leaves = list()
    #print 'Now determining extent for %s' % start_city
    burning_cities.append([start_city, actual_depth,[]])
    while  burning_cities:
        expanded = False
        burn_city = burning_cities.pop(0)
        burned_cities.append(burn_city[0])

        #print 'burned_cities'
        #print burned_cities

        #print 'on back_burner:'
        #print burning_cities

        #print 'burning: %s' % burn_city

        for city_edge in get_adjacent_cities(burn_city[0], routes, player):
            #print 'city_edge is: %s' % str(city_edge)
            if (city_edge[0] not in burned_cities):
                #print 'in burn, current edge history'
                edges = burn_city[2][:]
                edges.append(city_edge[1])
                #print edges
                expanded= True;
                burning_cities.append([city_edge[0], burn_city[1] + 1,edges])
                #Check if edge would connect something which is already connected
                if str(city_edge[0]) == str(start_city) and burn_city[1] > 1 and not allow_loop_back:
                    burning_cities = list()
                    burning_cities.append([start_city, 0,[]])
                    return burning_cities;
            if not expanded and burn_city[1]>0:
                leaves.append(burn_city)
                #print 'adding a leaf %s'% burn_city

    return leaves


"""
def _expand(city_depth,path,player,routes):
    current_depth = city_depth[1]
    path.append(city_depth)
    possible_path = path[:]
    for city  in get_adjacent_cities(current_city,routes,player):
        _expand([city,current_depth+1],path,player,routes)


def longest_path_length(start_city,player,player_cities,routes):
    #cities_to_burn = list()
    #cities_to_burn.append([start_city,0])
    tracked_cities = player_cities[:]
    path_list = list()
    for city in tracked_cities
        #cities_to_burn.pop[0]
        _expand(city_depth,player,routes)

    return depth
"""

"""
Get the maximum depth of routes from a city
"""


def depth_of_path_from(player, city, player_cities, routes):
    return_on_fork = False
    city_depths = brushfire_from(city, player, return_on_fork, routes)
    #print ' These are the city depths we have for city: %s ' % city
    #print city_depths
    
    max_car_length = 0
    edge_depth = 0
    edges = []
    
    for city_depth in city_depths:
        car_length = 0
        for edge in city_depth[2]:
            car_length = car_length + edge.cost
        if car_length > max_car_length:
            #print edge
            max_car_length = car_length
            edge_depth = city_depth[1]
            edges = city_depth[2]
            
    return {'edge_depth':edge_depth,'car_length':max_car_length,'edges':edges}


"""
Is a city in a list of edges
"""
def city_in_edges(city,edges):
    for edge in edges:
        if city is edge.city1:
            return True
        if city is edge.city2:
            return True
    return False
            


"""
Get edges of that are easily threatened for a specific player near city
"""
def threatened_edge_near(start_city, player_cities, player, min_num_cars, routes):
    #print 'Looking for threathened_edge_near %s' %start_city
    harmful_edges = list()
    for city_edge in get_adjacent_cities(start_city, routes, 'unclaimed'):
        #print 'Threatened edges looking at:'
        #print city_edge

        if (city_edge[0] in player_cities):
            city1 = city_edge[1].city1
            city2 = city_edge[1].city2
            city1_extent = depth_of_path_from(player,city1 , player_cities, routes)
            city2_extent = depth_of_path_from(player,city2, player_cities, routes)
            cost = city1_extent['car_length'] + city2_extent['car_length']
            # city_edge[1].cost = cost;
            if cost > min_num_cars:
                #make sure we are not connecting something already connected
                #print' edges ___'
                #print city2_extent['edges']
                if not city_in_edges(city1,city2_extent['edges']):
                    #print 'cost: %f'% cost
                    harmful_edges.append([city_edge[1],cost])
            
    # print 'player cities'
    # print player_cities
    #print 'harmful edges:'
    #print harmful_edges
    return harmful_edges


def get_player_cities(player, routes):
    player_cities = list()
    for route in routes:
        if routes.get(route) is player:
            if route.city1 not in player_cities:
                player_cities.append(route.city1)
            if route.city2 not in player_cities:
                player_cities.append(route.city2)
    return player_cities


"""
Get edges of that are easily threatened for a specific player
------>Steve, this is the method you want
:param player: the player whom you are checking for threats
:param routes: the dictionary of claimed edges
:param min_num_cars: the minium number of cars on the path you are bisecting
:return: list([threatened_edge,path_car_length])
"""
def get_threatened_edges(player, routes,min_num_cars = 1):
    threatened_edges = list()
    # get list of cities which opponent has edges which connect to it
    player_cities = get_player_cities(player, routes)

    for city in player_cities:
        # search for beginings of other paths at depth
        for edge_group in threatened_edge_near(city, player_cities, player,min_num_cars, routes):
            if edge_group not in threatened_edges:
                threatened_edges.append(edge_group)
            
    #print 'these are the threatened edges of player %s' % player
    #print threatened_edges
    #print 'try again'
    #print list(set(threatened_edges))


    return threatened_edges
