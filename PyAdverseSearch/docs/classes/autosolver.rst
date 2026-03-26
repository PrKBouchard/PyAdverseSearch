.. docs/classes/autosolver.rst

AutoSolver — Sélecteur automatique d'algorithmes
==================================================

.. automodule:: PyAdverseSearch.classes.autosolver
   :members:
   :undoc-members:
   :private-members:
   :show-inheritance:

Description
-----------

:class:`AutoSolver` est un méta-algorithme qui sélectionne dynamiquement le
meilleur algorithme de recherche selon la phase de jeu. Il expose la même
interface que les autres algorithmes (méthode :meth:`choose_best_move`) et
enregistre des statistiques pour chaque coup joué.

Modes disponibles
-----------------

``"fast"`` (recommandé)
    Utilise uniquement MTD(f) et PN-Search. Optimal en termes de vitesse.

    - Par défaut : MTD(f) avec Iterative Deepening + Zobrist
    - En fin de partie (<= 10 cases vides) : PN-Search (résolution exacte)

``"classic"``
    Utilise tous les algorithmes disponibles de manière séquentielle
    selon le numéro de coup :

    .. list-table::
       :header-rows: 1
       :widths: 20 30 40

       * - Coup(s)
         - Algorithme
         - Raison
       * - 0
         - Minimax
         - Référence de base
       * - 1-3
         - Alpha-Beta + TT
         - Debut de partie, élagage efficace
       * - 4-5
         - MTD(f)
         - Fenêtre nulle, rapide
       * - 6-8
         - Negamax
         - Variante simplifiée
       * - 9-12
         - Alpha-Beta + TT
         - Milieu de partie fiable
       * - 13-15
         - Monte Carlo ou Alpha-Beta
         - Selon le facteur de branchement
       * - > 15
         - PN-Search ou Alpha-Beta
         - Selon le nombre de cases vides

Classe AlgoRecord
-----------------

.. autoclass:: PyAdverseSearch.classes.autosolver.AlgoRecord
   :members:
   :no-index:

Chaque coup joué génère un :class:`AlgoRecord` accessible via :meth:`get_records` ::

    records = solver.get_records()
    for r in records:
        print(r)
    # Coup 1: Alpha-Beta+TT (0.042s) - Debut de partie (coup 2) - ...

Exemple complet
---------------

::

    from PyAdverseSearch.classes.autosolver import AutoSolver

    # Mode rapide recommandé pour Puissance 4
    solver = AutoSolver(game=my_game, depth=7, mode="fast", rows=6, cols=7)
    best_state = solver.choose_best_move(current_state)

    print(solver.current_algo_name())   # ex. "MTD(f)"
    print(solver.current_reason())      # ex. "MTD(f) + Iterative Deepening..."

    # Après la partie
    for record in solver.get_records():
        print(record)


