from random import randrange

from game import Player, Game
from game.methods import find_paths_for_destinations
from game.board import create_board
from game.classes import FailureCause, Path
from game.actions import DrawDeckAction

#TODO: Only recalculate if route is taken by opponent.
class GreedyAI(Player):
    """
    AI that plays by finding the ideal path to all destinations that is affordable and maximizes score.  It will
    randomly claim edges in the best path until there are none left to claim, then it behaves randomly.  If it cannot
    claim any edges it wants, it will draw cards from the deck until it can.
    """
    def __init__(self, name):
        Player.__init__(self, name)
        self.city_edges, edges = create_board()

        self.sort_method = lambda path: -path.score

    def take_turn(self, game):
        info = game.get_player_info(self)
        edge_claims = game.get_edge_claims()
        remaining_edges = []
        path = None

        # Get all paths.
        all_paths = find_paths_for_destinations(info.destinations, self.city_edges, info.num_cars, player=self,
                                                edge_claims=edge_claims, sort_method=self.sort_method)

        if not all_paths or game.cards_in_deck() == 0:
            # Random action for now when no paths remain to check.
            # TODO: Instead of behaving randomly, try to get the edges that will get you the most points.
            actions = self.on_no_more_destinations(game)
        elif game.get_remaining_actions(self) == 1:
            # Draw from the deck if that's the only option.
            actions = self.on_already_drew(game)
        else:
            # Try to take an edge.
            path = all_paths[0]

            actions = []

            # Pick an edge in the path and try to take it.
            for edge in path.edges:
                if edge_claims[edge] != self.name:
                    connection_actions = Game.all_connection_actions(edge, info.hand.cards)

                    # Using the first possible action means we will try the action that uses the least wilds.
                    if connection_actions:
                        actions.append(connection_actions[0])

                    remaining_edges.append(edge)

            # No actions, just draw randomly.
            if not actions:
                actions = self.on_not_enough_cards(game)

        # Randomly select the action from available actions.
        return actions[randrange(0, len(actions))]

    def game_ended(self, game):
        pass

    def path_cost(self, path, all_paths, game):
        return path.cost

    def on_not_enough_cards(self, game):
        """
        Executes when there aren't enough cards to play anything.

        :param game: The game object.
        :return: The actions to perform.  Will randomly pick from the list of actions.
        """
        return [DrawDeckAction()]

    def on_no_more_destinations(self, game):
        """
        Executes when there are no more destinations for the player to play.

        :param game: The game object.
        :return: The action(s) to perform.  Will randomly pick from the list of actions.
        """
        return game.get_available_actions(self)

    def on_already_drew(self, game):
        """
        Executes when it's this player's turn but they already drew.

        :param game: The game object.
        :return: The actions to perform.  Will randomly pick from the list of actions.
        """
        return [DrawDeckAction()]

    # TODO: Overwrite debug_print
