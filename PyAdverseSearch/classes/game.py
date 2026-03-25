"""
Module game
===========

Ce module contient la classe :class:`Game`, point d'entrée principal de la bibliothèque.
Elle centralise les règles, les fonctions d'évaluation et l'état initial d'un jeu.
"""

# FILE: game.py
from PyAdverseSearch.classes.tree import GameTree


class Game:
    """
    Classe principale représentant un jeu à deux joueurs.

    La classe :class:`Game` est utilisée par les développeurs pour configurer
    un jeu adverse. Elle regroupe toutes les fonctions définies par l'utilisateur
    (règles, état terminal, utilité, heuristique) et les expose via une interface
    unifiée utilisée par les algorithmes de recherche.

    :param initial_state: État initial du jeu (instance d'une sous-classe de :class:`State`).
    :type initial_state: State or None
    :param possible_actions: Fonction retournant la liste des actions légales depuis un état.
    :type possible_actions: callable or None
    :param is_terminal: Fonction vérifiant si un état est terminal (fin de partie).
    :type is_terminal: callable or None
    :param winner_function: Fonction déterminant le gagnant dans un état terminal.
    :type winner_function: callable or None
    :param utility: Fonction d'utilité évaluant un état terminal (ex. +1, -1, 0).
    :type utility: callable or None
    :param heuristic: Fonction heuristique évaluant un état non-terminal.
    :type heuristic: callable or None
    :param isMaxStarting: Indique si le joueur MAX commence la partie.
    :type isMaxStarting: bool

    Exemple d'utilisation::

        game = Game(
            initial_state=my_state,
            possible_actions=my_possible_actions,
            is_terminal=my_is_terminal,
            winner_function=my_winner,
            utility=my_utility,
            heuristic=my_heuristic,
            isMaxStarting=True
        )
    """

    def __init__(self, initial_state=None, possible_actions=None, is_terminal=None,
                 winner_function=None, utility=None, heuristic=None, isMaxStarting=True):
        self.state = initial_state
        self.possible_actions = possible_actions
        self.is_terminal = is_terminal
        self.winner_function = winner_function
        self.utility = utility
        self.heuristic = heuristic
        self.isMaxStarting = isMaxStarting
        if self.state is not None:
            self.state.game = self

    def game_possible_actions(self, state):
        """
        Retourne la liste des actions légales depuis l'état donné.

        Délègue l'appel à la fonction ``possible_actions`` fournie à l'initialisation.

        :param state: État courant du jeu.
        :type state: State
        :return: Liste des actions disponibles.
        :rtype: list
        """
        return self.possible_actions(state)

    def game_is_terminal(self, state):
        """
        Vérifie si l'état donné est un état terminal (fin de partie).

        Délègue l'appel à la fonction ``is_terminal`` fournie à l'initialisation.

        :param state: État courant du jeu.
        :type state: State
        :return: ``True`` si la partie est terminée, ``False`` sinon.
        :rtype: bool
        """
        return self.is_terminal(state)

    def game_utility(self, state):
        """
        Retourne la valeur d'utilité d'un état terminal.

        Ne doit être appelée que si l'état est terminal (voir :meth:`game_is_terminal`).
        Convention : valeur positive si MAX gagne, négative si MIN gagne, 0 pour match nul.

        :param state: État terminal du jeu.
        :type state: State
        :return: Valeur numérique représentant le résultat final.
        :rtype: float
        """
        return self.utility(state)

    def game_heuristic(self, state):
        """
        Retourne l'évaluation heuristique d'un état non-terminal.

        Utilisée par les algorithmes pour évaluer des états intermédiaires
        à la profondeur maximale de recherche.

        :param state: État non-terminal du jeu.
        :type state: State
        :return: Score heuristique de la position.
        :rtype: float
        """
        return self.heuristic(state)

    def get_winner(self):
        """
        Retourne le gagnant de la partie si elle est terminée, sinon ``None``.

        :return: Nom du gagnant (``"MAX"``, ``"MIN"`` ou ``None``).
        :rtype: str or None
        """
        return self.winner_function(self.state)
