import tkinter as tk
from maxn import choose_move

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


class TerritoryState:
    def __init__(self, board=None, player='BLEU'):
        if board is None:
            board = [[' ' for _ in range(SIZE)] for _ in range(SIZE)]

            board[0][0] = 'BLEU'
            board[0][SIZE-1] = 'ROUGE'
            board[SIZE-1][0] = 'JAUNE'
            board[SIZE-1][SIZE-1] = 'VIOLET'

        self.board = board
        self.player = player

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

        if not moves:
            return [None]

        return moves

    def apply_action(self, move):
        new_board = [row[:] for row in self.board]

        if move:
            r, c = move
            new_board[r][c] = self.player

        next_idx = (PLAYERS.index(self.player) + 1) % len(PLAYERS)
        next_player = PLAYERS[next_idx]

        return TerritoryState(new_board, next_player)

    def is_terminal(self):
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

        return [scores[p] for p in PLAYERS]


class Menu:
    def __init__(self, root):
        self.root = root
        self.root.title("Configuration")

        self.frame = tk.Frame(root)
        self.frame.pack(padx=20, pady=20)

        tk.Label(self.frame, text="Nombre de joueurs humains :", font=("Arial", 14)).pack(pady=10)

        self.player_count = tk.IntVar(value=1)

        for i in range(1, 5):
            tk.Radiobutton(self.frame, text=f"{i} joueur(s)", variable=self.player_count, value=i).pack(anchor="w")

        tk.Button(self.frame, text="Lancer", command=self.start).pack(pady=20)

    def start(self):
        count = self.player_count.get()
        human_players = PLAYERS[:count]

        self.frame.destroy()
        TerritoryWindow(self.root, human_players)


class TerritoryWindow:
    def __init__(self, root, human_players):
        self.root = root
        self.root.title("Territory")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack()

        self.state = TerritoryState()
        self.human_players = human_players

        self.canvas.bind("<Button-1>", self.click)

        self.draw()
        self.loop()

    def draw(self):
        self.canvas.delete("all")

        for r in range(SIZE):
            for c in range(SIZE):
                x1 = c * CELL
                y1 = r * CELL
                x2 = x1 + CELL
                y2 = y1 + CELL

                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")

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
        text = " | ".join([f"{p}:{scores[i]}" for i, p in enumerate(PLAYERS)])
        self.canvas.create_text(10, HEIGHT-10, anchor="sw", text=text)

        if self.state.is_terminal():
            scores_dict = {p: scores[i] for i, p in enumerate(PLAYERS)}
            winner = max(scores_dict, key=scores_dict.get)

            self.canvas.create_text(WIDTH//2, HEIGHT//2,
                                    text=f"{winner} gagne !",
                                    font=("Arial", 24))

    def click(self, event):
        if self.state.is_terminal():
            return

        if self.state.player not in self.human_players:
            return

        r = event.y // CELL
        c = event.x // CELL

        for move in self.state.get_possible_moves():
            if move and move == (r, c):
                self.state = self.state.apply_action(move)
                self.draw()
                return

    def loop(self):
        if not self.state.is_terminal():
            if self.state.player not in self.human_players:
                self.state = choose_move(self.state, PLAYERS, depth=3)
                self.draw()

        self.root.after(300, self.loop)


if __name__ == "__main__":
    root = tk.Tk()
    Menu(root)
    root.mainloop()
