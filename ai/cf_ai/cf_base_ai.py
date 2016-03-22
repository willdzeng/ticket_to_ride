from random import randrange

from game import Player, Game
from game.methods import find_paths_for_destinations
from game.board import create_board
from game.actions import DrawDeckAction


# TODO: Only recalculate if route is taken by opponent.
class CFBaseAI(Player):
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
        Player.__init__(self, name)
        self.city_edges, edges = create_board()
        self.path = None
        self.path_costs = {}
        self.edge_costs = {}
        self.all_paths = []

    def take_turn(self, game):
        info = game.get_player_info(self)
        edge_claims = game.get_edge_claims()

        last_actions = game.get_last_actions()
        last_action = last_actions[0] if last_actions else None

        # Get the costs for all edges.
        for edge in edge_claims:
            if edge_claims[edge] == self.name:
                self.edge_costs[edge] = 0
            else:
                self.edge_costs[edge] = self.edge_cost(edge, self.all_paths, game)

        # Get the path to work with only if it either does not exist or one of the old path's routes has been taken.
        if self.path is None or \
                (last_action is not None and last_action.is_connect() and last_action.edge in self.path.edges):

            # Get all paths.
            self.all_paths = find_paths_for_destinations(info.destinations, self.city_edges, info.num_cars, player=self,
                                                         edge_claims=edge_claims, sort_paths=False)

            # Get the costs for all paths.
            for path in self.all_paths:
                self.path_costs[path] = self.path_cost(path, self.all_paths, self.edge_costs, game)

            self.all_paths.sort(key=lambda path: self.path_costs[path])

            if self.all_paths:
                self.path = self.all_paths[0]

        if not self.path or not info.destinations or game.cards_in_deck() == 0:
            # Perform correct action when no more destinations are left to take.
            actions = self.on_no_more_destinations(game)
        elif game.get_remaining_actions(self) == 1:
            # Perform correct action when the player has already drawn.
            actions = self.on_already_drew(game)
        else:
            # Pick an edge in the path and try to take it.
            actions = self.on_select_edge(self.path, self.edge_costs, game)

            # Perform correct action when the player doesn't have enough cards to connect any edge.
            if not actions:
                actions = self.on_cant_select_edge(game)

        # Randomly select the action from available actions.
        action = actions[randrange(0, len(actions))]

        return action

    def game_ended(self, game):
        pass

    def path_cost(self, path, all_paths, edge_costs, game):
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

    def edge_cost(self, edge, all_paths, game):
        """
        Determine the cost of an individual edge.  Note that this is only called on edges that aren't already
        claimed by the player.  Edges claimed by the player have cost 0 automatically, and won't have this function
        called.

        :param edge: The edge to calculate cost for.
        :param all_paths: The list of all paths.
        :param game: The game object.
        :return: An integer for the cost of the edge.  Lower numbers mean the edge is more favorable to select.
        """
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

        edge_claims = game.get_edge_claims()
        info = game.get_player_info(self)

        for edge in self.path.edges:
            if edge_claims[edge] != self.name:
                connection_actions = Game.all_connection_actions(edge, info.hand.cards)

                # Using the first possible action means we will try the action that uses the least wilds.
                if connection_actions:
                    actions.append(connection_actions[0])

        return actions

    def on_cant_select_edge(self, game):
        """
        Executes when there aren't enough cards to play anything.

        :param game: The game object.
        :return: The actions to perform.  Will randomly pick from the list of actions.
        """
        # Default: Draw randomly.
        return [DrawDeckAction()]

    def on_no_more_destinations(self, game):
        """
        Executes when there are no more destinations for the player to play.

        :param game: The game object.
        :return: The action(s) to perform.  Will randomly pick from the list of actions.
        """
        # Default: Play randomly.
        # TODO: Instead of behaving randomly, try to get the edges that will get you the most points.
        return game.get_available_actions(self)

    def on_already_drew(self, game):
        """
        Executes when it's this player's turn but they already drew.

        :param game: The game object.
        :return: The actions to perform.  Will randomly pick from the list of actions.
        """
        return [DrawDeckAction()]

    def debug_print(self, game):
        remaining_edges = self.path.edges - game.get_edges_for_player(self) if self.path is not None else []

        return "Path:%s\nRemaining Edges: [%s]" % (str(self.path), ", ".join([str(edge) for edge in remaining_edges]))
