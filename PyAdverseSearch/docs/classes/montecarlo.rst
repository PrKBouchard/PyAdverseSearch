.. docs/classes/montecarlo.rst

MonteCarlo — Monte Carlo Tree Search
======================================

.. automodule:: PyAdverseSearch.classes.montecarlo
   :members:
   :undoc-members:
   :show-inheritance:

Description
-----------

:class:`MonteCarlo` implémente Monte Carlo Tree Search (MCTS) avec la formule
d'exploration UCB1. L'algorithme ne nécessite pas de fonction heuristique
explicite : il évalue les positions par des simulations aléatoires.

Les quatre phases MCTS
-----------------------

.. code-block:: text

    1. SELECTION    : descendre dans l'arbre via UCB1 jusqu'à un noeud feuille
    2. EXPANSION    : ajouter un ou plusieurs enfants au noeud feuille
    3. SIMULATION   : rollout aléatoire jusqu'à un état terminal
    4. BACKPROP     : remonter le résultat vers la racine

Formule UCB1
-------------

.. math::

    UCB1(n) = \frac{w_n}{v_n} + C \sqrt{\frac{\ln V_n}{v_n}}

Avec :math:`w_n` = gains, :math:`v_n` = visites du noeud, :math:`V_n` = visites du parent,
:math:`C = \sqrt{2}` par défaut.

Pour le joueur MIN, le score est inversé (``-avg_score``) afin de
conserver la logique de maximisation UCB1.

Quand l'utiliser
----------------

- Grands espaces d'états où une fonction heuristique fiable est difficile à définir
- Jeux avec fort facteur de branchement
- Lorsqu'une limite de temps (plutôt que de profondeur) est préférable

Exemple::

    from PyAdverseSearch.classes.montecarlo import MonteCarlo

    algo = MonteCarlo(game=my_game, max_iterations=5000, max_time_seconds=2.0)
    best_state = algo.choose_best_move(current_state)

