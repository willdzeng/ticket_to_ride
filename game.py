from copy import deepcopy

import operator

from board import create_board
from cards import init_decks
from classes import Colors, Hand, PlayerInfo
from methods import connected


class FailureCause:
    def __init__(self):
        pass

    none, no_route, wrong_turn, missing_cards, incompatible_cards, already_drew, deck_empty, invalid_card_index, \
        insufficient_cars, game_over, deck_out_of_cards = range(11)


class Game:
    starting_hand_size = 5

    def __init__(self, players):
        self._city_edges, self._edges, self._scoring = create_board()
        self._deck, self._destinations = init_decks()

        self._players = players

        # Initialize info for all players.
        self._player_info = {}
        for player in players:
            # Give each player a hand of 5 cards from the top of the deck.
            hand = Hand([self._deck.pop() for x in range(self.starting_hand_size)])

            score = 0

            # Give each player 3 destinations.
            destinations = [self._destinations.pop(), self._destinations.pop(),
                            self._destinations.pop()]

            # Reduce score by all incomplete destinations.
            for destination in destinations:
                score -= destination.value

            num_cars = 45

            self._player_info[player] = PlayerInfo(hand, destinations, num_cars, score)

        # Visible scores are set to zero.
        self._visible_scores = {player.name: 0 for player in self._players}

        # Set the first player to have the first turn.
        self._current_player_index = 0

        # Select 5 face up cards.
        self._face_up_cards = [self._deck.pop() for x in range(5)]

        # The number of actions the player has left to take this turn.
        self._num_actions_remaining = 2

        # Initialize edge claims
        self._edge_claims = {edge: None for edge in self._edges}

        self._game_is_over = False

    def get_scoring(self):
        """
        :return: The scoring dictionary.
        """
        return dict(self._scoring)

    def get_edge_claims(self):
        """
        :return: All edge claims.
        """
        return dict(self._edge_claims)

    def get_face_up_cards(self):
        """
        See the face up cards.
        """
        return list(self._face_up_cards)

    def get_player_info(self, player):
        """
        Get all of the game info of player.

        :param player: The player.
        :return: The player's game info.
        """
        return deepcopy(self._player_info[player])

    def get_visible_scores(self):
        """
        See the visible scores of all players.

        :return: A dictionary of all opponents by name and their scores.
        """
        return dict(self._visible_scores)

    def cards_in_deck(self):
        """
        Determine how many cards are left in the deck.

        :return: The number of cards in the deck.
        """
        return len(self._deck)

    def is_turn(self, player):
        """
        Determine if it is this player's turn.

        :param player: The player.
        :return: True if it is this player's turn, false otherwise.
        """
        return player == self._players[self._current_player_index]

    def is_game_over(self):
        """
        Determine if the game is over.

        :return: A tuple with a boolean and a string.  The Boolean is True if the game is over, false otherwise.  The
        String is the name of the winning player, or None otherwise.
        """
        if self._game_is_over:
            return True, max(self._visible_scores.iteritems(), key=operator.itemgetter(1))[0]

        return False, None

    def num_players(self):
        """
        Get the number of players.

        :return: The number of players.
        """
        return len(self._players)

    def in_hand(self, player, cards):
        """
        Determine if the given cards are in the player's hand.

        :param player: The player to check.
        :param cards: The cards to check for.
        :return: True if the cards are present, false otherwise.
        """
        return self._player_info[player].hand.contains_cards(cards)

    @staticmethod
    def cards_match(edge, cards):
        """
        Determine if a given list of cards match what the edge requires. Cards can be of the same color or have no
        color.

        :param edge: The edge to check.
        :param cards: The cards to check.
        :return: True if the cards are acceptable, False otherwise.
        """
        # Make sure there are the right number of cards.
        if len(cards) != edge.cost:
            return False

        # Figure out which color the cards need to match.  Since "None" is the highest possible color,
        # use the minimum of the list.
        if edge.color == Colors.none:
            color_to_match = min(cards)
        else:
            color_to_match = edge.color

        # Check the cards.
        for card in cards:
            if card != color_to_match and card != Colors.none:
                return False

        return True

    def draw_face_up_card(self, player, card_index):
        """
        Have a player draw a card from the face up pile.

        :param player: The player who will be drawing.
        :param card_index: The index of the card being drawn.
        :return: A tuple containing a boolean and an int.  Boolean will be True if the action succeeded,
        False otherwise.  Integer will correspond to a failure cause in the FailureCause object.
        """
        # Make sure the game is not over.
        if self._game_is_over:
            return False, FailureCause.game_over

        # Make sure it is the correct turn.
        if not self.is_turn(player):
            return False, FailureCause.wrong_turn

        # Make sure index is valid.
        if card_index >= len(self._face_up_cards):
            return False, FailureCause.invalid_card_index

        # Make sure that there are cards to draw.
        if not self._deck:
            return False, FailureCause.deck_out_of_cards

        card = self._face_up_cards[card_index]
        hand = self._player_info[player].hand

        # Wilds require 2 actions.
        if card == Colors.none and self._num_actions_remaining == 1:
            return False, FailureCause.already_drew

        # Put card in hand.
        hand.add_card(card)

        # Replace face up card.
        self._face_up_cards[card_index] = self._deck.pop()

        # Complete action.
        self._use_actions(1 if card != Colors.none else 2)

        return True, FailureCause.none

    def draw_from_deck(self, player):
        """
        Have a player draw a card from the deck.

        :param player: The player who will be drawing.
        :return: A tuple containing a boolean and an int.  Boolean will be True if the action succeeded,
        False otherwise.  Integer will correspond to a failure cause in the FailureCause object.
        """
        # Make sure the game is not over.
        if self._game_is_over:
            return False, FailureCause.game_over

        # Make sure it is the correct turn.
        if not self.is_turn(player):
            return False, FailureCause.wrong_turn

        # Make sure that there are cards to draw.
        if not self._deck:
            return False, FailureCause.deck_out_of_cards

        hand = self._player_info[player].hand

        hand.add_card(self._deck.pop())

        self._use_actions(1)

        return True, FailureCause.none

    def connect_cities(self, player, city1, city2, edge_color, cards):
        """
        Connect 2 cities.  It must the player's turn to call this.

        :param player: The player who will be performing the connection.
        :param city1: The first city to connect.
        :param city2: The second city to connect.
        :param edge_color: The color of the connection.  This is important because some cities have multiple edges of
        different colors.
        :param cards: The cards from the player's hand to use when making the claim.
        :return: A tuple containing a boolean and an int.  Boolean will be True if the action succeeded,
        False otherwise.  Integer will correspond to a failure cause in the FailureCause object.
        """
        # Make sure the game is not over.
        if self._game_is_over:
            return False, FailureCause.game_over

        # Make sure it is the correct turn.
        if not self.is_turn(player):
            return False, FailureCause.wrong_turn

        # 2 Actions must remain
        if self._num_actions_remaining != 2:
            return False, FailureCause.already_drew

        # Find the edge and claim it if possible.
        for edge in city1.edges:
            if edge.contains_city(city2) and not self._edge_is_claimed(edge) and edge.color == edge_color:
                # Player must have the given cards.
                if not self.in_hand(player, cards):
                    return False, FailureCause.missing_cards

                # Cards must match the edge's requirements.
                if not self.cards_match(edge, cards):
                    return False, FailureCause.incompatible_cards

                # Player must have enough cars.
                if self._player_info[player].num_cars < edge.cost:
                    return False, FailureCause.insufficient_cars

                self._claim_edge(edge, player)
                self._lose_cards(player, cards)
                self._player_info[player].num_cars -= edge.cost

                # Update score.
                self._player_info[player].score += self._scoring[edge.cost]
                self._visible_scores[player.name] += self._scoring[edge.cost]
                self._check_connections(player)

                # Check if game is over.
                if self._player_info[player].num_cars <= 3:
                    self._end_game()

                # End turn.
                self._use_actions(2)

                return True, FailureCause.none

        return False, FailureCause.no_route

    def _lose_cards(self, player, cards):
        """
        Remove cards from a player's hand.  If the cards aren't in the player's hand, then those cards aren't affected.

        :param player: The player whose cards to remove.
        :param cards: The cards to remove.
        """
        hand = self._player_info[player].hand

        for card in cards:
            hand.remove_card(card)

    def _check_connections(self, player):
        """
        Check if a player has made any connections from their hand of destinations.  If they have, remove that
        destination and give them points for it.

        :param player: The player.
        """
        for destination in list(self._player_info[player].destinations):
            if connected(destination.city1, destination.city2, self._city_edges, self._edge_claims, player):
                self._player_info[player].score += destination.value * 2

                self._player_info[player].destinations.remove(destination)

    def _claim_edge(self, edge, player):
        """
        Claim an edge for a player.

        :param edge:
        :param player:
        """
        self._edge_claims[edge] = player.name

    def _edge_is_claimed(self, edge):
        """
        Determines if an edge is claimed.

        :param edge: The edge to claim.
        :return: True if the edge is claimed, false otherwise.
        """
        return self._edge_claims[edge] is not None

    def _use_actions(self, num_actions):
        """
        Use up actions for the current player this turn.

        :param num_actions: The number of actions to use up.
        """
        self._num_actions_remaining -= num_actions

        # Running out of actions means the turn is over.
        if self._num_actions_remaining <= 0:
            self._num_actions_remaining = 2
            self._current_player_index = (self._current_player_index + 1) % len(self._players)

    def _end_game(self):
        """
        End the game.
        """
        self._game_is_over = True

        # Update visible scores to final values.
        self._visible_scores = {player.name: self._player_info[player].score for player in self._players}
