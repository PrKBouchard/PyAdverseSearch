"""
Module montecarlo
=================

Ce module implémente l'algorithme Monte Carlo Tree Search (MCTS) avec la
formule UCB1 pour l'équilibre exploration/exploitation.
"""

import math
import random
import time
from PyAdverseSearch.classes.algorithm import SearchAlgorithm
from PyAdverseSearch.classes.node import Node

class MonteCarlo(SearchAlgorithm):
    """
    Implémentation de Monte Carlo Tree Search (MCTS) avec UCB1.

    L'algorithme repose sur quatre phases répétées : sélection, expansion,
    simulation (rollout aléatoire) et rétropropagation. Il n'a pas besoin
    de fonction heuristique explicite et fonctionne bien avec un grand
    nombre d'itérations.

    :param game: Instance du jeu configuré.
    :type game: Game or None
    :param max_iterations: Nombre maximum de simulations à effectuer.
    :type max_iterations: int
    :param max_time_seconds: Limite de temps en secondes (``None`` = pas de limite).
    :type max_time_seconds: float or None

    Référence :
        Kocsis, L. & Szepesvari, C. (2006). Bandit based Monte-Carlo Planning.

    Exemple::

        algo = MonteCarlo(game=my_game, max_iterations=5000, max_time_seconds=2.0)
        best_state = algo.choose_best_move(current_state)
    """

    def __init__(self, game=None, max_iterations=10000, max_time_seconds=None):
        self.game = game
        self.max_iterations = max_iterations
        self.max_time = max_time_seconds
        self.start_time = None

    def choose_best_move(self, state):
        """
        Sélectionne le meilleur coup via MCTS.

        Lance jusqu'à ``max_iterations`` simulations depuis l'état racine,
        puis retourne le coup le plus visité.

        :param state: État courant du jeu.
        :type state: State
        :return: L'état enfant correspondant au coup le plus prometteur.
        :rtype: State
        """
        root = Node(state, parent=None, depth=0)
        stats = {}
        self.start_time = time.time()

        for _ in range(self.max_iterations):
            if self.time_limit_reached():
                break
            self.run_simulation(root, stats)

        if not root.children:
            root._expand()
        if not root.children:
            return state

        best_child = max(
            root.children,
            key=lambda child: stats.get(child.id, (0, 0))[1]
        )
        return best_child.state

    def run_simulation(self, root, stats):
        """
        Exécute une simulation complète (sélection + expansion + rollout + rétropropagation).

        :param root: Noeud racine de la recherche.
        :type root: Node
        :param stats: Dictionnaire de statistiques ``{node_id: (wins, visits)}``.
        :type stats: dict
        """
        node = self.select(root, stats)
        if not self.game.game_is_terminal(node.state):
            node._expand()
            if node.children:
                node = random.choice(node.children)

        result = self.simulate(node)
        self.backpropagate(node, result, stats)

    def select(self, node, stats):
        """
        Sélectionne le noeud feuille le plus prometteur via UCB1.

        Descend dans l'arbre en appliquant :meth:`ucb1_select` tant que
        le noeud courant possède des enfants.

        :param node: Noeud de départ.
        :type node: Node
        :param stats: Statistiques de visite.
        :type stats: dict
        :return: Noeud feuille sélectionné.
        :rtype: Node
        """
        while node.children:
            node = self.ucb1_select(node, stats)
        return node

    def ucb1_select(self, node, stats):
        """
        Sélectionne l'enfant avec le meilleur score UCB1.

        La formule UCB1 équilibre exploitation (score moyen) et exploration
        (noeuds peu visités). Le score est inversé pour les noeuds MIN.

        :param node: Noeud parent dont on sélectionne un enfant.
        :type node: Node
        :param stats: Statistiques de visite ``{node_id: (wins, visits)}``.
        :type stats: dict
        :return: Noeud enfant sélectionné.
        :rtype: Node
        """
        total_visits = sum(stats.get(child.id, (0, 1))[1] for child in node.children)
        log_total = math.log(total_visits + 1)
        best_score = -float('inf')
        best_child = None
        is_max_turn = (node.player == "MAX")

        for child in node.children:
            wins, visits = stats.get(child.id, (0, 1))
            avg_score = wins / visits
            exploitation = avg_score if is_max_turn else -avg_score
            ucb1 = exploitation + math.sqrt(2 * log_total / visits)
            if ucb1 > best_score:
                best_score = ucb1
                best_child = child

        return best_child

    def simulate(self, node):
        """
        Effectue un rollout aléatoire depuis le noeud donné jusqu'à un état terminal.

        :param node: Noeud de départ du rollout.
        :type node: Node
        :return: Résultat de la simulation (+1 victoire MAX, -1 victoire MIN, 0 nul).
        :rtype: int
        """
        state = node.state
        while not self.game.game_is_terminal(state):
            actions = state._possible_actions()
            if not actions:
                break
            action = random.choice(actions)
            state = state._apply_action(action)
        return self.evaluate_winner(state)

    def evaluate_winner(self, state):
        """
        Évalue le résultat d'un état terminal.

        :param state: État terminal du jeu.
        :type state: State
        :return: ``+1`` si MAX gagne, ``-1`` si MIN gagne, ``0`` pour nul.
        :rtype: int
        """
        winner = self.game.winner_function(state)
        if winner == "MAX":
            return 1
        elif winner == "MIN":
            return -1
        else:
            return 0

    def backpropagate(self, node, result, stats):
        """
        Propage le résultat d'une simulation vers la racine.

        Met à jour les statistiques (gains et visites) de chaque noeud
        sur le chemin depuis le noeud simulé jusqu'à la racine.

        :param node: Noeud depuis lequel remonter.
        :type node: Node
        :param result: Résultat de la simulation (+1, -1 ou 0).
        :type result: int
        :param stats: Dictionnaire de statistiques à mettre à jour.
        :type stats: dict
        """
        while node is not None:
            if node.id not in stats:
                stats[node.id] = (0, 0)
            wins, visits = stats[node.id]
            stats[node.id] = (wins + result, visits + 1)
            node = node.parent

    def time_limit_reached(self):
        """
        Vérifie si la limite de temps de calcul est atteinte.

        :return: ``True`` si le temps alloué est dépassé, ``False`` sinon.
        :rtype: bool
        """
        if self.max_time is None:
            return False
        return (time.time() - self.start_time) >= self.max_time
