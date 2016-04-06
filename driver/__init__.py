import time

from ai.cf_ai.cheapest_path_ai import CheapestPathAI
from ai.cf_ai.greedy_ai import GreedyAI
from ai.random_ai import RandomAI
from ai.cf_ai.cf_random_ai import CFRandomAI
from ai.cf_ai.cf_base_ai import CFBaseAI
from game import Game
from game.classes import FailureCause,Colors
from human_player.console_player import ConsolePlayer

p1 = CFRandomAI("P1")
# p1 = ConsolePlayer("Human")
# p2 = Player("P2")
p2 = CFBaseAI("P2")
# p2 = GreedyAI("P2")

players = [p1, p2]

use_gui = False
print_debug = True
exception_on_bad_action = True
pause_between_turns = 0
maximum_rounds = 1000

game_gui = None

if use_gui:
    from gui import gui
    game_gui = gui.GUI()
    # time.sleep(5)

game = Game(players, maximum_rounds)

# Main game loop.  Tells players when to take their turn.
while not game.is_game_over()[0]:
    for player in players:
        if game.is_turn(player):
            action_to_perform = player.take_turn(game)
            if use_gui:
                game_gui.update(game)

            player_info = game.get_player_info(player)

            # Perform action.
            action_result = game.perform_action(player, action_to_perform)

            player.on_action_complete(game, action_result)

            # Print results.  This happens after the action is performed so the timing is correct when drawing
            # destinations.
            if print_debug:
                game.print_face_up_cards()
                print "Player %s: %s\nDoing Action: %s" % \
                      (player.name, player_info, action_to_perform)

                debug_print = player.debug_print(game)

                if debug_print != "":
                    print debug_print

                print ""

            # If the action fails, raise an exception indicating what went wrong.
            if not action_result[0] and exception_on_bad_action:
                raise Exception("Failure", FailureCause.str(action_result[1]))

            if pause_between_turns > 0:
                time.sleep(pause_between_turns)

            break

# Game's over.  Tell the players and print out some results.
for player in players:
    player.game_ended(game)

print "Game Over"
print "Winner: %s" % game.is_game_over()[1]
print "Final Scores: %s" % game.get_visible_scores()

if use_gui:
    game_gui.update_game_ended(game)
