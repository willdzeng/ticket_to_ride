from game.classes import Colors, Edge


class FailureCause:
    def __init__(self):
        pass

    none, no_route, wrong_turn, missing_cards, incompatible_cards, already_drew, invalid_card_index,\
    insufficient_cars, game_over, deck_out_of_cards, no_action, already_claim, insufficient_power = range(13)

    cause_list = ['None', 'No Such Route', "Wrong Turn", "Missing Cards", "Incompatible Cards", "Already Drew",
                  "Invalid Card Index", "Insufficient Cards", "Game Over", "Deck out of Cards", "No Action",
                  "Route already claimed", "Player Power Insufficient"]

    @staticmethod
    def str(failure_cause):
        return FailureCause.cause_list[failure_cause] if len(FailureCause.cause_list) > failure_cause else "Unknown"


class Route:
    def __init__(self, city1, city2, cost, color):
        self.owner = None  # record owner
        self.city1 = City(city1)
        self.city2 = City(city2)
        self.cost = cost
        self.color = color
        self.index = -1

    def claim(self, player):
        if self.owner is not None:
            return False, FailureCause.already_claim
        self.owner = player.name
        return True

    def __str__(self):
        return "(%s, %s, %s, %s, %s, %s)" % (str(self.city1.name), str(self.city2.name),
                                             str(self.cost), Colors.str(self.color), str(self.index),
                                             str(self.owner))


class City:
    def __init__(self, name):
        self.name = name
        self.neighbors = []  # store the neighbor city
        self.routes = []  # store the routes connected to the neighbor city

    # add route into the city and automatically add the corespondent city
    def add_route(self, route):
        if route not in self.routes:
            if self != route.city1 and self != route.city2:
                return False
            self.routes += [route]
            if self == route.city1:
                # add duplicated city for easy accessing
                self.neighbors += [route.city2]
            if self == route.city2:
                self.neighbors += [route.city1]
        return True

    def __str__(self):
        route_string = ""
        neighbor_string = ""
        for route in self.routes:
            route_string += "%d " % route.index
        for neighbor in self.neighbors:
            neighbor_string += "%s, " % (str(neighbor.name))
        return "(City name: %s\n Neighbor Cities: %s\n Routes Connected: %s)\n" \
               % (str(self.name), neighbor_string, route_string)


def create_cites(routes):
    cities = []

    # Get all city instances, and put input list
    for route_index, route in enumerate(routes):
        route.index = route_index
        city1_added = False
        city2_added = False
        for city in cities:
            if route.city1.name == city.name:
                route.city1 = city
                city1_added = True
            if route.city2.name == city.name:
                route.city2 = city
                city2_added = True
        if city1_added is False:
            cities += [route.city1]
        if city2_added is False:
            cities += [route.city2]

    # Create the connectivity graph between cities, don't emerge with the for loop above
    for route in routes:
        for city in cities:
            if route.city1 == city or route.city2 == city:
                if not city.add_route(route):
                    return False, "can't add route, something wrong"
    return cities


def create_routes(edges):
    routes = []
    for edge in edges:
        routes += [Route(edge.city1, edge.city2, edge.cost, edge.color)]
    return routes
