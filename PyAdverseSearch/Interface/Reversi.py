import arcade
import time
import tkinter as tk

from PyAdverseSearch.classes.state import State
from PyAdverseSearch.classes.game import Game
from PyAdverseSearch.classes.minimax import Minimax

SIZE = 8
CELL = 60
WIDTH = SIZE * CELL
HEIGHT = SIZE * CELL
UI_HEIGHT = 80
MARGIN = 2

EMPTY = 0
BLACK = 1
WHITE = -1

class ReversiState(State):
    SIZE = 8

    DIRECTIONS = [
        (-1,-1), (-1,0), (-1,1),
        (0,-1),           (0,1),
        (1,-1),  (1,0),   (1,1)
    ]

    def __init__(self, board=None, player='MAX', parent=None, game=None):
        if board is None:
            board = [[' ' for _ in range(self.SIZE)] for _ in range(self.SIZE)]
            # Position initiale officielle
            board[3][3] = 'W'
            board[3][4] = 'B'
            board[4][3] = 'B'
            board[4][4] = 'W'

        super().__init__(board, player, parent)

        self.board = board
        self.player = player
        self.parent = parent
        self.game = game

    def get_possible_moves(self):
        moves = possible_actions(self)

        # Gestion automatique du PASS
        if not moves:
            return [None]  # None = PASS

        return moves

    def _apply_action(self, action):

        if action is None:
            next_player = 'MIN' if self.player == 'MAX' else 'MAX'
            return ReversiState(
                [r[:] for r in self.board],
                next_player,
                parent=self,
                game=self.game
            )
        
        row, col = action
        new_board = [r[:] for r in self.board]

        player_piece = 'B' if self.player == 'MAX' else 'W'
        opponent = 'W' if self.player == 'MAX' else 'B'

        new_board[row][col] = player_piece

        # Retourner les pions capturés
        for dr, dc in self.DIRECTIONS:
            r, c = row + dr, col + dc
            pieces_to_flip = []

            while 0 <= r < self.SIZE and 0 <= c < self.SIZE:
                if new_board[r][c] == opponent:
                    pieces_to_flip.append((r, c))
                elif new_board[r][c] == player_piece:
                    for rr, cc in pieces_to_flip:
                        new_board[rr][cc] = player_piece
                    break
                else:
                    break

                r += dr
                c += dc

        next_player = 'MIN' if self.player == 'MAX' else 'MAX'
        return ReversiState(new_board, next_player, parent=self, game=self.game)

    def is_game_over(self):
        return is_terminal(self)

    def get_utility(self):
        return utility(self)

    def get_winner(self):
        return winner_function(self)

    def evaluate(self):
        return heuristic(self)

def possible_actions(state):
    moves = []

    for i in range(8):
        for j in range(8):
            if state.board[i][j] == ' ' and is_valid_move(state, i, j):
                moves.append((i, j))

    return moves


def is_valid_move(state, row, col):
    opponent = 'W' if state.player == 'MAX' else 'B'
    player_piece = 'B' if state.player == 'MAX' else 'W'

    for dr, dc in ReversiState.DIRECTIONS:
        r, c = row + dr, col + dc
        found_opponent = False

        while 0 <= r < 8 and 0 <= c < 8:
            if state.board[r][c] == opponent:
                found_opponent = True
            elif state.board[r][c] == player_piece:
                if found_opponent:
                    return True
                break
            else:
                break

            r += dr
            c += dc

    return False


def is_terminal(state):
    # Si joueur courant a des coups → pas terminal
    if possible_actions(state):
        return False

    # Tester adversaire
    other_player = 'MIN' if state.player == 'MAX' else 'MAX'
    temp_state = ReversiState(state.board, other_player, game=state.game)  # <-- passer le game

    if possible_actions(temp_state):
        return False

    return True


def utility(state):
    flat = [cell for row in state.board for cell in row]
    b_count = flat.count('B')
    w_count = flat.count('W')

    if b_count > w_count:
        return 1000
    elif w_count > b_count:
        return -1000
    return 0


def winner_function(state):
    flat = [cell for row in state.board for cell in row]
    b_count = flat.count('B')
    w_count = flat.count('W')

    if b_count > w_count:
        return 'MAX'
    elif w_count > b_count:
        return 'MIN'
    return None


def heuristic(state):

    flat = [cell for row in state.board for cell in row]
    b_count = flat.count('B')
    w_count = flat.count('W')

    piece_diff = b_count - w_count

    # Coins = ultra importants
    corners = [(0,0),(0,7),(7,0),(7,7)]
    corner_score = 0

    for r, c in corners:
        if state.board[r][c] == 'B':
            corner_score += 10
        elif state.board[r][c] == 'W':
            corner_score -= 10

    # Mobilité
    mobility = len(possible_actions(state))

    return piece_diff + corner_score + 0.2 * mobility

def generate_reversi_game(isMaxStartingParameter=True):

    initial_state = ReversiState()

    game = Game(
        initial_state=initial_state,
        possible_actions=possible_actions,
        is_terminal=is_terminal,
        winner_function=winner_function,
        utility=utility,
        heuristic=heuristic,
        isMaxStarting=isMaxStartingParameter
    )

    initial_state.game = game

    return game

class ReversiWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Reversi - IA")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT + UI_HEIGHT, bg="darkgreen")
        self.canvas.pack()

        self.game = generate_reversi_game()
        self.state = self.game.state
        self.minimax = Minimax(self.game, max_depth=3)

        self.human_player = 'MAX'
        self.ai_player = 'MIN'

        # Boutons
        self.restart_btn = tk.Button(root, text="Rejouer", command=self.restart_game)
        self.quit_btn = tk.Button(root, text="Quitter", command=root.quit)

        self.restart_btn.pack(side="left", padx=20, pady=10)
        self.quit_btn.pack(side="right", padx=20, pady=10)

        # Clic souris
        self.canvas.bind("<Button-1>", self.on_mouse_press)

        self.draw()

    def draw(self):
        self.canvas.delete("all")

        # Plateau
        for r in range(SIZE):
            for c in range(SIZE):
                x1 = c * CELL
                y1 = r * CELL
                x2 = x1 + CELL
                y2 = y1 + CELL

                self.canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="black")

                cell = self.state.board[r][c]

                if cell == 'B':
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="black")
                elif cell == 'W':
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="white")

        # Coups possibles
        if self.state.player == self.human_player:
            for move in self.state.get_possible_moves():
                if move:
                    r, c = move
                    x = c * CELL + CELL//2
                    y = r * CELL + CELL//2
                    self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="gray")

        # Fin de partie
        if self.state.is_game_over():
            winner = self.state.get_winner()

            if winner == 'MAX':
                text = "NOIR GAGNE"
            elif winner == 'MIN':
                text = "BLANC GAGNE"
            else:
                text = "MATCH NUL"

            self.canvas.create_text(WIDTH//2, HEIGHT//2, text=text, fill="white", font=("Arial", 20))

    def on_mouse_press(self, event):
        if self.state.is_game_over():
            return

        if self.state.player == self.human_player:
            c = event.x // CELL
            r = event.y // CELL

            for move in self.state.get_possible_moves():
                if move and move == (r, c):
                    self.state = self.state._apply_action(move)

                    self.draw()
                    self.root.after(3000, self.play_turn)

                    return

    def play_turn(self):
        if self.state.is_game_over():
            self.draw()
            return

        moves = self.state.get_possible_moves()

        # PASS automatique
        if moves == [None]:
            self.state = self.state._apply_action(None)
            self.draw()
            self.root.after(3000, self.play_turn)
            return

        # Tour IA
        if self.state.player == self.ai_player:
            best_state = self.minimax.choose_best_move(self.state)

            if best_state is None:
                self.state = self.state._apply_action(None)
            else:
                self.state = best_state

            self.draw()

            self.root.after(3000, self.play_turn)
            return

        # Tour humain → on attend
        self.draw()

    def restart_game(self):
        self.game = generate_reversi_game()
        self.state = self.game.state
        self.minimax = Minimax(self.game, max_depth=3)
        self.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = ReversiWindow(root)
    root.mainloop()

"""
"Version Arcade (interface graphique plus avancée) - nécessite la bibliothèque 'arcade' installée"
class ReversiWindow(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT + UI_HEIGHT, "Reversi - IA")
        self.game = generate_reversi_game()
        self.state = self.game.state
        self.minimax = Minimax(self.game, max_depth=3)
        self.game_over = False
        self.winner = None
        self.human_player = 'MAX'     # MAX = Noir
        self.ai_player = 'MIN'        # MIN = Blanc
        self.button_width = 150
        self.button_height = 40

        self.button_width = 150
        self.button_height = 40

        # Bouton Rejouer
        self.restart_button = {
            "left": 40,
            "right": 40 + self.button_width,
            "bottom": HEIGHT + 20,
            "top": HEIGHT + 20 + self.button_height
        }

        # Bouton Quitter
        self.quit_button = {
            "left": WIDTH - 40 - self.button_width,
            "right": WIDTH - 40,
            "bottom": HEIGHT + 20,
            "top": HEIGHT + 20 + self.button_height
        }

    def on_draw(self):
        self.clear()
        arcade.draw_lrbt_rectangle_filled(
            0, WIDTH,
            HEIGHT, HEIGHT + UI_HEIGHT,
            arcade.color.DARK_GRAY
        )
        arcade.set_background_color(arcade.color.DARK_GREEN)

        for r in range(SIZE):
            for c in range(SIZE):

                x = c * CELL + CELL // 2
                y = (SIZE - 1 - r) * CELL + CELL // 2

                left = x - CELL // 2 + MARGIN
                right = x + CELL // 2 - MARGIN
                bottom = y - CELL // 2 + MARGIN
                top = y + CELL // 2 - MARGIN

                arcade.draw_lrbt_rectangle_filled(
                    left, right, bottom, top, arcade.color.GREEN
                )
                arcade.draw_lrbt_rectangle_outline(
                    left, right, bottom, top, arcade.color.BLACK
                )

                # Affichage des pions
                if self.state.board[r][c] == 'B':
                    arcade.draw_circle_filled(x, y, CELL//2 - 5, arcade.color.BLACK)
                elif self.state.board[r][c] == 'W':
                    arcade.draw_circle_filled(x, y, CELL//2 - 5, arcade.color.WHITE)

        # Affichage coups valides pour humain
        if self.state.player == self.human_player:
            moves = self.state.get_possible_moves()
            for move in moves:
                if move is not None:
                    r, c = move
                    x = c * CELL + CELL // 2
                    y = (SIZE - 1 - r) * CELL + CELL // 2
                    arcade.draw_circle_filled(x, y, 5, arcade.color.GRAY)
        # Bouton Rejouer
        arcade.draw_lrbt_rectangle_filled(
            self.restart_button["left"],
            self.restart_button["right"],
            self.restart_button["bottom"],
            self.restart_button["top"],
            arcade.color.BLUE
        )
        arcade.draw_text(
            "Rejouer",
            self.restart_button["left"] + 30,
            self.restart_button["bottom"] + 10,
            arcade.color.WHITE,
            14
        )

        # Bouton Quitter
        arcade.draw_lrbt_rectangle_filled(
            self.quit_button["left"],
            self.quit_button["right"],
            self.quit_button["bottom"],
            self.quit_button["top"],
            arcade.color.RED
        )
        arcade.draw_text(
            "Quitter",
            self.quit_button["left"] + 35,
            self.quit_button["bottom"] + 10,
            arcade.color.WHITE,
            14
        )
        if self.state.is_game_over():
            winner = self.state.get_winner()

            if winner == 'MAX':
                message = "NOIR (MAX) GAGNE !"
            elif winner == 'MIN':
                message = "BLANC (MIN) GAGNE !"
            else:
                message = "MATCH NUL !"

            arcade.draw_text(
                message,
                WIDTH // 2,
                HEIGHT // 2,
                arcade.color.ASH_GREY,
                28,
                anchor_x="center"
            )

    def on_mouse_press(self, x, y, button, modifiers):
        # Boutons UI : Rejouer / Quitter
        if (self.restart_button["left"] <= x <= self.restart_button["right"] and
            self.restart_button["bottom"] <= y <= self.restart_button["top"]):
            self.game = generate_reversi_game()
            self.state = self.game.state
            self.minimax = Minimax(self.game, max_depth=3)
            return

        if (self.quit_button["left"] <= x <= self.quit_button["right"] and
            self.quit_button["bottom"] <= y <= self.quit_button["top"]):
            arcade.close_window()
            return

        # Ignorer clics sur le plateau si partie terminée
        if self.state.is_game_over() and y < HEIGHT:
            return

        # Si c’est le tour du joueur humain
        if self.state.player == self.human_player:
            r = int(SIZE - 1 - (y // CELL))
            c = int(x // CELL)
            possible_moves = self.state.get_possible_moves()
            for move in possible_moves:
                if move is not None and move == (r, c):
                    self.state = self.state._apply_action(move)
                    self.play_turn()  # lancer la boucle automatique après coup humain
                    return

    def play_turn(self):
        while not self.state.is_game_over():
            possible_moves = self.state.get_possible_moves()

            # PASS automatique si aucun coup
            if possible_moves == [None]:
                self.state = self.state._apply_action(None)
                self.on_draw()
                # changer de joueur, continuer la boucle
                continue

            # Tour de l'IA
            if self.state.player == self.ai_player:
                best_state = self.minimax.choose_best_move(self.state)
                if best_state is None:
                    self.state = self.state._apply_action(None)
                else:
                    self.state = best_state

                self.on_draw()
                # continuer la boucle si l'humain n'a aucun coup
                continue

            # Si c’est le joueur humain et qu’il a au moins un coup → attendre clic
            break
        
if __name__ == "__main__":
    window = ReversiWindow()
    arcade.run()
"""


"""
# --- Version Console (sans interface graphique) ---
def print_board(state):
    board = state.board
    moves = state.get_possible_moves()

    # Transformer la liste des coups en set de coordonnées (i, j)
    move_positions = set()
    if moves and moves != [None]:
        for move in moves:
            move_positions.add(move)

    print("\n    0   1   2   3   4   5   6   7")
    print("  +---+---+---+---+---+---+---+---+")

    for i in range(8):
        row_str = f"{i} |"
        for j in range(8):
            cell = board[i][j]

            if cell != ' ':
                row_str += f" {cell} |"
            elif (i, j) in move_positions:
                row_str += " . |"  # <-- coup possible
            else:
                row_str += "   |"

        print(row_str)
        print("  +---+---+---+---+---+---+---+---+")

    b_count = sum(row.count('B') for row in board)
    w_count = sum(row.count('W') for row in board)

    print(f"\nScore -> B (MAX): {b_count} | W (MIN): {w_count}")
    print(f"Tour actuel : {'B (MAX)' if state.player == 'MAX' else 'W (MIN)'}")

def print_possible_moves(state):
    moves = possible_actions(state)

    if not moves:
        print("Aucun coup possible -> PASS")
        return

    print("Coups possibles :")
    for idx, move in enumerate(moves):
        print(f"{idx} : {move}")

def play_console():

    game = generate_reversi_game()
    state = ReversiState(game=game)

    while not state.is_game_over():

        print_board(state)
        moves = state.get_possible_moves()

        # Gestion du PASS
        if moves == [None]:
            print("PASS automatique")
            state = state._apply_action(None)
            continue

        print_possible_moves(state)

        choice = input("Choisissez le numéro du coup : ")

        try:
            move_index = int(choice)
            move = moves[move_index]
        except:
            print("Entrée invalide.")
            continue

        state = state._apply_action(move)

    # Fin de partie
    print_board(state)
    winner = state.get_winner()

    if winner == 'MAX':
        print("B (MAX) gagne")
    elif winner == 'MIN':
        print("W (MIN) gagne")
    else:
        print("Match nul")

if __name__ == "__main__":
    play_console()
"""
