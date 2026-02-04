import time
from PyAdverseSearch.test.state_tictactoe import generate_tictactoe_game
from PyAdverseSearch.classes.montecarlo import MonteCarlo
from PyAdverseSearch.classes.algorithm import choose_best_move

# # Génère une partie de Tic-Tac-Toe
# game = generate_tictactoe_game()
# state = game.state
#
# # On suppose que le joueur qui commence est le joueur MAX
# max_player = state.player
#
# # Boucle de jeu
# while not game.is_terminal(state):
#     print("\nÉtat actuel :")
#     state.display()
#
#     best = choose_best_move('montecarlo', game, state, max_iterations=2000)
#     print("\nCoup joué :")
#     best.display()
#
#     state = best
#
# # État final
# print("\nPartie terminée. Résultat final :")
# print("Valeur retournée par utility(state) :", game.utility(state))
# state.display()
#
# # Déterminer le résultat via game.utility (qui retourne 1, 0, ou -1)
# result = game.utility(state)
# if result == 1000:
#     print("Joueur MAX (X) gagne.")
# elif result == -1000:
#     print("Joueur MIN (O) gagne.")
# else:
#     print("Match nul.")


def test_montecarlo_vs_human_tictactoe():
    print("=== TESTING MONTE CARLO (MCTS) AGAINST HUMAN PLAYER (TIC TAC TOE) ===")

    # 1. Configuration du jeu
    maxStarting = input("Would you like to start (y/n)? ")
    if maxStarting == 'y':
        maxStarting = False  # Human is MIN (plays first)
    elif maxStarting == 'n':
        maxStarting = True  # AI is MAX (plays first)
    else:
        print("Invalid input, defaulting to AI starts.")
        maxStarting = True

    game = generate_tictactoe_game(maxStarting)
    state = game.state
    print("Initial Board :")
    state.display()

    # 2. Initialisation de l'IA
    # Pour le Morpion, 1000 à 5000 itérations suffisent largement pour être invincible.
    # On instancie la classe directement comme pour Minimax.
    algorithm = MonteCarlo(game=game, max_iterations=5000)

    move_count = 10
    for i in range(move_count):
        # Détermine à qui le tour
        current_player_is_max = (i % 2 == 0) if maxStarting else (i % 2 != 0)
        player_name = "Max (MCTS AI)" if current_player_is_max else "Your"

        print(f"\n--- Move {i + 1} | {player_name} turn ---")

        if current_player_is_max:
            # --- TOUR DE L'IA (MCTS) ---
            print("MCTS is thinking...")
            start = time.time()

            # C'est ici que la magie opère : MCTS lance ses milliers de simulations
            best_state = algorithm.choose_best_move(state)

            end = time.time()

            if best_state is None:
                print("No move found (bug or end of game).")
                break

            print(f"AI played in {end - start:.3f} seconds.")
            best_state.display()
            state = best_state

        else:
            # --- TOUR DE L'HUMAIN ---
            print("Here are all the possible moves you could do :")
            possible_moves = state._generate_successors()

            # Affiche les options
            for j in range(len(possible_moves)):
                print(f"Option {j + 1}:")
                possible_moves[j].display()

            # Boucle de validation de l'entrée utilisateur
            while True:
                user_input = input(f"Which one do you wish to do? (1-{len(possible_moves)}): ")
                try:
                    choice = int(user_input)
                    if 1 <= choice <= len(possible_moves):
                        state = possible_moves[choice - 1]
                        state.display()
                        break
                    else:
                        print(f"Invalid choice. 1 to {len(possible_moves)} please.")
                except ValueError:
                    print("Please enter a number.")

        # 3. Vérification de fin de partie
        if state._is_terminal():
            print("\n--- GAME OVER ---")
            winner = game.winner_function(state)
            if not winner:
                print("It's a draw!")
            elif winner == "MAX":
                print("MCTS AI (MAX) wins! (Comme prévu...)")
            else:
                print("You (MIN) win! (Bravo, c'est rare contre MCTS)")
            break


if __name__ == "__main__":
    test_montecarlo_vs_human_tictactoe()