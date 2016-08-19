from random import randrange

import game.board as board
from game import Player, Game
from game.actions import *
from game.classes import Colors
from game.methods import find_paths_for_destinations
from game.cards import shuffle_destinations

from cf_action_eval_ai import CFActionEvalAI
class CFOpponentEstimation(CFActionEvalAI):
    "Evaluate Every Action Based on the cost function"

    Destination_Threshold = 15
    Wild_Card_Value = 2
    Wild_Card_Cost = 7
    def __init__(self, name):
        CFActionEvalAI.__init__(self, name)
        self.all_destination = shuffle_destinations()


    def make_decision(self,game):
        """
        Evaluate every available action and select the best
        :param game:
        :return:
        """
         # decision making part
        values = []
        for action in self.available_actions:
            value = self.eval_action(action)
            values.append(value)
            if self.print_debug:
                print action,"has value",value
        if self.print_debug:
            self.print_cards_needed()

        action = self.available_actions[values.index(max(values))]
        self.action_history.append(action)

        return action

    def estimation_destination_card(self,game):
        self.history = game.get_history()
