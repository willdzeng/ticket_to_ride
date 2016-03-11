class Player:
    """
    A player.  In addition to being a token that allows moves to happen, also has events that trigger on certain game
    states.
    """

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    # TODO: Test.
    def take_turn(self, game):
        pass

    # TODO: Test.
    def game_ended(self, game):
        pass
