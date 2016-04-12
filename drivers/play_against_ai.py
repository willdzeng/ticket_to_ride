from driver import Driver
from ai.cf_ai.cheapest_path_ai import CheapestPathAI
from ai.adversarial_ai import AdversarialAI
from ai.cf_ai.greedy_ai import GreedyAI
from ai.random_ai import RandomAI
from ai.cf_ai.cf_random_ai import CFRandomAI
from ai.cf_ai.cf_base_ai import CFBaseAI
from ai.cf_ai.cf_action_eval_ai import CFActionEvalAI
from game import Game
from game.classes import FailureCause,Colors
from human_player.console_player import ConsolePlayer

# p1 = CFRandomAI("CFRandom")
p1 = ConsolePlayer("P1")
# p2 = Player("P2")


# p2 = CFRandomAI("P1")
# p2 = CFRandomAI("CFRandom2")
# p2 = CFBaseAI("CFBaseAI")
#p2 = CFActionEvalAI("CFAE")
# p2 = GreedyAI("P2")
p2 = AdversarialAI("P2")
players = [p1, p2]
use_gui = True
print_debug=True
exception_on_bad_action=True
pause_between_turns = 0
driver = Driver(players,use_gui,print_debug,exception_on_bad_action,pause_between_turns)
driver.run_game()
