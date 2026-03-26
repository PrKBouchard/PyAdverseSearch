.. docs/classes/negamax.rst

NegamaxSolver — Negamax avec quiescence
=========================================

.. automodule:: PyAdverseSearch.classes.negamax
   :members:
   :undoc-members:
   :private-members:
   :show-inheritance:

Description
-----------

:class:`NegamaxSolver` implémente l'algorithme Negamax, une variante de Minimax
qui exploite la symétrie du score entre les deux joueurs :

.. math::

    \text{max}(a, b) = -\text{min}(-a, -b)

Ainsi, les deux joueurs utilisent la même logique de maximisation, le signe
du score étant inversé à chaque niveau.

Fonctionnalités avancées
-------------------------

**Table de transposition**
    Évite de recalculer des positions déjà visitées. Utilise le hash de l'état
    (``hash(state)`` si disponible, sinon hash du plateau).

**Tri des coups (move ordering)**
    Avant d'explorer les enfants, les coups sont triés par score heuristique
    décroissant pour maximiser l'efficacité de l'élagage alpha-beta.

**Recherche de quiescence**
    Lorsque la profondeur maximale est atteinte, la recherche continue sur les
    coups tactiques (captures) pour éviter l'effet d'horizon. Utilise :

    - *Stand-pat evaluation* : si le score de base est déjà supérieur à beta, on coupe.
    - *Delta pruning* : si même le meilleur gain possible ne dépasse pas alpha, on coupe.

Statistiques disponibles
-------------------------

Après ``get_best_move`` ou ``_negamax``, les attributs suivants sont disponibles ::

    solver.nodes_visited  # int : noeuds explorés
    solver.cutoffs        # int : nombre de coupures alpha-beta

Exemple::

    from PyAdverseSearch.classes.negamax import NegamaxSolver
    from PyAdverseSearch.classes.node import Node

    solver = NegamaxSolver(depth_limit=6)
    root = Node(state=current_state)
    best_board = solver.get_best_move(root)

.. note::
    :meth:`get_best_move` retourne le **plateau** (``board``) du meilleur état,
    pas l'état lui-même. Pour obtenir l'état, chercher dans les enfants celui
    dont le plateau correspond.

