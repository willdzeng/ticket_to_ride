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
    def __init__(self):

        print('initializing gui')

        img = mpimg.imread('../gui/world2.png')
        plt.ion()  #uncomment to let go of string
        fig = plt.figure() #uncomment to let go of string
        imgplot = plt.imshow(img)
        plt.xlim([0,1080])
        plt.ylim([700,0])
        imgplot.axes.get_xaxis().set_visible(False)
        imgplot.axes.get_yaxis().set_visible(False)


        #imgplot = plt.imdraw(img)
        self.place_cities()
        self.plot_board()
        self.set_colors()
        plt.plot(self.x, self.y, 'ro')
        [city_edges, edges] = create_board()


        #Plot the edges for connecting cities
        for edge in edges:
            x_1 = []
            y_1 = []
            x_1.append(self.cities[edge.city1][0])
            y_1.append(self.cities[edge.city1][1])
            x_1.append(self.cities[edge.city2][0])
            y_1.append(self.cities[edge.city2][1])
            l1 = plt.plot(x_1, y_1, self.colors[edge.color])
            plt.setp(l1, linewidth=2)

            x_mean = (x_1[0] +x_1[1])/2
            y_mean = (y_1[0] +y_1[1])/2

            self.edge_weights[edge] =plt.plot(x_mean,y_mean,'go')
            plt.setp(self.edge_weights[edge],'ms',10.0)
            plt.text(x_mean-7,y_mean+7,str(edge.cost),fontdict=None)
            #Plot the numbers of cards player 1 and 2 have

        #First for player 1
        x = 705
        y = 33
        i = 0
        for i in range(9):
            self.player_1_cards[str(i)] = plt.text(x, y, '0', fontdict=None)
            x = x+ 22
        self.p1_score = plt.text(x+77,y,'0',fontdict=None)
        self.p1_cars = plt.text(x+22,y,'0',fontdict=None)

        #Next for player 2
        x = 705
        y = 103
        i = 0
        for i in range(9):
            self.player_2_cards[str(i)] = plt.text(x, y, '0', fontdict=None)
            x = x+ 22
        self.p2_score = plt.text(x+77,y,'0',fontdict=None)
        self.p2_cars = plt.text(x+22,y,'0',fontdict=None)

        self.cards['0'] = mpimg.imread('../gui/red.png')
        self.cards['1'] = mpimg.imread('../gui/orange.png')
        self.cards['2'] = mpimg.imread('../gui/blue.png')
        self.cards['3'] = mpimg.imread('../gui/yellow.png')
        self.cards['4'] = mpimg.imread('../gui/green.png')
        self.cards['5'] = mpimg.imread('../gui/pink.png')
        self.cards['6'] = mpimg.imread('../gui/black.png')
        self.cards['7'] = mpimg.imread('../gui/white.png')
        self.cards['8'] = mpimg.imread('../gui/wild.png')

        #self.cards['Red'] = mpimg.imread('../gui/red.png')
        #self.cards['Orange'] = mpimg.imread('../gui/orange.png')
        #self.cards['Blue'] = mpimg.imread('../gui/blue.png')
        #self.cards['Yellow'] = mpimg.imread('../gui/yellow.png')
        #self.cards['Green'] = mpimg.imread('../gui/green.png')
        #self.cards['Pink'] = mpimg.imread('../gui/pink.png')
        #self.cards['Black'] = mpimg.imread('../gui/black.png')
        #self.cards['White'] = mpimg.imread('../gui/white.png')
        #self.cards['Wild'] = mpimg.imread('../gui/wild.png')

        i=0
        x = 1045
        y = 50
        for i in range(4):
            self.table_card_slots.append(fig.add_axes([x, y+22*i, 11, 22]))




        plt.draw()
       # plt.show()
    colors = []
    cities = dict()
    x = []
    y = []
    player_1_cards = dict()
    player_2_cards = dict()
    edge_weights = dict()
    cards = dict()
    table_card_slots = list()
    p1_score=[]
    p2_score=[]
    p1_cars=[]
    p2_cars=[]



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
        # TODO: Implement.
        self.update_display(game)
        self.update_edges(game)
        #self.update_cards(game)
        plt.draw()
        pass

    def update_cards(self,game):
            face_up_cards = game.get_face_up_cards()
            i=0;
            for card_key in face_up_cards:
                print(str(card_key))
                if(i < len(self.table_card_slots)):
                    self.table_card_slots[i].imshow(self.cards[str(card_key)])
                    i = i+1
            
                                              

    def update_display(self,game):
        scores = game.get_visible_scores()

        print scores
        for player in game._players:
            cards = game.get_player_info(player).hand.cards
            for card in cards:
                if(player.name == 'P1'):
                    self.player_1_cards[str(card)].set_text(str(cards[card]))
                    self.p1_score.set_text(str(scores[player.name]))
                    self.p1_cars.set_text(str(game.get_player_info(player).num_cars))
                elif(player.name == 'P2'):
                    self.player_2_cards[str(card)].set_text(str(cards[card]))
                    self.p2_score.set_text(str(scores[player.name]))
                    self.p2_cars.set_text(str(game.get_player_info(player).num_cars))


    def update_edges(self,game):
        edges = game.get_edge_claims()
        for edge in edges:
            #print(edge)
            #print(edges[edge])
            if(edges[edge] == 'P1'):
                plt.setp(self.edge_weights[edge],'color','b')
            elif(edges[edge] == 'P2'):
                plt.setp(self.edge_weights[edge],'color','r')

                #print(card_value)
                #print(game.get_player_info(player).hand.cards{card})
                #i=i+1

                #print(self.cards_pos_x[int(card)])
                #print(self.cards_pos_y[j])

               # plt.text(self.cards_pos_x[int(card)], self.cards_pos_y[j], str(cards[card]), fontdict=None)


    def update_game_ended(self, game):
        self.update(game)
        plt.ioff()
        plt.show()
        # TODO: Implement.
        pass

    # game.add_turn_ended_event(self.update)
