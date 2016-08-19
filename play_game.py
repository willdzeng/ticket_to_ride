#!/usr/bin/python
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

# you can chose the player you want by change this two line with other constructor
p1 = CFActionEvalAI("CFAE")
p2 = CFCombinedAI("CF Combined")

# For example 
# p2 = CFBaseAI("CF Base AI")
# p2 = RandomAI("R2")
# p2 = AdversarialAI("Adversarial AI")
# p2 = RandomAI("random AI")

## you can use Console Player to play with AI, be sure to enable GUI
# p2 = ConsolePlayer("Human")

players = [p1, p2]
use_gui = False
iterations = 1

# To have multiple tests run at once, create multiple log drivers with different combinations of players, then run each
# one.
driver = LogDriver(use_gui = use_gui, players=players, print_debug=False, iterations=iterations, switch_order=True,
                   replay_deck=True, replay_destinations=True)
driver.run_game()
