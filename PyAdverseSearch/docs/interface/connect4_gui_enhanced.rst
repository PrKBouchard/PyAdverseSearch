.. docs/interface/connect4_gui_enhanced.rst

Connect4GUI Enhanced — Interface Puissance 4 complète
======================================================

.. automodule:: PyAdverseSearch.Interface.connect4_gui_enhanced
   :members:
   :undoc-members:
   :show-inheritance:

Description
-----------

Version avancée de l'interface Puissance 4 intégrant tous les algorithmes
de la bibliothèque, un panneau de statistiques en temps réel, et la
génération d'un rapport PDF de fin de partie.

Lancement
---------

::

    python -m PyAdverseSearch.Interface.connect4_gui_enhanced

Fonctionnalités
---------------

**Algorithmes disponibles**

- Mode Rapide : MTD(f) + PN-Search (recommandé)
- Mode Auto Equilibré : AutoSolver avec tous les algorithmes
- Minimax, Alpha-Beta, MTD(f), Negamax, Monte Carlo, PN-Search (manuels)

**Interface de jeu**

- Plateau 6x7 interactif avec animation des coups
- Indicateur de la colonne survolée
- Mise en surbrillance de l'alignement gagnant

**Panneau de statistiques**

Affiché en temps réel pendant la partie :

- Algorithme utilisé par l'IA pour le dernier coup
- Raison du choix (pour AutoSolver)
- Durée de calcul de l'IA
- Nombre de coups joués

**Export PDF**

Bouton disponible en fin de partie pour générer un rapport complet via
:mod:`~PyAdverseSearch.Interface.pdf_report`.

Architecture interne
--------------------

.. code-block:: text

    Connect4GUI
    ├── create_config_screen()   -- écran de configuration initial
    ├── start_game()             -- initialisation + sélection de l'algo
    ├── create_game_board()      -- création du plateau Tkinter
    ├── human_click(col)         -- gestion du clic humain
    ├── ai_move()                -- déclenchement du calcul IA (thread)
    ├── update_board()           -- rafraîchissement visuel
    ├── check_game_over()        -- détection fin de partie
    ├── update_stats_panel()     -- mise à jour du panneau stats
    └── export_pdf()             -- génération du rapport PDF

