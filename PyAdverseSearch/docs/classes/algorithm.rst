.. docs/classes/algorithm.rst

SearchAlgorithm — Classe de base abstraite
==========================================

.. automodule:: PyAdverseSearch.classes.algorithm
   :members:
   :undoc-members:
   :show-inheritance:

Description
-----------

:class:`SearchAlgorithm` est la classe abstraite dont héritent tous les
algorithmes de la bibliothèque. Elle impose l'implémentation de la méthode
:meth:`choose_best_move`.

Le module fournit également la fonction utilitaire :func:`choose_best_move`
qui permet de sélectionner dynamiquement un algorithme par son nom (chaîne
de caractères), utile pour les scripts de comparaison ou les interfaces.

Algorithmes disponibles via ``choose_best_move``
-------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 40

   * - Nom
     - Classe associée
   * - ``'minimax'``
     - :class:`~PyAdverseSearch.classes.minimax.Minimax`
   * - ``'alphabeta'``
     - :class:`~PyAdverseSearch.classes.alphabeta.AlphaBeta`
   * - ``'mtdf'``
     - :class:`~PyAdverseSearch.classes.mtdf.MTDf`
   * - ``'montecarlo'``
     - :class:`~PyAdverseSearch.classes.montecarlo.MonteCarlo`
   * - ``'pnsearch'``
     - :class:`~PyAdverseSearch.classes.pnsearch.PNSearch`
   * - ``'negamax'``
     - :class:`~PyAdverseSearch.classes.negamax.NegamaxSolver`

Exemple::

    from PyAdverseSearch.classes.algorithm import choose_best_move

    best_state = choose_best_move('alphabeta', game, state, max_depth=7)

