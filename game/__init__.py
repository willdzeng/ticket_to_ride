from classes import Player, Colors
from game import *

p1 = Player("P1")
p2 = Player("P2")

game = Game([p1, p2])

print ", ".join(map(Colors.str_card, game.get_face_up_cards()))

print game.get_player_info(p1).hand

print game.draw_face_up_card(p1, 3)
print game.draw_face_up_card(p1, 3)
print game.draw_face_up_card(p1, 3)

print game.get_player_info(p1).hand
print ", ".join(map(Colors.str_card, game.get_face_up_cards()))

# TODO: Log of last player's actions.
# TODO: All Available Actions
