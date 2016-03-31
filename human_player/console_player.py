from game import Player, Colors, DrawDeckAction, DrawFaceUpAction, DrawDestinationAction, Game, Hand


class ConsolePlayer(Player):
    """
    A Human player that uses the console to play the game.
    """
    def __init__(self, name):
        Player.__init__(self, name)

    def take_turn(self, game):
        action = None
        all_actions = game.get_available_actions(self)
        player_info = game.get_player_info(self)

        print "Scores: %s" % game.get_visible_scores()
        print "Status: %s" % player_info

        # Loop until there is an action to take.
        while action is None:
            # Ask the user to select a type of action if they have any options.
            if game.get_remaining_actions(self) != 1:
                print ""
                print "Choose a type of action to take:"
                print "0: Draw Card"
                print "1: Draw Tickets"
                print "2: Connect Cities"

                action_type = int(raw_input("Selection: "))
            else:
                action_type = 0

            if action_type == 0:
                # Pick from available cards
                face_up_cards = game.get_face_up_cards()

                print ""
                print "Choose draw:"
                print "0: Draw from Deck"

                for i in range(len(face_up_cards)):
                    # Make sure that the user does not have the option to draw wilds.
                    if face_up_cards[i] != Colors.none or game.get_remaining_actions(self) != 1:
                        print "%d: %s" % (i + 1, Colors.str_card(face_up_cards[i]))

                print "%d: Cancel" % (len(face_up_cards) + 1)

                selection = int(raw_input("Selection: "))

                if selection == 0:
                    action = DrawDeckAction()
                elif 0 < selection <= len(face_up_cards):
                    if face_up_cards[selection - 1] != Colors.none or game.get_remaining_actions(self) != 1:
                        action = DrawFaceUpAction(selection - 1, face_up_cards[selection - 1])
            elif action_type == 1:
                # Draw a destination card
                action = DrawDestinationAction()
            elif action_type == 2:
                # Connect Edges
                edges_seen = set()

                # Find all edges that can be connected with the set of currently available actions.
                for action_iter in all_actions:
                    if action_iter.is_connect():
                        edges_seen.add(action_iter.edge)

                edges_seen = list(edges_seen)
                edges_seen.sort(key=lambda edge: edge.color)

                # Show options for selection to user.
                print ""
                print "Choose a route to claim:"
                for i in range(len(edges_seen)):
                    print "%d: %s" % (i, str(edges_seen[i]))

                print "%d: Cancel" % (len(edges_seen))

                selection = int(raw_input("Selection: "))

                if 0 <= selection < len(edges_seen):
                    # Ask how the user would like to claim the edge.
                    possible_actions = Game.all_connection_actions(edges_seen[selection], player_info.hand.cards)

                    print ""
                    print "Choose which cards to use:"
                    for i in range(len(possible_actions)):
                        print "%d: %s" % (i, Hand.cards_str(possible_actions[i].cards))

                    print "%d: Cancel" % (len(possible_actions))

                    selection = int(raw_input("Selection: "))

                    if 0 <= selection < len(possible_actions):
                        action = possible_actions[selection]

        print "\n"
        return action

    def game_ended(self, game):
        pass

    def select_destinations(self, game, destinations):
        # Choice will indicate which destination the player chose to remove.
        selection = -1

        while not (0 <= selection <= len(destinations)) and len(destinations) > 1:
            print "Choose a ticket to discard:"
            print "0: Keep all tickets"
            for i in range(len(destinations)):
                print "%d: %s" % (i + 1, str(destinations[i]))

            selection = int(raw_input("Selection: "))

            if selection != 0:
                del destinations[selection - 1]
                selection = -1
            else:
                break

            print ""

        return destinations

    def select_starting_destinations(self, game, destinations):
        # Choice will indicate which destination the player chose to remove.
        selection = -1

        while not (0 <= selection <= len(destinations)):
            print "Choose a ticket to discard:"
            print "0: Keep all tickets"
            for i in range(len(destinations)):
                print "%d: %s" % (i + 1, str(destinations[i]))

            selection = int(raw_input("Selection: "))

        if selection != 0:
            del destinations[selection - 1]

        print ""

        return destinations
