.. docs/classes/state.rst

State — Représentation d'un état de jeu
========================================

.. automodule:: PyAdverseSearch.classes.state
   :members:
   :undoc-members:
   :private-members:
   :show-inheritance:

Description
-----------

:class:`State` est la **classe abstraite** dont doit hériter toute représentation
d'état de jeu. Elle définit l'interface utilisée par les algorithmes de recherche
et l'arbre de jeu.

Méthodes à implémenter dans les sous-classes
---------------------------------------------

Seule ``_apply_action`` doit obligatoirement être surchargée, car les autres
méthodes délèguent automatiquement à l'instance :class:`Game` :

.. list-table::
   :header-rows: 1
   :widths: 30 50

   * - Méthode
     - Rôle
   * - ``_apply_action(action)``
     - **Obligatoire.** Retourne le nouvel état après application de l'action.
   * - ``_possible_actions()``
     - Délègue à ``game.game_possible_actions()``.
   * - ``_is_terminal()``
     - Délègue à ``game.game_is_terminal()``.
   * - ``_utility()``
     - Délègue à ``game.game_utility()``.
   * - ``_evaluate()``
     - Délègue à ``game.game_heuristic()``.
   * - ``display()``
     - Affiche le plateau (peut être surchargée).

Exemple d'implémentation
-------------------------

::

    from PyAdverseSearch.classes.state import State

    class MyGameState(State):
        def __init__(self, board, player='MAX', parent=None, game=None):
            super().__init__(board, parent, game)
            self.player = player

        def _apply_action(self, action):
            new_board = [row[:] for row in self.board]
            # ... appliquer l'action ...
            next_player = 'MIN' if self.player == 'MAX' else 'MAX'
            return MyGameState(new_board, next_player, parent=self, game=self.game)

        def display(self):
            for row in self.board:
                print('|'.join(str(c) for c in row))

.. note::
    L'attribut ``game`` est défini automatiquement par :class:`Game`
    lors de l'initialisation si ``initial_state`` est fourni.

