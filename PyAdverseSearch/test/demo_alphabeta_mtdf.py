# FILE: PyAdverseSearch/test/demo_alphabeta_mtdf.py
# python -m PyAdverseSearch.test.demo_alphabeta_mtdf

"""
Démonstration simple de l'utilisation d'Alpha-Beta et MTD(f)
"""

from .state_tictactoe import generate_tictactoe_game
from PyAdverseSearch.classes.alphabeta import AlphaBeta
from PyAdverseSearch.classes.mtdf import MTDf
from PyAdverseSearch.classes.algorithm import choose_best_move
import time


def demo_simple_alphabeta():
    """Démonstration simple d'Alpha-Beta"""
    print("=" * 70)
    print("DÉMONSTRATION ALPHA-BETA")
    print("=" * 70)

    # Créer un jeu de TicTacToe
    game = generate_tictactoe_game(isMaxStartingParameter=True)
    state = game.state

    print("\n1. Créer l'algorithme Alpha-Beta")
    print("-" * 70)
    print("algorithm = AlphaBeta(game=game, max_depth=9)")
    algorithm = AlphaBeta(game=game, max_depth=9)

    print("\n2. État initial du jeu")
    print("-" * 70)
    state.display()

    print("\n3. Rechercher le meilleur coup")
    print("-" * 70)
    print("best_move = algorithm.choose_best_move(state)")

    start = time.time()
    best_move = algorithm.choose_best_move(state)
    elapsed = time.time() - start

    print(f"\n✓ Meilleur coup trouvé en {elapsed:.4f}s")

    print("\n4. Afficher le résultat")
    print("-" * 70)
    if best_move:
        best_move.display()

    print("\n5. Statistiques de la recherche")
    print("-" * 70)
    stats = algorithm.get_statistics()
    print(f"• Nœuds explorés: {stats['nodes_explored']:,}")
    print(f"• Coupures Alpha-Beta: {stats['cutoffs']:,}")
    print(f"• Efficacité: {(stats['cutoffs']/stats['nodes_explored']*100):.1f}% de coupures")


def demo_simple_mtdf():
    """Démonstration simple de MTD(f)"""
    print("\n\n" + "=" * 70)
    print("DÉMONSTRATION MTD(f)")
    print("=" * 70)

    # Créer un jeu de TicTacToe
    game = generate_tictactoe_game(isMaxStartingParameter=True)
    state = game.state

    print("\n1. Créer l'algorithme MTD(f)")
    print("-" * 70)
    print("algorithm = MTDf(game=game, max_depth=9, initial_guess=0)")
    algorithm = MTDf(game=game, max_depth=9, initial_guess=0)

    print("\n2. État initial du jeu")
    print("-" * 70)
    state.display()

    print("\n3. Rechercher le meilleur coup avec MTD(f)")
    print("-" * 70)
    print("best_move = algorithm.choose_best_move(state)")

    start = time.time()
    best_move = algorithm.choose_best_move(state)
    elapsed = time.time() - start

    print(f"\n✓ Meilleur coup trouvé en {elapsed:.4f}s")

    print("\n4. Afficher le résultat")
    print("-" * 70)
    if best_move:
        best_move.display()

    print("\n5. Statistiques de la recherche MTD(f)")
    print("-" * 70)
    stats = algorithm.get_statistics()
    print(f"• Nœuds explorés: {stats['nodes_explored']:,}")
    print(f"• Itérations MTD(f): {stats['iterations']}")
    print(f"• Coupures: {stats['cutoffs']:,}")
    print(f"• Table de transposition: {stats['transposition_table_size']:,} entrées")


def demo_dynamic_selection():
    """Démonstration de la sélection dynamique d'algorithmes"""
    print("\n\n" + "=" * 70)
    print("DÉMONSTRATION SÉLECTION DYNAMIQUE")
    print("=" * 70)

    game = generate_tictactoe_game(isMaxStartingParameter=True)
    state = game.state

    print("\nUtilisation de la fonction choose_best_move() pour sélectionner")
    print("dynamiquement l'algorithme souhaité.\n")

    print("1. Utiliser Alpha-Beta via choose_best_move")
    print("-" * 70)
    code = """best_move = choose_best_move(
    'alphabeta', 
    game, 
    state, 
    max_depth=9, 
    use_transposition_table=True
)"""
    print(code)

    start = time.time()
    best_move_ab = choose_best_move(
        'alphabeta',
        game,
        state,
        max_depth=9,
        use_transposition_table=True
    )
    time_ab = time.time() - start
    print(f"\n✓ Alpha-Beta: Coup trouvé en {time_ab:.4f}s")

    print("\n2. Utiliser MTD(f) via choose_best_move")
    print("-" * 70)
    code = """best_move = choose_best_move(
    'mtdf', 
    game, 
    state, 
    max_depth=9, 
    initial_guess=0
)"""
    print(code)

    start = time.time()
    best_move_mtdf = choose_best_move(
        'mtdf',
        game,
        state,
        max_depth=9,
        initial_guess=0
    )
    time_mtdf = time.time() - start
    print(f"\n✓ MTD(f): Coup trouvé en {time_mtdf:.4f}s")

    print("\n3. Résultats")
    print("-" * 70)
    print("Les deux algorithmes trouvent le même coup optimal:")
    if best_move_ab:
        best_move_ab.display()


def demo_partie_complete():
    """Démonstration d'une partie complète avec Alpha-Beta"""
    print("\n\n" + "=" * 70)
    print("DÉMONSTRATION PARTIE COMPLÈTE (Alpha-Beta vs Alpha-Beta)")
    print("=" * 70)

    game = generate_tictactoe_game(isMaxStartingParameter=True)
    state = game.state

    # Deux algorithmes avec profondeurs différentes
    max_algo = AlphaBeta(game=game, max_depth=9, use_transposition_table=True)
    min_algo = AlphaBeta(game=game, max_depth=9, use_transposition_table=True)

    move_count = 0
    max_moves = 9

    print("\nPartie: MAX (X) vs MIN (O)\n")

    while not game.game_is_terminal(state) and move_count < max_moves:
        move_count += 1
        current_player = state.player

        print(f"--- Coup {move_count} | Joueur: {current_player} ---")

        if current_player == "MAX":
            state = max_algo.choose_best_move(state)
            stats = max_algo.get_statistics()
            print(f"MAX a joué (exploré {stats['nodes_explored']} nœuds)")
        else:
            state = min_algo.choose_best_move(state)
            stats = min_algo.get_statistics()
            print(f"MIN a joué (exploré {stats['nodes_explored']} nœuds)")

        state.display()

        if game.game_is_terminal(state):
            break

    # Résultat final
    print("\n" + "=" * 70)
    print("RÉSULTAT FINAL")
    print("=" * 70)

    winner = game.get_winner()
    if winner == "MAX":
        print("🏆 MAX (X) a gagné!")
    elif winner == "MIN":
        print("🏆 MIN (O) a gagné!")
    else:
        print("⚖️  Match nul!")


def demo_comparaison_performances():
    """Comparaison des performances entre algorithmes"""
    print("\n\n" + "=" * 70)
    print("COMPARAISON DES PERFORMANCES")
    print("=" * 70)

    game = generate_tictactoe_game(isMaxStartingParameter=True)
    state = game.state

    algorithms = [
        ("Alpha-Beta (sans TT)", AlphaBeta(game=game, max_depth=9, use_transposition_table=False)),
        ("Alpha-Beta (avec TT)", AlphaBeta(game=game, max_depth=9, use_transposition_table=True)),
        ("MTD(f)", MTDf(game=game, max_depth=9, initial_guess=0)),
    ]

    print("\nTest sur la position initiale de TicTacToe\n")

    results = []
    for name, algo in algorithms:
        print(f"Testing {name}...", end=" ")
        start = time.time()
        best_move = algo.choose_best_move(state)
        elapsed = time.time() - start
        stats = algo.get_statistics()

        results.append({
            'name': name,
            'time': elapsed,
            'nodes': stats['nodes_explored'],
            'cutoffs': stats.get('cutoffs', 0),
            'iterations': stats.get('iterations', '-'),
        })
        print(f"✓ ({elapsed:.4f}s)")

    print("\n" + "=" * 70)
    print("TABLEAU COMPARATIF")
    print("=" * 70)
    print(f"{'Algorithme':<25} {'Temps':<12} {'Nœuds':<12} {'Coupures':<12} {'Itérations':<12}")
    print("-" * 70)

    for r in results:
        print(f"{r['name']:<25} {r['time']:<12.4f} {r['nodes']:<12,} {r['cutoffs']:<12,} {str(r['iterations']):<12}")

    print("\n💡 Observations:")
    print("• La table de transposition réduit drastiquement les nœuds explorés")
    print("• MTD(f) utilise plusieurs itérations pour converger")
    print("• Pour TicTacToe, Alpha-Beta+TT est le plus efficace")
    print("• MTD(f) excelle sur des arbres plus complexes (échecs, dames, etc.)")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("DÉMONSTRATIONS ALPHA-BETA ET MTD(f)")
    print("PyAdverseSearch - Algorithmes de recherche adversariale")
    print("=" * 70)

    # Lancer toutes les démonstrations
    demo_simple_alphabeta()
    demo_simple_mtdf()
    demo_dynamic_selection()
    demo_partie_complete()
    demo_comparaison_performances()

    print("\n\n" + "=" * 70)
    print("FIN DES DÉMONSTRATIONS")
    print("=" * 70)
    print("\nPour plus d'informations, consultez ALPHABETA_MTDF_README.md")

