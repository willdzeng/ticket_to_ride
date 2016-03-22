from collections import namedtuple, Counter


class Colors:
    """
    Used as an enum to hold possible color values.
    """

    def __init__(self):
        pass

    red, orange, blue, yellow, green, pink, black, white, none = range(9)
    colors_list = ['Red', 'Orange', 'Blue', 'Yellow', 'Green', 'Pink', 'Black', 'White']

    @staticmethod
    def str(color):
        return Colors.colors_list[color] if len(Colors.colors_list) > color else 'None'

    @staticmethod
    def str_card(color):
        return Colors.colors_list[color] if len(Colors.colors_list) > color else 'Wild'


class FailureCause:
    def __init__(self):
        pass

    none, no_route, wrong_turn, missing_cards, incompatible_cards, already_drew, invalid_card_index, \
    insufficient_cars, game_over, deck_out_of_cards, no_action, incorrect_destinations = range(12)

    cause_list = ['None', 'No Route', "Wrong Turn", "Missing Cards", "Incompatible Cards", "Already Drew",
                  "Invalid Card Index", "Insufficient Cards", "Game Over", "Deck out of Cards", "No Action",
                  "Incorrect Destinations"]

    @staticmethod
    def str(failure_cause):
        return FailureCause.cause_list[failure_cause] if len(FailureCause.cause_list) > failure_cause else "Unknown"


class Edge(namedtuple("Edge", "city1 city2 cost color")):
    def __new__(cls, city1, city2, cost, color):
        return tuple.__new__(cls, (city1, city2, cost, color))

    def __init__(self, city1, city2, cost, color):
        super(Edge, self).__init__()

    def other_city(self, city):
        if city == self.city1:
            return self.city2
        if city == self.city2:
            return self.city1
        return None

    def contains_city(self, city):
        return self.city1 == city or self.city2 == city

    def __str__(self):
        return "(%s, %s, %s, %s)" % (str(self.city1), str(self.city2), str(self.cost), Colors.str(self.color))

    def __repr__(self):
        return str(self)


class Destination(namedtuple("Destination", "city1 city2 value")):
    def __new__(cls, city1, city2, value):
        return tuple.__new__(cls, (city1, city2, value))

    def __init__(self, city1, city2, value):
        super(Destination, self).__init__()

    def __str__(self):
        return "(%s, %s, %s)" % (str(self.city1), str(self.city2), str(self.value))


class Hand:
    def __init__(self, cards):
        self.cards = Counter(cards)

    def add_card(self, card):
        self.cards[card] += 1

    def remove_card(self, card):
        self.cards[card] = max(self.cards[card] - 1, 0)

    def contains_cards(self, cards):
        for card in cards:
            if self.cards[card] - cards[card] < 0:
                return False

        return True

    def __str__(self):
        return Hand.cards_str(self.cards)

    @staticmethod
    def cards_str(cards):
        return "(%s)" % ", ".join(map(Colors.str_card, [card for card in cards.elements()]))


class PlayerInfo:
    def __init__(self, hand, destinations, num_cars, score=0):
        self.score = score
        self.destinations = destinations
        self.completed_destinations = []
        self.hand = hand
        self.num_cars = num_cars

    def __str__(self):
        return "{\n\tPrivate Score: %s\n" \
               "\tHand: %s\n" \
               "\tCars Remaining: %s\n" \
               "\tDestinations: [%s]\n" \
               "\tCompleted Destinations: [%s]}" % (str(self.score), str(self.hand), str(self.num_cars),
                                                    ", ".join(map(str, self.destinations)),
                                                    ", ".join(map(str, self.completed_destinations)))


class Path:
    def __init__(self, edges, scoring, player=None, edge_claims=None):
        self.edges = edges
        self.cost = 0
        self.score = 0

        for edge in edges:
            # If the player owns the edge, then the there's no cost or score to the edge.
            if player is None or edge_claims is None or edge_claims[edge] != player.name:
                self.cost += edge.cost
                self.score += scoring[edge.cost]

    def add_edge(self, edge, scoring, player=None, edge_claims=None):
        self.edges.add(edge)

        # If the player owns the edge, then the there's no cost or score to the edge.
        if player is None or edge_claims is None or edge_claims[edge] != player.name:
            self.cost += edge.cost
            self.score += scoring[edge.cost]

    @staticmethod
    def default_sort_method(path):
        return path.cost

    def __repr__(self):
        return "(%s, %s, [%s])" % (str(self.cost), str(self.score),
                                   ", ".join(["(%s, %s)" % (edge.city1, edge.city2) for edge in self.edges]))
