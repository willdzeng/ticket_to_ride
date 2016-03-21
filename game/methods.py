from collections import deque
from copy import copy, deepcopy

from board import get_scoring
from classes import Path


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


def find_paths_for_destinations(destinations, city_edges, max_cost, scoring=get_scoring()):
    """
    Finds all paths that connect all destinations for less than the max_cost.

    :param destinations: A list of the destinations to connect.
    :param city_edges: All of the edges that make up the map.
    :param max_cost: The maximum cost of all paths returned.
    :param scoring: The scoring dictionary for the game.
    :return: A list of paths, ordered from cheapest to most expensive.  Paths may not be continuous.
    """
    dest_paths = {}
    all_paths = []

    # First step: get candidate paths.
    for dest in destinations:
        # Perform breadth first search to get all paths below the max_cost.
        dest_paths[dest] = find_paths(dest.city1, dest.city2, city_edges, max_cost, scoring)

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
                for path2 in dest_paths:
                    # Combine the paths and add them to all_paths if they're still below max_cost.
                    combined_path = Path(path1.edges.union(path2.edges), scoring)

                    if combined_path.cost <= max_cost:
                        all_paths.append(combined_path)

    # Third step: Sort by path cost in ascending order.
    return sorted(all_paths, key=lambda path: path.cost)


def find_paths(city1, city2, city_edges, max_cost, scoring):
    """
    Find all paths that connect two cities for less than the max_cost.

    :param city1: The first city to connect.
    :param city2: The second city to connect.
    :param city_edges: All of the edges that make up the map.
    :param max_cost: The maximum cost of all paths returned.
    :param scoring: The scoring dictionary for the game.
    :return: A list of paths.
    """
    queue = deque()
    result = []

    # Put the first city into the queue.
    queue.append((city1, set(city1), Path(set(), scoring)))

    while queue:
        city, visited, path = queue.popleft()

        # Add all neighbors to the queue.
        for outgoing_edge in city_edges[city]:
            other_city = outgoing_edge.other_city(city)

            if other_city not in visited and path.cost + outgoing_edge.cost <= max_cost:
                # Create a copy of the path thus far with the new edge added.
                updated_path = deepcopy(path)
                updated_path.add_edge(outgoing_edge, scoring)

                if other_city == city2:
                    # The updated path is a valid path between the two cities.
                    result.append(updated_path)
                else:
                    # Add the updated path and new city to the queue.
                    queue.append((other_city, visited.union(set(other_city)), updated_path))

    return result
