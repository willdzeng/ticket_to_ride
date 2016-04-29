from game.classes import *
from game.player import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from game.board import create_board


# cities = dict()
# cities = dict()
# x = []
# y = []



class GUI:
    def __init__(self, x_size=20, y_size=10):

        print('initializing gui')

        img = mpimg.imread('../gui/world2.png')
        plt.ion()  # uncomment to let go of string
        self.fig = plt.figure(figsize=(x_size, y_size))  # uncomment to let go of string
        imgplot = plt.imshow(img)
        plt.xlim([0, 1080])
        plt.ylim([700, 0])
        imgplot.axes.get_xaxis().set_visible(False)
        imgplot.axes.get_yaxis().set_visible(False)
        self.needs_reset = False

        # imgplot = plt.imdraw(img)
        self.place_cities()
        self.plot_board()
        self.set_colors()

        [city_edges, edges] = create_board()

        x_offset = 5
        y_offset = 5

        # Plot the edges for connecting cities
        for index1, edge in enumerate(edges):
            offset = 0
            for index2, edge2 in enumerate(edges):
                # Check if this is a double edge
                if edge.city1 is edge2.city1 and edge.city2 is edge2.city2 and edge is not edge2:
                    if (index1 > index2):
                        offset = -1
                    else:
                        offset = 1

            x_1 = []
            y_1 = []
            x_1.append(self.cities[edge.city1][0] + offset * x_offset)
            y_1.append(self.cities[edge.city1][1] + offset * y_offset)
            x_1.append(self.cities[edge.city2][0] + offset * x_offset)
            y_1.append(self.cities[edge.city2][1] + offset * y_offset)
            self.edge_colors[edge] = plt.plot(x_1, y_1, self.colors[edge.color])
            plt.setp(self.edge_colors[edge], linewidth=4)

            x_mean = (x_1[0] + x_1[1]) / 2
            y_mean = (y_1[0] + y_1[1]) / 2
            self.edge_means[edge] = [x_mean, y_mean]

            self.edge_weights[edge] = plt.plot(x_mean, y_mean, 'go')
            plt.setp(self.edge_weights[edge], 'ms', 15.0)
            self.edge_numbers[edge] = plt.text(x_mean - 5, y_mean + 5, str(edge.cost), fontdict=None)

        for city in self.cities:
            self.city_points[city] = plt.plot(self.cities[city][0], self.cities[city][1], 'ro')
            self.city_texts[city] = plt.text(self.cities[city][0] - 5, self.cities[city][1] + 5, '', fontdict=None)

        # Plot the numbers of cards player 1 and 2 have
        # First for player 1
        x = 705
        y = 33
        i = 0
        for i in range(9):
            self.player_1_cards[str(i)] = plt.text(x, y, '0', fontdict=None)
            x = x + 22
        self.p1_score = plt.text(x + 77, y, '0', fontdict=None)
        self.p1_cars = plt.text(x + 22, y, '0', fontdict=None)

        # Next for player 2
        x = 705
        y = 103
        i = 0
        for i in range(9):
            self.player_2_cards[str(i)] = plt.text(x, y, '0', fontdict=None)
            x = x + 22
        self.p2_score = plt.text(x + 77, y, '0', fontdict=None)
        self.p2_cars = plt.text(x + 22, y, '0', fontdict=None)

        self.cards['0'] = mpimg.imread('../gui/red.png')
        self.cards['1'] = mpimg.imread('../gui/orange.png')
        self.cards['2'] = mpimg.imread('../gui/blue.png')
        self.cards['3'] = mpimg.imread('../gui/yellow.png')
        self.cards['4'] = mpimg.imread('../gui/green.png')
        self.cards['5'] = mpimg.imread('../gui/pink.png')
        self.cards['6'] = mpimg.imread('../gui/black.png')
        self.cards['7'] = mpimg.imread('../gui/white.png')
        self.cards['8'] = mpimg.imread('../gui/wild.png')

        i = 0
        x = 0.858
        y = 0.78
        for i in range(5):
            self.table_card_slots.append(self.fig.add_axes([x, y - 0.020 * i, 0.034, 0.016], 'auto_scale_on'))
            self.table_card_slots[i].get_xaxis().set_visible(False)
            self.table_card_slots[i].get_yaxis().set_visible(False)
        plt.draw()
        # plt.show()

    # Variables
    colors = []
    cities = dict()
    x = []
    y = []
    player_1_cards = dict()
    player_2_cards = dict()
    edge_weights = dict()
    edge_colors = dict()
    cards = dict()
    table_card_slots = list()
    p1_score = []
    p2_score = []
    p1_cars = []
    p2_cars = []
    fig = []
    edge_icons = dict()
    edge_numbers = dict()
    edge_means = dict()
    need_reset = False
    city_points = dict()
    city_texts = dict()
    destination_cities = dict()

    player_1 = None
    player_2 = None

    def set_city(self, city, number):
        plt.setp(self.city_points[city], 'color', 'w')
        plt.setp(self.city_points[city], marker='H')
        plt.setp(self.city_points[city], 'ms', 20.0)
        plt.setp(self.city_texts[city], text=str(number))

    def reset_cities(self):
        for city in self.city_points:
            plt.setp(self.city_points[city], 'color', 'r')
            plt.setp(self.city_points[city], marker='o')
            plt.setp(self.city_points[city], 'ms', 1.0)
            plt.setp(self.city_texts[city], text=str(''))

    # Display the destinations
    def show_destinations(self, destinations):
        for index, destination in enumerate(destinations):
            self.set_city(destination.city1, index)
            self.set_city(destination.city2, index)
            # plt.ioff()
            # plt.show()

    def show_path(self, path):
        # print 'in show path'
        for edge in path.edges:
            # print edge
            plt.setp(self.edge_colors[edge], linewidth=10)
            plt.setp(self.edge_colors[edge], linestyle='solid')
        self.needs_reset = True
        plt.ioff()
        plt.draw()

    def reset_edge_labels(self, edges):
        for edge in edges:
            plt.setp(self.edge_weights[edge], 'color', 'g')
            plt.setp(self.edge_weights[edge], marker='o')
            plt.setp(self.edge_weights[edge], linewidth=2)
            plt.setp(self.edge_numbers[edge], text=str(edge.cost))
            plt.setp(self.edge_colors[edge], linewidth=2)
            plt.setp(self.edge_colors[edge], linestyle='solid')

    def show_edges(self, edges):
        for index, edge in enumerate(edges):
            # print 'updating:'
            # print edge
            plt.setp(self.edge_weights[edge], 'color', 'w')
            plt.setp(self.edge_weights[edge], marker='s')
            plt.setp(self.edge_numbers[edge], text=str(index))

        self.needs_reset = True
        plt.ioff()
        plt.draw()

    def place_cities(self):
        self.cities = {"Atlanta": [775, 516],
                       "Boston": [1018, 315.5],
                       "Calgary": [235, 85.7],
                       "Charleston": [857, 537],
                       "Chicago": [717, 329],
                       "Dallas": [549, 537],
                       "Denver": [397.3, 380.3],
                       "Duluth": [633.2, 203.6],
                       "El Paso": [370.7, 559.1],
                       "Helena": [270.1, 208.3],
                       "Houston": [573.2, 601.5],
                       "Kansas City": [588, 394.6],
                       "Las Vegas": [213.1, 461.6],
                       "Little Rock": [630, 494],
                       "Los Angeles": [157.4, 508.9],
                       "Miami": [850.3, 683.5],
                       "Montreal": [971.5, 237.1],
                       "Nashville": [730, 461],
                       "New Orleans": [670, 597.4],
                       "New York": [962.9, 356.7],
                       "Oklahoma City": [533.9, 477.8],
                       "Omaha": [562.1, 343.1],
                       "Phoenix": [268.8, 522.45],
                       "Pittsburgh": [854, 362.7],
                       "Portland": [76.9, 236.7],
                       "Raleigh": [877.5, 470.881],
                       "Saint Louis": [668.1, 406.26],
                       "Salt Lake City": [272, 354.775],
                       "San Francisco": [81.6, 426],
                       "Santa Fe": [381.1, 472.8],
                       "Sault St. Marie": [774, 211.5],
                       "Seattle": [82.7, 181.6],
                       "Toronto": [864.5, 283.9],
                       "Vancouver": [68.6, 135.9],
                       "Washington DC": [908.5, 398.8],
                       "Winnipeg": [540.9, 118.8]
                       }

    def set_colors(self):
        self.colors = ['#b61c16', '#bc5510', '#1033bc', '#d8c413', '#13750a', '#6c0a75', '#030203', '#ebeaeb',
                       '#6d696d']

    def plot_board(self):
        for city in self.cities:
            self.x.append(self.cities[city][0])
            self.y.append(self.cities[city][1])

    def update(self, game):
        self.player_1 = str(game._players[0])
        self.player_2 = str(game._players[1])

        if self.needs_reset:
            self.reset_cities()
            self.reset_edge_labels(game.get_edge_claims())
            self.needs_reset = False
        # TODO: Implement.
        self.update_display(game)
        self.update_edges(game)
        self.update_cards(game)
        plt.draw()
        pass

    def update_cards(self, game):
        face_up_cards = game.get_face_up_cards()
        i = 0
        for card_key in face_up_cards:
            # print(str(card_key))
            if (i < len(self.table_card_slots)):
                self.table_card_slots[i].imshow(self.cards[str(card_key)])
                i = i + 1

    def update_display(self, game):
        scores = game.get_visible_scores()

        # print scores
        for player in game._players:
            cards = game.get_player_info(player).hand.cards
            for card in cards:
                if (player.name == self.player_1):
                    self.player_1_cards[str(card)].set_text(str(cards[card]))
                    self.p1_score.set_text(str(scores[player.name]))
                    self.p1_cars.set_text(str(game.get_player_info(player).num_cars))
                elif (player.name == self.player_2):
                    self.player_2_cards[str(card)].set_text(str(cards[card]))
                    self.p2_score.set_text(str(scores[player.name]))
                    self.p2_cars.set_text(str(game.get_player_info(player).num_cars))

    def update_edges(self, game):
        edges = game.get_edge_claims()

        # scoring = dict()

        for index, edge in enumerate(edges):
            # print(edge)
            # print(edges[edge])

            # scoring[edge.cost] = 0

            if (edges[edge] == self.player_1):
                plt.setp(self.edge_weights[edge], 'color', 'b')
                plt.setp(self.edge_colors[edge], 'color', 'b')
                plt.setp(self.edge_colors[edge], marker='.')
                plt.setp(self.edge_colors[edge], linewidth=6)
                plt.setp(self.edge_colors[edge], linestyle='--')
                plt.setp(self.edge_colors[edge], 'ms', 10.0)
            elif (edges[edge] == self.player_2):
                plt.setp(self.edge_weights[edge], 'color', 'r')
                plt.setp(self.edge_colors[edge], 'color', 'r')
                plt.setp(self.edge_colors[edge], marker='.')
                plt.setp(self.edge_colors[edge], linewidth=6)
                plt.setp(self.edge_colors[edge], linestyle='--')
                plt.setp(self.edge_colors[edge], 'ms', 10.0)

                # print(card_value)
                # print(game.get_player_info(player).hand.cards{card})
                # i=i+1

                # print(self.cards_pos_x[int(card)])
                # print(self.cards_pos_y[j])

                # plt.text(self.cards_pos_x[int(card)], self.cards_pos_y[j], str(cards[card]), fontdict=None)
                # path = Path(edges,scoring)
                # self.show_path(path)

    def close(self):
        plt.clf()
        plt.close()
        print "GUI closed figure"
        # colors = []
        # cities = dict()
        # x = []
        # y = []
        # player_1_cards = dict()
        # player_2_cards = dict()
        # edge_weights = dict()
        # edge_colors = dict()
        # cards = dict()
        # table_card_slots = list()
        # p1_score=[]
        # p2_score=[]
        # p1_cars=[]
        # p2_cars=[]
        # fig = []
        # edge_icons = dict()
        # edge_numbers = dict()
        # edge_means = dict()
        # need_reset =False
        # city_points = dict()
        # city_texts = dict()
        # destination_cities = dict()

    def update_game_ended(self, game):
        self.update(game)
        plt.ioff()
        plt.draw()
        # TODO: Implement.
        pass

    def update_game_ended_and_close(self, game):
        self.update(game)
        plt.ioff()
        plt.draw()
        # TODO: Implement.
        pass

        # game.add_turn_ended_event(self.update)
