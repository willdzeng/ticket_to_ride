from classes import Edge, Colors


cities = ("Atlanta",
          "Boston",
          "Calgary",
          "Charleston",
          "Chicago",
          "Dallas",
          "Denver",
          "Duluth",
          "El Paso",
          "Helena",
          "Houston",
          "Kansas City",
          "Las Vegas",
          "Little Rock",
          "Los Angeles",
          "Miami",
          "Montreal",
          "Nashville",
          "New Orleans",
          "New York",
          "Oklahoma City",
          "Omaha",
          "Phoenix",
          "Pittsburgh",
          "Portland",
          "Raleigh",
          "Saint Louis",
          "Salt Lake City",
          "San Francisco",
          "Santa Fe",
          "Sault St. Marie",
          "Seattle",
          "Toronto",
          "Vancouver",
          "Washington DC",
          "Winnipeg",
          )


def create_board():
    """
    Initializes the entirety of the board state.
    """
    # Create all the edges between cities.
    edges = [
        Edge("Atlanta", "Charleston", cost=2, color=Colors.none),
        Edge("Atlanta", "Miami", cost=5, color=Colors.blue),
        Edge("Atlanta", "Nashville", cost=1, color=Colors.none),
        Edge("Atlanta", "New Orleans", cost=4, color=Colors.orange),
        Edge("Atlanta", "New Orleans", cost=4, color=Colors.yellow),
        Edge("Atlanta", "Raleigh", cost=2, color=Colors.none),
        Edge("Boston", "Montreal", cost=2, color=Colors.none),
        Edge("Boston", "Montreal", cost=2, color=Colors.none),
        Edge("Boston", "New York", cost=2, color=Colors.red),
        Edge("Boston", "New York", cost=2, color=Colors.yellow),
        Edge("Calgary", "Helena", cost=4, color=Colors.none),
        Edge("Calgary", "Seattle", cost=4, color=Colors.none),
        Edge("Calgary", "Vancouver", cost=3, color=Colors.none),
        Edge("Calgary", "Winnipeg", cost=6, color=Colors.white),
        Edge("Charleston", "Miami", cost=4, color=Colors.pink),
        Edge("Charleston", "Raleigh", cost=1, color=Colors.none),
        Edge("Chicago", "Duluth", cost=3, color=Colors.red),
        Edge("Chicago", "Omaha", cost=4, color=Colors.blue),
        Edge("Chicago", "Pittsburgh", cost=3, color=Colors.black),
        Edge("Chicago", "Pittsburgh", cost=3, color=Colors.orange),
        Edge("Chicago", "Saint Louis", cost=2, color=Colors.green),
        Edge("Chicago", "Saint Louis", cost=2, color=Colors.white),
        Edge("Chicago", "Toronto", cost=4, color=Colors.white),
        Edge("Dallas", "El Paso", cost=4, color=Colors.red),
        Edge("Dallas", "Houston", cost=1, color=Colors.none),
        Edge("Dallas", "Houston", cost=1, color=Colors.none),
        Edge("Dallas", "Little Rock", cost=2, color=Colors.none),
        Edge("Dallas", "Oklahoma City", cost=2, color=Colors.none),
        Edge("Dallas", "Oklahoma City", cost=2, color=Colors.none),
        Edge("Denver", "Helena", cost=4, color=Colors.green),
        Edge("Denver", "Kansas City", cost=4, color=Colors.black),
        Edge("Denver", "Kansas City", cost=4, color=Colors.orange),
        Edge("Denver", "Oklahoma City", cost=4, color=Colors.red),
        Edge("Denver", "Omaha", cost=4, color=Colors.pink),
        Edge("Denver", "Phoenix", cost=4, color=Colors.white),
        Edge("Denver", "Salt Lake City", cost=3, color=Colors.red),
        Edge("Denver", "Salt Lake City", cost=3, color=Colors.yellow),
        Edge("Denver", "Santa Fe", cost=2, color=Colors.none),
        Edge("Duluth", "Helena", cost=6, color=Colors.orange),
        Edge("Duluth", "Omaha", cost=2, color=Colors.none),
        Edge("Duluth", "Omaha", cost=2, color=Colors.none),
        Edge("Duluth", "Sault St. Marie", cost=3, color=Colors.none),
        Edge("Duluth", "Toronto", cost=6, color=Colors.pink),
        Edge("Duluth", "Winnipeg", cost=4, color=Colors.black),
        Edge("El Paso", "Houston", cost=6, color=Colors.green),
        Edge("El Paso", "Los Angeles", cost=6, color=Colors.black),
        Edge("El Paso", "Oklahoma City", cost=5, color=Colors.yellow),
        Edge("El Paso", "Phoenix", cost=3, color=Colors.none),
        Edge("El Paso", "Santa Fe", cost=2, color=Colors.none),
        Edge("Helena", "Calgary", cost=4, color=Colors.none),
        Edge("Helena", "Omaha", cost=5, color=Colors.red),
        Edge("Helena", "Seattle", cost=6, color=Colors.yellow),
        Edge("Helena", "Winnipeg", cost=4, color=Colors.blue),
        Edge("Houston", "New Orleans", cost=2, color=Colors.none),
        Edge("Kansas City", "Oklahoma City", cost=2, color=Colors.none),
        Edge("Kansas City", "Oklahoma City", cost=2, color=Colors.none),
        Edge("Kansas City", "Omaha", cost=1, color=Colors.none),
        Edge("Kansas City", "Omaha", cost=1, color=Colors.none),
        Edge("Kansas City", "Saint Louis", cost=2, color=Colors.blue),
        Edge("Kansas City", "Saint Louis", cost=2, color=Colors.pink),
        Edge("Las Vegas", "Los Angeles", cost=2, color=Colors.none),
        Edge("Las Vegas", "Salt Lake City", cost=3, color=Colors.orange),
        Edge("Little Rock", "Nashville", cost=3, color=Colors.white),
        Edge("Little Rock", "New Orleans", cost=3, color=Colors.green),
        Edge("Little Rock", "Oklahoma City", cost=2, color=Colors.none),
        Edge("Little Rock", "Saint Louis", cost=2, color=Colors.none),
        Edge("Los Angeles", "Phoenix", cost=2, color=Colors.black),
        Edge("Los Angeles", "San Francisco", cost=3, color=Colors.pink),
        Edge("Los Angeles", "San Francisco", cost=3, color=Colors.yellow),
        Edge("Miami", "New Orleans", cost=6, color=Colors.red),
        Edge("Montreal", "New York", cost=3, color=Colors.blue),
        Edge("Montreal", "Sault St. Marie", cost=5, color=Colors.black),
        Edge("Montreal", "Toronto", cost=3, color=Colors.none),
        Edge("Nashville", "Pittsburgh", cost=4, color=Colors.yellow),
        Edge("Nashville", "Raleigh", cost=3, color=Colors.black),
        Edge("Nashville", "Saint Louis", cost=2, color=Colors.none),
        Edge("New York", "Pittsburgh", cost=2, color=Colors.green),
        Edge("New York", "Pittsburgh", cost=2, color=Colors.white),
        Edge("New York", "Washington DC", cost=2, color=Colors.black),
        Edge("New York", "Washington DC", cost=2, color=Colors.orange),
        Edge("Phoenix", "Santa Fe", cost=3, color=Colors.none),
        Edge("Pittsburgh", "Saint Louis", cost=5, color=Colors.green),
        Edge("Portland", "Salt Lake City", cost=6, color=Colors.blue),
        Edge("Portland", "San Francisco", cost=5, color=Colors.green),
        Edge("Portland", "San Francisco", cost=5, color=Colors.pink),
        Edge("Portland", "Seattle", cost=1, color=Colors.none),
        Edge("Portland", "Seattle", cost=1, color=Colors.none),
        Edge("Raleigh", "Washington DC", cost=2, color=Colors.none),
        Edge("Salt Lake City", "San Francisco", cost=5, color=Colors.orange),
        Edge("Salt Lake City", "San Francisco", cost=5, color=Colors.white),
        Edge("Sault St. Marie", "Toronto", cost=2, color=Colors.none),
        Edge("Sault St. Marie", "Winnipeg", cost=6, color=Colors.none),
        Edge("Seattle", "Vancouver", cost=1, color=Colors.none),
    ]

    return create_city_edges(edges), edges


def create_city_edges(edges):
    city_edges = {}

    # Map cities to edges.
    for edge in edges:
        if edge.city1 not in city_edges:
            city_edges[edge.city1] = ()
        if edge.city2 not in city_edges:
            city_edges[edge.city2] = ()

        city_edges[edge.city1] = city_edges[edge.city1] + (edge,)
        city_edges[edge.city2] = city_edges[edge.city2] + (edge,)

    return city_edges


def get_scoring():
    # Create a dictionary for scoring.
    return {1: 1,
            2: 2,
            3: 4,
            4: 7,
            5: 10,
            6: 15}
