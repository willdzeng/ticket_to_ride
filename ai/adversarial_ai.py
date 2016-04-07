from cf_ai.greedy_ai import GreedyAI
from game.methods import *
from random import randrange
from game import Player, Game

class AdversarialAI(GreedyAI):
    """
    Plays the same as the greedy AI, but looks for the cheapest path, instead of the one with the best score. (Also is quite mean >:-{)
    """
    def __init__(self, name):
        GreedyAI.__init__(self, name)
        self.sort_method = lambda path: path.cost


    def take_turn(self, game):
        info = game.get_player_info(self)
        steal_edges = get_threatened_edges('P1',game.get_edge_claims())
        original_action = GreedyAI.take_turn(self,game)
        actions = []

        #If there are edges to steal, then adversarial AI will attempt to take them, otherwise it will execute normally
        if(steal_edges):
            print 'Taking adversarial Action!!!!!!!!'
            print 'Want to take edges:'
            #print steal_edges
            for steal_edge in steal_edges:
                print steal_edge
                possible_action = Game.all_connection_actions(steal_edge, info.hand.cards)
                if possible_action:
                    actions.append(possible_action[0])
                    print str(possible_action)
                print actions
            # No actions, then do normal actions
            if not actions:
                print 'Do not have required cards'
                return original_action
            else:
                print 'returning action'
                return actions[randrange(0, len(actions))]
        else:
            return original_action

