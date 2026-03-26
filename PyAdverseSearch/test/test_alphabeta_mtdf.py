# FILE: PyAdverseSearch/test/test_alphabeta_mtdf.py
# python -m PyAdverseSearch.test.test_alphabeta_mtdf

"""
Test et comparaison des algorithmes Alpha-Beta et MTD(f)
"""

from .state_tictactoe import generate_tictactoe_game
from PyAdverseSearch.classes.alphabeta import AlphaBeta
from PyAdverseSearch.classes.mtdf import MTDf
import time


def test_alphabeta_basic():
    """Test basique d'Alpha-Beta sur TicTacToe"""
    print("=" * 60)
    print("TEST ALPHA-BETA - TIC TAC TOE")
    print("=" * 60)

    game = generate_tictactoe_game(isMaxStartingParameter=True)
    state = game.state

    print("\nÉtat initial :")
    state.display()

    # Test avec Alpha-Beta standard
    print("\n--- Alpha-Beta sans table de transposition ---")
    algorithm = AlphaBeta(game=game, max_depth=9, use_transposition_table=False)

    start = time.time()
    best_state = algorithm.choose_best_move(state)
    end = time.time()

    print(f"Temps de recherche : {end - start:.4f}s")
    stats = algorithm.get_statistics()
    print(f"Nœuds explorés : {stats['nodes_explored']}")
    print(f"Coupures (cutoffs) : {stats['cutoffs']}")
    print("\nMeilleur coup trouvé :")
    if best_state:
        best_state.display()

    # Test avec table de transposition
    print("\n--- Alpha-Beta avec table de transposition ---")
    algorithm_tt = AlphaBeta(game=game, max_depth=9, use_transposition_table=True)

    start = time.time()
    best_state_tt = algorithm_tt.choose_best_move(state)
    end = time.time()

    print(f"Temps de recherche : {end - start:.4f}s")
    stats_tt = algorithm_tt.get_statistics()
    print(f"Nœuds explorés : {stats_tt['nodes_explored']}")
    print(f"Coupures (cutoffs) : {stats_tt['cutoffs']}")
    print(f"Taille table de transposition : {stats_tt['transposition_table_size']}")
    print("\nMeilleur coup trouvé :")
    if best_state_tt:
        best_state_tt.display()


def test_mtdf_basic():
    """Test basique de MTD(f) sur TicTacToe"""
    print("\n" + "=" * 60)
    print("TEST MTD(f) - TIC TAC TOE")
    print("=" * 60)

    game = generate_tictactoe_game(isMaxStartingParameter=True)
    state = game.state

    print("\nÉtat initial :")
    state.display()

    print("\n--- MTD(f) ---")
    algorithm = MTDf(game=game, max_depth=9, initial_guess=0)

    start = time.time()
    best_state = algorithm.choose_best_move(state)
    end = time.time()

    print(f"Temps de recherche : {end - start:.4f}s")
    stats = algorithm.get_statistics()
    print(f"Nœuds explorés : {stats['nodes_explored']}")
    print(f"Coupures (cutoffs) : {stats['cutoffs']}")
    print(f"Itérations MTD(f) : {stats['iterations']}")
    print(f"Taille table de transposition : {stats['transposition_table_size']}")
    print("\nMeilleur coup trouvé :")
    if best_state:
        best_state.display()


def test_comparison():
    """Compare Alpha-Beta et MTD(f) sur plusieurs positions"""
    print("\n" + "=" * 60)
    print("COMPARAISON ALPHA-BETA vs MTD(f)")
    print("=" * 60)

    game = generate_tictactoe_game(isMaxStartingParameter=True)
    state = game.state

    print("\nÉtat initial :")
    state.display()

    # Alpha-Beta avec TT
    print("\n--- Alpha-Beta (avec table de transposition) ---")
    ab_algo = AlphaBeta(game=game, max_depth=9, use_transposition_table=True)
    ab_start = time.time()
    ab_best = ab_algo.choose_best_move(state)
    ab_time = time.time() - ab_start
    ab_stats = ab_algo.get_statistics()

    # MTD(f)
    print("\n--- MTD(f) ---")
    mtdf_algo = MTDf(game=game, max_depth=9, initial_guess=0)
    mtdf_start = time.time()
    mtdf_best = mtdf_algo.choose_best_move(state)
    mtdf_time = time.time() - mtdf_start
    mtdf_stats = mtdf_algo.get_statistics()

    # Affichage des résultats
    print("\n" + "=" * 60)
    print("RÉSULTATS DE LA COMPARAISON")
    print("=" * 60)

    print(f"\nAlpha-Beta :")
    print(f"  Temps         : {ab_time:.4f}s")
    print(f"  Nœuds explorés: {ab_stats['nodes_explored']}")
    print(f"  Coupures      : {ab_stats['cutoffs']}")
    print(f"  Table de transposition: {ab_stats['transposition_table_size']} entrées")

    print(f"\nMTD(f) :")
    print(f"  Temps         : {mtdf_time:.4f}s")
    print(f"  Nœuds explorés: {mtdf_stats['nodes_explored']}")
    print(f"  Coupures      : {mtdf_stats['cutoffs']}")
    print(f"  Itérations    : {mtdf_stats['iterations']}")
    print(f"  Table de transposition: {mtdf_stats['transposition_table_size']} entrées")

    print(f"\nGain de performance :")
    if ab_stats['nodes_explored'] > 0:
        node_reduction = (1 - mtdf_stats['nodes_explored'] / ab_stats['nodes_explored']) * 100
        print(f"  Réduction nœuds: {node_reduction:+.1f}%")
    if ab_time > 0:
        time_reduction = (1 - mtdf_time / ab_time) * 100
        print(f"  Réduction temps: {time_reduction:+.1f}%")

    print("\nMeilleur coup Alpha-Beta :")
    if ab_best:
        ab_best.display()

    print("Meilleur coup MTD(f) :")
    if mtdf_best:
        mtdf_best.display()


def test_alphabeta_vs_human():
    """Jouer contre Alpha-Beta"""
    print("\n" + "=" * 60)
    print("JOUER CONTRE ALPHA-BETA")
    print("=" * 60)

    max_starting = input("\nVoulez-vous commencer (y/n) ? ")
    if max_starting == 'y':
        max_starting = False
    elif max_starting == 'n':
        max_starting = True
    else:
        print("Réponse invalide, programme terminé...")
        return

    game = generate_tictactoe_game(max_starting)
    state = game.state
    print("\nPlateau initial :")
    state.display()

    algorithm = AlphaBeta(game=game, max_depth=9, use_transposition_table=True)

    move_count = 10
    for i in range(move_count):
        current_player_is_max = (i % 2 == 0) if max_starting else (i % 2 != 0)
        print(f"\n--- Coup {i+1} | Tour de {'MAX (IA)' if current_player_is_max else 'MIN (Vous)'} ---")

        if current_player_is_max:
            start = time.time()
            best_state = algorithm.choose_best_move(state)
            end = time.time()

            if best_state is None:
                print("Pas de coup trouvé (état terminal).")
                break

            stats = algorithm.get_statistics()
            print(f"L'IA a joué en {end - start:.4f}s")
            print(f"Nœuds explorés: {stats['nodes_explored']}, Coupures: {stats['cutoffs']}")
            best_state.display()
            state = best_state
        else:
            print("Voici tous les coups possibles :")
            possible_moves = state._generate_successors()
            for j in range(len(possible_moves)):
                print(f"Option {j + 1}:")
                possible_moves[j].display()

            while True:
                user_input = input(f"Quel coup choisissez-vous ? (1-{len(possible_moves)}): ")
                try:
                    choice = int(user_input) - 1
                    if 0 <= choice < len(possible_moves):
                        state = possible_moves[choice]
                        break
                    else:
                        print(f"Choisissez un nombre entre 1 et {len(possible_moves)}")
                except ValueError:
                    print("Entrée invalide")

        # Vérifier si le jeu est terminé
        if game.game_is_terminal(state):
            print("\n" + "=" * 60)
            print("JEU TERMINÉ")
            print("=" * 60)
            state.display()
            winner = game.get_winner()
            if winner == "MAX":
                print("L'IA (MAX) a gagné !")
            elif winner == "MIN":
                print("Vous (MIN) avez gagné !")
            else:
                print("Match nul !")
            break


def test_mtdf_vs_human():
    """Jouer contre MTD(f)"""
    print("\n" + "=" * 60)
    print("JOUER CONTRE MTD(f)")
    print("=" * 60)

    max_starting = input("\nVoulez-vous commencer (y/n) ? ")
    if max_starting == 'y':
        max_starting = False
    elif max_starting == 'n':
        max_starting = True
    else:
        print("Réponse invalide, programme terminé...")
        return

    game = generate_tictactoe_game(max_starting)
    state = game.state
    print("\nPlateau initial :")
    state.display()

    algorithm = MTDf(game=game, max_depth=9, initial_guess=0)

    move_count = 10
    for i in range(move_count):
        current_player_is_max = (i % 2 == 0) if max_starting else (i % 2 != 0)
        print(f"\n--- Coup {i+1} | Tour de {'MAX (IA)' if current_player_is_max else 'MIN (Vous)'} ---")

        if current_player_is_max:
            start = time.time()
            best_state = algorithm.choose_best_move(state)
            end = time.time()

            if best_state is None:
                print("Pas de coup trouvé (état terminal).")
                break

            stats = algorithm.get_statistics()
            print(f"L'IA a joué en {end - start:.4f}s")
            print(f"Nœuds: {stats['nodes_explored']}, Itérations: {stats['iterations']}")
            best_state.display()
            state = best_state
        else:
            print("Voici tous les coups possibles :")
            possible_moves = state._generate_successors()
            for j in range(len(possible_moves)):
                print(f"Option {j + 1}:")
                possible_moves[j].display()

            while True:
                user_input = input(f"Quel coup choisissez-vous ? (1-{len(possible_moves)}): ")
                try:
                    choice = int(user_input) - 1
                    if 0 <= choice < len(possible_moves):
                        state = possible_moves[choice]
                        break
                    else:
                        print(f"Choisissez un nombre entre 1 et {len(possible_moves)}")
                except ValueError:
                    print("Entrée invalide")

        # Vérifier si le jeu est terminé
        if game.game_is_terminal(state):
            print("\n" + "=" * 60)
            print("JEU TERMINÉ")
            print("=" * 60)
            state.display()
            winner = game.get_winner()
            if winner == "MAX":
                print("L'IA (MAX) a gagné !")
            elif winner == "MIN":
                print("Vous (MIN) avez gagné !")
            else:
                print("Match nul !")
            break


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("TESTS ALPHA-BETA ET MTD(f)")
    print("=" * 60)

    # Tests automatiques
    test_alphabeta_basic()
    test_mtdf_basic()
    test_comparison()

    # Test interactif (décommenter pour jouer)
    # test_alphabeta_vs_human()
    # test_mtdf_vs_human()




