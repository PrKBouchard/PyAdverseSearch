# FILE: PyAdverseSearch/classes/algorithm.py

from abc import ABC, abstractmethod

class SearchAlgorithm(ABC):
    @abstractmethod
    def choose_best_move(self, state):
        """
        À partir d'un état donné, retourne le meilleur coup (ou action) à jouer,
        ou un état enfant (selon votre choix).
        """
        pass

# Dictionnaire d'algorithmes – initialement vide pour éviter l'import circulaire
ALGORITHMS = {}

def choose_best_move(algo_name, game, state, **kwargs):
    """
    Permet de sélectionner dynamiquement l'algorithme voulu (par son nom)
    et de retourner le meilleur coup/enfant à partir de l'état fourni.
    """
    # Import local pour éviter le cercle d'import
    if algo_name == 'minimax':
        from .minimax import Minimax
        AlgoClass = Minimax
    elif algo_name == 'alphabeta':
        from .alphabeta import AlphaBeta
        AlgoClass = AlphaBeta
    elif algo_name == 'mtdf':
        from .mtdf import MTDf
        AlgoClass = MTDf
    elif algo_name == 'montecarlo':
        from .montecarlo import MonteCarlo
        AlgoClass = MonteCarlo
    elif algo_name == 'pnsearch':
        from .pnsearch import PNSearch
        AlgoClass = PNSearch
    elif algo_name == 'negamax':
        from .negamax import NegamaxSolver
        AlgoClass = NegamaxSolver
    else:
        raise ValueError(f"Algorithme inconnu : {algo_name}")

    algo = AlgoClass(game=game, **kwargs)
    return algo.choose_best_move(state)
