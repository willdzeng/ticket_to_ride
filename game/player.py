class Player:
    """
    A player.  In addition to being a token that allows moves to happen, also has events that trigger on certain game
    states.
    """

    def __init__(self, name, print_debug=False):
        self.name = name
        self.print_debug = print_debug

    def __str__(self):
        return self.name

    def initialize_game(self,game):
        pass

    def take_turn(self, game):
        pass

    def game_ended(self, game):
        pass

    def debug_print(self, game):
        """
        Prints extra debug information.

        :param game:
        :return: A string to print with debug information.
        """
        return ""

    def on_action_complete(self, game, result):
        """
        A callback that is performed on the player after the player performs an action.

        :param game:
        :param result: The result of the action, which will be a tuple with a boolean for success and a failure cause.
        """
        pass

    def select_destinations(self, game, destinations):
        """
        Selects up to three but at least one of the the destinations this player has drawn.

        :param game:
        :param destinations: A list of the destinations to select from.
        :return: A sublist of the destinations passed in with at least one element.
        """
        # TODO: In game, make sure that the returned destinations were in the parameter

        return destinations

    def select_starting_destinations(self, game, destinations):
        """
        Selects up to three but at least one of the the destinations this player has drawn.

        :param game:
        :param destinations: A list of the destinations to select from.
        :return: A sublist of the destinations passed in with at least one element.
        """
        # TODO: In game, make sure that the returned destinations were in the parameter
        return destinations
