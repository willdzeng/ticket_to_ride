from random import randrange

from game import Player, Game
from game.methods import find_paths_for_destinations
from game.board import create_board
from game.classes import FailureCause, Path
from game.actions import DrawDeckAction


class GreedyAI(Player):
    """
    AI that plays by finding the ideal path to all destinations that is affordable and maximizes score.  It will
    randomly claim edges in the best path until there are none left to claim, then it behaves randomly.  If it cannot
    claim any edges it wants, it will draw cards from the deck until it can.
    """
    def __init__(self, name):
        Player.__init__(self, name)
        self.city_edges, edges = create_board()

        self.sort_method = lambda path: path.score

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
            print game.cards_in_discard()
            actions = game.get_available_actions(self)
        elif game.get_remaining_actions(self) == 1:
            # Draw from the deck if that's the only option.
            actions = [DrawDeckAction()]
        else:
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
                actions = [DrawDeckAction()]

        # Randomly select the action from available actions.
        action_to_perform = actions[randrange(0, len(actions))]

        # Outputs
        print "Player %s: %s" % (self.name, game.get_player_info(self))
        print "Path: %s" % repr(path)
        print "Remaining edges: %s" % remaining_edges
        print "%s" % action_to_perform
        print "\n"

        # Perform action.
        action_result = game.perform_action(self, action_to_perform)

        # If the action fails, raise an exception indicating what went wrong.
        if not action_result[0]:
            raise Exception("Failure", "%s: %s" % (str(action_to_perform),
                                                   FailureCause.str(game.perform_action(self, action_to_perform)[1])))

    def game_ended(self, game):
        pass
