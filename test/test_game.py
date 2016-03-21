import unittest
from game import Game
from game.classes import *
from game.player import Player
from game.board import create_city_edges, get_scoring
from game.game import FailureCause
from game.methods import connected, find_paths, find_paths_for_destinations


class TestGame(unittest.TestCase):
    def setUp(self):
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")

        self.edges, self.city_edges = self.create_test_board()
        self.deck, self.destinations = self.create_test_deck()

        self.game = Game([self.player1, self.player2], custom_settings=True, edges=self.edges,
                         city_edges=self.city_edges, deck=self.deck, num_cars=12,
                         destinations=self.destinations)

    def create_test_board(self):
        # ----------------------
        #       A---3--B
        #       |     / \
        #       |    /   2
        #       4   6     \
        #       |  /       D--5--E
        #       | /
        #       C
        # ---------------------

        edges = [
            Edge("A", "B", 3, Colors.blue),
            Edge("A", "C", 4, Colors.red),
            Edge("B", "C", 6, Colors.none),
            Edge("B", "D", 2, Colors.red),
            Edge("D", "E", 5, Colors.red),
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

        self.assertDictEqual(hand1.cards, Counter([Colors.red] * 4), "Player 1 should have 4 red cards.")
        self.assertDictEqual(hand2.cards, Counter([Colors.blue] * 4), "Player 2 should have 4 blue cards.")

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

        self.assertTrue(self.game.draw_from_deck(self.player1), (True, FailureCause.none))

        # One less card in deck
        self.assertEqual(self.game.cards_in_deck(), 7)

        hand = self.game.get_player_info(self.player1).hand

        # Should have drawn a wild card
        self.assertDictEqual(hand.cards, Counter(([Colors.red] * 4) + [Colors.none]))
        self.assertEqual(self.game.cards_in_deck(), 7)

    def test_draw_face_up(self):
        self.assertEqual(self.game.cards_in_deck(), 8)
        self.assertListEqual(self.game.get_face_up_cards(), [Colors.green] * 3 + [Colors.none] * 2)

        self.assertEqual(self.game.draw_face_up_card(self.player1, 2), (True, FailureCause.none))

        # One less card in deck.
        self.assertEqual(self.game.cards_in_deck(), 7)

        hand = self.game.get_player_info(self.player1).hand

        # Assert face up cards changed
        self.assertListEqual(self.game.get_face_up_cards(), [Colors.green] * 2 + [Colors.none] * 3)

        # Should have drawn a green card
        self.assertDictEqual(hand.cards, Counter(([Colors.red] * 4) + [Colors.green]))
        self.assertEqual(self.game.cards_in_deck(), 7)

    def test_draw_deck_ends_turn(self):
        self.assertEqual(self.game.draw_from_deck(self.player1), (True, FailureCause.none))
        self.assertTrue(self.game.is_turn(self.player1), "Player 2's turn is not over")

        self.assertEqual(self.game.draw_from_deck(self.player1), (True, FailureCause.none))

        self.assertFalse(self.game.is_turn(self.player1), "Player 2's turn is over")
        self.assertTrue(self.game.is_turn(self.player2), "Player 1's turn begins")

    def test_draw_face_up_ends_turn(self):
        self.assertEqual(self.game.draw_face_up_card(self.player1, 1), (True, FailureCause.none))
        self.assertTrue(self.game.is_turn(self.player1), "Player 2's turn is not over")

        self.assertEqual(self.game.draw_face_up_card(self.player1, 0), (True, FailureCause.none))

        self.assertFalse(self.game.is_turn(self.player1), "Player 2's turn is over")
        self.assertTrue(self.game.is_turn(self.player2), "Player 1's turn begins")

    def test_draw_face_up_wild_ends_turn(self):
        self.assertEqual(self.game.draw_face_up_card(self.player1, 4), (True, FailureCause.none))
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

    def test_edge_other_city(self):
        edge = Edge("A", "B", 3, Colors.blue)

        self.assertEqual(edge.other_city("A"), "B")
        self.assertEqual(edge.other_city("B"), "A")

    def test_edge_contains_city(self):
        edge = Edge("A", "B", 3, Colors.blue)

        self.assertTrue(edge.contains_city("A"))
        self.assertTrue(edge.contains_city("B"))
        self.assertFalse(edge.contains_city("C"))

    def test_hand_str(self):
        hand = self.game.get_player_info(self.player1).hand
        self.assertEqual(str(hand), "(Red, Red, Red, Red)")

    def test_color_str(self):
        self.assertEqual(str(Colors.str(Colors.green)), "Green")
        self.assertEqual(str(Colors.str(Colors.none)), "None")
        self.assertEqual(str(Colors.str_card(Colors.none)), "Wild")

    def test_connected_multiple_edge(self):
        edge_claims = self.game.get_edge_claims()

        self.assertFalse(connected("A", "D", self.city_edges, edge_claims, self.player1))

        edge_claims[self.edges[0]] = self.player1.name
        edge_claims[self.edges[3]] = self.player1.name

        self.assertTrue(connected("A", "D", self.city_edges, edge_claims, self.player1))
        self.assertTrue(connected("D", "A", self.city_edges, edge_claims, self.player1))

    def test_connected_player_in_way(self):
        edge_claims = self.game.get_edge_claims()

        self.assertFalse(connected("A", "D", self.city_edges, edge_claims, self.player1))

        edge_claims[self.edges[0]] = self.player1.name
        edge_claims[self.edges[3]] = self.player1.name

        self.assertFalse(connected("A", "E", self.city_edges, edge_claims, self.player1))
        self.assertFalse(connected("E", "A", self.city_edges, edge_claims, self.player1))

        edge_claims[self.edges[4]] = self.player2.name

        self.assertFalse(connected("A", "E", self.city_edges, edge_claims, self.player1))
        self.assertFalse(connected("E", "A", self.city_edges, edge_claims, self.player1))

    def test_connected_all_edge(self):
        edge_claims = self.game.get_edge_claims()

        self.assertFalse(connected("A", "D", self.city_edges, edge_claims, self.player1))

        edge_claims[self.edges[0]] = self.player1.name
        edge_claims[self.edges[1]] = self.player1.name
        edge_claims[self.edges[2]] = self.player1.name
        edge_claims[self.edges[3]] = self.player1.name
        edge_claims[self.edges[4]] = self.player1.name

        self.assertTrue(connected("A", "B", self.city_edges, edge_claims, self.player1))
        self.assertTrue(connected("A", "C", self.city_edges, edge_claims, self.player1))
        self.assertTrue(connected("A", "D", self.city_edges, edge_claims, self.player1))
        self.assertTrue(connected("A", "E", self.city_edges, edge_claims, self.player1))
        self.assertTrue(connected("B", "D", self.city_edges, edge_claims, self.player1))
        self.assertTrue(connected("C", "D", self.city_edges, edge_claims, self.player1))

    def test_connected_singe_edge(self):
        edge_claims = self.game.get_edge_claims()

        self.assertFalse(connected("A", "B", self.city_edges, edge_claims, self.player1))

        edge_claims[self.edges[0]] = self.player1.name

        self.assertTrue(connected("A", "B", self.city_edges, edge_claims, self.player1))

    def test_cards_match(self):
        cards1 = Counter({Colors.red: 4})
        cards2 = Counter({Colors.green: 4})
        edge = Edge("A", "B", color=Colors.red, cost=4)

        self.assertTrue(Game.cards_match_exact(edge, cards1))
        self.assertFalse(Game.cards_match_exact(edge, cards2))

        edge = Edge("A", "B", color=Colors.red, cost=5)
        self.assertFalse(Game.cards_match_exact(edge, cards1))

    def test_cards_match_wild(self):
        cards1 = Counter([Colors.red] * 2 + [Colors.none] * 2)
        cards2 = Counter([Colors.green] * 4)
        edge = Edge("A", "B", color=Colors.red, cost=4)

        self.assertTrue(Game.cards_match_exact(edge, cards1))
        self.assertFalse(Game.cards_match_exact(edge, cards2))

    def test_cards_match_none(self):
        cards1 = Counter([Colors.red] * 4)
        cards2 = Counter([Colors.green] * 4)
        edge = Edge("A", "B", color=Colors.none, cost=4)

        self.assertTrue(Game.cards_match_exact(edge, cards1))
        self.assertTrue(Game.cards_match_exact(edge, cards2))

    def test_connect_cities(self):
        old_info = self.game.get_player_info(self.player1)

        self.assertEqual(self.game.connect_cities(self.player1, Edge("A", "C", 4, Colors.red),
                                                  Counter([Colors.red] * 4)),
                         (True, FailureCause.none))
        self.assertTrue(self.game.is_turn(self.player2))
        self.assertFalse(self.game.is_turn(self.player1))

        info = self.game.get_player_info(self.player1)

        # No cards should be left in the player's hand.
        self.assertEqual(sum(info.hand.cards.values()), 0)

        # Check that score changed.
        self.assertEqual(info.score, old_info.score + 7)
        self.assertEqual(self.game.get_visible_scores()[self.player1.name], 7)

        self.assertEqual(info.num_cars, old_info.num_cars - 4)
        self.assertEqual(self.game.cards_in_discard(), 4)

    def test_connect_cities_already_drew(self):
        self.game.draw_from_deck(self.player1)

        self.assertEqual(self.game.connect_cities(self.player1, Edge("A", "C", 4, Colors.red), [Colors.red] * 4),
                         (False, FailureCause.already_drew))

        self.assertTrue(self.game.is_turn(self.player1))

    def test_find_paths(self):
        # There are 2 paths from A to E.
        self.assertEqual("[(10, 16, [(A, B), (B, D), (D, E)]), (17, 34, [(D, E), (B, C), (A, C), (B, D)])]",
                         str(find_paths("A", "E", self.city_edges, 45, get_scoring())))

        # TODO: Test game ending conditions
        # TODO: Check empty deck gets shuffled
        # TODO: Test connection failures

    def test_find_path_one_destination(self):
        # Make sure that find_paths_for_destination works with a single destination.
        self.assertEqual(str(find_paths_for_destinations([Destination("A", "E", 2)], self.city_edges, 45,
                                                         get_scoring())),
                         str(find_paths("A", "E", self.city_edges, 45, get_scoring())))

    def test_find_paths_destination(self):
        # ----------------------
        #     A-2-B---4---D
        #     |  /
        #     2 3
        #     |/
        #     C
        # ---------------------

        edges = [
            Edge("A", "B", 2, Colors.blue),
            Edge("A", "C", 2, Colors.red),
            Edge("B", "C", 3, Colors.none),
            Edge("B", "D", 4, Colors.none),
        ]

        city_edges = create_city_edges(edges)

        # Sets up a situation where BC would be cheapest by itself, but it'd be better to go BAC because AB is also a
        # destination.
        self.assertEqual("[(4, 4, [(A, C), (A, B)]), (5, 6, [(B, C), (A, B)]), (5, 6, [(A, C), (B, C)]), "
                         "(7, 8, [(A, C), (A, B), (B, C)])]",
                         str(find_paths_for_destinations([Destination("A", "B", 5), Destination("B", "C", 4)],
                                                         city_edges, 15,
                                                         get_scoring())))

        # Test again with a maximum cost.
        self.assertEqual("[(4, 4, [(A, C), (A, B)]), (5, 6, [(B, C), (A, B)]), (5, 6, [(A, C), (B, C)])]",
                         str(find_paths_for_destinations([Destination("A", "B", 5), Destination("B", "C", 4)],
                                                         city_edges, 5,
                                                         get_scoring())))


if __name__ == '__main__':
    unittest.main()
