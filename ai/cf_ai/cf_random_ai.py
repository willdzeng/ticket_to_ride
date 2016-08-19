from random import randrange

import game.board as board
from game import Player, Game
from game.actions import *
from game.classes import Colors
from game.methods import find_paths_for_destinations
from cf_base_ai import CFBaseAI
class CFRandomAI(CFBaseAI):
    """
    AI that plays by finding the ideal path to all destinations that is affordable and maximizes a predefined cost
    function.  It will randomly claim edges in the best path until there are none left to claim, then it behaves
    randomly.  If it cannot claim any edges it wants, it will draw cards from the deck until it can.

    The functions to extend when overwriting this class are `path_cost` and `edge_cost`, which determine the
    special costs of all edges and paths.  The selected path will be the lowest cost path, until one of the edges in
    that path is taken by an opponent.

    All methods starting with "on" (`on_select_edge`, `on_cant_select_edge`, `on_no_more_destinations`,
    and `on_already_drew`) can also
    be overridden, and correspond to the behavior under certain conditions when taking an edge is not possible.
    """

    def __init__(self, name):
        CFBaseAI.__init__(self, name)


    def eval_path(self, path, all_paths, edge_costs, game):
        """
        Determine the cost of an individual path.  Note that this is called only after all of the edges have a cost.

        :param path: The path to calculate cost for.
        :param all_paths: The list of all paths.
        :param edge_costs: A dictionary containing the costs of all edges.  The key is an edge and the value is it's
        cost.  Edges claimed by the player will have 0 cost.
        :param game: The game object.
        :return: An integer for the cost of the path.  Lower numbers mean the path is more likely to be selected.
        """
        return - path.score

    def eval_edge(self, edge, all_paths, game):
        """
        Determine the cost of an individual edge.  Note that this is only called on edges that aren't already
        claimed by the player.  Edges claimed by the player have cost 0 automatically, and won't have this function
        called.

        :param edge: The edge to calculate cost for.
        :param all_paths: The list of all paths.
        :param game: The game object.
        :return: An integer for the cost of the edge.  Lower numbers mean the edge is more favorable to select.
        """
        # calculate
        return edge.cost

    def on_select_edge(self, path, edge_costs, game):
        """
        Executes when it's time to select which edge on the path to take.

        :param game: The game object.
        :return: The actions to perform.  Will randomly pick from the list of actions.  If list is empty,
        will call `on_cant_select_edge`.
        """
        # Default: Select random edge that is playable.

        actions = []
        best_action =[]

        edge_claims = self.edge_claims
        info = self.info

        for edge in self.path.edges:
            if edge_claims[edge] != self.name:
                connection_actions = Game.all_connection_actions(edge, info.hand.cards, info.num_cars)

                # Using the first possible action means we will try the action that uses the least wilds.
                if connection_actions:
                    actions.append(connection_actions[0])
        if actions:
            best_action.append(actions[randrange(0, len(actions))])

        # return actions
        return best_action

    def draw_best_card(self, game):
        """
        Draw the best card based on the path we planned.
        :param game:
        :return:
        """
        action = DrawDeckAction()
        return [action]