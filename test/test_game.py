import unittest
from game import Game
from game.classes import *
from game.board import create_city_edges
from game.game import FailureCause


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
        #       5   6     \
        #       |  /       D
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

        deck = ([Colors.none] * 10) + ([Colors.green] * 3) + ([Colors.blue] * 4) + ([Colors.red] * 4)

        destinations = [Destination("A", "B", 5),
                        Destination("A", "D", 10),
                        Destination("B", "C", 3), ] * 2

        return deck, destinations

    def test_starting_hands(self):
        hand1 = self.game.get_player_info(self.player1).hand
        hand2 = self.game.get_player_info(self.player2).hand

        self.assertListEqual(hand1.cards, [Colors.red] * 4, "Player 1 should have 4 red cards.")
        self.assertListEqual(hand2.cards, [Colors.blue] * 4, "Player 2 should have 4 blue cards.")

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

    def test_draw_deck(self):
        self.assertEqual(self.game.cards_in_deck(), 8)

        self.assertTrue(self.game.draw_from_deck(self.player1))

        # One less card in deck
        self.assertEqual(self.game.cards_in_deck(), 7)

        hand = self.game.get_player_info(self.player1).hand

        # Should have drawn a wild card
        self.assertListEqual(hand.cards, ([Colors.red] * 4) + [Colors.none])
        self.assertEqual(self.game.cards_in_deck(), 7)

    def test_draw_face_up(self):
        self.assertEqual(self.game.cards_in_deck(), 8)
        self.assertListEqual(self.game.get_face_up_cards(), [Colors.green] * 3 + [Colors.none] * 2)

        self.assertTrue(self.game.draw_face_up_card(self.player1, 2))

        # One less card in deck.
        self.assertEqual(self.game.cards_in_deck(), 7)

        hand = self.game.get_player_info(self.player1).hand

        # Assert face up cards changed
        self.assertListEqual(self.game.get_face_up_cards(), [Colors.green] * 2 + [Colors.none] * 3)

        # Should have drawn a green card
        self.assertListEqual(hand.cards, ([Colors.red] * 4) + [Colors.green])
        self.assertEqual(self.game.cards_in_deck(), 7)

    def test_draw_deck_ends_turn(self):
        self.assertTrue(self.game.draw_from_deck(self.player1))
        self.assertTrue(self.game.is_turn(self.player1), "Player 2's turn is not over")

        self.assertTrue(self.game.draw_from_deck(self.player1))

        self.assertFalse(self.game.is_turn(self.player1), "Player 2's turn is over")
        self.assertTrue(self.game.is_turn(self.player2), "Player 1's turn begins")

    def test_draw_face_up_ends_turn(self):
        self.assertTrue(self.game.draw_face_up_card(self.player1, 1))
        self.assertTrue(self.game.is_turn(self.player1), "Player 2's turn is not over")

        self.assertTrue(self.game.draw_face_up_card(self.player1, 0))

        self.assertFalse(self.game.is_turn(self.player1), "Player 2's turn is over")
        self.assertTrue(self.game.is_turn(self.player2), "Player 1's turn begins")

    def test_draw_face_up_wild_ends_turn(self):
        self.assertTrue(self.game.draw_face_up_card(self.player1, 4))
        self.assertFalse(self.game.is_turn(self.player1), "Player 2's turn is over")
        self.assertTrue(self.game.is_turn(self.player2), "Player 1's turn begins")

    def test_draw_face_up_then_wild(self):
        self.game.draw_face_up_card(self.player1, 1)

        self.assertEqual(self.game.draw_face_up_card(self.player1, 4), (False, FailureCause.already_drew))

    def test_cannot_draw_deck_wrong_turn(self):
        self.assertEqual(self.game.draw_from_deck(self.player2), (False, FailureCause.wrong_turn))

    def test_cannot_draw_face_up_wrong_turn(self):
        self.assertEqual(self.game.draw_face_up_card(self.player2, 3), (False, FailureCause.wrong_turn))

    def test_draw_face_up_wrong_index(self):
        self.assertEqual(self.game.draw_face_up_card(self.player1, -1), (False, FailureCause.invalid_card_index))
        self.assertEqual(self.game.draw_face_up_card(self.player1, 5), (False, FailureCause.invalid_card_index))

    # TODO: Test game ending conditions
    # TODO: Test connections


if __name__ == '__main__':
    unittest.main()
