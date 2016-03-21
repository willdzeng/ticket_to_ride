from greedy_ai import GreedyAI


class CheapestPathAI(GreedyAI):
    def __init__(self, name):
        GreedyAI.__init__(self, name)
        self.sort_method = lambda path: path.cost
