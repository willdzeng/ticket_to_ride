from driver import Driver
from ai.cf_ai.cheapest_path_ai import CheapestPathAI
from ai.adversarial_ai import AdversarialAI
from ai.cf_ai.greedy_ai import GreedyAI
from ai.random_ai import RandomAI
from ai.cf_ai.cf_random_ai import CFRandomAI
from ai.cf_ai.cf_base_ai import CFBaseAI
from game import Game
from game.classes import FailureCause,Colors
from human_player.console_player import ConsolePlayer

p1 = CFRandomAI("CFRandom")
p2 = CFBaseAI("CFBase")

players = [p1, p2]
use_gui = False
print_debug = False
exception_on_bad_action=True
pause_between_turns = 0

game_repeat = 50
winning_rounds = 0
for i in range(game_repeat):
    driver = Driver(players,use_gui,print_debug,exception_on_bad_action,pause_between_turns)
    driver.run_game()
    if driver.get_winner() == p1.name:
        winning_rounds += 1

winning_rates = winning_rounds/game_repeat
print "after %d rounds of game"%game_repeat
print "p1 winning rates:",
print "p2 winning rates:", 1 - winning_rates