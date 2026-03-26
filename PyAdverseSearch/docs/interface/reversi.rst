.. docs/interface/reversi.rst

Reversi — Interface Othello / Reversi
=======================================

.. automodule:: PyAdverseSearch.Interface.Reversi
   :members:
   :undoc-members:
   :show-inheritance:

Description
-----------

Interface graphique Arcade pour le jeu de Reversi (Othello) sur un plateau 8x8.
Utilise la bibliothèque `python-arcade <https://api.arcade.academy/>`_ pour
le rendu graphique.

Installation de la dépendance
------------------------------

::

    pip install arcade

Lancement
---------

::

    python -m PyAdverseSearch.Interface.Reversi

Règles du Reversi implémentées
-------------------------------

- Plateau 8x8 avec position initiale officielle (4 pions au centre)
- Pions noirs (``B``) pour MAX, pions blancs (``W``) pour MIN
- Retournement des pions capturés dans les 8 directions
- Gestion du PASS automatique si aucun coup légal n'est disponible
- Détection de fin de partie (plateau plein ou deux PASS consécutifs)

Classe ReversiState
--------------------

La classe :class:`ReversiState` hérite de :class:`~PyAdverseSearch.classes.state.State`
et implémente directement dans le même fichier les fonctions de règles
(``possible_actions``, ``is_terminal``, ``utility``, ``winner_function``).

Elle s'intègre avec :class:`~PyAdverseSearch.classes.minimax.Minimax` via l'API :class:`~PyAdverseSearch.classes.game.Game`.

Algorithme utilisé
------------------

L'IA utilise :class:`~PyAdverseSearch.classes.minimax.Minimax` avec une profondeur de 3.
Pour des performances améliorées, il est possible de substituer
:class:`~PyAdverseSearch.classes.alphabeta.AlphaBeta` avec une profondeur plus élevée.

Constantes de configuration
-----------------------------

.. code-block:: python

    SIZE       = 8     # Taille du plateau
    CELL       = 60    # Taille d'une cellule en pixels
    WIDTH      = 480   # Largeur de la fenêtre
    HEIGHT     = 480   # Hauteur du plateau
    UI_HEIGHT  = 80    # Hauteur de la zone d'interface

