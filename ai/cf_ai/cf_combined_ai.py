from random import randrange

import game.board as board
from game import Player, Game
from game.actions import *
from game.classes import Colors
from game.methods import find_paths_for_destinations
from cf_base_ai import CFBaseAI
from cf_action_eval_ai import CFActionEvalAI
from game.methods import get_threatened_edges


class CFCombinedAI(CFActionEvalAI):
    "Evaluate Every Action Based on the cost function"
    T_Remaining_Cars = 4  # constant related to the remaining cars when evaluating threaten edge
    T_Edge_Weight = 0.05  # constant related to edge cost when evaluating threaten edge
    T_Edge_Group_Length = 2  # constant related to the length of edge group when evaluating threaten edge
    Threat_Action_Weight = 0.03  # total weight when combined with other cost
    Threat_Edge_Threshold = 15  # the threshold when evaluate if it's a threaten edge
    T_Multi_Edge_Penalty = 20  # the penalty of having multiple threaten edge
    gui_debug = False

    def __init__(self, name):
        CFActionEvalAI.__init__(self, name)

    def eval_threatened_edges(self):
        """
        get and evaluate threatened edges
        :return: nothing returned, the evaluation will store in the threatened_edges and threatened_edges_score
        """
        threatened_edges = get_threatened_edges(self.opponent_name[0], self.edge_claims,
                                                self.Threat_Edge_Threshold)
        self.threatened_edges = []

        # first added the result into self
        for tmp_edge_group in threatened_edges:
            t_edge = tmp_edge_group[0]
            self.threatened_edges.append(t_edge)

        # then find out the double edges in the group
        t_edge_length = len(self.threatened_edges)
        double_edge = []
        for i in range(0, t_edge_length - 1):
            for j in range(i + 1, t_edge_length):
                edge1 = self.threatened_edges[i]
                edge2 = self.threatened_edges[j]
                if (edge1.city1 == edge2.city1 and edge1.city2 == edge2.city2) \
                        or (edge1.city1 == edge2.city2 and edge1.city2 == edge1.city1):
                    double_edge.append(i)
                    double_edge.append(j)

        # remove the double edges
        new_edge = [v for i, v in enumerate(self.threatened_edges) if i not in double_edge]
        self.threatened_edges = new_edge
        self.threatened_edges_score = []

        # score the threatened edges
        penalty = (len(threatened_edges) - 1) * self.T_Multi_Edge_Penalty
        for tmp_edge_group in threatened_edges:
            if len(tmp_edge_group) is not 3:
                print "##### A bug of getting threatened edge ######"
                continue
            left_edge_group = tmp_edge_group[1]
            right_edge_group = tmp_edge_group[2]
            score = 0 - penalty
            # add score based on the player's remaining cars.
            score += self.T_Remaining_Cars * (45 - self.player_cars_count[self.opponent_name[0]])
            for edge_group in [left_edge_group, right_edge_group]:
                for edge in edge_group:
                    # add score based on all the edge's cost
                    score += edge.cost * self.T_Edge_Weight
                # add score based on the length of the edge group
                score += len(edge_group) ** self.T_Edge_Group_Length
            # make sure the score is higher than 0
            if score < 0:
                score = 0
            # if we have multiple threaten edges, we shouldn't claim anythings
            self.threatened_edges_score.append(score)
            # if self.print_debug:
            #     print tmp_edge_group,'has score ',score
