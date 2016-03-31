import operator
from collections import Counter
from copy import deepcopy
from random import shuffle

from actions import *
from board import create_board, get_scoring
from cards import init_decks, shuffle_deck
from classes import PlayerInfo, FailureCause, HistoryEvent, Hand
from methods import connected


class Game:
    STARTING_HAND_SIZE = 4
    INITIAL_CAR_NUM = 150

    def __init__(self, players, maximum_rounds=5000, custom_settings=False, city_edges=None, edges=None, deck=None,
                 destinations=None, num_cars=45):
        if not custom_settings:
            self._city_edges, self._edges = create_board()
            self._deck, self._destinations = init_decks()

            self._num_cars = self.INITIAL_CAR_NUM
        else:
            self._city_edges = city_edges
            self._edges = edges
            self._deck = deck
            self._destinations = destinations

            self._num_cars = num_cars
        self._maximum_rounds = maximum_rounds
        self._rounds_count = 0
        self._scoring = get_scoring()

        self._players = players

        # Initialize info for all players.
        self._player_info = {}
        for player in players:
            # Give each player a hand of 5 cards from the top of the deck.
            # noinspection PyUnusedLocal
            hand = Hand([self._deck.pop() for x in range(self.STARTING_HAND_SIZE)])

            score = 0

            # Give each player 3 destinations.
            possible_destinations = [self._destinations.pop(), self._destinations.pop(),
                                     self._destinations.pop()]

            destinations = player.select_starting_destinations(self, possible_destinations)

            if len(destinations) < 2:
                raise Exception("Failure", FailureCause.str(FailureCause.not_enough_destinations))

            for destination in destinations:
                # Make sure the destination card is in the possible_destination cards set
                if destination not in possible_destinations:
                    raise Exception("Failure", FailureCause.str(FailureCause.wrong_destination_card))

                # Reduce score by all incomplete destinations.
                score -= destination.value

            self._player_info[player] = PlayerInfo(hand, destinations, self._num_cars, score)

        # Visible scores are set to zero.
        self._visible_scores = {player.name: 0 for player in self._players}

        # Set the first player to have the first turn.
        self._current_player_index = 0

        # Select 5 face up cards.
        # noinspection PyUnusedLocal
        self._face_up_cards = [self._deck.pop() for x in range(5)]

        # The number of actions the player has left to take this turn.
        self._num_actions_remaining = 2

        # Initialize edge claims
        self._edge_claims = {edge: None for edge in self._edges}

        self._game_is_over = False

        self._discards = []

        # Create the sets for events that will trigger when the game ends or begins.
        self._turn_ended_events = set()
        self._game_ended_events = set()

        # Store a history of all actions taken.
        self._history = []

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

    def get_rounds_played(self):
        """
        see the how many rounds have played

        :return: rounds play count number
        """
        return self._rounds_count

    def get_remaining_actions(self, player):
        """
        Get the remaining actions for a player this turn.
        :param player:
        :return: The number of actions or 0 if it is the wrong turn.
        """
        if self.is_turn(player):
            return self._num_actions_remaining
        else:
            return 0

    def get_edges_for_player(self, player):
        """
        Gets all the edges a player has.

        :param player: The player.
        :return: A set of all edges this player owns
        """
        result = set()

        for edge in self._edge_claims:
            if self._edge_claims[edge] == player.name:
                result.add(edge)

        return result

    def get_history(self):
        """
        Gets the history of all moves played this game.

        :return: A list of history events, with the first event played this game at index 0.
        """
        return deepcopy(self._history)

    def cards_in_deck(self):
        """
        Determine how many cards are left in the deck.

        :return: The number of cards in the deck.
        """
        return len(self._deck)

    def cards_in_discard(self):
        """
        Determine how many cards are in the discard pile.

        :return: The number of cards in the discard pile.
        """
        return len(self._discards)

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
    def cards_match_exact(edge, cards):
        """
        Determine if a given counter of cards match what the edge requires. Cards can be of the same color or have no
        color.

        :param edge: The edge to check.
        :param cards: The cards to check as a Counter.
        :return: True if the cards are acceptable, False otherwise.
        """
        # Remove non-zero elements.
        cards += Counter()

        # Make sure there are at most 2 colors.
        if len(cards.items()) > 2:
            return False
        # Make sure that if there are 2 colors, then one is wild.
        elif len(cards.items()) == 2 and cards[Colors.none] == 0:
            return False

        if edge.color == Colors.none:
            # Since there are the right number of cards and at most 1 non-wild color, that's all we need to check.
            return sum(cards.values()) == edge.cost
        else:
            # Make sure that there are the right number of cards.
            return cards[edge.color] + cards[Colors.none] == edge.cost and sum(cards.values()) == edge.cost

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
        if card_index >= len(self._face_up_cards) or card_index < 0:
            return False, FailureCause.invalid_card_index

        # Make sure that there are cards to draw.
        if not self._deck:
            self._deck = shuffle_deck()
            # return False, FailureCause.deck_out_of_cards

        card = self._face_up_cards[card_index]
        hand = self._player_info[player].hand

        # Wilds require 2 actions.
        if card == Colors.none and self._num_actions_remaining == 1:
            return False, FailureCause.already_drew

        # Put card in hand.
        hand.add_card(card)

        # Replace face up card.
        self._face_up_cards[card_index] = self._deck.pop()

        # Update history.
        self._history.append(HistoryEvent(player.name, DrawFaceUpAction(card_index, card)))

        # Complete action.
        self._use_actions(1 if card != Colors.none else 2)

        # Check that the deck is not empty.
        self._check_deck()

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
            self._deck = shuffle_deck()
            # return False, FailureCause.deck_out_of_cards

        hand = self._player_info[player].hand

        hand.add_card(self._deck.pop())

        # Update history.
        self._history.append(HistoryEvent(player.name, DrawDeckAction()))

        self._use_actions(1)

        # Check that the deck is not empty.
        self._check_deck()

        return True, FailureCause.none

    def draw_destination_cards(self, player):
        """
        Draw Destination Cards. Player will draw three destination card and choose one of it

        :param player: the player to draw the cards
        :return: If the action success or not
        """
        possible_destinations = [self._destinations.pop(),
                                 self._destinations.pop(),
                                 self._destinations.pop()]

        # call player's select destination function to confirm which card it want to keep
        selected_destinations = player.select_destinations(self, possible_destinations)

        # Make sure the return is a list
        if not isinstance(selected_destinations, list):
            selected_destinations = [selected_destinations]

        # Must return at least 1 card in between game
        if len(selected_destinations) < 1:
            return False, FailureCause.not_enough_destinations

        # add the selected card into it's hand
        self._player_info[player].destinations += selected_destinations

        for destination in selected_destinations:
            # Make sure the destination card is in the possible_destination cards set
            if destination not in possible_destinations:
                print destination
                for a in possible_destinations:
                    print a
                print "aaa"
                return False, FailureCause.wrong_destination_card

            # immediately subtract the cost of the destination card from the player's score
            self._player_info[player].score -= destination.value

        self._use_actions(2)
        # TODO Whether we need to add the card the player don't want back to the stack in case of
        # short of ticket card

        return True, FailureCause.none

    def connect_cities(self, player, edge, cards):
        """
        Connect 2 cities.  It must the player's turn to call this.

        :param player: The player who will be performing the connection.
        :param edge: The edge to connect.
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
        if edge in self._edges and not self._edge_is_claimed(edge):
            # Player must have the given cards.
            if not self.in_hand(player, cards):
                return False, FailureCause.missing_cards

            # Cards must match the edge's requirements.
            if not self.cards_match_exact(edge, cards):
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

            # Update history.
            self._history.append(HistoryEvent(player.name, ConnectAction(edge, cards)))

            return True, FailureCause.none

        if edge not in self._edges:
            return False, FailureCause.no_route

        if self._edge_claims[edge] != player.name:
            return False, FailureCause.already_claimed_opponent

        if self._edge_claims[edge] != player.name:
            return False, FailureCause.already_claimed_self

    def get_available_actions(self, player):
        """
        Gets all available actions for a player.
        :param player: The player to check.
        :return: A list of actions that a player can perform.
        """
        result = []
        # Make sure that it is this player's turn.
        if not self.is_turn(player):
            return result

        # Make sure the player has action remaining
        if self._num_actions_remaining < 1:  # action remain == 0
            return result

        result += [DrawDeckAction()]

        if self._num_actions_remaining > 1:  # action remain == 2
            #
            result += [DrawDestinationAction()]

            # Add the ability to draw any face up cards.
            result += [DrawFaceUpAction(i, self._face_up_cards[i]) for i in range(5)]

            hand = self.get_player_info(player).hand

            # Add the ability to connect any connectible cities.
            for edge in self._edge_claims:
                if self._edge_claims[edge] is None:
                    result += self.all_connection_actions(edge, hand.cards)

        else:  # action remain == 1
            # If only one action remains, then only allow non-wild face-up draws.
            for i in range(len(self._face_up_cards)):
                if self._face_up_cards[i] != Colors.none:
                    result += [DrawFaceUpAction(i, self._face_up_cards[i])]

        # TODO: Add action for destinations.

        return result

    def perform_action(self, player, action):
        """
        Perform an action using an action representation.

        :param player: The player.
        :param action: The action.
        :return: The result of performing the action.
        """
        result = (False, FailureCause.no_action)
        if action.is_draw_deck():
            result = self.draw_from_deck(player)
        elif action.is_draw_face_up():
            result = self.draw_face_up_card(player, action.index)
        elif action.is_connect():
            result = self.connect_cities(player, action.edge, action.cards)
        elif action.is_draw_destination():
            result = self.draw_destination_cards(player)

        return result

    @staticmethod
    def all_connection_actions(edge, cards):
        """
        Gets all available connection actions available given a certain set of cards for a certain edge.
        :param edge: The edge to check.
        :param cards: The hand to check the edge against.
        :return: A list off all possible actions that can be performed with the given hand on the given edge.
        """
        result = []

        # A short circuit in case there definitely can't be enough cards.
        if edge.cost > cards.most_common(1)[0][1] + cards[Colors.none]:
            return result

        # Route has no color.
        if edge.color == Colors.none:
            for card in cards:
                if card != Colors.none and cards[card] + cards[Colors.none] >= edge.cost:
                    # Find all possible combinations of cards that can be used to claim the edge.
                    # Using min(edge.cost - 1) guarantees that we will not accidentally add unnecessary plays that
                    # use all wilds.
                    for i in range(min(edge.cost - 1, cards[Colors.none] + 1)):
                        if cards[card] >= edge.cost - i:
                            result.append(ConnectAction(edge, Counter({card: edge.cost - i, Colors.none: i})))
        # Route has a color.
        else:
            if cards[edge.color] + cards[Colors.none] >= edge.cost:
                # Find all possible combinations of cards that can be used to claim the edge.
                # Using min(edge.cost - 1) guarantees that we will not accidentally add unnecessary plays that
                # use all wilds.
                for i in range(min(edge.cost - 1, cards[Colors.none] + 1)):
                    if cards[edge.color] >= edge.cost - i:
                        result.append(ConnectAction(edge, Counter({edge.color: edge.cost - i, Colors.none: i})))

        # If player has enough wilds to just get the route on wilds.
        if cards[Colors.none] >= edge.cost:
            result.append(ConnectAction(edge, Counter({Colors.none: edge.cost})))

        return result

    def _lose_cards(self, player, cards):
        """
        Remove cards from a player's hand.  If the cards aren't in the player's hand, then those cards aren't affected.

        :param player: The player whose cards to remove.
        :param cards: The cards to remove as a Counter.
        """
        hand = self._player_info[player].hand

        for card in cards.elements():
            hand.remove_card(card)

            self._discards.append(card)

    def _check_connections(self, player):
        """
        Check if a player has made any connections from their hand of destinations.  If they have, remove that
        destination and give them points for it.

        :param player: The player.
        """
        for destination in list(self._player_info[player].destinations):
            if connected(destination.city1, destination.city2, self._city_edges, self._edge_claims, player):
                self._player_info[player].score += destination.value * 2

                self._player_info[player].completed_destinations.append(destination)
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
            self._rounds_count += 1
            if self._rounds_count > self._maximum_rounds:
                self._end_game()
            self._num_actions_remaining = 2
            self._current_player_index = (self._current_player_index + 1) % len(self._players)

    def _end_game(self):
        """
        End the game.
        """
        self._game_is_over = True

        # Update visible scores to final values.
        self._visible_scores = {player.name: self._player_info[player].score for player in self._players}

        # Trigger all events for when the game ends.
        for event in self._game_ended_events:
            event(self)
        print "Rounds played: %d" % self._rounds_count

    def _check_deck(self):
        """
        If the deck is empty, shuffle the discards back in and create a new deck.
        """
        if not self._deck:
            self._deck = self._discards
            shuffle(self._deck)
            self._discards = []
