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

p1 = CFRandomAI("P1")
p1 = ConsolePlayer("Human")
# p2 = Player("P2")

p2 = CFRandomAI("P1")

p2 = CFBaseAI("P2")
# p2 = GreedyAI("P2")
p2 = AdversarialAI("P2")
players = [p1, p2]
use_gui = False

driver = Driver(players,True,True,True,500)
driver.run_game();
