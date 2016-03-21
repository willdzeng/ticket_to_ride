from random import randrange
from time import sleep

from game import Player, FailureCause


class RandomAI(Player):
    def take_turn(self, game):
        actions = game.get_available_actions(self)

        # Randomly select the action from available actions.
        action_to_perform = actions[randrange(0, len(actions))]

        print "Player %s: %s" % (self.name, game.get_player_info(self))
        print "%s" % action_to_perform

        # Perform action.
        action_result = game.perform_action(self, action_to_perform)

        # If the action fails, raise an exception indicating what went wrong.
        if not action_result[0]:
            raise Exception("Failure", FailureCause.str(game.perform_action(self, action_to_perform)[1]))

        print "\n"

        # Pause for pacing.
        # sleep(0.2)

    def game_ended(self, game):
        pass
