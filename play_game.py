import time

from ai.cf_ai.cheapest_path_ai import CheapestPathAI
from ai.adversarial_ai import AdversarialAI
from ai.cf_ai.greedy_ai import GreedyAI
from ai.random_ai import RandomAI
from ai.cf_ai.cf_random_ai import CFRandomAI
from ai.cf_ai.cf_base_ai import CFBaseAI
from drivers.driver import Driver
from drivers.log_driver import LogDriver
from game import Game
from game.classes import FailureCause, Colors
from human_player.console_player import ConsolePlayer

p1 = CFRandomAI("CF Random AI")
# p1 = RandomAI("R1")
# p1 = ConsolePlayer("Human")
# p2 = Player("P2")

p2 = CFBaseAI("CF Base AI")
# p2 = RandomAI("R2")
# p2 = GreedyAI("P2")
p3 = AdversarialAI("Adversarial AI")
players = [p1, p2, p3]

driver = LogDriver(use_gui=False, players=players, print_debug=False, iterations=2, switch_order=True)

# driver = Driver(use_gui=False, players=players)

driver.run_game()
