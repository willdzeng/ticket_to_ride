from collections import deque
from copy import copy, deepcopy

from drivers.driver import Driver
from game import init_decks, Game, create_board
from logging.csv_log import CSVLog


class LogDriver(Driver):
    def __init__(self, players, use_gui, iterations=1, switch_order=True, replay_deck=True, replay_destinations=True,
                 print_debug=False, exception_on_bad_action=True, pause_between_turns=0, maximum_rounds=1000):
        Driver.__init__(self, players, use_gui, print_debug, exception_on_bad_action, pause_between_turns,
                        maximum_rounds)

        self.iterations = iterations
        self.switch_order = switch_order
        self.replay_deck = replay_deck
        self.replay_destinations = replay_destinations

        # Create a list to use in the header of the CSV file, with Player 1, Player 2, etc.\.
        header_list = []
        for i in range(len(players)):
            header_list.append("Player %d" % (i + 1))
            header_list.append("P%d Score" % (i + 1))

        header_list.append("Winner")

        # Create a name for the log file created.
        name = "i%d_s%s_deck%s_dest%s" % (iterations, "T" if switch_order else "F", "T" if replay_deck else "F",
                                          "T" if replay_destinations else "F")

        self.csv_log = CSVLog(name, *header_list)

    def run_game(self):
        # Play the number of games specified by iterations value.
        for i in range(self.iterations):

            if self.switch_order:
                # The game should be played with the same deck and destinations, but the players rotated.
                deck, destinations = init_decks()

                # Use a deque to rotate the players.
                player_deque = deque(self.players)
                for j in range(len(self.players)):
                    print "Starting Game", i * 2 + j + 1
                    print ""

                    # If the deck should not be replayed, don't replay it.
                    if not self.replay_deck:
                        deck = init_decks()[0]

                    # If the destinations should not be replayed, don't replay them.
                    if not self.replay_destinations:
                        destinations = init_decks()[1]

                    # Play the same game over for the different players.
                    player_deque.rotate(1)

                    self.players = list(player_deque)
                    game = self.create_custom_game(list(player_deque), deepcopy(deck), deepcopy(destinations))
                    self.play_game(game)
            else:
                # Just play one game.
                self.play_game(self.create_game())

        self.csv_log.write()

    def game_over(self, game):
        Driver.game_over(self, game)

        # Log results of game.
        scores = game.get_visible_scores()
        log_line = []

        # Output each player and their scores.
        for player in self.players:
            log_line.append(player.name)
            log_line.append(scores[player.name])

        log_line.append(game.is_game_over()[1])

        # Add line to log.
        self.csv_log.append(*log_line)

    def create_custom_game(self, players, deck, destinations):
        city_edges, edges = create_board()
        return Game(players=players, maximum_rounds=self.maximum_rounds, print_debug=self.print_debug,
                    custom_settings=True, deck=deck, destinations=destinations, city_edges=city_edges, edges=edges)
