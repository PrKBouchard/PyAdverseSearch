"""
Module state
============

Ce module définit la classe abstraite :class:`State`, base de toutes les représentations
d'état de jeu dans PyAdverseSearch.
"""

# FILE: state.py

from abc import ABC, abstractmethod

class State(ABC):
    """
    Classe abstraite représentant un état de jeu.

    Chaque jeu doit fournir sa propre sous-classe de :class:`State` en implémentant
    au minimum la méthode :meth:`_apply_action`. Les autres méthodes délèguent leurs
    appels à l'instance de :class:`Game` associée via l'attribut ``game``.

    :param board: Représentation du plateau de jeu (liste de listes, tableau NumPy, etc.).
    :param parent: État précédent dans l'arbre de recherche (``None`` pour l'état racine).
    :type parent: State or None
    :param game: Référence à l'instance :class:`Game` pour accéder aux fonctions de règles.
    :type game: Game or None

    .. note::
        L'attribut ``game`` doit être initialisé avant tout appel aux méthodes
        ``_possible_actions``, ``_is_terminal``, ``_utility`` ou ``_evaluate``.
    """

    def __init__(self, board, parent=None, game=None):
        self.board = board
        self.parent = parent
        self.value = None
        self.game = game

    def _possible_actions(self):
        """
        Retourne la liste des actions légales depuis cet état.

        Délègue l'appel à :meth:`Game.game_possible_actions`.

        :return: Liste des actions disponibles.
        :rtype: list
        """
        return self.game.game_possible_actions(self)

    def _is_terminal(self):
        """
        Vérifie si cet état est un état terminal (fin de partie).

        Délègue l'appel à :meth:`Game.game_is_terminal`.

        :return: ``True`` si la partie est terminée, ``False`` sinon.
        :rtype: bool
        """
        return self.game.game_is_terminal(self)

    def _utility(self):
        """
        Retourne la valeur d'utilité de cet état terminal.

        Délègue l'appel à :meth:`Game.game_utility`.

        :return: Valeur numérique du résultat final.
        :rtype: float
        """
        return self.game.game_utility(self)

    def _evaluate(self):
        """
        Retourne l'évaluation heuristique de cet état non-terminal.

        Délègue l'appel à :meth:`Game.game_heuristic`.

        :return: Score heuristique de la position.
        :rtype: float
        """
        return self.game.game_heuristic(self)

    def _generate_successors(self):
        """
        Génère et retourne tous les états successeurs possibles.

        Applique chaque action légale à l'état courant et retourne
        la liste des états résultants.

        :return: Liste des états successeurs.
        :rtype: list[State]
        """
        return [self._apply_action(action) for action in self._possible_actions()]

    def display(self):
        """
        Affiche le plateau de jeu dans la console.

        Implémentation par défaut pour les plateaux de type liste de listes.
        Peut être surchargée dans les sous-classes pour un affichage personnalisé.
        """
        for row in self.board:
            print('|'.join(row))
        print("\n")
