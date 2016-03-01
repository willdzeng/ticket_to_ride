import collections


class Colors:
    """
    Used as an enum to hold possible color values.
    """
    red, orange, blue, yellow, green, pink, black, white, none = range(9)
    colors_list = ['Red', 'Orange', 'Blue', 'Yellow', 'Green', 'Pink', 'Black', 'White' 'None']

    @staticmethod
    def str(color):
        return Colors.colors_list[color] if len(Colors.colors_list) > color else 'None'


class Edge(collections.namedtuple("Edge", "city1 city2 cost color")):
    def __new__(cls, city1, city2, cost, color):
        return tuple.__new__(cls, (city1, city2, cost, color))

    def other_city(self, city):
        if city == self.city1:
            return self.city2
        if city == self.city1:
            return self.city2
        return None

    def contains_city(self, city):
        return self.city1 == city or self.city2 == city

    def __str__(self):
        return "(%s, %s, %s, %s)" % (str(self.city1), str(self.city2), str(self.cost), Colors.str(self.color))


class Destination(collections.namedtuple("Destination", "city1 city2 value")):
    def __new__(cls, city1, city2, value):
        return tuple.__new__(cls, (city1, city2, value))


class Hand:
    def __init__(self, cards):
        self.cards = cards

    def add_card(self, card):
        self.cards.append(card)

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


class Player:
    """
    A player.  This is more a token to identify a player than anything else, since it contains no information.
    """

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class PlayerInfo:
    def __init__(self, hand, destinations, num_cars, score=0):
        self.score = score
        self.destinations = destinations
        self.hand = hand
        self.num_cars = num_cars
