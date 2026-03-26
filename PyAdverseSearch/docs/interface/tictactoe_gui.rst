.. docs/interface/tictactoe_gui.rst

TicTacToeGUI — Interface Morpion
==================================

.. automodule:: PyAdverseSearch.Interface.tictactoe_gui
   :members:
   :undoc-members:
   :show-inheritance:

Description
-----------

Interface graphique Tkinter pour le jeu du Morpion (Tic-Tac-Toe) avec
un thème sombre moderne. Supporte trois algorithmes contre lesquels jouer.

Lancement
---------

::

    python -m PyAdverseSearch.Interface.tictactoe_gui

Fonctionnalités
---------------

- Thème sombre (fond ``#1e1e2e``, accents violets)
- Ecran de configuration avec boutons radio stylisés
- Plateau 3x3 interactif (cellules 130x130 px)
- Détection automatique de la victoire et du match nul
- Option de rejouer

Algorithmes disponibles
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 40

   * - Algorithme
     - Profondeur
     - Remarque
   * - Alpha-Beta
     - 9
     - Recommandé (rapide et optimal)
   * - Monte Carlo
     - 1200 itérations
     - Non déterministe
   * - Minimax
     - 9
     - Optimal mais plus lent

Palette de couleurs
-------------------

.. list-table::
   :header-rows: 1
   :widths: 30 30

   * - Élément
     - Couleur
   * - Fond principal
     - ``#1e1e2e``
   * - Cartes / panneaux
     - ``#2b2b3b``
   * - Accent
     - ``#7289da``
   * - Symbole X
     - ``#ff5555``
   * - Symbole O
     - ``#50fa7b``

