"""
Module tree
===========

Ce module définit la classe :class:`GameTree` qui construit et gère l'arbre de jeu complet.
"""

from .node import Node

class GameTree:
    """
    Construit et gère l'arbre de jeu à partir d'un état initial.

    La construction de l'arbre est effectuée de manière récursive à la création
    de l'instance. Chaque noeud est développé jusqu'à la profondeur maximale
    spécifiée ou jusqu'à atteindre un état terminal.

    :param initial_state: État initial du jeu (racine de l'arbre).
    :type initial_state: State
    :param max_depth: Profondeur maximale de construction de l'arbre
                      (``float('inf')`` pour un développement complet).
    :type max_depth: int or float

    :ivar root: Noeud racine de l'arbre.
    :vartype root: Node
    :ivar node_count: Nombre de noeuds internes (non-feuilles) construits.
    :vartype node_count: int
    :ivar leaf: Nombre de noeuds feuilles (états terminaux ou limite de profondeur).
    :vartype leaf: int

    .. warning::
        Pour des jeux complexes, la construction complète de l'arbre peut consommer
        beaucoup de mémoire. Utiliser ``max_depth`` pour limiter l'exploration.

    Exemple::

        tree = GameTree(initial_state, max_depth=4)
        tree.display()
    """

    def __init__(self, initial_state, max_depth=float('inf')):
        self.root = Node(initial_state, parent=None, depth=0)
        self.node_count = 0
        self.leaf = 0
        self.max_depth = max_depth
        self.__build_tree(self.root)

    def __build_tree(self, node):
        """
        Construit récursivement l'arbre depuis le noeud donné.

        Méthode privée : ne pas appeler directement depuis l'extérieur.
        Développe chaque noeud non-terminal jusqu'à ``max_depth``.

        :param node: Noeud à développer.
        :type node: Node
        """
        if node.utility is not None:
            self.leaf += 1
            return
        elif node.depth < self.max_depth:
            node._expand()
            self.node_count += 1
            for child in node.children:
                self.__build_tree(child)

    def display(self):
        """
        Affiche un résumé de l'arbre (nombre de noeuds et de feuilles)
        suivi de la structure complète depuis la racine.
        """
        print("Nombre de noeuds :", self.node_count)
        print("Nombre de feuilles :", self.leaf)
        self.root.display()
