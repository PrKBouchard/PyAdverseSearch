# FILE: PyAdverseSearch/classes/autosolver.py

"""
Module autosolver
=================

AutoSolver - Selecteur automatique d'algorithmes pour les jeux adversariaux.

Deux modes disponibles :

- ``"classic"`` : utilise tous les algorithmes disponibles de facon intelligente
  selon la phase de jeu (debut / milieu / fin).
- ``"fast"`` : utilise uniquement les algorithmes les plus rapides
  (MTD(f) avec iterative deepening + PN-Search en fin de partie).

Chaque appel a ``choose_best_move`` enregistre des statistiques sur l'algorithme
utilise, la raison du choix et les performances mesurees.
"""

import time
from PyAdverseSearch.classes.algorithm import SearchAlgorithm
from PyAdverseSearch.classes.minimax import Minimax
from PyAdverseSearch.classes.alphabeta import AlphaBeta
from PyAdverseSearch.classes.mtdf import MTDf
from PyAdverseSearch.classes.montecarlo import MonteCarlo
from PyAdverseSearch.classes.negamax import NegamaxSolver
from PyAdverseSearch.classes.pnsearch import PNSearch
from PyAdverseSearch.classes.node import Node


class AlgoRecord:
    """Enregistrement des statistiques d'un coup joue par AutoSolver."""

    def __init__(self, move_number, algo_name, reason, elapsed, stats):
        self.move_number = move_number   # Numero du coup (1-base)
        self.algo_name = algo_name       # Nom lisible de l'algorithme
        self.reason = reason             # Explication du choix
        self.elapsed = elapsed           # Temps de calcul en secondes
        self.stats = stats               # Dict de statistiques brutes

    def __repr__(self):
        return (f"Coup {self.move_number}: {self.algo_name} "
                f"({self.elapsed:.3f}s) - {self.reason}")


class AutoSolver(SearchAlgorithm):
    """
    Selecteur automatique d'algorithmes.

    Parametres
    ----------
    game : instance du jeu (doit exposer game_is_terminal / game_utility)
    depth : profondeur de recherche souhaitee
    mode  : "classic" (tous les algos) ou "fast" (MTDf + PNSearch uniquement)
    rows  : nombre de lignes du plateau (pour calculer le remplissage)
    cols  : nombre de colonnes du plateau
    """

    # Timeouts pour le mode classic (secondes)
    TIMEOUT_MAP = {3: 0.5, 5: 1.0, 7: 2.0, 9: 3.0}
    # Timeouts pour le mode fast : encore plus courts
    TIMEOUT_MAP_FAST = {3: 0.3, 5: 0.8, 7: 1.2, 9: 2.0}

    def __init__(self, game, depth=5, mode="classic", rows=6, cols=7):
        if mode not in ("classic", "fast"):
            raise ValueError("mode doit etre 'classic' ou 'fast'")
        self.game = game
        self.depth = depth
        self.mode = mode
        self.rows = rows
        self.cols = cols

        # Historique des enregistrements (un par coup joue)
        self.records: list[AlgoRecord] = []
        self._moves_played = 0

    # ------------------------------------------------------------------
    # Interface publique
    # ------------------------------------------------------------------

    def choose_best_move(self, state):
        """
        Selectionne dynamiquement le meilleur algorithme pour cet etat,
        appelle choose_best_move sur cet algorithme et enregistre les stats.

        Retourne l'etat fils correspondant au meilleur coup.
        """
        self._moves_played += 1

        if self.mode == "fast":
            algo, algo_name, reason = self._pick_fast(state)
        else:
            algo, algo_name, reason = self._pick_classic(state)

        start = time.time()
        best_state = self._invoke(algo, state)
        elapsed = time.time() - start

        raw_stats = self._collect_stats(algo, elapsed)

        record = AlgoRecord(
            move_number=self._moves_played,
            algo_name=algo_name,
            reason=reason,
            elapsed=elapsed,
            stats=raw_stats,
        )
        self.records.append(record)

        return best_state

    def get_records(self) -> list:
        """Retourne la liste des AlgoRecord enregistres."""
        return list(self.records)

    def current_algo_name(self) -> str:
        """Nom du dernier algorithme utilise (ou '' si aucun)."""
        if self.records:
            return self.records[-1].algo_name
        return ""

    def current_reason(self) -> str:
        """Raison du dernier choix (ou '' si aucun)."""
        if self.records:
            return self.records[-1].reason
        return ""

    # ------------------------------------------------------------------
    # Logique de selection - mode FAST
    # ------------------------------------------------------------------

    def _pick_fast(self, state):
        """
        Mode RAPIDE : MTD(f) par defaut, PN-Search si fin de partie proche.
        """
        empty = self._count_empty(state)
        timeout = self.TIMEOUT_MAP_FAST.get(self.depth, 1.0)
        # En fast on limite aussi la profondeur a max 5 pour rester rapide
        fast_depth = min(self.depth, 5)

        if empty <= 10:
            algo = PNSearch(game=self.game, max_nodes=30000,
                            use_transposition_table=True)
            name = "PN-Search"
            reason = (f"Fin de partie ({empty} cases vides) - "
                      "PN-Search prouve la victoire directement")
        else:
            algo = MTDf(game=self.game, max_depth=fast_depth,
                        max_time_seconds=timeout, initial_guess=0)
            name = "MTD(f)"
            reason = (f"MTD(f) + Iterative Deepening + Zobrist "
                      f"(profondeur {fast_depth}, timeout {timeout}s)")

        return algo, name, reason

    # ------------------------------------------------------------------
    # Logique de selection - mode CLASSIC
    # ------------------------------------------------------------------

    def _pick_classic(self, state):
        """
        Mode CLASSIC : utilise tous les algorithmes de maniere intelligente
        selon la phase de jeu.

        Repartition par numero de coup :
          0       -> Minimax (reference, profondeur limitee)
          1-3     -> Alpha-Beta + TT (debut, elagage efficace)
          4-5     -> MTD(f) (fenetre nulle, rapide)
          6-8     -> Negamax (variante simplifiee)
          9-12    -> Alpha-Beta + TT (milieu de partie fiable)
          13-15   -> Monte Carlo si arbre large, sinon Alpha-Beta
          > 15    -> PN-Search si <= 8 cases, Alpha-Beta sinon
        """
        moves = self._moves_played - 1  # avant incrementation, c'est le coup numero moves_played
        empty = self._count_empty(state)
        total = self.rows * self.cols
        filled_ratio = (total - empty) / total
        possible = len(state._possible_actions())
        timeout = self.TIMEOUT_MAP.get(self.depth, 5.0)

        if moves == 0:
            algo = Minimax(game=self.game, max_depth=min(self.depth, 4))
            name = "Minimax"
            reason = ("Premier coup - Minimax comme reference "
                      "(algorithme de base, profondeur limitee a 4)")

        elif moves <= 3:
            algo = AlphaBeta(game=self.game, max_depth=self.depth,
                             use_transposition_table=True)
            name = "Alpha-Beta+TT"
            reason = (f"Debut de partie (coup {moves + 1}) - "
                      "Alpha-Beta avec table de transposition")

        elif moves <= 5:
            algo = MTDf(game=self.game, max_depth=self.depth,
                        max_time_seconds=timeout, initial_guess=0)
            name = "MTD(f)"
            reason = (f"Coup {moves + 1} - MTD(f) fenetre nulle "
                      f"(profondeur {self.depth}, timeout {timeout}s)")

        elif moves <= 8:
            algo = NegamaxSolver(depth_limit=self.depth)
            name = "Negamax"
            reason = (f"Coup {moves + 1} - Negamax (meme logique MAX/MIN, "
                      "implementation simplifiee)")

        elif moves <= 12:
            algo = AlphaBeta(game=self.game, max_depth=self.depth,
                             use_transposition_table=True)
            name = "Alpha-Beta+TT"
            reason = (f"Milieu de partie (coup {moves + 1}) - "
                      "Alpha-Beta, standard fiable")

        elif moves <= 15:
            if possible >= 6:
                iterations = 1000 * self.depth
                algo = MonteCarlo(game=self.game, max_iterations=iterations)
                name = "Monte Carlo"
                reason = (f"Coup {moves + 1}, arbre large ({possible} colonnes) - "
                          f"Monte Carlo ({iterations} simulations)")
            else:
                algo = AlphaBeta(game=self.game, max_depth=self.depth,
                                 use_transposition_table=True)
                name = "Alpha-Beta+TT"
                reason = (f"Coup {moves + 1}, arbre etroit ({possible} colonnes) - "
                          "Alpha-Beta prefere a Monte Carlo")

        elif empty <= 8:
            algo = PNSearch(game=self.game, max_nodes=50000,
                            use_transposition_table=True)
            name = "PN-Search"
            reason = (f"Fin de partie ({empty} cases vides) - "
                      "PN-Search prouve mathematiquement victoire/defaite")

        elif filled_ratio > 0.7 or empty < 12:
            algo = AlphaBeta(game=self.game, max_depth=self.depth,
                             use_transposition_table=True)
            name = "Alpha-Beta+TT"
            reason = (f"Fin proche ({empty} cases vides, "
                      f"{filled_ratio * 100:.0f}% rempli) - Alpha-Beta + cache")

        else:
            algo = AlphaBeta(game=self.game, max_depth=self.depth,
                             use_transposition_table=True)
            name = "Alpha-Beta+TT"
            reason = "Cas par defaut - Alpha-Beta le plus fiable"

        return algo, name, reason

    # ------------------------------------------------------------------
    # Invocation generique d'un algorithme
    # ------------------------------------------------------------------

    def _invoke(self, algo, state):
        """Appelle l'algorithme avec sa propre interface."""
        if isinstance(algo, NegamaxSolver):
            root_node = Node(state)
            best_board = algo.get_best_move(root_node)
            for col in state._possible_actions():
                test_state = state._apply_action(col)
                if test_state.board == best_board:
                    return test_state
            return None
        else:
            return algo.choose_best_move(state)

    # ------------------------------------------------------------------
    # Collecte de statistiques selon le type d'algorithme
    # ------------------------------------------------------------------

    def _collect_stats(self, algo, elapsed) -> dict:
        stats = {"elapsed": elapsed}
        if isinstance(algo, (AlphaBeta, MTDf)):
            raw = algo.get_statistics()
            stats["nodes_explored"] = raw.get("nodes_explored", 0)
            stats["cutoffs"] = raw.get("cutoffs", 0)
            tt_hit = raw.get("tt_hit_rate", None)
            if tt_hit is not None:
                stats["tt_hit_rate"] = tt_hit
        elif isinstance(algo, PNSearch):
            raw = algo.get_statistics()
            stats["nodes_explored"] = raw.get("nodes_explored", 0)
            stats["tt_size"] = raw.get("transposition_table_size", 0)
        elif isinstance(algo, MonteCarlo):
            stats["iterations"] = getattr(algo, "max_iterations", 0)
        elif isinstance(algo, NegamaxSolver):
            stats["nodes_explored"] = getattr(algo, "nodes_visited", 0)
            stats["cutoffs"] = getattr(algo, "cutoffs", 0)
        elif isinstance(algo, Minimax):
            stats["nodes_explored"] = getattr(algo, "nodes_explored", 0)
        return stats

    # ------------------------------------------------------------------
    # Utilitaires
    # ------------------------------------------------------------------

    def _count_empty(self, state) -> int:
        return sum(row.count(' ') for row in state.board)

