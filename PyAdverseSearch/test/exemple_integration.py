"""
Exemple d'utilisation des algorithmes Alpha-Beta et MTD(f)
avec différentes interfaces de jeu

Ce fichier montre comment brancher facilement les algorithmes
sur n'importe quelle interface de jeu compatible.
"""

from PyAdverseSearch.classes.alphabeta import AlphaBeta
from PyAdverseSearch.classes.mtdf import MTDf
from PyAdverseSearch.classes.algorithm import choose_best_move


# ============================================================================
# EXEMPLE 1 : Utilisation Directe avec une Classe
# ============================================================================

def exemple_utilisation_directe():
    """Utilisation directe de la classe AlphaBeta ou MTDf"""
    from PyAdverseSearch.test.state_tictactoe import generate_tictactoe_game

    # Créer le jeu
    game = generate_tictactoe_game(isMaxStartingParameter=True)
    state = game.state

    # Créer l'algorithme Alpha-Beta
    algo_ab = AlphaBeta(
        game=game,
        max_depth=9,
        use_transposition_table=True
    )

    # Obtenir le meilleur coup
    best_move = algo_ab.choose_best_move(state)
    print("Meilleur coup (Alpha-Beta):", best_move)

    # Créer l'algorithme MTD(f)
    algo_mtdf = MTDf(
        game=game,
        max_depth=9,
        initial_guess=0
    )

    # Obtenir le meilleur coup
    best_move = algo_mtdf.choose_best_move(state)
    print("Meilleur coup (MTD(f)):", best_move)


# ============================================================================
# EXEMPLE 2 : Sélection Dynamique d'Algorithme
# ============================================================================

def exemple_selection_dynamique(algo_name='alphabeta'):
    """Sélection dynamique de l'algorithme à utiliser"""
    from PyAdverseSearch.test.state_tictactoe import generate_tictactoe_game

    game = generate_tictactoe_game(isMaxStartingParameter=True)
    state = game.state

    # Paramètres selon l'algorithme choisi
    params = {
        'alphabeta': {'max_depth': 9, 'use_transposition_table': True},
        'mtdf': {'max_depth': 9, 'initial_guess': 0},
        'minimax': {'max_depth': 9},
    }

    # Choisir le meilleur coup avec l'algorithme sélectionné
    best_move = choose_best_move(
        algo_name,
        game,
        state,
        **params.get(algo_name, {})
    )

    print(f"Meilleur coup ({algo_name}):", best_move)
    return best_move


# ============================================================================
# EXEMPLE 3 : Interface de Jeu Générique
# ============================================================================

class GameInterface:
    """Interface générique pour brancher n'importe quel algorithme"""

    def __init__(self, game, algorithm_name='alphabeta', **algo_params):
        self.game = game
        self.algorithm_name = algorithm_name
        self.algo_params = algo_params
        self.current_state = game.state

    def get_ai_move(self):
        """Obtenir le coup de l'IA"""
        return choose_best_move(
            self.algorithm_name,
            self.game,
            self.current_state,
            **self.algo_params
        )

    def make_move(self, move_state):
        """Appliquer un coup"""
        self.current_state = move_state

    def is_game_over(self):
        """Vérifier si le jeu est terminé"""
        return self.game.game_is_terminal(self.current_state)

    def get_winner(self):
        """Obtenir le gagnant"""
        return self.game.get_winner()


def exemple_interface_generique():
    """Démonstration de l'interface générique"""
    from PyAdverseSearch.test.state_tictactoe import generate_tictactoe_game

    game = generate_tictactoe_game(isMaxStartingParameter=True)

    # Interface avec Alpha-Beta
    interface_ab = GameInterface(
        game,
        algorithm_name='alphabeta',
        max_depth=9,
        use_transposition_table=True
    )

    # Interface avec MTD(f)
    interface_mtdf = GameInterface(
        game,
        algorithm_name='mtdf',
        max_depth=9,
        initial_guess=0
    )

    # Utiliser l'interface
    print("Coup IA (Alpha-Beta):", interface_ab.get_ai_move())
    print("Coup IA (MTD(f)):", interface_mtdf.get_ai_move())


# ============================================================================
# EXEMPLE 4 : Comparaison Multi-Algorithmes
# ============================================================================

class AlgorithmComparator:
    """Compare plusieurs algorithmes sur la même position"""

    def __init__(self, game, state):
        self.game = game
        self.state = state
        self.results = {}

    def test_algorithm(self, algo_name, **params):
        """Teste un algorithme et stocke les résultats"""
        import time

        start = time.time()
        best_move = choose_best_move(
            algo_name,
            self.game,
            self.state,
            **params
        )
        elapsed = time.time() - start

        self.results[algo_name] = {
            'move': best_move,
            'time': elapsed,
            'params': params
        }

        return best_move

    def compare_all(self):
        """Compare tous les algorithmes disponibles"""
        # Alpha-Beta sans TT
        self.test_algorithm('alphabeta', max_depth=9, use_transposition_table=False)

        # Alpha-Beta avec TT
        self.test_algorithm('alphabeta_tt', max_depth=9, use_transposition_table=True)

        # MTD(f)
        self.test_algorithm('mtdf', max_depth=9, initial_guess=0)

        # Minimax
        self.test_algorithm('minimax', max_depth=9)

    def print_results(self):
        """Affiche les résultats de comparaison"""
        print("\n" + "=" * 60)
        print("RÉSULTATS DE COMPARAISON")
        print("=" * 60)

        for algo_name, result in self.results.items():
            print(f"\n{algo_name}:")
            print(f"  Temps: {result['time']:.4f}s")
            print(f"  Paramètres: {result['params']}")


def exemple_comparaison():
    """Démonstration de la comparaison multi-algorithmes"""
    from PyAdverseSearch.test.state_tictactoe import generate_tictactoe_game

    game = generate_tictactoe_game(isMaxStartingParameter=True)
    state = game.state

    comparator = AlgorithmComparator(game, state)
    comparator.compare_all()
    comparator.print_results()


# ============================================================================
# EXEMPLE 5 : Wrapper pour Interface Graphique
# ============================================================================

class GUIWrapper:
    """
    Wrapper pour faciliter l'intégration dans une interface graphique
    (PyQt, Tkinter, etc.)
    """

    def __init__(self, game_generator, algorithm='alphabeta', **algo_params):
        self.game_generator = game_generator
        self.algorithm = algorithm
        self.algo_params = algo_params
        self.game = None
        self.history = []

    def new_game(self, max_starts=True):
        """Démarre une nouvelle partie"""
        self.game = self.game_generator(isMaxStartingParameter=max_starts)
        self.history = [self.game.state]
        return self.game.state

    def get_ai_move(self):
        """Retourne le coup de l'IA pour l'état actuel"""
        if not self.game:
            raise ValueError("Aucune partie en cours")

        current_state = self.history[-1]

        # Créer l'algorithme selon le choix
        if self.algorithm == 'alphabeta':
            algo = AlphaBeta(self.game, **self.algo_params)
        elif self.algorithm == 'mtdf':
            algo = MTDf(self.game, **self.algo_params)
        else:
            # Utiliser la sélection dynamique
            return choose_best_move(
                self.algorithm,
                self.game,
                current_state,
                **self.algo_params
            )

        return algo.choose_best_move(current_state)

    def apply_move(self, move_state):
        """Applique un coup (joueur ou IA)"""
        self.history.append(move_state)

    def undo_move(self):
        """Annule le dernier coup"""
        if len(self.history) > 1:
            self.history.pop()
        return self.history[-1]

    def get_current_state(self):
        """Retourne l'état actuel"""
        return self.history[-1] if self.history else None

    def is_game_over(self):
        """Vérifie si la partie est terminée"""
        current = self.get_current_state()
        return self.game.game_is_terminal(current) if current else False

    def get_winner(self):
        """Retourne le gagnant"""
        return self.game.get_winner() if self.is_game_over() else None


def exemple_gui_wrapper():
    """Démonstration du wrapper GUI"""
    from PyAdverseSearch.test.state_tictactoe import generate_tictactoe_game

    # Créer le wrapper avec Alpha-Beta
    gui = GUIWrapper(
        generate_tictactoe_game,
        algorithm='alphabeta',
        max_depth=9,
        use_transposition_table=True
    )

    # Nouvelle partie
    state = gui.new_game(max_starts=True)
    print("Nouvelle partie créée")

    # L'IA joue
    ai_move = gui.get_ai_move()
    gui.apply_move(ai_move)
    print("L'IA a joué")

    # Vérifier l'état
    print("Partie terminée?", gui.is_game_over())


# ============================================================================
# MAIN - Exemples d'exécution
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("EXEMPLES D'UTILISATION DES ALGORITHMES")
    print("=" * 60)

    print("\n1. Utilisation directe")
    print("-" * 60)
    # exemple_utilisation_directe()

    print("\n2. Sélection dynamique")
    print("-" * 60)
    exemple_selection_dynamique('alphabeta')
    exemple_selection_dynamique('mtdf')

    print("\n3. Interface générique")
    print("-" * 60)
    exemple_interface_generique()

    print("\n4. Wrapper GUI")
    print("-" * 60)
    exemple_gui_wrapper()

    # print("\n5. Comparaison multi-algorithmes")
    # print("-" * 60)
    # exemple_comparaison()

    print("\n" + "=" * 60)
    print("FIN DES EXEMPLES")
    print("=" * 60)

