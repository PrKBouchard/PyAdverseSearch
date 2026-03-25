# FILE: PyAdverseSearch/classes/mtdf.py

import time
import random
from PyAdverseSearch.classes.algorithm import SearchAlgorithm


class MTDf(SearchAlgorithm):
    """
    MTD(f) - Memory-enhanced Test Driver.

    Corrections apportees :

    - MTDf appelle ``_alpha_beta_tt`` sur la RACINE (pas sur chaque enfant)
    - Le first-guess est la valeur exacte rendue par la profondeur d-1
    - La TT est conservee entre les profondeurs de l'iterative deepening
    - Move ordering : center-bias Puissance 4 + score heuristique
      sans double ``_apply_action`` (les enfants sont calcules une seule fois)
    - Killer moves : memorise les actions qui ont produit des coupures

    Reference: Aske Plaat et al. "MTD(f), a new chess algorithm" (1996)
    """

    def __init__(self, game=None, max_depth=6, max_time_seconds=2.0, initial_guess=0):
        if max_depth is not None and (max_depth <= 0 or not isinstance(max_depth, int)):
            print("Error: max_depth must be a positive integer")
            return
        if max_time_seconds is not None and (max_time_seconds <= 0 or not isinstance(max_time_seconds, (int, float))):
            print("Error: max_time_seconds must be a positive number")
            return

        self.game = game
        self.max_depth = max_depth
        self.max_time = max_time_seconds if max_time_seconds is not None else 2.0
        self.initial_guess = initial_guess
        self.start_time = None

        # TT conservee entre les profondeurs : key -> {'lb', 'ub', 'depth', 'best_action'}
        self.transposition_table = {}

        # Killer moves par profondeur : depth -> [action1, action2]
        self._killers = {}

        # Zobrist
        self._zobrist_table = None
        self._zobrist_cols = 0
        self._zobrist_rows = 0

        # Stats
        self.nodes_explored = 0
        self.cutoffs = 0
        self.iterations = 0
        self._tt_hits = 0
        self._tt_lookups = 0

    # ------------------------------------------------------------------
    # Zobrist
    # ------------------------------------------------------------------

    def _init_zobrist(self, rows, cols):
        if (self._zobrist_table is not None
                and self._zobrist_cols == cols
                and self._zobrist_rows == rows):
            return
        self._zobrist_rows = rows
        self._zobrist_cols = cols
        rng = random.Random(42)
        self._zobrist_table = [
            [[rng.getrandbits(64) for _ in range(cols)] for _ in range(rows)]
            for _ in range(2)
        ]

    def _zobrist_hash(self, board):
        rows = len(board)
        cols = len(board[0]) if rows > 0 else 0
        self._init_zobrist(rows, cols)
        h = 0
        for r in range(rows):
            for c in range(cols):
                cell = board[r][c]
                if cell == 'X':
                    h ^= self._zobrist_table[0][r][c]
                elif cell == 'O':
                    h ^= self._zobrist_table[1][r][c]
        return h

    def _get_state_key(self, state):
        board = state.board
        if hasattr(board, 'tobytes'):
            return hash(board.tobytes())
        return self._zobrist_hash(board)

    # ------------------------------------------------------------------
    # Table de transposition (bornes correctes lb/ub)
    # ------------------------------------------------------------------

    def _tt_lookup(self, key, depth, alpha, beta):
        """
        Retourne (hit, valeur, alpha_ajuste, beta_ajuste).
        Accepte les entrees de profondeur >= depth (plus profondes = plus precises).
        """
        self._tt_lookups += 1
        entry = self.transposition_table.get(key)
        if entry is None or entry['depth'] < depth:
            return False, None, alpha, beta

        self._tt_hits += 1
        lb, ub = entry['lb'], entry['ub']

        if lb >= beta:
            return True, lb, alpha, beta
        if ub <= alpha:
            return True, ub, alpha, beta

        alpha = max(alpha, lb)
        beta  = min(beta,  ub)
        if alpha >= beta:
            return True, lb, alpha, beta

        return False, None, alpha, beta

    def _tt_store(self, key, g, alpha_orig, beta, depth, best_action=None):
        entry = self.transposition_table.get(key)
        # Ne pas ecraser une entree strictement plus profonde
        if entry is not None and entry['depth'] > depth:
            return

        if g <= alpha_orig:
            lb, ub = -float('inf'), g        # borne superieure
        elif g >= beta:
            lb, ub = g, float('inf')         # borne inferieure
        else:
            lb, ub = g, g                    # valeur exacte

        self.transposition_table[key] = {
            'lb': lb, 'ub': ub,
            'depth': depth,
            'best_action': best_action,
        }

    # ------------------------------------------------------------------
    # Move ordering
    # ------------------------------------------------------------------

    def _order_actions(self, state, actions, depth, is_max):
        """
        Tri des actions pour maximiser l'elagage :
        1. Killer moves (actions ayant produit des coupures a cette profondeur)
        2. Best action memorisee dans la TT pour cet etat
        3. Center-bias Puissance 4 (colonne centrale en premier)
        4. Score heuristique de l'etat enfant

        Les enfants ne sont calcules qu'une seule fois ici puis renvoyes
        pour eviter le double _apply_action dans _alpha_beta_tt.
        """
        if not actions:
            return []

        cols = len(state.board[0]) if state.board else 7
        center = cols // 2

        # Recuperer le best_action de la TT pour cet etat
        key = self._get_state_key(state)
        tt_best = self.transposition_table.get(key, {}).get('best_action')

        killers = self._killers.get(depth, [])

        scored = []
        for action in actions:
            child = state._apply_action(action)

            # Priorite 1 : TT best action
            if action == tt_best:
                priority = 3
            # Priorite 2 : killer move
            elif action in killers:
                priority = 2
            else:
                priority = 0

            center_bonus = (center - abs(action - center)) * 0.1
            try:
                h = self.game.game_heuristic(child)
            except Exception:
                h = 0.0

            scored.append((action, child, priority, h + center_bonus))

        # Trier : priority DESC, puis heuristique (MAX veut haut, MIN veut bas)
        scored.sort(key=lambda x: (x[2], x[3] if is_max else -x[3]), reverse=True)
        return [(a, c) for a, c, _, _ in scored]

    def _add_killer(self, depth, action):
        if depth not in self._killers:
            self._killers[depth] = []
        killers = self._killers[depth]
        if action not in killers:
            killers.insert(0, action)
            if len(killers) > 2:
                killers.pop()

    # ------------------------------------------------------------------
    # Alpha-Beta avec memoire (noyau MTDf)
    # ------------------------------------------------------------------

    def _alpha_beta_tt(self, state, depth, alpha, beta, is_max):
        self.nodes_explored += 1

        if self.time_limit_reached():
            return self.game.game_heuristic(state)

        key = self._get_state_key(state)
        alpha_orig = alpha

        hit, val, alpha, beta = self._tt_lookup(key, depth, alpha, beta)
        if hit:
            return val

        if self.game.game_is_terminal(state):
            v = self.game.game_utility(state)
            self._tt_store(key, v, alpha_orig, beta, depth)
            return v

        if depth == 0:
            v = self.game.game_heuristic(state)
            self._tt_store(key, v, alpha_orig, beta, depth)
            return v

        actions = state._possible_actions()
        if not actions:
            v = self.game.game_heuristic(state)
            self._tt_store(key, v, alpha_orig, beta, depth)
            return v

        ordered = self._order_actions(state, actions, depth, is_max)

        best_action = None
        if is_max:
            g = -float('inf')
            for action, child in ordered:
                if self.time_limit_reached():
                    break
                v = self._alpha_beta_tt(child, depth - 1, alpha, beta, False)
                if v > g:
                    g = v
                    best_action = action
                alpha = max(alpha, g)
                if g >= beta:
                    self.cutoffs += 1
                    self._add_killer(depth, action)
                    break
        else:
            g = float('inf')
            for action, child in ordered:
                if self.time_limit_reached():
                    break
                v = self._alpha_beta_tt(child, depth - 1, alpha, beta, True)
                if v < g:
                    g = v
                    best_action = action
                beta = min(beta, g)
                if g <= alpha:
                    self.cutoffs += 1
                    self._add_killer(depth, action)
                    break

        self._tt_store(key, g, alpha_orig, beta, depth, best_action)
        return g

    # ------------------------------------------------------------------
    # MTDf : convergence par fenetres nulles successives sur la RACINE
    # ------------------------------------------------------------------

    def _mtdf_at_depth(self, state, depth, f, is_max):
        """
        MTDf correct : appele sur la RACINE, encadre la valeur par fenetres nulles
        jusqu'a ce que lb == ub (convergence), puis retourne la valeur exacte.
        """
        g  = f
        lb = -float('inf')
        ub =  float('inf')

        while lb < ub:
            self.iterations += 1
            if self.time_limit_reached():
                break

            beta = g + 1 if g == lb else g
            beta = max(beta, lb + 1)

            g = self._alpha_beta_tt(state, depth, beta - 1, beta, is_max)

            if g < beta:
                ub = g
            else:
                lb = g

        return g

    # ------------------------------------------------------------------
    # Interface publique
    # ------------------------------------------------------------------

    def choose_best_move(self, state):
        """
        Iterative Deepening + MTDf.

        A chaque profondeur :
        1. MTDf est appele sur la RACINE -> valeur exacte de la position
        2. Cette valeur sert de first-guess pour la profondeur suivante
        3. Le meilleur coup est lu depuis la TT (best_action stocke a la racine)
        """
        self.start_time = time.time()
        self.nodes_explored = 0
        self.cutoffs = 0
        self.iterations = 0
        self._tt_hits = 0
        self._tt_lookups = 0
        self._killers = {}
        # On NE vide PAS la TT entre les profondeurs : les entrees plus
        # profondes restent valables et servent de guide pour les passes suivantes.
        # On vide seulement si la TT depasse 500 000 entrees pour eviter OOM.
        if len(self.transposition_table) > 500_000:
            self.transposition_table.clear()

        is_max = (state.player == "MAX")
        actions = state._possible_actions()

        if not actions:
            return None

        # Coup par defaut : centre du plateau
        cols = len(state.board[0]) if state.board else 7
        center = cols // 2
        best_move = state._apply_action(
            min(actions, key=lambda a: abs(a - center))
        )
        f = self.initial_guess  # first-guess initial

        root_key = self._get_state_key(state)

        for depth in range(1, self.max_depth + 1):
            if self.time_limit_reached():
                break

            # MTDf sur la racine entiere
            f = self._mtdf_at_depth(state, depth, f, is_max)

            # Lire le meilleur coup depuis la TT
            tt_entry = self.transposition_table.get(root_key)
            if tt_entry and tt_entry.get('best_action') is not None:
                best_action = tt_entry['best_action']
                if best_action in actions:
                    best_move = state._apply_action(best_action)

            if self.time_limit_reached():
                break

        return best_move

    # ------------------------------------------------------------------
    # Utilitaires
    # ------------------------------------------------------------------

    def time_limit_reached(self):
        if self.start_time is None:
            return False
        return (time.time() - self.start_time) >= self.max_time

    def get_statistics(self):
        hit_rate = (self._tt_hits / self._tt_lookups * 100) if self._tt_lookups > 0 else 0
        return {
            'nodes_explored': self.nodes_explored,
            'cutoffs': self.cutoffs,
            'iterations': self.iterations,
            'transposition_table_size': len(self.transposition_table),
            'tt_hit_rate': hit_rate,
            'tt_hits': self._tt_hits,
            'tt_lookups': self._tt_lookups,
        }

    def clear_transposition_table(self):
        self.transposition_table.clear()

