.. docs/classes/tree.rst

GameTree — Arbre de jeu complet
================================

.. automodule:: PyAdverseSearch.classes.tree
   :members:
   :undoc-members:
   :private-members:
   :show-inheritance:

Description
-----------

:class:`GameTree` construit récursivement l'arbre de jeu complet à partir
d'un état initial. La construction se fait dans le constructeur via la méthode
privée ``__build_tree``.

.. warning::
    Pour des jeux complexes comme Puissance 4 ou les Échecs, un développement
    complet de l'arbre est **impossible en pratique** (espace mémoire exponentiel).
    Toujours spécifier ``max_depth`` pour limiter l'exploration.

Cas d'utilisation recommandés
------------------------------

- Jeux petits (morpion 3x3) : développement complet possible.
- Visualisation pédagogique d'arbres de jeu à faible profondeur.
- Pré-calcul d'arbres pour des analyses offline.

Exemple::

    from PyAdverseSearch.classes.tree import GameTree

    # Développement limité à 3 niveaux
    tree = GameTree(initial_state=my_state, max_depth=3)
    tree.display()
    # Affiche : "Nombre de noeuds : X" et "Nombre de feuilles : Y"

