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
    Wild_Card_Cost = 6
    def __init__(self, name):
        CFBaseAI.__init__(self, name)


    def make_decision(self,game):
         # decision making part
        values = []
        for action in self.available_actions:
            value = self.eval_action(action)
            values.append(value)
            if self.print_debug:
                print action,"has value",value
        print self.cards_needed
        action = self.available_actions[values.index(max(values))]
        self.action_history.append(action)

        return action

    def eval_action(self,action):
        """
        Evaluate action based on path and cost function
        :param action:
        :return:
        """

        value = 0
        if action.is_connect():
            # add the score to the value first
            value += board.get_scoring()[action.edge.cost]
            # if we have path, we double reward the action
            if self.path is not None:
                if action.edge in self.remaining_edge:
                    value += board.get_scoring()[action.edge.cost] + self.path.score
            else:
                value += 1
            # subtract the cost of card using
            for card in action.cards:
                # if card is Wild card
                if card == Colors.none:
                    value -= self.Wild_Card_Cost
                else:
                    # if edge is gray
                    if action.edge.color == Colors.none:
                        value -= self.cards_needed[card]

            return value

        if action.is_draw_destination():
            if self.info.destinations:
                return -1
            else: # if we don't have destination card
                value = self.Destination_Threshold + self.info.num_cars
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
            print "DMCF made decisions as below:"
            for action in self.action_history:
                print action