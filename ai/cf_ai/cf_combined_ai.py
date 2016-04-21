from random import randrange

import game.board as board
from game import Player, Game
from game.actions import *
from game.classes import Colors
from game.methods import find_paths_for_destinations
from cf_base_ai import CFBaseAI
from game.methods import get_threatened_edges

class CFCombinedAI(CFBaseAI):
    "Evaluate Every Action Based on the cost function"
    Threat_Edge_Multiplier = 1
    Destination_Threshold = 15
    Wild_Card_Value = 2
    Wild_Card_Cost = 7
    gui_debug = True
    def __init__(self, name):
        CFBaseAI.__init__(self, name)
        self.threatened_edge = None
        self.threatened_edge_score = 0

    def make_decision(self,game):
        """
        Evaluate every available action and select the best
        :param game:
        :return:
        """
         # decision making part

        if not self.opponent_name:
            self.opponent_name = game.get_opponents_name(self)


        self.remaining_edge_score = 0
        for edge in self.remaining_edge:
            self.remaining_edge_score += board.get_scoring()[edge.cost]

        ####
        # threatened_edges_group = get_threatened_edges(self.opponent_name[0],self.edge_claims,15)
        # self.threatened_edge_score = 0
        # self.threatened_edge = None
        # if threatened_edges_group:
        #     print threatened_edges_group
        #     print len(threatened_edges_group)
        #     self.threatened_edge = threatened_edges_group[0][0]
        #     for group in threatened_edges_group[1]:
        #         for edge in group:
        #             print edge
        #             self.threatened_edge_score += edge.cost
        #     self.threatened_edge_score *= self.Threat_Edge_Multiplier
        ####

        # calculate the value of each action
        values = []
        for action in self.available_actions:
            value = self.eval_action(action)
            values.append(value)
            if self.print_debug:
                print action, "has value", value
        if self.print_debug:
            self.print_cards_needed()

        action = self.available_actions[values.index(max(values))]
        self.action_history.append(action)



        return action

    def eval_action(self, action):
        """
        Evaluate action based on path and cost function
        :param action: the action to be evaluated
        :return: the value of the action
        """

        value = 0
        if action.is_connect():
            # add the score to the value first
            # value += board.get_scoring()[action.edge.cost]
            # if we have path, we double reward the action

            if self.threatened_edge is not None:
                if action.edge == self.threatened_edge:
                    value += self.threatened_edge_score

            if self.path is not None:
                if action.edge in self.remaining_edge:
                    # intuition here is:
                    # when we just have a few edge remains, the action to claim those edge would be high
                    value += board.get_scoring()[action.edge.cost] + self.path.score - self.remaining_edge_score
                    if self.print_debug:
                        print "Found a good action that in the remaining edges"
                        print "Before counting for the card cost it has value:", value
                else:  # edge is not in path
                    # intuition here is if the we have path, and we may still claim it
                    # if it has higher score than the remaining destination
                    # value += board.get_scoring()[action.edge.cost] - self.path.cost
                    # intuition here is never claim other routes
                    value += -1
                # subtract the cost of card using if we have a path
                for card in action.cards.elements():
                    # if card is Wild card
                    if card == Colors.none:
                        value -= self.Wild_Card_Cost
                    else:
                        # if edge is gray
                        if action.edge.color == Colors.none:
                            value -= self.cards_needed[card]
            else:  # if path is None
                # when we don't have path, we better claim the best path that has the highest score
                value += board.get_scoring()[action.edge.cost]
            return value

        if action.is_draw_destination():
            if self.info.destinations:
                return -1
            else:  # if we don't have destination card
                value = -self.Destination_Threshold + self.info.num_cars
                return value

        if action.is_draw_deck():
            value += 1
            return value

        if action.is_draw_face_up():
            if action.card == Colors.none:
                value += self.Wild_Card_Value
            else:
                value += self.cards_needed[action.card]
            return value

    def game_ended(self, game):
        if self.print_debug:
            print "CFAE made decisions as below:"
            for action in self.action_history:
                print action
            print "########\nDi:To cancel the action print in cf_action_eval_ai.py line 25-26\n#########\n"
