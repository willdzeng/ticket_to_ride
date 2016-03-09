from game.classes import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from game.board import create_board


#cities = dict()

#cities = dict()
#x = []
#y = [] 

class GUI():
    colors = []
    cities = dict()
    x = []
    y = [] 
    def place_cities(self):
        self.cities = {"Atlanta": [775 , 516],
                       "Boston": [1018 , 315.5],
                       "Calgary": [235 , 85.7],
                       "Charleston":  [857 , 537],
                       "Chicago" :  [717 , 329],
                       "Dallas":  [549 , 537],
                       "Denver":  [397.3 , 380.3],
                       "Duluth": [ 633.2, 203.6 ],
                       "El Paso": [ 370.7, 559.1 ],
                       "Helena": [ 270.1, 208.3 ],
                       "Houston": [ 573.2, 601.5 ],
                       "Kansas City": [ 588, 394.6 ],
                       "Las Vegas": [ 213.1, 461.6 ],
                       "Little Rock": [ 630, 494 ],
                       "Los Angeles": [ 157.4, 508.9 ],
                       "Miami": [ 850.3, 683.5 ],
                       "Montreal": [ 971.5, 237.1 ],
                       "Nashville": [ 730, 461 ],
                       "New Orleans": [ 670, 597.4 ],
                       "New York": [ 962.9, 356.7 ],
                       "Oklahoma City": [ 533.9, 477.8 ],
                       "Omaha": [ 562.1, 343.1 ],
                       "Phoenix": [ 268.8, 522.45 ],
                       "Pittsburgh": [ 854, 362.7 ],
                       "Portland": [ 76.9, 236.7 ],
                       "Raleigh": [ 877.5, 470.881 ],
                       "Saint Louis": [ 668.1, 406.26 ],
                       "Salt Lake City": [ 272, 354.775 ],
                       "San Francisco": [ 81.6, 426 ],
                       "Santa Fe": [ 381.1, 472.8 ],
                       "Sault St. Marie": [ 774, 211.5 ],
                       "Seattle": [ 82.7, 181.6 ],
                       "Toronto": [ 864.5 , 283.9 ],
                       "Vancouver": [ 68.6, 135.9 ],
                       "Washington DC": [ 908.5, 398.8 ],
                       "Winnipeg": [ 540.9, 118.8 ]
                   }

    def setColors(self):
        #self.colors={'Red':'#185aa9',
        #             'Orange':'#185aa9', 
        #             'Blue':'AA3939',
        #             'Yellow':'#185aa9',
        #             'Green':'#185aa9',
        #             'Pink':'#185aa9',
        #             'Black':'#185aa9',
        #             'White':'#185aa9',
        #             'None':'#185aa9',
        #         }
        self.colors=['#b61c16','#bc5510','#1033bc','#d8c413','#13750a','#6c0a75','#030203','#ebeaeb','#6d696d']
                     
    def plot_board(self):
        for city in self.cities:
            self.x.append(self.cities[city][0])
            self.y.append(self.cities[city][1])        
  
                
if __name__ == '__main__':
    gui = GUI()
    img=mpimg.imread('world2.png')
    imgplot = plt.imshow(img)
    gui.place_cities()
    gui.plot_board()
    gui.setColors()
    plt.plot(gui.x,gui.y,'ro')
    [city_edges,edges] = create_board()
    
    for edge in edges:
        x_1 = []
        y_1 = []
        x_1.append(gui.cities[edge.city1][0])
        y_1.append(gui.cities[edge.city1][1])
        x_1.append(gui.cities[edge.city2][0])
        y_1.append(gui.cities[edge.city2][1])
        plt.plot(x_1,y_1,gui.colors[edge.color])

    plt.show()





