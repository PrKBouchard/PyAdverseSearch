.. docs/classes/mtdf.rst

MTDf — Memory-enhanced Test Driver
=====================================

.. automodule:: PyAdverseSearch.classes.mtdf
   :members:
   :undoc-members:
   :private-members:
   :show-inheritance:

Description
-----------

:class:`MTDf` implémente l'algorithme MTD(f) (*Memory-enhanced Test Driver with
value f*), décrit par Aske Plaat et al. (1996). C'est une des implémentations
les plus efficaces pour les jeux à deux joueurs avec une bonne fonction
heuristique.

Principe de MTD(f)
-------------------

MTD(f) effectue plusieurs recherches Alpha-Beta à **fenêtre nulle** (``[f-1, f]``)
en raffinant progressivement la valeur ``f`` jusqu'à converger vers la valeur exacte.
Cette approche nécessite une table de transposition (TT) persistante entre les appels.

.. code-block:: text

    MTDf(root, f):
        g = f
        upper = +inf
        lower = -inf
        repeat:
            beta = g si g == lower else g+1
            g = AlphaBeta(root, beta-1, beta)  # fenêtre nulle
            if g < beta:
                upper = g
            else:
                lower = g
        until lower >= upper
        return g

Fonctionnalités intégrées
--------------------------

**Iterative Deepening (ID)**
    Exploration progressive de profondeur 1 à ``max_depth``.
    Le résultat de la profondeur ``d-1`` sert de ``first_guess`` pour la profondeur ``d``.

**Table de transposition avec bornes lb/ub**
    Stocke les bornes exactes (inférieure et supérieure) pour chaque état,
    permettant des coupures plus agressives.

**Hachage Zobrist**
    Hachage incrémental efficace pour les plateaux de type liste de listes.
    Initialisé automatiquement à la première utilisation.

**Killer moves**
    Mémorise les actions qui ont produit des coupures beta à chaque profondeur
    pour les explorer en priorité lors des itérations suivantes.

**Tri des coups (move ordering)**
    Combine : TT best action > killer moves > center-bias (Puissance 4) > heuristique.

Statistiques disponibles
-------------------------

::

    stats = algo.get_statistics()
    # {
    #     'nodes_explored': int,
    #     'cutoffs': int,
    #     'iterations': int,     # profondeurs d'iterative deepening effectuées
    #     'tt_hits': int,
    #     'tt_lookups': int,
    #     'tt_hit_rate': float,
    #     'transposition_table_size': int
    # }

Référence
---------

Plaat, A., Schaeffer, J., Pijls, W., & de Bruin, A. (1996).
*MTD(f), a new chess algorithm.*
ICCA Journal, 19(4), 233–243.

Exemple::

    from PyAdverseSearch.classes.mtdf import MTDf

    algo = MTDf(game=my_game, max_depth=7, max_time_seconds=2.0)
    best_state = algo.choose_best_move(current_state)

    stats = algo.get_statistics()
    print(f"Profondeurs explorées : {stats['iterations']}")
    print(f"Taux de hit TT : {stats['tt_hit_rate']:.1%}")

