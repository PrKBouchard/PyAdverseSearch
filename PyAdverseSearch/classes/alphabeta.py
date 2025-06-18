import time
from PyAdverseSearch.classes.algorithm import SearchAlgorithm
from PyAdverseSearch.classes.node import Node

class AlphaBeta(SearchAlgorithm):
    def __init__(self, game=None, max_depth=9, max_time_seconds=None):
        # Verifying parameters
        if max_depth is not None and (max_depth <= 0 or not isinstance(max_depth, int)):
            print("Error: max_depth must be a positive integer")
            return
        if max_time_seconds is not None and (max_time_seconds <= 0 or not isinstance(max_time_seconds, (int, float))):
            print("Error: max_time_seconds must be a positive number")
            return

        self.game = game
        self.max_depth = max_depth
        self.max_time = max_time_seconds
        self.start_time = None

    def choose_best_move(self, state):
        """
        Selects the best move for the current player using alpha-beta pruning.
        """
        self.start_time = time.time()
        is_max = (state.player == "MAX")
        
        best_score = -float('inf') if is_max else float('inf')
        best_move = None
        alpha = -float('inf')
        beta = float('inf')

        for action in state._possible_actions():
            child = state._apply_action(action)
            
            if self.time_limit_reached():
                break

            if is_max:
                score = self.min_value(child, self.max_depth - 1, alpha, beta)
                if score > best_score:
                    best_score = score
                    best_move = child
                    alpha = max(alpha, best_score)
            else:
                score = self.max_value(child, self.max_depth - 1, alpha, beta)
                if score < best_score:
                    best_score = score
                    best_move = child
                    beta = min(beta, best_score)

        return best_move

    def max_value(self, state, depth, alpha, beta):
        """
        Returns the highest value for MAX with alpha-beta pruning.
        """
        if self.time_limit_reached():
            return self.game.game_heuristic(state)

        # Terminal state
        if self.game.game_is_terminal(state):
            return self.game.game_utility(state)
        # Depth cutoff
        if depth == 0:
            return self.game.game_heuristic(state)

        v = -float('inf')
        for action in state._possible_actions():
            child = state._apply_action(action)
            v = max(v, self.min_value(child, depth - 1, alpha, beta))
            alpha = max(alpha, v)
            if v >= beta:
                return v 
        return v

    def min_value(self, state, depth, alpha, beta):
        """
        Returns the smallest value for MIN with alpha-beta pruning.
        """
        if self.time_limit_reached():
            return self.game.game_heuristic(state)

        # Terminal state
        if self.game.game_is_terminal(state):
            return self.game.game_utility(state)
        # Depth cutoff
        if depth == 0:
            return self.game.game_heuristic(state)

        v = float('inf')
        for action in state._possible_actions():
            child = state._apply_action(action)
            v = min(v, self.max_value(child, depth - 1, alpha, beta))
            beta = min(beta, v)
            if v <= alpha:
                return v  # Alpha cutoff
        return v

    def time_limit_reached(self):
        if self.max_time is None:
            return False
        return (time.time() - self.start_time) >= self.max_time


    def next_move(self, node):
        """
        Selects the best next move using alpha-beta pruning.
        """
        if not node.children:
            return None

        child_utils = [(child, self.default_utility(child)) for child in node.children]
        if node.state.player == "MAX":
            best_child = max(child_utils, key=lambda x: x[1])[0]
        else:
            best_child = min(child_utils, key=lambda x: x[1])[0]
        return best_child