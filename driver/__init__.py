import gui
from ai.random_ai import RandomAI
from game import Player, Game


p1 = RandomAI("P1")
# p2 = Player("P2")
p3 = RandomAI("P3")

players = [p1, p3]

game_gui = gui.GUI()
game = Game(players)

while not game.is_game_over()[0]:
    for player in players:
        if game.is_turn(player):
            player.take_turn(game)
            game_gui.update(game)
