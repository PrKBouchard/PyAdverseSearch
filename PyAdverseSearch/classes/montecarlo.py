import math
import random
import time
from PyAdverseSearch.classes.algorithm import SearchAlgorithm
from PyAdverseSearch.classes.node import Node

class MonteCarlo(SearchAlgorithm):
    def __init__(self, game=None, max_iterations=10000, max_time_seconds=None):
        self.game = game
        self.max_iterations = max_iterations
        self.max_time = max_time_seconds
        self.start_time = None

    def choose_best_move(self, state):
        root = Node(state, parent=None, depth=0)
        stats = {}

        self.start_time = time.time()

        for _ in range(self.max_iterations):
            if self.time_limit_reached():
                break
            self.run_simulation(root, stats)

        if not root.children:
            root._expand()

        if not root.children:
            return state  # Aucun coup possible

        best_child = max(
            root.children,
            key=lambda child: stats.get(child.id, (0, 0))[1]
        )
        return best_child.state

    def run_simulation(self, root, stats):
        node = self.select(root, stats)
        if not self.game.game_is_terminal(node.state):
            node._expand()
            if node.children:
                node = random.choice(node.children)

        result = self.simulate(node)
        self.backpropagate(node, result, stats)

    def select(self, node, stats):
        while node.children:
            node = self.ucb1_select(node, stats)
        return node

    def ucb1_select(self, node, stats):
        total_visits = sum(stats.get(child.id, (0, 1))[1] for child in node.children)
        log_total = math.log(total_visits + 1)
        
        best_score = -float('inf')
        best_child = None

        # Determine if the current node's player is MAX or MIN
        is_max_turn = (node.player == "MAX")

        for child in node.children:
            wins, visits = stats.get(child.id, (0, 1))
            
            # Average score from MAX's perspective (-1 to 1)
            avg_score = wins / visits
            
            # If it's MIN's turn, they want to minimize the score (make it negative).
            # To use the standard UCB maximization formula, we can invert the score for MIN.
            # If MIN is playing, a score of -1 (MIN win) is "good" (+1 for MIN).
            
            if is_max_turn:
                exploitation = avg_score
            else:
                exploitation = -avg_score # Invert so that -1 becomes +1 (good for MIN)

            # UCB1 formula
            ucb1 = exploitation + math.sqrt(2 * log_total / visits)

            if ucb1 > best_score:
                best_score = ucb1
                best_child = child

        return best_child

    def simulate(self, node):
        state = node.state
        while not self.game.game_is_terminal(state):
            actions = state._possible_actions()
            if not actions:
                break
            action = random.choice(actions)
            state = state._apply_action(action)
        return self.evaluate_winner(state)

    def evaluate_winner(self, state):
        winner = self.game.winner_function(state)
        if winner == "MAX":
            return 1
        elif winner == "MIN":
            return -1
        else:
            return 0

    def backpropagate(self, node, result, stats):
        while node is not None:
            if node.id not in stats:
                stats[node.id] = (0, 0)
            wins, visits = stats[node.id]
            stats[node.id] = (wins + result, visits + 1)
            node = node.parent

    def time_limit_reached(self):
        if self.max_time is None:
            return False
        return (time.time() - self.start_time) >= self.max_time
