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
                                edge_claims=None, sort_method=Path.default_sort_method):
    """
    Finds all paths that connect all destinations for less than the max_cost.

    :param destinations: A list of the destinations to connect.
    :param city_edges: All of the edges that make up the map.
    :param max_cost: The maximum cost of all paths returned.
    :param scoring: The scoring dictionary for the game.
    :param player: Optional parameter for a player.  If included, all edges owned by the player have 0 cost.
    :param edge_claims: Optional parameter for edge_claims.  If included, all edges owned by the player have 0 cost.
    :param sort_method: Optional function to use when sorting.  Will take a path and return a value to sort with in
    ascending order.
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
    return sorted(all_paths, key=sort_method)


def find_paths(city1, city2, city_edges, max_cost, scoring, player=None, edge_claims=None, ):
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

                    # Don't find paths more than three times the cost of the cheapest path.
                    if updated_path.cost * 2 < max_cost:
                        max_cost = updated_path.cost * 2
                else:
                    # Add the updated path and new city to the queue.
                    queue.append((other_city, visited.union(set(other_city)), updated_path))

    return result
