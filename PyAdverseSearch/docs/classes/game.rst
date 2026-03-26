.. docs/classes/game.rst

Game — Configuration du jeu
============================

.. automodule:: PyAdverseSearch.classes.game
   :members:
   :undoc-members:
   :show-inheritance:

Description
-----------

La classe :class:`Game` est le **point d'entrée principal** pour les utilisateurs
de la bibliothèque. Elle centralise toutes les fonctions définies par l'utilisateur
et les expose via une interface unifiée consommée par les algorithmes.

Schéma de fonctionnement
------------------------

.. code-block:: text

    Utilisateur définit :
        - possible_actions(state) -> list
        - is_terminal(state)      -> bool
        - utility(state)          -> float
        - heuristic(state)        -> float
        - winner_function(state)  -> str

    Game(initial_state, possible_actions, is_terminal, ...)

    Algorithme.choose_best_move(state)
        |-> state._possible_actions()   -> game.game_possible_actions()
        |-> state._is_terminal()        -> game.game_is_terminal()
        |-> state._utility()            -> game.game_utility()
        `-> state._evaluate()           -> game.game_heuristic()

Exemple complet
---------------

::

    from PyAdverseSearch.classes.game import Game
    from PyAdverseSearch.classes.minimax import Minimax

    def possible_actions(state):
        return [c for c in range(7) if state.board[0][c] == ' ']

    def is_terminal(state):
        # ... logique de fin de partie ...
        return False

    def utility(state):
        return 0

    def heuristic(state):
        return 0

    def winner(state):
        return None

    game = Game(
        initial_state=my_state,
        possible_actions=possible_actions,
        is_terminal=is_terminal,
        winner_function=winner,
        utility=utility,
        heuristic=heuristic,
    )

    algo = Minimax(game=game, max_depth=5)
    best = algo.choose_best_move(game.state)

