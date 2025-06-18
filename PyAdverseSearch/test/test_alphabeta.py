#python -m PyAdverseSearch.test.test_alphabeta

from .state_tictactoe import generate_tictactoe_game
from .state_connect4 import generate_connect4_game
from PyAdverseSearch.classes.alphabeta import AlphaBeta
import time

def test_alphabeta_vs_human_tictactoe():
    print("TESTING ALPHABETA WITH A HUMAN PLAYER AS MIN (TIC TAC TOE)")
    maxStarting = input("Would you like to start (y/n)? ")
    if maxStarting == 'y':
        maxStarting = False 
    elif maxStarting == 'n':
        maxStarting = True 
    else:
        print("Answer didn't match 'y' or 'n', program ended...")
        return

    game = generate_tictactoe_game(maxStarting)
    state = game.state
    print("Initial Board :")
    state.display()

    algorithm = AlphaBeta(game=game, max_depth=9)

    move_count = 10
    for i in range(move_count):
        current_player_is_max = (i % 2 == 0) if maxStarting else (i % 2 != 0)
        print(f"\n--- Move {i+1} | {'Max (AI)' if current_player_is_max else 'Your'} turn ---")

        if current_player_is_max:
            start = time.time()
            best_state = algorithm.choose_best_move(state)
            end = time.time()
            if best_state is None:
                print("No move found (final state or a mistake...).")
                break

            print("AI played in " + str(end - start) + "s.")
            best_state.display()
            state = best_state
        else:
            print("Here are all the possible moves you could do :")
            possible_moves = state._generate_successors()
            for j in range(len(possible_moves)):
                print(f"Option {j + 1}:")
                possible_moves[j].display()
            while True:
                user_input = input(f"Which one do you wish to do? (number between 1 and {len(possible_moves)}): ")

                try:
                    choice = int(user_input)
                    if 1 <= choice <= len(possible_moves):
                        state = possible_moves[choice - 1]
                        state.display()
                        break
                    else:
                        print(f"Invalid input! Please enter a number between 1 and {len(possible_moves)}.")
                except ValueError:
                    print("Invalid input! Please enter a numeric value.")

        if state._is_terminal():
            print("Final state reached.")
            winner = game.winner_function(state)
            if not winner:
                print("It's a draw!")
            else:
                print(f"Winner is: {winner}")
            break


"""

CONNECT 4

"""
def test_alphabeta_vs_human_connect4():
    print("TESTING ALPHABETA AGAINST HUMAN PLAYER (CONNECT 4)")
    maxStarting = input("Would you like to start (y/n)? ")
    if maxStarting == 'y':
        maxStarting = False
    elif maxStarting == 'n':
        maxStarting = True 
    else:
        print("Answer didn't match 'y' or 'n', program ended...")
        return

    game = generate_connect4_game(maxStarting)
    state = game.state
    print("Initial Board :")
    state.display()

    algorithm = AlphaBeta(game=game, max_depth=10)

    move_count = 43
    for i in range(move_count):
        current_player_is_max = (i % 2 == 0) if maxStarting else (i % 2 != 0)
        print(f"\n--- Move {i+1} | {'Max (AI)' if current_player_is_max else 'Your'} turn ---")

        if current_player_is_max:
            start = time.time()
            best_state = algorithm.choose_best_move(state)
            end = time.time()

            if best_state is None:
                print("No move found (final state or a mistake...).")
                break

            print(f"AI played in {end - start:.3f} seconds.")
            best_state.display()
            state = best_state
        else:
            print("Here are all the possible moves you could do :")
            possible_moves = state._generate_successors()
            for j in range(len(possible_moves)):
                print(f"Option {j + 1}:")
                possible_moves[j].display()

            while True:
                user_input = input(f"Which one do you wish to do? (number between 1 and {len(possible_moves)}): ")

                try:
                    choice = int(user_input)
                    if 1 <= choice <= len(possible_moves):
                        state = possible_moves[choice - 1]
                        state.display()
                        break
                    else:
                        print(f"Invalid input! Please enter a number between 1 and {len(possible_moves)}.")
                except ValueError:
                    print("Invalid input! Please enter a numeric value.")

        if state._is_terminal():
            print("Final state reached.")
            winner = game.winner_function(state)
            if not winner:
                print("It's a draw!")
            else:
                print(f"Winner is: {winner}")
            break


if __name__ == "__main__":
    game = input("TicTacToe or Connect 4 ? (t or c) : ")
    if game == "t" : test_alphabeta_vs_human_tictactoe()
    elif game == "c" : test_alphabeta_vs_human_connect4()
    else : print("No game choosen.")
