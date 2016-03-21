from greedy_ai import GreedyAI


class CheapestPathAI(GreedyAI):
    """
    Plays the same as the greedy AI, but looks for the cheapest path, instead of the one with the best score.
    """
    def __init__(self, name):
        GreedyAI.__init__(self, name)
        self.sort_method = lambda path: path.cost
