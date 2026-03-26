.. docs/classes/alphabeta.rst

AlphaBeta — Minimax avec élagage
==================================

.. automodule:: PyAdverseSearch.classes.alphabeta
   :members:
   :undoc-members:
   :show-inheritance:

Description
-----------

:class:`AlphaBeta` est une amélioration de Minimax qui élague les branches
de l'arbre qui ne peuvent pas influencer la décision finale. Il garantit
le même résultat que Minimax tout en explorant significativement moins de noeuds.

Principe de l'élagage
----------------------

.. code-block:: text

    alpha = meilleure valeur garantie pour MAX (borne inférieure)
    beta  = meilleure valeur garantie pour MIN (borne supérieure)

    Si alpha >= beta -> coupure (beta cutoff pour MAX, alpha cutoff pour MIN)

    Cas ideal (coups triés) : O(b^(d/2)) — deux fois plus profond que Minimax

Table de transposition
-----------------------

Activable via ``use_transposition_table=True``. Mémorise les états déjà explorés
pour éviter de les recalculer. Particulièrement utile pour les jeux avec
des transpositions fréquentes (ex. Puissance 4).

Statistiques disponibles
-------------------------

Après :meth:`choose_best_move`, la méthode :meth:`get_statistics` retourne ::

    {
        'nodes_explored': int,       # Noeuds visités
        'cutoffs': int,              # Nombre de coupures alpha/beta
        'transposition_table_size': int  # Taille de la TT (si activée)
    }

Complexité
----------

- **Meilleur cas** : O(b\ :sup:`d/2`) (coups triés parfaitement)
- **Pire cas** : O(b\ :sup:`d`) (équivalent à Minimax)
- **Cas moyen** : O(b\ :sup:`3d/4`)

Exemple::

    from PyAdverseSearch.classes.alphabeta import AlphaBeta

    algo = AlphaBeta(game=my_game, max_depth=7, use_transposition_table=True)
    best_state = algo.choose_best_move(current_state)

    stats = algo.get_statistics()
    print(f"Noeuds explorés : {stats['nodes_explored']}")
    print(f"Coupures : {stats['cutoffs']}")

