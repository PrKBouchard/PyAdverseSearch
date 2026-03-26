"""
Module node
===========

Ce module définit la classe :class:`Node`, représentant un noeud dans l'arbre de jeu.
"""

# FILE: node.py

class Node:
    """
    Represente un noeud dans l'arbre de jeu.

    Chaque noeud encapsule un état du jeu, maintient les relations parent/enfant
    dans l'arbre, et stocke des informations d'évaluation (utilité, heuristique).

    :param state: L'état de jeu associé à ce noeud.
    :type state: State
    :param parent: Le noeud parent dans l'arbre (``None`` si racine).
    :type parent: Node or None
    :param depth: Profondeur du noeud dans l'arbre (0 = racine).
    :type depth: int

    :ivar children: Liste des noeuds successeurs.
    :vartype children: list[Node]
    :ivar utility: Valeur d'utilité si le noeud est terminal, ``None`` sinon.
    :vartype utility: float or None
    :ivar valuation: Score heuristique de l'état (évaluation non-terminale).
    :vartype valuation: float
    :ivar id: Identifiant unique auto-incrémenté du noeud.
    :vartype id: int
    :ivar player: Joueur actif à ce noeud (``"MAX"`` ou ``"MIN"``).
    :vartype player: str
    """

    next_id = 0

    def __init__(self, state, parent=None, depth=0):
        """
        Initialise un noeud avec l'état de jeu donné, le noeud parent et la profondeur.

        Calcule également le joueur actif et évalue l'état si le noeud n'est pas terminal.

        :param state: L'état de jeu à ce noeud.
        :param parent: Le noeud parent dans l'arbre (None si racine).
        :param depth: La profondeur du noeud dans l'arbre.
        """
        self.state = state
        self.parent = parent
        self.depth = depth
        self.player = None
        self.children = []
        if self.is_terminal():
            self.utility = self.state._utility()
        else:
            self.utility = None
        self.valuation = self.state._evaluate()
        self.id = Node.next_id
        Node.next_id += 1
        self.calculatePlayer()

    def _expand(self):
        """
        Génère tous les états successeurs et les ajoute comme noeuds enfants.

        Pour chaque action légale depuis l'état courant, crée un nouveau
        :class:`Node` enfant et l'ajoute à la liste :attr:`children`.
        """
        for action in self.state._possible_actions():
            new_state = self.state._apply_action(action)
            child_node = Node(state=new_state, parent=self, depth=self.depth + 1)
            self.children.append(child_node)

    def is_terminal(self):
        """
        Vérifie si ce noeud représente un état terminal.

        :return: ``True`` si l'état est terminal, ``False`` sinon.
        :rtype: bool
        """
        return self.state._is_terminal()

    def display(self, depth=0):
        """
        Affiche récursivement la structure de l'arbre dans la console.

        :param depth: Niveau d'indentation courant (utilisé en récursion).
        :type depth: int
        """
        space = "  " * depth
        print(f"{space}Depth: {self.depth}, Player: {self.state.player}, "
              f"Heuristic: {self.valuation}, utility: {self.utility}")
        self.state.display()
        for child in self.children:
            child.display(depth + 1)

    def calculatePlayer(self):
        """
        Détermine et assigne le joueur actif pour ce noeud.

        Si l'état possède déjà un attribut ``player`` renseigné, celui-ci est utilisé
        directement. Sinon, le joueur est déterminé en fonction de la parité de
        la profondeur et de ``isMaxStarting`` dans la configuration du jeu.
        """
        if hasattr(self.state, 'player') and self.state.player is not None:
            self.player = self.state.player
            return

        isMaxStarting = self.state.game.isMaxStarting
        if self.depth % 2 == 0:
            self.player = "MAX" if isMaxStarting else "MIN"
        else:
            self.player = "MIN" if isMaxStarting else "MAX"