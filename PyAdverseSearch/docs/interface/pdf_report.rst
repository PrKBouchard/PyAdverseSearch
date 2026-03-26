.. docs/interface/pdf_report.rst

pdf_report — Générateur de rapport PDF
========================================

.. automodule:: PyAdverseSearch.Interface.pdf_report
   :members:
   :undoc-members:
   :show-inheritance:

Description
-----------

Module de génération de rapports PDF de fin de partie pour Puissance 4.
Utilise la bibliothèque `ReportLab <https://www.reportlab.com/>`_.

Installation de la dépendance
------------------------------

::

    pip install reportlab

Point d'entrée principal
-------------------------

La fonction :func:`export_game_pdf` est le seul point d'entrée public.
Elle ouvre une boite de dialogue pour choisir l'emplacement de sauvegarde,
puis génère le fichier PDF.

Structure du rapport généré
----------------------------

Le rapport PDF contient les sections suivantes :

1. **En-tête** : titre, date/heure, résultat de la partie
2. **Résumé de la partie** : gagnant, nombre de coups, durée, mode IA, difficulté
3. **Historique des coups** : liste numérotée de tous les coups joués
4. **Statistiques IA** : tableau des algorithmes utilisés avec temps de calcul et stats

Format du paramètre ``game_summary``
--------------------------------------

::

    game_summary = {
        "winner":       str,    # "Joueur", "IA" ou "Match nul"
        "total_moves":  int,    # Nombre total de coups
        "duration":     float,  # Durée en secondes
        "algo_mode":    str,    # "classic", "fast" ou nom d'algo fixe
        "difficulty":   str,    # "easy", "medium", "hard" ou "expert"
        "human_starts": bool,   # True si l'humain commence
    }

Format du paramètre ``algo_records``
--------------------------------------

Liste d'objets :class:`~PyAdverseSearch.classes.autosolver.AlgoRecord` ou
de dictionnaires avec les clés : ``move_number``, ``algo_name``,
``reason``, ``elapsed``, ``stats``.

Palette de couleurs du rapport
--------------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 30

   * - Élément
     - Couleur
   * - En-tête
     - ``#0066cc``
   * - Lignes paires
     - ``#e8f0fe``
   * - En-tête algo
     - ``#1a237e``
   * - Victoire
     - ``#1b5e20``
   * - Défaite
     - ``#b71c1c``
   * - Match nul
     - ``#e65100``

Exemple d'utilisation
----------------------

::

    from PyAdverseSearch.Interface.pdf_report import export_game_pdf

    export_game_pdf(
        game_summary={
            "winner": "IA",
            "total_moves": 18,
            "duration": 42.5,
            "algo_mode": "fast",
            "difficulty": "hard",
            "human_starts": True,
        },
        move_history=["1. Vous: Col 4", "2. IA: Col 4", ...],
        algo_records=solver.get_records(),
    )

