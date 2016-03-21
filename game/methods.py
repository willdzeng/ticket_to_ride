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

# def find_paths()