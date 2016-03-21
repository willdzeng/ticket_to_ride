from random import randrange
from time import sleep

from game import Player, FailureCause


class RandomAI(Player):
    def take_turn(self, game):
        actions = game.get_available_actions(self)

        # Randomly select the action from available actions.
        action_to_perform = actions[randrange(0, len(actions))]
        return action_to_perform

    def game_ended(self, game):
        pass
