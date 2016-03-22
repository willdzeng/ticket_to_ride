from game.classes import *
from game.board import *
import numpy as np

class GraphTopology:
    claimants = dict()
    city_to_i = dict()
    Laplacian = None
    Degree = None
    Adjacency = None
    cities = None
    routes = None

    def __init__(self):
        pass

    #Set edge weights based on who has claimed them
    def set_claim_value(self,claimant,value):
        claimants[claimant] = value

    def route_weight(route):
        return self.claimants[self.routes[route]]
  
    def initialize_matrices(self):
        #self.laplacian = [[0 for i in range(40)] for j in range(40)]
        self.degree = [[0 for i in range(40)] for j in range(40)]
        self.adjacency =  [[0 for i in range(40)] for j in range(40)]
        self.cities = dict()
        self.city_to_i = dict()

    #Create a new adjacency matrix based on claims
    def update_game_board(self,game):
        initialize_matrices()
        self.routes = game.get_edge_claims()
        i=0;
        for route in self.routes:
            if route_weight(route) > 0:
                if route.city1 is not in self.cities:
                    self.cities.append(route.city1)
                    self.city_to_i[route.city1]=i
                    i=i+1
                if route.city2 is not in self.cities:
                    self.cities.append(route.city2)
                    self.city_to_i[route.city2]=i
                    i=i+1
                city1 = self.city_to_i[route.city1]
                city2 = self.city_to_i[route.city2]
                self.adjacency[city1][city2] = route_weight(route)
                self.degree [city1][city1] =  self.degree [city1][city1] +1;
                self.degree [city2][city2] =  self.degree [city2][city2] +1;
        
        self.adjacency = self.adjacency[1:i-1][1:i-1]
        self.degrees = self.degree[1:i-1][1:i-1]
        self.laplacian = self.degree - self.adjacency

    def get_edge(self):
        w,v = np.linalg.eig(self.laplacian)
        return w 


