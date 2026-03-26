.. docs/classes/minimax.rst

Minimax — Algorithme classique
================================

.. automodule:: PyAdverseSearch.classes.minimax
   :members:
   :undoc-members:
   :show-inheritance:

Description
-----------

:class:`Minimax` implémente l'algorithme Minimax classique tel que défini par
Russell & Norvig (2020). Il garantit un jeu optimal si la recherche est exhaustive,
au prix d'une complexité exponentielle.

Principe
--------

.. code-block:: text

    MAX veut maximiser -> choisit le coup avec la valeur MAX la plus haute
    MIN veut minimiser -> choisit le coup avec la valeur MIN la plus basse

    max_value(s, d):
        si terminal(s)  -> utility(s)
        si d == 0       -> heuristic(s)
        return max over children of min_value(child, d-1)

    min_value(s, d):
        si terminal(s)  -> utility(s)
        si d == 0       -> heuristic(s)
        return min over children of max_value(child, d-1)

Complexité
----------

- **Temporelle** : O(b\ :sup:`d`) avec b = facteur de branchement, d = profondeur
- **Spatiale** : O(b x d)

Quand l'utiliser
----------------

- Référence de base pour comparer les autres algorithmes
- Jeux avec faible facteur de branchement (morpion)
- Analyse pédagogique du processus de décision

Limitations
-----------

- Beaucoup plus lent qu'Alpha-Beta pour les mêmes résultats
- Pas de table de transposition intégrée
- Pour des performances optimales, préférer :class:`~PyAdverseSearch.classes.alphabeta.AlphaBeta`
  ou :class:`~PyAdverseSearch.classes.mtdf.MTDf`

Exemple::

    from PyAdverseSearch.classes.minimax import Minimax

    algo = Minimax(game=my_game, max_depth=5)
    best_state = algo.choose_best_move(current_state)

