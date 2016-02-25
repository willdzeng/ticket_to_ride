class Colors:
    """
    Used as an enum to hold possible color values.
    """
    red, orange, blue, yellow, green, pink, black, white, none = range(9)
    colors_list = ['Red', 'Orange', 'Blue', 'Yellow', 'Green', 'Pink', 'Black', 'White' 'None']

    @staticmethod
    def str(color):
        return Colors.colors_list[color] if len(Colors.colors_list) > color else 'None'


class City():
    def __init__(self, name, abbreviation):
        self.name = name
        self.abbreviation = abbreviation
        self.edges = []

    def to_tuple(self):
        return CityTuple(self.name, self.abbreviation, self.edges)


class CityTuple(tuple):
    def __new__(cls, name, abbreviation, edges):
        return tuple.__new__(cls, (name, abbreviation, tuple(edges)))

    def __str__(self):
        return self[0]

    def abbreviation(self):
        return self[1]

    def edges(self):
        return self[2]


class Edge:
    def __init__(self, city1, city2, cost, color):
        self.city1 = city1
        self.city2 = city2
        self.color = color
        self.cost = cost
        self.claimed_by = None
        city1.edges.append(self)
        city2.edges.append(self)

    def claim(self, player):
        self.claimed_by = player

    def other_city(self, city):
        if city == self.city1:
            return self.city2
        if city == self.city2:
            return self.city1
        return None

    def contains_city(self, city):
        return self.city1 == city or self.city2 == city

    def is_claimed(self):
        return self.claimed_by is not None

    def __str__(self):
        return "(%s, %s, %s, %s, %s)" % \
               (str(self.city1), str(self.city2), Colors.str(self.color), str(self.cost), str(self.claimed_by))


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
    def connected(city1, city2, player):
        """
        Perform a depth-first search to determine if 2 cities are connected by a route from a given player.

        :param city1: The first city.
        :param city2: The second city.
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

            for edge in city.edges:
                if edge.claimedBy == player:
                    other_city = edge.other_city(city)

                    # We're done if this is the other city
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
