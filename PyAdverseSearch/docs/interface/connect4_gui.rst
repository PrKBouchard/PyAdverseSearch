.. docs/interface/connect4_gui.rst

Connect4GUI — Interface Puissance 4 (version de base)
=======================================================

.. automodule:: PyAdverseSearch.Interface.connect4_gui
   :members:
   :undoc-members:
   :show-inheritance:

Description
-----------

Interface graphique Tkinter pour jouer au Puissance 4 contre une IA.
Cette version de base propose trois algorithmes (Minimax, Alpha-Beta, Monte Carlo)
et trois niveaux de difficulté.

Lancement
---------

::

    python -m PyAdverseSearch.Interface.connect4_gui

Fonctionnalités
---------------

- Écran de configuration (qui commence, algorithme, difficulté)
- Plateau 6x7 interactif avec détection de la colonne survolée
- Affichage des cellules gagnantes en vert
- Rejouer sans fermer la fenêtre

Niveaux de difficulté
---------------------

.. list-table::
   :header-rows: 1
   :widths: 20 20

   * - Niveau
     - Profondeur
   * - Facile
     - 3
   * - Moyen
     - 5
   * - Difficile
     - 7

Algorithmes disponibles
-----------------------

- Minimax
- Alpha-Beta
- Monte Carlo (1 000 à 3 000 itérations selon la difficulté)

