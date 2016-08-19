from driver import Driver
from ai.cf_ai.cf_adversarial_ai import AdversarialAI
from human_player.console_player import ConsolePlayer

p1 = ConsolePlayer("P1")
p2 = AdversarialAI("P2")

players = [p1, p2]
use_gui = True
print_debug=True
exception_on_bad_action=True
pause_between_turns = 0
driver = Driver(players,use_gui,print_debug,exception_on_bad_action,pause_between_turns)
driver.run_game()
