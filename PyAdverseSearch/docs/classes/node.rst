.. docs/classes/node.rst

Node — Noeud de l'arbre de jeu
================================

.. automodule:: PyAdverseSearch.classes.node
   :members:
   :undoc-members:
   :private-members:
   :show-inheritance:

Description
-----------

La classe :class:`Node` représente un noeud dans l'arbre de jeu.
Chaque noeud encapsule un état, maintient les relations parent/enfant,
et stocke les valeurs d'évaluation (utilité pour les terminaux, heuristique
pour les autres).

Attributs principaux
--------------------

.. list-table::
   :header-rows: 1
   :widths: 20 15 45

   * - Attribut
     - Type
     - Description
   * - ``state``
     - ``State``
     - État de jeu associé à ce noeud.
   * - ``parent``
     - ``Node``
     - Noeud parent (``None`` pour la racine).
   * - ``depth``
     - ``int``
     - Profondeur dans l'arbre (0 = racine).
   * - ``children``
     - ``list[Node]``
     - Liste des noeuds successeurs.
   * - ``player``
     - ``str``
     - Joueur actif (``"MAX"`` ou ``"MIN"``).
   * - ``utility``
     - ``float | None``
     - Valeur d'utilité si terminal, sinon ``None``.
   * - ``valuation``
     - ``float``
     - Score heuristique (évaluation non-terminale).
   * - ``id``
     - ``int``
     - Identifiant unique auto-incrémenté.

Identifiants uniques
--------------------

Les identifiants ``id`` sont gérés par le compteur de classe ``Node.next_id``
qui s'incrémente à chaque création d'instance. Cela permet à des structures
de statistiques (ex. dans MCTS) de référencer un noeud de manière stable.

Exemple::

    from PyAdverseSearch.classes.node import Node

    root = Node(state=initial_state, parent=None, depth=0)
    root._expand()

    for child in root.children:
        print(child.player, child.valuation)

