import time
from PyAdverseSearch.classes.algorithm import SearchAlgorithm

class AlphaBeta(SearchAlgorithm):
    """
    Algorithme Alpha-Beta avec élagage pour la recherche dans les arbres de jeu.

    Alpha-Beta est une amélioration de Minimax qui élague les branches de l'arbre
    qui ne peuvent pas influencer la décision finale, réduisant ainsi le nombre
    de nœuds explorés tout en garantissant le même résultat que Minimax.
    """

    def __init__(self, game=None, max_depth=9, max_time_seconds=None, use_transposition_table=False):
        """
        Initialise l'algorithme Alpha-Beta.

        :param game: Instance du jeu
        :param max_depth: Profondeur maximale de recherche
        :param max_time_seconds: Temps maximum de recherche en secondes
        :param use_transposition_table: Utiliser une table de transposition pour mémoriser les états
        """
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
        self.use_transposition_table = use_transposition_table
        self.transposition_table = {} if use_transposition_table else None
        self.nodes_explored = 0
        self.cutoffs = 0

    def choose_best_move(self, state):
        """
        Selects the best move for the current player using alpha-beta pruning.

        :param state: État actuel du jeu
        :return: Le meilleur état enfant trouvé
        """
        self.start_time = time.time()
        self.nodes_explored = 0
        self.cutoffs = 0
        if self.use_transposition_table:
            self.transposition_table.clear()

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

        :param state: État actuel
        :param depth: Profondeur restante
        :param alpha: Meilleure valeur pour MAX
        :param beta: Meilleure valeur pour MIN
        :return: Valeur de l'état
        """
        self.nodes_explored += 1

        if self.time_limit_reached():
            return self.game.game_heuristic(state)

        # Check transposition table
        state_key = None
        if self.use_transposition_table:
            state_key = self._get_state_key(state)
            if state_key in self.transposition_table:
                cached = self.transposition_table[state_key]
                if cached['depth'] >= depth:
                    return cached['value']

        # Terminal state
        if self.game.game_is_terminal(state):
            value = self.game.game_utility(state)
            if self.use_transposition_table and state_key is not None:
                self.transposition_table[state_key] = {'value': value, 'depth': depth}
            return value

        # Depth cutoff
        if depth == 0:
            value = self.game.game_heuristic(state)
            if self.use_transposition_table and state_key is not None:
                self.transposition_table[state_key] = {'value': value, 'depth': depth}
            return value

        v = -float('inf')
        for action in state._possible_actions():
            child = state._apply_action(action)
            v = max(v, self.min_value(child, depth - 1, alpha, beta))
            alpha = max(alpha, v)
            if v >= beta:
                self.cutoffs += 1
                if self.use_transposition_table and state_key is not None:
                    self.transposition_table[state_key] = {'value': v, 'depth': depth}
                return v  # Beta cutoff

        if self.use_transposition_table and state_key is not None:
            self.transposition_table[state_key] = {'value': v, 'depth': depth}
        return v

    def min_value(self, state, depth, alpha, beta):
        """
        Returns the smallest value for MIN with alpha-beta pruning.

        :param state: État actuel
        :param depth: Profondeur restante
        :param alpha: Meilleure valeur pour MAX
        :param beta: Meilleure valeur pour MIN
        :return: Valeur de l'état
        """
        self.nodes_explored += 1

        if self.time_limit_reached():
            return self.game.game_heuristic(state)

        # Check transposition table
        state_key = None
        if self.use_transposition_table:
            state_key = self._get_state_key(state)
            if state_key in self.transposition_table:
                cached = self.transposition_table[state_key]
                if cached['depth'] >= depth:
                    return cached['value']

        # Terminal state
        if self.game.game_is_terminal(state):
            value = self.game.game_utility(state)
            if self.use_transposition_table and state_key is not None:
                self.transposition_table[state_key] = {'value': value, 'depth': depth}
            return value

        # Depth cutoff
        if depth == 0:
            value = self.game.game_heuristic(state)
            if self.use_transposition_table and state_key is not None:
                self.transposition_table[state_key] = {'value': value, 'depth': depth}
            return value

        v = float('inf')
        for action in state._possible_actions():
            child = state._apply_action(action)
            v = min(v, self.max_value(child, depth - 1, alpha, beta))
            beta = min(beta, v)
            if v <= alpha:
                self.cutoffs += 1
                if self.use_transposition_table and state_key is not None:
                    self.transposition_table[state_key] = {'value': v, 'depth': depth}
                return v  # Alpha cutoff

        if self.use_transposition_table and state_key is not None:
            self.transposition_table[state_key] = {'value': v, 'depth': depth}
        return v

    def time_limit_reached(self):
        """Vérifie si la limite de temps est atteinte."""
        if self.max_time is None:
            return False
        return (time.time() - self.start_time) >= self.max_time

    def _get_state_key(self, state):
        """
        Génère une clé unique pour un état (pour la table de transposition).

        :param state: État du jeu
        :return: Clé hashable représentant l'état
        """
        if hasattr(state.board, 'tobytes'):
            # Pour les numpy arrays
            return state.board.tobytes()
        elif isinstance(state.board, (list, tuple)):
            # Pour les listes/tuples
            return str(state.board)
        else:
            # Fallback
            return str(state.board)

    def get_statistics(self):
        """
        Retourne les statistiques de la dernière recherche.

        :return: Dictionnaire avec les statistiques
        """
        return {
            'nodes_explored': self.nodes_explored,
            'cutoffs': self.cutoffs,
            'transposition_table_size': len(self.transposition_table) if self.use_transposition_table else 0
        }




