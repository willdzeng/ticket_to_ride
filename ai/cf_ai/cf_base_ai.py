from random import randrange

import game.board as board
from game import Player, Game
from game.actions import *
from game.classes import Colors
from game.methods import find_paths_for_destinations


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
    Edge_Color_Multiplier = 8 # used when calculate how much a edge cost when it's color is not none
    Edge_Score_Multiplier = 0.1 # used to reward a edge based on it's score
    Wild_Card_Cost = 8 # used when claiming routes, how much this claiming action cost when it's using wild card
    Wild_Card_Value = 3 # used when selecting the best cards to evaluate how much a wild card values
    Ticket_Score_Multiplier = 2 # used when selecting ticket
    debug = True # enable to print more debug stuff

    def __init__(self, name):
        Player.__init__(self, name)
        self.city_edges, self.edges = board.create_board()
        self.path = None
        self.path_costs = {}
        self.edge_costs = {}
        self.all_paths = []
        self.info = None
        self.edge_claims = None

    def take_turn(self, game):

        # update game state first
        self.info = game.get_player_info(self)
        self.edge_claims = game.get_edge_claims()
        self.available_actions = game.get_available_actions(self)
        self.face_up_cards = game.get_face_up_cards()
        self.action_remaining = game.get_remaining_actions(self)
        # the first thing to check is if we already drew.
        # then we don't need to calculate anything but draw another card
        if self.action_remaining == 1:
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
        # if we have destination cards, plan a path based on them
        if info.destinations:
            if self.path is None or not path_clear:
                self.path, self.all_paths = self.find_best_path(game, info.destinations)
        else:  # else we don't have path
            self.path = None

        # TODO: need to discuss what should we do if the path search can't find a path but we still have tickets card
        # TODO: Put print statements into separate method.  Maybe have 2 different debug prints?
        if self.debug: print "Path: %s" % self.path
        if self.debug: print "Path is clear" if path_clear else "Path is not clear"
        # if we can't get a path after re-calculate then we need to decide if we want to draw a new destination card
        if self.path is None:
            if self.debug: print "#############AI: no path found##############"
            # Perform correct action when no path is found
            actions = self.on_cant_find_path(game)
        else:
            # Pick an edge in the path and try to take it.
            actions = self.on_select_edge(self.path, self.edge_costs, game)

            # for action in actions:
            #     print action

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
        all_paths = []

        # if there is no destination card, return None
        if not destinations:
            return path, all_paths

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
        cost = 0
        for edge in path.edges:
            cost += self.eval_edge(edge, all_paths, game)

        # return - path.score
        return cost

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
        if edge.color == Colors.none:
            Kcolor = 1
        else:
            Kcolor = self.Edge_Color_Multiplier
        # color cost
        cost = Kcolor * edge.cost
        # score reward
        cost -= self.Edge_Score_Multiplier * board.get_scoring()[edge.cost]

        return cost

    def on_select_edge(self, path, edge_costs, game):
        """
        Executes when it's time to select which edge on the path to take.

        :param game: The game object.
        :return: The actions to perform.  Will randomly pick from the list of actions.  If list is empty, 
        will call `on_cant_select_edge`.
        """
        # Default: Select random edge that is playable.

        edge_claims = self.edge_claims
        info = self.info

        all_connection_actions = []

        cards_needed = self.get_cards_needed(self.path)

        # get all the connection action first
        for edge in self.path.edges:

            # if edge_claims[edge] != self.name:
            if edge_claims[edge] is None:
                connection_actions = Game.all_connection_actions(edge, info.hand.cards, info.num_cars)

                # Using the first possible action means we will try the action that uses the least wilds.
                if connection_actions:
                    all_connection_actions += connection_actions

        best_action = []
        # if we have any connection action, we choose the best one
        if all_connection_actions:
            # evaluate every action based on a cost function
            min_index = 0
            min_cost = 100000
            for index, action in enumerate(all_connection_actions):
                cost = 0
                for card in action.cards:
                    if card == Colors.none:
                        cost += self.Wild_Card_Cost
                    else:
                        cost += cards_needed[card]
                cost -= self.Edge_Score_Multiplier * board.get_scoring()[action.edge.cost]
                if self.debug: print action, "has cost", cost
                if cost < min_cost:
                    min_cost = cost
                    min_index = index

            best_action = [all_connection_actions[min_index]]

        # return actions
        return best_action

    def get_cards_needed(self,path):
        """
        get the cards needed of giving path
        :param path: the path to evaluate
        :return: the cards dictionary {card_index : number_of_cards}
        """
        cards_needed = {i:0 for i in range(9)}
        if path is not None:
            for edge in path.edges:
                cards_needed[edge.color] += edge.cost
        return cards_needed

    def on_cant_find_path(self, game):
        """
        Execute when it can't find any path
        :param game:
        :return: the actions to perform, list of action
        """
        best_action = []
        draw_ticket_action = []

        # if we don't have enough destination, we will see if we want to draw a ticket or not
        if not self.info.destinations:
            draw_ticket_action = self.on_no_more_destinations(game)
        # TODO: need to discuss if we want to draw a ticket card, but there are routes claimable, should we claim
        # if we want to draw a ticket card then draw it.
        if draw_ticket_action:
            return draw_ticket_action

        # get all the connection action first
        connect_action = []
        for action in self.available_actions:
            if action.is_connect():
                connect_action.append(action)

        # if we have any connection action, find the best one
        if connect_action:
            # choose the best connection action based on how much score it has
            maximum_score = 0
            best_action_index = 0
            for index, action in enumerate(connect_action):
                score = action.edge.cost
                if score > maximum_score:
                    maximum_score = score
                    best_action_index = index
            best_action = [connect_action[best_action_index]]

        # if we still can't find a good action, then just draw the best card
        if not best_action:
            best_action = self.draw_best_card(game)

        return best_action

    def on_cant_select_edge(self, game):
        """
        Executes when there aren't enough cards to play anything.

        :param game: The game object.
        :return: The actions to perform.  Will randomly pick from the list of actions.
        """
        return self.draw_best_card(game)

    def on_no_more_destinations(self, game):
        """
        Executes when there are no more destinations for the player to play.

        :param game: The game object.
        :return: The action(s) to perform.  Will randomly pick from the list of actions.
        """
        # Default: Play randomly.
        # TODO: Need to figure out a rule of when to draw destination card
        action = []
        if self.info.num_cars > 20:
            action = [DrawDestinationAction()]
        # else:
        #     action = self.draw_best_card(game)

        return action

    def on_already_drew(self, game):
        """
        Executes when it's this player's turn but they already drew.

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
        cards_needed = self.get_cards_needed(self.path)
        values = []
        if cards_needed:
            for card in self.face_up_cards:
                # if the card is a wild card
                if card == Colors.none:
                    # if we don't have 2 action point
                    if self.action_remaining == 1:
                        # append -1 so that it won't choose it at all
                        values.append(-1)
                        continue
                    else:
                        values.append(self.Wild_Card_Value)
                else:
                    values.append(cards_needed[card])
            best_card_index = values.index(max(values))
            action = DrawFaceUpAction(best_card_index,self.face_up_cards[best_card_index])
        else:
            action = DrawDeckAction

        return [action]

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
        # selecting the best combination of ticket cards by using cost - K * score
        self.info = game.get_player_info(self)
        self.edge_claims = game.get_edge_claims()
        combinations = [[0, 1], [1, 2], [0, 2], [0, 1, 2]]
        possible_destination_comb = []
        costs = []

        for combination in combinations:
            possible_destination = []
            for index in combination:
                possible_destination.append(destinations[index])
            path, all_path = self.find_best_path(game, possible_destination)
            if path is None:
                costs.append(10000)
                possible_destination_comb.append(possible_destination)
            else:
                possible_destination_comb.append(possible_destination)
                costs.append(path.cost - self.Ticket_Score_Multiplier * path.score)

        min_index = costs.index(min(costs))
        selected_destinations = possible_destination_comb[min_index]

        return selected_destinations

    def debug_print(self, game):
        '''
        print some more detailed info, activated by the game manager
        :param game:
        :return:
        '''
        remaining_edges = self.path.edges - game.get_edges_for_player(self) if self.path is not None else []

        return "Path:%s\nRemaining Edges: [%s]" % (str(self.path), ", ".join([str(edge) for edge in remaining_edges]))
