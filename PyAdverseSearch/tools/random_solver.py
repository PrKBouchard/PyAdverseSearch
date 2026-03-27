import random

class RandomSolver:
    def __init__(self):
        self.name = "Random Baseline"

    def get_best_move(self, root_node):
        successors = root_node.state._generate_successors()
        if not successors:
            return None
        # Just pick one at random
        chosen = random.choice(successors)
        return chosen.board