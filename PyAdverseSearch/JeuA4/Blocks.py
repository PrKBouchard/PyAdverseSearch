import tkinter as tk

from PyAdverseSearch.classes.state import State
from PyAdverseSearch.classes.game import Game

from maxn import choose_move_maxn


SIZE = 12
CELL = 50
WIDTH = SIZE * CELL
HEIGHT = SIZE * CELL

PLAYERS = ['BLEU', 'ROUGE', 'JAUNE', 'VIOLET']

COLORS = {
    'BLEU': 'blue',
    'ROUGE': 'red',
    'JAUNE': 'yellow',
    'VIOLET': 'purple'
}

DIRECTIONS = [(-1,0),(1,0),(0,-1),(0,1)]


class TerritoryState(State):
    def __init__(self, board=None, player='BLEU', parent=None, game=None):
        if board is None:
            board = [[' ' for _ in range(SIZE)] for _ in range(SIZE)]
            board[0][0] = 'BLEU'
            board[0][SIZE-1] = 'ROUGE'
            board[SIZE-1][0] = 'JAUNE'
            board[SIZE-1][SIZE-1] = 'VIOLET'

        super().__init__(board, player, parent)

        self.board = board
        self.player = player
        self.parent = parent
        self.game = game

    def inside(self, r, c):
        return 0 <= r < SIZE and 0 <= c < SIZE

    def is_adjacent(self, r, c, player):
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if self.inside(nr, nc) and self.board[nr][nc] == player:
                return True
        return False

    def get_possible_moves(self):
        moves = []
        for r in range(SIZE):
            for c in range(SIZE):
                if self.board[r][c] == ' ' and self.is_adjacent(r, c, self.player):
                    moves.append((r, c))
        return moves if moves else [None]

    def _apply_action(self, move):
        new_board = [row[:] for row in self.board]

        if move:
            r, c = move
            new_board[r][c] = self.player

        next_idx = (PLAYERS.index(self.player) + 1) % len(PLAYERS)
        next_player = PLAYERS[next_idx]

        return TerritoryState(new_board, next_player, parent=self, game=self.game)

    def is_game_over(self):
        for p in PLAYERS:
            temp = TerritoryState(self.board, p)
            if temp.get_possible_moves() != [None]:
                return False
        return True

    def get_scores(self):
        scores = {p: 0 for p in PLAYERS}
        for row in self.board:
            for cell in row:
                if cell in scores:
                    scores[cell] += 1
        return scores


def heuristic_scores(state):
    raw_scores = state.get_scores()
    scores = [raw_scores[p] for p in PLAYERS]

    size = len(state.board)
    center = size // 2

    for i, p in enumerate(PLAYERS):
        temp = TerritoryState(state.board, p)
        mobility = len([m for m in temp.get_possible_moves() if m])
        scores[i] += 2 * mobility

    for r in range(size):
        for c in range(size):
            cell = state.board[r][c]
            if cell in PLAYERS:
                i = PLAYERS.index(cell)
                dist = abs(r - center) + abs(c - center)
                scores[i] += max(0, 6 - dist)

    for r in range(size):
        for c in range(size):
            cell = state.board[r][c]
            if cell in PLAYERS:
                i = PLAYERS.index(cell)
                adj = 0
                for dr, dc in DIRECTIONS:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < size and 0 <= nc < size:
                        if state.board[nr][nc] == cell:
                            adj += 1
                if adj == 0:
                    scores[i] -= 3

    return scores


def generate_territory_game():
    initial_state = TerritoryState()

    game = Game(
        initial_state=initial_state,
        possible_actions=lambda s: s.get_possible_moves(),
        is_terminal=lambda s: s.is_game_over(),
        winner_function=lambda s: max(s.get_scores(), key=s.get_scores().get),
        utility=lambda s: max(s.get_scores().values()),
        heuristic=heuristic_scores,
        isMaxStarting=True
    )

    initial_state.game = game
    return game


class TerritoryWindow:
    def __init__(self, root, human_players):
        self.root = root

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack()

        self.bottom = tk.Frame(root)
        self.bottom.pack(fill="x", pady=10)

        tk.Button(self.bottom, text="Rejouer", command=self.back_to_menu).pack(side="left", padx=20)

        self.score_label = tk.Label(self.bottom, font=("Arial", 14))
        self.score_label.pack(side="left", expand=True)

        tk.Button(self.bottom, text="Quitter", command=root.quit).pack(side="right", padx=20)

        self.human_players = human_players
        self.cache = {}

        self.restart()

        self.canvas.bind("<Button-1>", self.click)

        self.loop()

    def restart(self):
        self.game = generate_territory_game()
        self.state = self.game.state
        self.cache = {}
        self.draw()

    def draw(self):
        self.canvas.delete("all")

        for r in range(SIZE):
            for c in range(SIZE):
                x1 = c * CELL
                y1 = r * CELL
                x2 = x1 + CELL
                y2 = y1 + CELL

                self.canvas.create_rectangle(x1, y1, x2, y2)

                cell = self.state.board[r][c]
                if cell != ' ':
                    self.canvas.create_rectangle(
                        x1+5, y1+5, x2-5, y2-5,
                        fill=COLORS[cell]
                    )

        if self.state.player in self.human_players:
            for move in self.state.get_possible_moves():
                if move:
                    r, c = move
                    x = c * CELL + CELL//2
                    y = r * CELL + CELL//2
                    self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="gray")

        scores = self.state.get_scores()
        self.score_label.config(
            text=" | ".join([f"{p}: {scores[p]}" for p in PLAYERS])
        )

        if self.state.is_game_over():
            winner = max(scores, key=scores.get)
            self.canvas.create_text(WIDTH//2, HEIGHT//2,
                                    text=f"{winner} gagne !",
                                    font=("Arial", 24))

    def click(self, event):
        if self.state.is_game_over():
            return

        if self.state.player not in self.human_players:
            return

        r = event.y // CELL
        c = event.x // CELL

        for move in self.state.get_possible_moves():
            if move == (r, c):
                self.state = self.state._apply_action(move)
                self.draw()

    def loop(self):
        if not self.state.is_game_over():
            if self.state.player not in self.human_players:
                self.state = choose_move_maxn(
                    self.state,
                    PLAYERS,
                    heuristic_scores,
                    depth=3
                )
                self.draw()

        self.root.after(300, self.loop)

    def back_to_menu(self):
        self.root.destroy()  # ferme la fenêtre actuelle

        import tkinter as tk
        from __main__ import Menu  # si ton fichier est exécuté directement

        root = tk.Tk()
        root.title("Territory")
        Menu(root)
        root.mainloop()


class Menu:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack(padx=20, pady=20)

        tk.Label(self.frame, text="Nombre de joueurs humains :", font=("Arial", 14)).pack()

        self.var = tk.IntVar(value=0)

        for i in range(0, 5):
            tk.Radiobutton(self.frame, text=f"{i} joueur(s)", variable=self.var, value=i).pack(anchor="w")

        tk.Button(self.frame, text="Lancer", command=self.start).pack(pady=20)

    def start(self):
        human_players = PLAYERS[:self.var.get()]
        self.frame.destroy()
        TerritoryWindow(self.root, human_players)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Territory")
    Menu(root)
    root.mainloop()
