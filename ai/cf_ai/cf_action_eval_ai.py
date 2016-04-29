from random import randrange

import game.board as board
from game import Player, Game
from game.actions import *
from game.classes import Colors
from game.methods import find_paths_for_destinations
from cf_base_ai import CFBaseAI


class CFActionEvalAI(CFBaseAI):
    "Evaluate Every Action Based on the cost function"

    Destination_Threshold = 15
    Wild_Card_Value = 2
    Wild_Card_Cost = 9
    Threat_Action_Weight = 0  # weight when combined with other cost
    gui_debug = False

    def __init__(self, name):
        CFBaseAI.__init__(self, name)
        self.remaining_edge_score = 0
        self.threatened_edges = []
        self.threatened_edges_score = []

    def make_decision(self, game):
        """
        Evaluate every available action and select the best
        :param game:
        :return:
        """
        # update remaining edge score
        self.remaining_edge_score = 0
        for edge in self.remaining_edge:
            self.remaining_edge_score += board.get_scoring()[edge.cost]

        # evaluate the threaten edge first
        self.eval_threatened_edges()

        # decision making part
        if not self.opponent_name:
            self.opponent_name = game.get_opponents_name(self)

        # calculate the value of each action
        values = []
        for action in self.available_actions:
            value = self.eval_action(action)
            values.append(value)
            # if self.print_debug:
            #     print action, "has value", value
        if self.print_debug:
            self.print_cards_needed()

        action = self.available_actions[values.index(max(values))]
        self.action_history.append(action)

        return action

    def eval_threatened_edges(self):
        # this will be implemented in combined AI
        pass

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

            # add the value of threatened edge
            # in CFAE this won't have any effect
            if self.threatened_edges:
                for id, edge in enumerate(self.threatened_edges):
                    if action.edge == edge:
                        value += self.threatened_edges_score[id] * self.Threat_Action_Weight
                        if self.print_debug:
                            print action
                            print '#### Threaten Action #####:', value

            # if we have path, we double reward the action
            if self.path is not None:
                if action.edge in self.remaining_edge:
                    # intuition here is:
                    # when we just have a few edge remains, the action to claim those edge would be high
                    value += self.Wild_Card_Value + board.get_scoring()[action.edge.cost] \
                             + self.path.score - self.remaining_edge_score
                    if self.print_debug:
                        print "Path action ", action
                        print "Before: ", value
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
                        # if edge is gray, make sure it doesn't take the cards we need for other edge
                        if action.edge.color == Colors.none:
                            value -= self.cards_needed[card]
            else:  # if path is None
                # when we don't have path, we better claim the best path that has the highest score
                value += board.get_scoring()[action.edge.cost]
            if action.edge in self.remaining_edge or action.edge in self.threatened_edges:
                if self.print_debug:
                    print "After: ", value
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
            if self.print_debug:
                print action, " has value ", value
            return value

    def game_ended(self, game):
        """
        end of the game, let's print some shit
        :param game:
        :return:
        """
        if self.print_debug:
            print "%s made decisions as below:" % self.name
            for action in self.action_history:
                print action
            print "########\nDi:To cancel the action print in cf_action_eval_ai.py line 25-26\n#########\n"

        # if self.gui is not None:
        #     self.gui.close()