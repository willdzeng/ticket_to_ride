import time

import gui
from ai.cf_ai.cheapest_path_ai import CheapestPathAI
from ai.adversarial_ai import AdversarialAI
from ai.cf_ai.greedy_ai import GreedyAI
from ai.random_ai import RandomAI
from game import Game
from game.classes import FailureCause

p1 = CheapestPathAI("P1")
# p2 = Player("P2")
p2 = AdversarialAI("P2")

players = [p1, p2]

use_gui =True
print_debug = True
maximum_rounds = 5000

game_gui = None

if use_gui:
    game_gui = gui.GUI()

game = Game(players, maximum_rounds)

# Main game loop.  Tells players when to take their turn.
while not game.is_game_over()[0]:
    for player in players:
        if game.is_turn(player):
            action_to_perform = player.take_turn(game)
            if use_gui:
                game_gui.update(game)

            if print_debug:
                print "Player %s: %s\nDoing Action: %s\n" % \
                      (player.name, game.get_player_info(player), action_to_perform)

                print player.debug_print()

            # Perform action.
            action_result = game.perform_action(player, action_to_perform)

            # If the action fails, raise an exception indicating what went wrong.
            if not action_result[0] and print_debug:
                raise Exception("Failure", FailureCause.str(action_result[1]))

            break

# Game's over.  Tell the players and print out some results.
for player in players:
    player.game_ended(game)

print "Game Over"
print "Winner: %s" % game.is_game_over()[1]
print "Final Scores: %s" % game.get_visible_scores()
print game.get_edge_claims()

if use_gui:
    game_gui.update_game_ended(game)
