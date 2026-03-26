.. docs/classes/pnsearch.rst

PNSearch — Proof-Number Search
================================

.. automodule:: PyAdverseSearch.classes.pnsearch
   :members:
   :undoc-members:
   :private-members:
   :show-inheritance:

Description
-----------

:class:`PNSearch` implémente l'algorithme **Proof-Number Search (PN-Search)**,
conçu pour prouver ou réfuter mathématiquement une position de jeu.
Contrairement aux algorithmes heuristiques, PN-Search garantit une réponse
exacte (PROVEN / DISPROVEN) dans la limite de noeuds allouée.

Référence :
    Allis, L. V. (1994). *Searching for Solutions in Games and Artificial Intelligence.*

Principe
--------

Chaque noeud maintient deux nombres :

.. list-table::
   :header-rows: 1
   :widths: 15 55

   * - Nombre
     - Signification
   * - ``phi``
     - Nombre de preuves (difficulté de prouver que le noeud est gagnant)
   * - ``delta``
     - Nombre de réfutations (difficulté de prouver que le noeud est perdant)

Pour un noeud OR (joueur MAX) : ``phi = min(enfants.phi)``, ``delta = sum(enfants.delta)``

Pour un noeud AND (joueur MIN) : ``phi = sum(enfants.phi)``, ``delta = min(enfants.delta)``

La recherche sélectionne toujours le **Most Proving Node (MPN)** : le noeud
dont l'exploration réduira le plus le nombre de preuve de la racine.

Classes internes
-----------------

.. autoclass:: PyAdverseSearch.classes.pnsearch.ProofStatus
   :members:
   :no-index:

.. autoclass:: PyAdverseSearch.classes.pnsearch.PNNode
   :members:
   :no-index:

Statuts de preuve
------------------

.. list-table::
   :header-rows: 1
   :widths: 20 50

   * - Statut
     - Signification
   * - ``UNKNOWN``
     - Position non encore résolue
   * - ``PROVEN``
     - Position prouvée gagnante pour le joueur à jouer
   * - ``DISPROVEN``
     - Position prouvée perdante pour le joueur à jouer

Quand l'utiliser
----------------

- En fin de partie (peu de cases vides) pour des résolutions exactes
- Combiné avec d'autres algorithmes dans :class:`~PyAdverseSearch.classes.autosolver.AutoSolver`
- Pour des problèmes de jeu à résoudre (ex. puzzles d'échecs)

Exemple::

    from PyAdverseSearch.classes.pnsearch import PNSearch

    algo = PNSearch(game=my_game, max_nodes=100000, use_transposition_table=True)
    best_state = algo.choose_best_move(current_state)

    stats = algo.get_statistics()
    print(f"Noeuds explorés : {stats['nodes_explored']}")


