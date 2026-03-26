.. docs/classes/index.rst

Classes principales
===================

Ce chapitre documente toutes les classes du coeur de la bibliothèque
situées dans ``PyAdverseSearch/classes/``.

Architecture d'ensemble
-----------------------

.. code-block:: text

    SearchAlgorithm (ABC)
    ├── Minimax
    ├── AlphaBeta
    ├── MTDf
    ├── MonteCarlo
    ├── NegamaxSolver
    ├── PNSearch
    └── AutoSolver

    State (ABC)          -- à sous-classer pour chaque jeu
    Game                 -- point d'entrée utilisateur
    Node                 -- noeud de l'arbre de jeu
    GameTree             -- arbre complet construit à l'init

.. toctree::
   :maxdepth: 2
   :caption: Classes

   algorithm
   game
   state
   node
   tree
   minimax
   alphabeta
   negamax
   montecarlo
   mtdf
   pnsearch
   autosolver

