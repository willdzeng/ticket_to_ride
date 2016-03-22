from game import Hand
from classes import Colors


class Action:
    def __init__(self):
        pass

    def is_draw_deck(self):
        return False

    def is_draw_face_up(self):
        return False

    def is_connect(self):
        return False

    def is_draw_destination(self):
        return False


class DrawDeckAction(Action):
    def __init__(self):
        Action.__init__(self)

    def is_draw_deck(self):
        return True

    def __str__(self):
        return "Action: Draw from Deck"


class DrawFaceUpAction(Action):
    def __init__(self, index, card):
        Action.__init__(self)
        self.index = index
        # Card color is more for convenience.  Not actually used when determining the action.
        self.card = card

    def is_draw_face_up(self):
        return True

    def __str__(self):
        return "Action: Draw from Table(%s, %s)" % (str(self.index), Colors.str_card(self.card))


class ConnectAction(Action):
    def __init__(self, edge, cards):
        Action.__init__(self)
        self.edge = edge
        self.cards = cards

    def is_connect(self):
        return True

    def __str__(self):
        return "Action: Connect Cities(%s, %s)" % \
               (self.edge, Hand.cards_str(self.cards))

# TODO: New destination action
