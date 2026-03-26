.. PyAdverseSearch documentation master file
   docs/index.rst

PyAdverseSearch - Documentation
================================

**PyAdverseSearch** est une bibliothèque Python modulaire dédiée aux algorithmes
d'exploration adverse dans les jeux à deux joueurs à somme nulle.

Elle fournit une infrastructure complète : classes abstraites, algorithmes de recherche,
interfaces graphiques et outils de rapport, le tout conçu pour être facilement extensible.

.. toctree::
   :maxdepth: 2
   :caption: Architecture principale

   classes/index

.. toctree::
   :maxdepth: 2
   :caption: Interfaces graphiques

   interface/index

.. toctree::
   :maxdepth: 1
   :caption: A propos

   about

Démarrage rapide
----------------

Installation ::

    git clone https://github.com/PrKBouchard/PyAdverseSearch.git
    cd PyAdverseSearch
    pip install -e .

Exemple minimal::

    from PyAdverseSearch.classes.game import Game
    from PyAdverseSearch.classes.alphabeta import AlphaBeta

    game = Game(
        initial_state=my_state,
        possible_actions=my_possible_actions,
        is_terminal=my_is_terminal,
        winner_function=my_winner,
        utility=my_utility,
        heuristic=my_heuristic,
    )

    algo = AlphaBeta(game=game, max_depth=7)
    best_state = algo.choose_best_move(game.state)

Index et recherche
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

