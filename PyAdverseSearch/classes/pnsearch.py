# FILE: PyAdverseSearch/classes/pnsearch.py

"""
Implémentation de l'algorithme Proof-Number Search (PN-Search) pour la résolution de fin de partie.

PN-Search est un algorithme de recherche dans les arbres de jeu qui vise à prouver qu'une position
est gagnante ou perdante en utilisant des nombres de preuve (phi) et de réfutation (delta).

Références :
- Allis, L. V. (1994). Searching for Solutions in Games and Artificial Intelligence.
"""

from PyAdverseSearch.classes.algorithm import SearchAlgorithm
from enum import Enum
import sys


class ProofStatus(Enum):
    """Statut de preuve d'un nœud PN-Search"""
    UNKNOWN = 0      # Statut inconnu
    PROVEN = 1       # Position prouvée gagnante pour le joueur à jouer
    DISPROVEN = 2    # Position prouvée perdante pour le joueur à jouer


class PNNode:
    """
    Nœud spécialisé pour l'algorithme PN-Search.
    Stocke les nombres de preuve (phi) et de réfutation (delta).
    """

    def __init__(self, state, parent=None, move=None):
        """
        Initialise un nœud PN-Search.

        :param state: État du jeu à ce nœud
        :param parent: Nœud parent (None pour la racine)
        :param move: Coup qui a mené à ce nœud depuis le parent
        """
        self.state = state
        self.parent = parent
        self.move = move  # Le coup qui a amené à cet état
        self.children = []  # Liste des nœuds enfants
        self.expanded = False  # Indique si le nœud a été étendu

        # Nombres de preuve et de réfutation
        self.phi = 1  # Nombre de preuve (difficulté de prouver que ce nœud est gagnant)
        self.delta = 1  # Nombre de réfutation (difficulté de prouver que ce nœud est perdant)

        # Statut de preuve
        self.proof_status = ProofStatus.UNKNOWN

        # Type de nœud (OR pour MAX, AND pour MIN)
        self.is_or_node = (state.player == "MAX")

    def is_proven(self):
        """Retourne True si la position est prouvée gagnante"""
        return self.proof_status == ProofStatus.PROVEN

    def is_disproven(self):
        """Retourne True si la position est prouvée perdante"""
        return self.proof_status == ProofStatus.DISPROVEN

    def is_solved(self):
        """Retourne True si la position est résolue (prouvée ou réfutée)"""
        return self.proof_status != ProofStatus.UNKNOWN


class PNSearch(SearchAlgorithm):
    """
    Implémentation de l'algorithme Proof-Number Search.

    PN-Search explore l'arbre de jeu de manière sélective en se concentrant
    sur les branches les plus prometteuses pour prouver ou réfuter une position.
    """

    INFINITY = sys.maxsize  # Valeur représentant l'infini

    def __init__(self, game=None, max_nodes=100000, use_transposition_table=True):
        """
        Initialise l'algorithme PN-Search.

        :param game: Instance de la classe Game
        :param max_nodes: Nombre maximum de nœuds à explorer (limite de mémoire)
        :param use_transposition_table: Active/désactive la table de transposition
        """
        if game is None:
            raise ValueError("Le paramètre 'game' est requis pour PNSearch")

        self.game = game
        self.max_nodes = max_nodes
        self.use_transposition_table = use_transposition_table

        # Table de transposition : hash de l'état -> PNNode
        self.transposition_table = {} if use_transposition_table else None

        # Compteur de nœuds explorés
        self.nodes_explored = 0

        # Pile pour détecter les cycles (chemin actuel dans l'arbre)
        self.current_path = set()

    def choose_best_move(self, state):
        """
        Point d'entrée principal : trouve le meilleur coup depuis l'état donné.

        :param state: État actuel du jeu
        :return: Meilleur état enfant à jouer, ou None si aucun coup gagnant trouvé
        """
        # Réinitialisation pour chaque nouvelle recherche
        self.transposition_table = {} if self.use_transposition_table else None
        self.nodes_explored = 0
        self.current_path = set()

        # Création du nœud racine
        root = PNNode(state)

        # Lancement de la recherche PN
        self.pn_search(root)

        # Analyse des résultats
        if root.is_proven():
            # Position gagnante : retourner le meilleur coup
            return self._extract_best_move(root)
        elif root.is_disproven():
            # Position perdante : retourner un coup par défaut (ou None)
            print("Position prouvée perdante. Aucun coup gagnant.")
            return self._get_fallback_move(state)
        else:
            # Non résolu dans la limite de nœuds
            print(f"Recherche incomplète après {self.nodes_explored} nœuds.")
            return self._extract_best_partial_move(root)

    def pn_search(self, root):
        """
        Algorithme principal de PN-Search.

        :param root: Nœud racine de la recherche
        """
        # Évaluation initiale de la racine
        self.evaluate(root)

        # Boucle principale : tant que la racine n'est pas résolue
        while not root.is_solved() and self.nodes_explored < self.max_nodes:
            # Sélection du nœud le plus prometteur (Most Proving Node)
            mpn = self.select_most_proving_node(root)

            if mpn is None:
                break

            # Expansion du nœud sélectionné
            self.expand_node(mpn)

            # Mise à jour des valeurs depuis le nœud étendu vers la racine
            self.update_ancestors(mpn)

    def evaluate(self, node):
        """
        Évalue un nœud et initialise ses valeurs phi et delta.

        :param node: Nœud à évaluer
        """
        # Vérification dans la table de transposition
        if self.use_transposition_table:
            state_hash = self._hash_state(node.state)
            if state_hash in self.transposition_table:
                cached_node = self.transposition_table[state_hash]
                node.phi = cached_node.phi
                node.delta = cached_node.delta
                node.proof_status = cached_node.proof_status
                return

        # Vérification si c'est un état terminal
        if self.game.game_is_terminal(node.state):
            self._evaluate_terminal(node)
        else:
            # État non terminal : initialisation par défaut
            node.phi = 1
            node.delta = 1
            node.proof_status = ProofStatus.UNKNOWN

        # Stockage dans la table de transposition
        if self.use_transposition_table:
            self.transposition_table[state_hash] = node

    def _evaluate_terminal(self, node):
        """
        Évalue un nœud terminal en fonction de l'utilité.

        :param node: Nœud terminal à évaluer
        """
        utility = self.game.game_utility(node.state)

        # Convention : utilité positive = victoire pour MAX, négative = victoire pour MIN
        # utility == 1 : victoire MAX, -1 : victoire MIN, 0 : match nul

        if node.is_or_node:  # Nœud MAX (OR)
            if utility > 0:  # MAX gagne
                node.proof_status = ProofStatus.PROVEN
                node.phi = 0
                node.delta = self.INFINITY
            elif utility < 0:  # MAX perd
                node.proof_status = ProofStatus.DISPROVEN
                node.phi = self.INFINITY
                node.delta = 0
            else:  # Match nul
                node.proof_status = ProofStatus.DISPROVEN
                node.phi = self.INFINITY
                node.delta = 0
        else:  # Nœud MIN (AND)
            if utility < 0:  # MIN gagne (donc MAX perd)
                node.proof_status = ProofStatus.PROVEN
                node.phi = 0
                node.delta = self.INFINITY
            elif utility > 0:  # MIN perd (donc MAX gagne)
                node.proof_status = ProofStatus.DISPROVEN
                node.phi = self.INFINITY
                node.delta = 0
            else:  # Match nul
                node.proof_status = ProofStatus.DISPROVEN
                node.phi = self.INFINITY
                node.delta = 0

    def select_most_proving_node(self, root):
        """
        Sélectionne le nœud le plus prometteur (Most Proving Node) à développer.
        Suit le chemin de l'arbre en choisissant à chaque niveau le meilleur enfant.

        :param root: Nœud racine
        :return: Nœud le plus prometteur (feuille non développée)
        """
        current = root

        # Descente dans l'arbre jusqu'à une feuille non développée
        while current.expanded and not current.is_solved():
            # Vérification de cycle
            state_hash = self._hash_state(current.state)
            if state_hash in self.current_path:
                # Cycle détecté : marquer comme non résolu et stopper
                return None

            self.current_path.add(state_hash)

            # Sélection du meilleur enfant
            if current.is_or_node:
                # Nœud OR : choisir l'enfant avec le plus petit phi
                best_child = min(current.children, key=lambda c: c.phi)
            else:
                # Nœud AND : choisir l'enfant avec le plus petit delta
                best_child = min(current.children, key=lambda c: c.delta)

            current = best_child

        # Nettoyage du chemin après sélection
        state_hash = self._hash_state(current.state)
        self.current_path.discard(state_hash)

        return current if not current.is_solved() else None

    def expand_node(self, node):
        """
        Étend un nœud en générant tous ses enfants.

        :param node: Nœud à étendre
        """
        if node.expanded or node.is_solved():
            return

        # Vérification de la limite de nœuds
        if self.nodes_explored >= self.max_nodes:
            return

        # Génération des enfants
        possible_moves = node.state._possible_actions()

        for move in possible_moves:
            child_state = node.state._apply_action(move)
            child_node = PNNode(child_state, parent=node, move=move)

            # Évaluation de l'enfant
            self.evaluate(child_node)

            node.children.append(child_node)
            self.nodes_explored += 1

            if self.nodes_explored >= self.max_nodes:
                break

        node.expanded = True

        # Mise à jour des valeurs phi/delta du nœud
        self.update_proof_numbers(node)

    def update_proof_numbers(self, node):
        """
        Met à jour les nombres de preuve et de réfutation d'un nœud
        en fonction de ses enfants.

        :param node: Nœud à mettre à jour
        """
        if not node.expanded or len(node.children) == 0:
            return

        if node.is_or_node:
            # Nœud OR (MAX) : il suffit qu'UN enfant soit prouvé
            # phi = min(phi des enfants)
            # delta = sum(delta des enfants)
            node.phi = min(child.phi for child in node.children)
            node.delta = sum(child.delta for child in node.children)

            # Gestion de l'overflow pour delta
            if node.delta > self.INFINITY:
                node.delta = self.INFINITY
        else:
            # Nœud AND (MIN) : TOUS les enfants doivent être prouvés
            # phi = sum(phi des enfants)
            # delta = min(delta des enfants)
            node.phi = sum(child.phi for child in node.children)
            node.delta = min(child.delta for child in node.children)

            # Gestion de l'overflow pour phi
            if node.phi > self.INFINITY:
                node.phi = self.INFINITY

        # Mise à jour du statut de preuve
        if node.phi == 0:
            node.proof_status = ProofStatus.PROVEN
        elif node.delta == 0:
            node.proof_status = ProofStatus.DISPROVEN
        else:
            node.proof_status = ProofStatus.UNKNOWN

    def update_ancestors(self, node):
        """
        Met à jour les ancêtres d'un nœud en remontant vers la racine.

        :param node: Nœud dont les ancêtres doivent être mis à jour
        """
        current = node.parent

        while current is not None:
            old_phi = current.phi
            old_delta = current.delta

            self.update_proof_numbers(current)

            # Optimisation : arrêter si les valeurs n'ont pas changé
            if current.phi == old_phi and current.delta == old_delta:
                break

            current = current.parent

    def _extract_best_move(self, root):
        """
        Extrait le meilleur coup d'une position prouvée gagnante.

        :param root: Nœud racine (doit être prouvé)
        :return: État résultant du meilleur coup
        """
        if not root.expanded or len(root.children) == 0:
            return None

        # Chercher l'enfant prouvé (phi == 0) pour un nœud OR
        # ou l'enfant avec le meilleur phi pour continuer
        if root.is_or_node:
            for child in root.children:
                if child.is_proven() or child.phi == 0:
                    return child.state
            # Si aucun enfant prouvé, prendre celui avec le plus petit phi
            best_child = min(root.children, key=lambda c: c.phi)
            return best_child.state
        else:
            # Pour un nœud AND, tous les enfants devraient être prouvés
            # Prendre le premier enfant avec delta minimal
            best_child = min(root.children, key=lambda c: c.delta)
            return best_child.state

    def _extract_best_partial_move(self, root):
        """
        Extrait le meilleur coup d'une position non complètement résolue.
        Utilise les valeurs phi/delta comme heuristique.

        :param root: Nœud racine
        :return: État résultant du meilleur coup estimé
        """
        if not root.expanded or len(root.children) == 0:
            # Pas d'enfants : retourner un coup aléatoire
            return self._get_fallback_move(root.state)

        # Choisir l'enfant avec les meilleures caractéristiques
        if root.is_or_node:
            # Pour OR : privilégier petit phi (plus facile à prouver)
            best_child = min(root.children, key=lambda c: (c.phi, -c.delta))
        else:
            # Pour AND : privilégier petit delta (plus facile à réfuter l'adversaire)
            best_child = min(root.children, key=lambda c: (c.delta, -c.phi))

        return best_child.state

    def _get_fallback_move(self, state):
        """
        Retourne un coup par défaut quand aucune analyse n'est disponible.

        :param state: État actuel
        :return: Premier coup possible ou None
        """
        possible_moves = state._possible_actions()
        if possible_moves:
            return state._apply_action(possible_moves[0])
        return None

    def _hash_state(self, state):
        """
        Génère un hash unique pour un état de jeu.
        Utilisé pour la table de transposition et la détection de cycles.

        :param state: État à hasher
        :return: Hash de l'état
        """
        # Conversion du plateau en tuple pour le rendre hashable
        try:
            # Si le plateau est une liste de listes
            if isinstance(state.board, list):
                return hash(tuple(tuple(row) if isinstance(row, list) else row
                                 for row in state.board))
            # Si le plateau est déjà hashable
            else:
                return hash(state.board)
        except (TypeError, AttributeError):
            # Fallback : utiliser l'id de l'objet (moins efficace)
            return id(state.board)

    def get_statistics(self):
        """
        Retourne des statistiques sur la recherche effectuée.

        :return: Dictionnaire de statistiques
        """
        return {
            'nodes_explored': self.nodes_explored,
            'transposition_table_size': len(self.transposition_table) if self.transposition_table else 0,
            'max_nodes': self.max_nodes
        }

