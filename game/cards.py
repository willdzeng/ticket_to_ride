from random import shuffle

from classes import Destination


def init_decks():
    """
    Initializes all decks
    """
    destinations = [
        Destination("Dallas", "New York", 11),
        Destination("Portland", "Phoenix", 11),
        Destination("Vancouver", "Santa Fe", 13),
        Destination("Seattle", "New York", 22),
        Destination("Montreal", "Atlanta", 9),
        Destination("Toronto", "Miami", 10),
        Destination("Boston", "Miami", 12),
        Destination("Los Angeles", "Chicago", 16),
        Destination("Winnipeg", "Houston", 12),
        Destination("Denver", "El Paso", 4),
        Destination("Duluth", "Houston", 8),
        Destination("San Francisco", "Atlanta", 17),
        Destination("Denver", "Pittsburgh", 11),
        Destination("Sault St. Marie", "Nashville", 8),
        Destination("Winnipeg", "Little Rock", 11),
        Destination("Duluth", "El Paso", 10),
        Destination("Seattle", "Los Angeles", 9),
        Destination("Helena", "Los Angeles", 8),
        Destination("Kansas City", "Houston", 5),
        Destination("Sault St. Marie", "Oklahoma City", 9),
        Destination("Portland", "Nashville", 17),
        Destination("Los Angeles", "New York", 21),
        Destination("Chicago", "Santa Fe", 9),
        Destination("Calgary", "Phoenix", 13),
        Destination("Calgary", "Salt Lake City", 7),
        Destination("Vancouver", "Montreal", 20),
        Destination("Los Angeles", "Miami", 20),
        Destination("Chicago", "New Orleans", 7),
        Destination("New York", "Atlanta", 6),
        Destination("Montreal", "New Orleans", 13)
    ]
    shuffle(destinations)
    deck = shuffle_deck()

    return deck, destinations

def shuffle_deck():
    # Initialize the deck to have 12 of each color and 14 wild cards (which are just cards colored "None").
    deck = [color for color in range(8)] * 12 + [8] * 14
    shuffle(deck)
    return deck