import time

from ai.cf_ai.cf_adversarial_ai import AdversarialAI
from ai.random_ai import RandomAI
from ai.cf_ai.cf_random_ai import CFRandomAI
from ai.cf_ai.cf_base_ai import CFBaseAI
from ai.cf_ai.cf_action_eval_ai import CFActionEvalAI
from ai.cf_ai.cf_combined_ai import CFCombinedAI
from drivers.driver import Driver
from drivers.log_driver import LogDriver
from game import Game
from game.classes import FailureCause, Colors
from human_player.console_player import ConsolePlayer


# for i in range(6):
# p1 = CFRandomAI("CF Random AI")
# p1 = RandomAI("R1")
# p1 = ConsolePlayer("Human")
# p2 = Player("P2")

# p2 = CFBaseAI("CF Base AI")
# p2 = RandomAI("R2")
# p2 = GreedyAI("P2")
# p3 = AdversarialAI("Adversarial AI")
# p4 = RandomAI("random AI")
p5 = CFActionEvalAI("CFAE")
p6 = CFCombinedAI("CF Combined")
players = [p5, p6]

# To have multiple tests run at once, create multiple log drivers with different combinations of players, then run each
# one.


driver = LogDriver(use_gui=False, players=players, print_debug=False, iterations=50, switch_order=True,
                   replay_deck=True, replay_destinations=True)

# driver = Driver(use_gui=False, players=players, print_debug=False)

driver.run_game()
