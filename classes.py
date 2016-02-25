class Colors:
    """
    Used as an enum to hold possible color values.
    """
    red, orange, blue, yellow, green, pink, black, white, none = range(9)
    colors_list = ['Red', 'Orange', 'Blue', 'Yellow', 'Green', 'Pink', 'Black', 'White' 'None']

    @staticmethod
    def str(color):
        return Colors.colors_list[color] if len(Colors.colors_list) > color else 'None'


class Edge(tuple):
    def __new__(cls, city1, city2, cost, color):
        return tuple.__new__(cls, (city1, city2, cost, color))

    def other_city(self, city):
        if city == self[0]:
            return self[1]
        if city == self[1]:
            return self[0]
        return None

    def contains_city(self, city):
        return self[0] == city or self[1] == city

    def city1(self):
        return self[0]

    def city2(self):
        return self[1]

    def cost(self):
        return self[2]

    def color(self):
        return self[3]

    def __str__(self):
        return "(%s, %s, %s, %s)" % (str(self[0]), str(self[1]), str(self[2]), Colors.str(self[3]))


class Destination(tuple):
    def __new__(cls, city1, city2, value):
        return tuple.__new__(cls, (city1, city2, value))

    def city1(self):
        return self[0]

    def city2(self):
        return self[1]

    def value(self):
        return self[2]


class Player:
    """
    A player.  This is more a token to identify a player than anything else.
    """

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Methods:
    @staticmethod
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

        while visited:
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


class Hand:
    def __init__(self, cards):
        self.cards = cards

    def add_card(self, card):
        self.cards.add(card)

    def remove_card(self, card):
        if card in self.cards:
            self.cards.remove(card)

    def contains_cards(self, cards):
        # Duplicate the cards.
        hand_clone = list(self.cards)

        # Figure out which cards are in the hand, by removing them one at a time from the clone of the current hand.
        for card in cards:
            if card in hand_clone:
                hand_clone.remove(card)
            else:
                return False

        return True
