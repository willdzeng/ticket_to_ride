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
        plt.figure() #uncomment to let go of string
        imgplot = plt.imshow(img)

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
        y = 60
        i = 0
        for i in range(9):

            print(str(i))
            self.player_1_cards[str(i)] = plt.text(x, y, '0', fontdict=None)
            x = x+ 39

            #Next for player 2
        x = 705
        y = 130
        i = 0
        for i in range(9):
            self.player_2_cards[str(i)] = plt.text(x, y, '0', fontdict=None)
            x = x+ 39



 #           iter_pos_x = iter(self.cards_pos_x)
 #           last_pos_x = self.cards_pos_x[0]
 #           inc = 30
 #           next(iter_pos_x)
 #           i=1
 #           for pos_x in iter_pos_x:
 #               self.cards_pos_x[i] = last_pos_x + inc
 #               last_pos_x = pos_x
                #print(pos_x)
 #               i=i+1
 #               print(self.cards_pos_x)
        plt.draw()

    colors = []
    cities = dict()
    x = []
    y = []
#cards_pos_x =[ 700 ,0 , 0 ,0 ,0 ,0 ,0 ,0 ,0, 0 ]
#    cards_pos_y = [ 100, 130]
    player_1_cards = dict()
    player_2_cards = dict()
    edge_weights = dict()


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
        # self.colors={'Red':'#185aa9',
        #             'Orange':'#185aa9', 
        #             'Blue':'AA3939',
        #             'Yellow':'#185aa9',
        #             'Green':'#185aa9',
        #             'Pink':'#185aa9',
        #             'Black':'#185aa9',
        #             'White':'#185aa9',
        #             'None':'#185aa9',
        #         }
        self.colors = ['#b61c16', '#bc5510', '#1033bc', '#d8c413', '#13750a', '#6c0a75', '#030203', '#ebeaeb',
                       '#6d696d']

    def plot_board(self):

        
        
        for city in self.cities:
            self.x.append(self.cities[city][0])
            self.y.append(self.cities[city][1])

    def update(self, game):
        # TODO: Implement.
        self.update_displayed_cards(game)
        #current_game_state = get_player_info(game)
        plt.draw()
        pass



    #current_game_state.in_hands

    def update_displayed_cards(self,game):
        for player in game._players:
            #print(player.name)
            #print('here')
            #print(game.get_player_info(player).hand.cards)
            cards = game.get_player_info(player).hand.cards
            for card in cards:
                #print('here 1')
                #print(card)
                #print(cards[card])
                if(player.name == 'P1'):
                    self.player_1_cards[str(card)].set_text(str(cards[card]))
                elif(player.name == 'P2'):
                    self.player_2_cards[str(card)].set_text(str(cards[card]))

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
        plt.show()
        # TODO: Implement.
        pass

    # game.add_turn_ended_event(self.update)
