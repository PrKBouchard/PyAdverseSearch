"""
Module minimax
==============

Ce module implémente l'algorithme Minimax classique avec limite de profondeur
et limite de temps optionnelle.
"""

# FILE: PyAdverseSearch/classes/minimax.py

import time
from PyAdverseSearch.classes.algorithm import SearchAlgorithm
from PyAdverseSearch.classes.node import Node

class Minimax(SearchAlgorithm):
    """
    Implémentation de l'algorithme Minimax classique.

    Minimax explore récursivement l'arbre de jeu en alternant entre
    la maximisation du gain (joueur MAX) et la minimisation (joueur MIN).
    Il garantit le choix optimal si la recherche est exhaustive.

    :param game: Instance du jeu configuré.
    :type game: Game or None
    :param max_depth: Profondeur maximale de recherche (couper l'exploration à cette profondeur).
    :type max_depth: int
    :param max_time_seconds: Limite de temps en secondes (``None`` = pas de limite).
    :type max_time_seconds: float or None

    Complexité temporelle : O(b^d) avec b le facteur de branchement et d la profondeur.

    Exemple::

        algo = Minimax(game=my_game, max_depth=5)
        best_state = algo.choose_best_move(current_state)
    """

    def __init__(self, game=None, max_depth=9, max_time_seconds=None):
        #verifying parameters
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
        Sélectionne le meilleur coup pour le joueur courant (MAX ou MIN).

        Les états terminaux recoivent un bonus de priorité (utilité x 1000)
        pour favoriser les victoires immédiates. Pour les états non-terminaux,
        appelle récursivement :meth:`min_value` ou :meth:`max_value`.

        :param state: État courant du jeu.
        :type state: State
        :return: L'état enfant correspondant au meilleur coup.
        :rtype: State or None
        """
        is_max = (state.player == "MAX")


        best_score = -float('inf') if is_max else float('inf')
        best_state = None

        for action in state._possible_actions():
            child = state._apply_action(action)

            # final state → strong score
            if self.game.game_is_terminal(child):
                util = self.game.game_utility(child)
                score = util * 1000
            else:
                # non-terminal → we call MAX or MIN accordingly
                if is_max:
                    score = self.min_value(child, self.max_depth - 1)
                else:
                    score = self.max_value(child, self.max_depth - 1)

            # choosing best child
            if (is_max and score > best_score) or (not is_max and score < best_score):
                best_score = score
                best_state = child

        return best_state

    def max_value(self, state, depth):
        """
        Retourne la valeur maximale (utilité ou heuristique) pour le joueur MAX.

        :param state: État courant.
        :type state: State
        :param depth: Profondeur restante.
        :type depth: int
        :return: Valeur maximale trouvée.
        :rtype: float
        """
        # final state
        if self.game.game_is_terminal(state):
            return self.game.game_utility(state)
        # Depth cutoff: return heuristic
        if depth == 0:
            return self.game.game_heuristic(state)

        v = -float('inf')
        for action in state._possible_actions():
            child = state._apply_action(action)
            v = max(v, self.min_value(child, depth - 1))
        return v

    def min_value(self, state, depth):
        """
        Retourne la valeur minimale (utilité ou heuristique) pour le joueur MIN.

        :param state: État courant.
        :type state: State
        :param depth: Profondeur restante.
        :type depth: int
        :return: Valeur minimale trouvée.
        :rtype: float
        """
        # Terminal state
        if self.game.game_is_terminal(state):
            return self.game.game_utility(state)
        # Depth cutoff: return heuristic
        if depth == 0:
            return self.game.game_heuristic(state)

        v = float('inf')
        for action in state._possible_actions():
            child = state._apply_action(action)
            v = min(v, self.max_value(child, depth - 1))
        return v


    def time_limit_reached(self):
        """
        Vérifie si la limite de temps de calcul est atteinte.

        :return: ``True`` si le temps alloué est dépassé, ``False`` sinon.
        :rtype: bool
        """
        if self.max_time is None:
            return False
        return (time.time() - self.start_time) >= self.max_time

    # If the node is terminal, it directly returns its utility value.
    # Otherwise, it recursively calculates utilities of all children.
    def default_utility(self, node):
        """
        Calcule récursivement la valeur d'utilité d'un noeud à partir de ses enfants.

        Si le noeud est terminal, retourne directement son utilité.
        Sinon, applique MAX ou MIN selon le joueur actif.

        :param node: Noeud à évaluer.
        :type node: Node
        :return: Valeur d'utilité calculée.
        :rtype: float
        """
        if node.is_terminal():
            return node.state._utility()

        # If there's no children, return the heuristic evaluation of the node.
        if not node.children:
            return node.valuation

        if node.state.player == "MAX":
            return max(self.default_utility(child) for child in node.children)
        else:  # MIN
            return min(self.default_utility(child) for child in node.children)


    def next_move(self, node):
        """
        Retourne le noeud enfant correspondant au meilleur coup depuis un noeud donné.

        Évalue chaque enfant avec :meth:`default_utility` et sélectionne
        le meilleur selon la perspective du joueur actif.

        :param node: Noeud courant (avec enfants développés).
        :type node: Node
        :return: Noeud enfant optimal, ou ``None`` si aucun enfant.
        :rtype: Node or None
        """
        if not node.children:
            return None

        # evaluates each children
        child_utils = [(child, self.default_utility(child)) for child in node.children]
        if node.state.player == "MAX":
            best_child = max(child_utils, key=lambda x: x[1])[0]
        else:
            best_child = min(child_utils, key=lambda x: x[1])[0]
        return best_child
