import unittest

from game import Game
from game.classes import *
from game.board import create_city_edges


class TestGame(unittest.TestCase):
    def setUp(self):
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")

        edges, city_edges = self.create_test_board()
        deck, destinations = self.create_test_deck()

        self.game = Game([self.player1, self.player2], custom_settings=True, edges=edges, city_edges=city_edges,
                         deck=deck,
                         destinations=destinations)

    def create_test_board(self):
        # ----------------------
        #       A---3--B
        #       |     / \
        #       |    /   2
        #       5   6    \
        #       |  /     D
        #       | /
        #       C
        # ---------------------

        edges = [
            Edge("A", "B", 3, Colors.blue),
            Edge("A", "C", 5, Colors.red),
            Edge("B", "C", 6, Colors.none),
            Edge("B", "D", 2, Colors.red),
        ]

        city_edges = create_city_edges(edges)

        return edges, city_edges

    def create_test_deck(self):
        """
        Create a test deck.  Player 1 gets all red, Player 2 gets all blue, and the face ups are 3 greens and 2 wilds.
        Both get the same destinations: A-B, B-C, A-D

        :return: A tuple with the colored cards and destinations.
        """

        deck = ([Colors.none] * 10) + ([Colors.green] * 3) + ([Colors.blue] * 5) + ([Colors.red] * 5)

        destinations = [Destination("A", "B", 5),
                        Destination("A", "D", 10),
                        Destination("B", "C", 3), ] * 2

        return deck, destinations

    def test_starting_hands(self):
        hand1 = self.game.get_player_info(self.player1).hand
        hand2 = self.game.get_player_info(self.player2).hand

        self.assertListEqual(hand1.cards, [Colors.red] * 5, "Player 1 should have 5 red cards.")
        self.assertListEqual(hand2.cards, [Colors.blue] * 5, "Player 2 should have 5 blue cards.")

    def test_starting_scores(self):
        score1 = self.game.get_player_info(self.player1).score
        score2 = self.game.get_player_info(self.player2).score

        self.assertEqual(score1, -18, "Negative scores for incomplete destinations.")
        self.assertEqual(score2, -18, "Negative scores for incomplete destinations.")

    def test_starting_visible_scores(self):
        self.assertDictEqual(self.game.get_visible_scores(), {"Player 1": 0, "Player 2": 0}, "Starting scores should "
                                                                                             "be zero.")

    def test_starting_destinations(self):
        destinations1 = self.game.get_player_info(self.player1).destinations
        destinations2 = self.game.get_player_info(self.player2).destinations

        self.assertListEqual(destinations1,
                             [Destination("B", "C", 3), Destination("A", "D", 10), Destination("A", "B", 5)])
        self.assertListEqual(destinations2, destinations1)

    def test_starting_turns(self):
        self.assertTrue(self.game.is_turn(self.player1))
        self.assertFalse(self.game.is_turn(self.player2))

    def test_starting_face_up_cards(self):
        self.assertListEqual(self.game.get_face_up_cards(), [Colors.green] * 3 + [Colors.none] * 2)

    def test_immutable_edge_claims(self):
        edge_claims = self.game.get_edge_claims()

        edge_claims[Edge("A", "B", 3, Colors.blue)] = self.player1.name

        self.assertIsNone(self.game.get_edge_claims()[Edge("A", "B", 3, Colors.blue)],
                          "The returned edge claims object was mutable.")

if __name__ == '__main__':
    unittest.main()
