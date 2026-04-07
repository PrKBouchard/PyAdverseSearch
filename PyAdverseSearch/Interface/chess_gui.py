import tkinter as tk
from tkinter import ttk

from PyAdverseSearch.test.Chess.state_chess import generate_chess_game
from PyAdverseSearch.classes.minimax import Minimax
from PyAdverseSearch.classes.alphabeta import AlphaBeta
from PyAdverseSearch.classes.montecarlo import MonteCarlo

coord=[
    'a8','b8','c8','d8','e8','f8','g8','h8',
    'a7','b7','c7','d7','e7','f7','g7','h7',
    'a6','b6','c6','d6','e6','f6','g6','h6',
    'a5','b5','c5','d5','e5','f5','g5','h5',
    'a4','b4','c4','d4','e4','f4','g4','h4',
    'a3','b3','c3','d3','e3','f3','g3','h3',
    'a2','b2','c2','d2','e2','f2','g2','h2',
    'a1','b1','c1','d1','e1','f1','g1','h1',
    ]

UNICODE_PIECES = {
    ('K', 'BORDER'): '♔', ('Q', 'BORDER'): '♕',
    ('R', 'BORDER'): '♖', ('B', 'BORDER'): '♗',
    ('N', 'BORDER'): '♘', ('P', 'BORDER'): '♙',
    ('K', 'FULL'): '♚', ('Q', 'FULL'): '♛',
    ('R', 'FULL'): '♜', ('B', 'FULL'): '♝',
    ('N', 'FULL'): '♞', ('P', 'FULL'): '♟',
    (' ', 'NONE'): '',
}

BG_ORANGE = "#C15F3C" 
BG_BEIGE  = "#F4F3EE" 

LIGHT_SQUARE = "#F0D9B5"  
DARK_SQUARE  = "#B58863" 

TITLE_FONT = ("Arial", 24, "bold")
FORM_FONT = ("Arial", 14, "bold")

class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Game IA ♟")
        self.show_menu()
        self.cell_size = 70
        self.board_size = 8
        self.selected_piece = False
        self.state = None
        self.from_pos = None
        self.to_pos = None

        


    def show_menu(self):
        self.root.configure(bg=BG_ORANGE)
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.columnconfigure(2, weight=1)
        self.root.geometry("700x700")
        self.root.configure(bg=BG_ORANGE)

         
        title = tk.Label(self.root, text="CHESS", font=TITLE_FONT, bg=BG_ORANGE, fg="white").grid(row=0, column=1, padx=20, pady=(80,10))

        frame = tk.Frame(self.root, bg=BG_BEIGE, highlightbackground=LIGHT_SQUARE, highlightthickness=3)
        frame.grid(row=2, column=1, padx=20, pady=20)

        color = tk.StringVar()
        color.set('white') 

        color_label = tk.Label(frame, text="COLOR :", font=FORM_FONT, fg=BG_ORANGE).grid(row=1, column=0, padx=20, pady=(20,10), columnspan=2)
        tk.Radiobutton(frame, text="White", variable=color, value='white').grid(row=2, column=0)
        tk.Radiobutton(frame, text="Black", variable=color, value='black').grid(row=2, column=1)

        algo_label = tk.Label(frame, text="ALGORITHM :", font=FORM_FONT, fg=BG_ORANGE).grid(row=4, column=0, padx=30, pady=(20,10), columnspan=2)
        algo_combo_box = ttk.Combobox(
            frame,
            values=["Alpha-Beta", "Minimax", "Monte Carlo"],
            state="readonly",
        )
        algo_combo_box.grid(row=5, column=0, columnspan=2)
        algo_combo_box.set("Alpha-Beta")

        level_label = tk.Label(frame, text="LEVEL :", font=FORM_FONT, fg=BG_ORANGE).grid(row=6, column=0, padx=20, pady=(20,10), columnspan=2)
        level_combo_box = ttk.Combobox(
            frame,
            values=["Easy (Depth 2)", "Medium (Depth 4)", "Hard (Depth 6)"],
            state="readonly",
        )
        level_combo_box.grid(row=7, column=0, columnspan=2)
        level_combo_box.set("Medium (Depth 4)")

        start_button = tk.Button(frame, text="Start Game", font=FORM_FONT, bg=BG_ORANGE, fg="white", command=lambda: self.start_game(color.get(), algo_combo_box.get(), level_combo_box.get()))
        start_button.grid(row=8, column=0, padx=20, pady=(40,20), columnspan=2)


    def start_game(self, color, algo, level):
        #print("Selected Color:"+ color +", Algorithm:" + algo +", Level: "+ level)
        
        """self.canvas = tk.Canvas(
            root, width=self.board_size * self.cell_size, height=self.board_size * self.cell_size
        )
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.pack(padx=20, pady=20)"""

        player_color = color.upper()
        maxStarting = True if color == 'white' else False
        depth = int(level.split('(')[1].split(')')[0].split()[1])
        
        game = generate_chess_game(maxStarting)
        self.state = game.state
        if algo == "Alpha-Beta":
            algorithm = AlphaBeta(game=game, max_depth=depth)
        elif algo == "Minimax":
            algorithm = Minimax(game=game, max_depth=depth)
        else:
            algorithm = MonteCarlo(game=game, max_iterations=depth*200)  # Adjust iterations based on depth

        self.draw_board()

    def draw_board(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        root.rowconfigure(2, weight=1)
        frame = tk.Frame(self.root, bg="#FFFFFF")
        frame.grid(column=1, row=1)
        # Faire un frame grid et un canva pour chaque case du plateau, et y placer une étiquette avec le symbole Unicode de la pièce correspondante. Utiliser les couleurs LIGHT_SQUARE et DARK_SQUARE pour les cases claires et foncées.
        index = 0
        
        for row in range(8):
            for col in range(8):
                square_color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                cell_canvas = tk.Canvas(frame, width=self.cell_size, height=self.cell_size, bg=square_color, highlightthickness=0)
                cell_canvas.grid(row=row, column=col)

                piece = self.state.board.cases[index]
                unicode_piece = UNICODE_PIECES.get((piece.name, "FULL"), '')

                color = "white" if piece.color == "WHITE" else "black"
                cell_canvas.create_text(self.cell_size/2, self.cell_size/2, font=("Segoe UI Symbol", 42), text=unicode_piece, fill=color)
                if color =="white":
                    unicode_border_piece = UNICODE_PIECES.get((piece.name, "BORDER"), '')
                    cell_canvas.create_text(self.cell_size/2, self.cell_size/2, font=("Segoe UI Symbol", 42), text=unicode_border_piece, fill="black")
                
                cell_canvas.bind("<Button-1>", lambda e, i=index: self.on_click(i))
                index += 1

            
    def on_click(self,i):
        piece_coo= coord[i]
        if self.selected_piece:
            self.to_pos = piece_coo
            self.move_piece(self.from_pos,self.to_pos)
            self.selected_piece = False
        else:
            self.from_pos = piece_coo
            self.selected_piece = True

    def move_piece(self, from_pos, to_pos):
        try:
            user_input= from_pos+to_pos
            user_state = self.state.user_move(user_input)
            self.state = user_state
            self.draw_board()
        except ValueError as error:
            print(str(error))


def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


if __name__ == "__main__":
    root = tk.Tk()
    app = ChessGUI(root)
    center(root)
    root.mainloop()