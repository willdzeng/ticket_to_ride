from time import sleep

from game import Player


class RandomAI(Player):
    # TODO: Test.
    def take_turn(self, game):
        print game.get_player_info(self).hand
        game.draw_from_deck(self)

        sleep(.5)

    # TODO: Test.
    def game_ended(self, game):
        pass
