from ai.cf_ai.cf_base_ai import CFBaseAI


class GreedyAI(CFBaseAI):
    """
    Plays the same as the CFBase AI, but looks for the path with the highest score.
    """
    def __init__(self, name):
        CFBaseAI.__init__(self, name)

    def path_cost(self, path, all_paths, edge_costs, game):
        return path.cost
