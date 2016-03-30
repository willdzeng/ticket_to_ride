from game.classes import *
from game.board import *
import numpy as np

class GraphTopology:
    claimants = dict()
    city_to_i = dict()
    Laplacian = None
    Degree = None
    Adjacency = None
    cities = list()
    routes = None

    def __init__(self):
        pass

    #Set edge weights based on who has claimed them
    def set_claim_value(self,claimant,value):
        self.claimants[claimant] = value

    def route_weight(self,route):
        #print self.claimants
        #print route
        #print self.routes.get(route) or 'unclaimed'
        #print self.claimants.get(self.routes.get(route,'unclaimed'))
        #return self.claimants[self.routes.get(route,'unclaimed')]
        return self.claimants[self.routes.get(route) or 'unclaimed' ]
        
    def initialize_matrices(self):
        #self.laplacian = [[0 for i in range(40)] for j in range(40)]
        self.degree = [[0 for i in range(40)] for j in range(40)]
        self.adjacency =  [[0 for i in range(40)] for j in range(40)]
        self.cities = list()
        self.city_to_i = dict()

    def get_2d_list_slice(self, matrix, start_row, end_row, start_col, end_col):
        return [row[start_col:end_col] for row in matrix[start_row:end_row]]

    #Create a new adjacency matrix based on claims
    def update_game_board(self,game):
        self.initialize_matrices()
        self.routes = game.get_edge_claims()
        i=0;
        for route in self.routes:
            if self.route_weight(route) > 0:
                if route.city1 not in self.cities:
                    self.cities.append(route.city1)
                    self.city_to_i[route.city1]=i
                    i=i+1
                if route.city2 not in self.cities:
                    self.cities.append(route.city2)
                    self.city_to_i[route.city2]=i
                    i=i+1
                city1 = self.city_to_i[route.city1]
                city2 = self.city_to_i[route.city2]
                self.adjacency[city1][city2] = self.route_weight(route)
                self.degree [city1][city1] =  self.degree [city1][city1] +1;
                self.degree [city2][city2] =  self.degree [city2][city2] +1;
        #print self.degree
        #print i
        #np.delete.adjacency(
    
        #self.adjacency2 = numpy.array(self.adjacency)[[0:i-1],[0:i-1]]
        #self.degree2 = numpy.array(self.degree)[[0:i-1][0:i-1]]
        
        self.adjacency = self.get_2d_list_slice(self.adjacency,0,i,0,i)
        self.degree = self.get_2d_list_slice(self.degree,0,i,0,i)

        print self.degree
        self.laplacian = np.subtract(self.degree, self.adjacency)
        print len(self.laplacian)
        print self.laplacian

    def get_edge(self):
        w,v = np.linalg.eig(self.laplacian)
        return w 


