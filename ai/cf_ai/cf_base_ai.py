from random import randrange

from game import Player, Game
from game.actions import *
from game.board import create_board
from game.methods import find_paths_for_destinations


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
        self.info = None

    def take_turn(self, game):

        # update game state first
        self.info = game.get_player_info(self)
        self.edge_claims = game.get_edge_claims()

        # the first thing to check is if we already drew.
        # then we don't need to calculate anything but draw another card
        if game.get_remaining_actions(self) == 1:
            action = self.on_already_drew(game)
            return action[0]

        edge_claims = self.edge_claims
        info = self.info

        # Get the costs for all edges.
        for edge in edge_claims:
            if edge_claims[edge] == self.name:
                self.edge_costs[edge] = 0
            else:
                self.edge_costs[edge] = self.eval_edge(edge, self.all_paths, game)

        # Make sure that none of the edges in the path have been taken by an opponent.
        path_clear = True

        if self.path is not None:
            for edge in self.path.edges:
                if edge_claims[edge] != self.name and edge_claims[edge] is not None:
                    path_clear = False

        # Get the path to work with only if it either does not exist or one of the old path's routes has been taken.
        if self.path is None or not path_clear:
            self.path, self.all_paths = self.find_best_path(game, info.destinations)

        # if we can't get a path after re-calculate then we need to decide if we want to draw a new destination card
        # TODO: need to discuss what should we do if the path search can't find a path but we still have tickets card
        if not self.path or not info.destinations:
            print "AI: no path found"
            # Perform correct action when no more destinations are left to take.
            actions = self.on_no_more_destinations(game)
        else:
            # Pick an edge in the path and try to take it.
            actions = self.on_select_edge(self.path, self.edge_costs, game)

            # Perform correct action when the player doesn't have enough cards to connect any edge.
            if not actions:
                actions = self.on_cant_select_edge(game)

        # Randomly select the action from available actions.
        action = actions[randrange(0, len(actions))]

        return action

    def find_best_path(self, game, destinations):
        """
        Find the best path of giving destination cards based on the cost function
        :param game: the game
        :param destinations: the destination card
        :return: return the best path
        """
        path = None

        info = self.info
        edge_claims = self.edge_claims

        # Get all paths.
        all_paths = find_paths_for_destinations(destinations, self.city_edges, info.num_cars, player=self,
                                                edge_claims=edge_claims, sort_paths=False)
        path_costs = {}
        # Get the costs for all paths.
        for path in all_paths:
            path_costs[path] = self.eval_path(path, all_paths, self.edge_costs, game)

        all_paths.sort(key=lambda path: path_costs[path])

        if all_paths:
            path = all_paths[0]

        return path, all_paths

    def game_ended(self, game):
        pass

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

        edge_claims = self.edge_claims
        info = self.info

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
        return self.draw_best_card(game)

    def draw_best_card(self, game):
        """
        Draw the best card based on the path we planned.
        :param game:
        :return:
        """
        # TODO: need to add draw face up card based on the current path.

        return [DrawDeckAction()]

    def on_no_more_destinations(self, game):
        """
        Executes when there are no more destinations for the player to play.

        :param game: The game object.
        :return: The action(s) to perform.  Will randomly pick from the list of actions.
        """
        # Default: Play randomly.
        # TODO: Need to figure out a rule of when to draw destination card

        if self.info.num_cars > 1:
            action = [DrawDestinationAction()]
        else:
            action = self.draw_best_card(game)

        return action

    def on_already_drew(self, game):
        """
        Executes when it's this player's turn but they already drew.

        :param game: The game object.
        :return: The actions to perform.  Will randomly pick from the list of actions.
        """
        return self.draw_best_card(game)

    def select_destinations(self, game, destinations):
        """
        Selects up to three but at least one of the the destinations this player has drawn.

        :param destinations: A list of the destinations to select from.
        :return: A sub-list of the destinations passed in with at least one element.
        """
        # TODO: Need to add rules to select destination after finished all the destination card
        destination_cost = []

        for destination in destinations:
            path, all_path = self.find_best_path(game, [destination])
            if path is None:
                destination_cost.append(100)
            else:
                destination_cost.append(path.cost)

        index = destination_cost.index(min(destination_cost))
        selected_destinations = destinations[index]
        # # randomly select one destination card
        # selected_destinations = destinations[randrange(0, len(destinations))]

        return [selected_destinations]

    def select_starting_destinations(self, game, destinations):
        """
        Selects up to three but at least one of the the destinations this player has drawn.

        :param destinations: A list of the destinations to select from.
        :return: A sub-list of the destinations passed in with at least one element.
        """
        # TODO: Need to add rules to select destination at the beginning of the game
        selected_destinations = destinations

        return selected_destinations

    def debug_print(self, game):
        remaining_edges = self.path.edges - game.get_edges_for_player(self) if self.path is not None else []

        return "Path:%s\nRemaining Edges: [%s]" % (str(self.path), ", ".join([str(edge) for edge in remaining_edges]))
