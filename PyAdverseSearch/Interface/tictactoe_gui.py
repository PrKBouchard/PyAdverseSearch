import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyAdverseSearch.test.state_tictactoe import generate_tictactoe_game
from PyAdverseSearch.classes.minimax import Minimax
from PyAdverseSearch.classes.alphabeta import AlphaBeta
from PyAdverseSearch.classes.montecarlo import MonteCarlo

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Morpion IA - Premium")
        self.root.configure(bg="#1e1e2e")
        
        self.FONT_MAIN = ("Segoe UI", 12)
        self.FONT_BOLD = ("Segoe UI", 14, "bold")
        self.BG_DARK = "#1e1e2e"
        self.BG_CARD = "#2b2b3b"
        self.ACCENT = "#7289da"
        self.X_COLOR = "#ff5555"
        self.O_COLOR = "#50fa7b"
        
        self.SIZE = 3
        self.CELL_SIZE = 130
        
        self.game = None
        self.state = None
        self.algorithm = None
        self.human_is_max = None
        self.game_over = False
        
        self.create_config_screen()
        
    def create_config_screen(self):
        """Écran de configuration moderne"""
        self.frame_config = tk.Frame(self.root, bg=self.BG_DARK, padx=40, pady=40)
        self.frame_config.pack(expand=True)

        tk.Label(self.frame_config, text="MORPION", font=("Segoe UI", 32, "bold"), 
                 fg=self.ACCENT, bg=self.BG_DARK).pack(pady=(0, 10))
        tk.Label(self.frame_config, text="Intelligence Artificielle", font=("Segoe UI", 10), 
                 fg="#a9a1e1", bg=self.BG_DARK).pack(pady=(0, 30))

        options_bg = self.BG_CARD
        card = tk.Frame(self.frame_config, bg=options_bg, padx=20, pady=20, 
                        highlightbackground=self.ACCENT, highlightthickness=1)
        card.pack(fill="both")

        tk.Label(card, text="QUI COMMENCE ?", font=self.FONT_BOLD, fg="white", bg=options_bg).pack(pady=5)
        self.start_choice = tk.StringVar(value="human")
        self.create_radio(card, "Vous (X)", "human", self.start_choice)
        self.create_radio(card, "IA (O)", "ai", self.start_choice)

        tk.Label(card, text="ALGORITHME", font=self.FONT_BOLD, fg="white", bg=options_bg).pack(pady=(20, 5))
        self.algo_choice = tk.StringVar(value="alphabeta")
        self.create_radio(card, "Alpha-Beta (Rapide)", "alphabeta", self.algo_choice)
        self.create_radio(card, "Monte Carlo", "montecarlo", self.algo_choice)
        self.create_radio(card, "Minimax", "minimax", self.algo_choice)

        btn_play = tk.Button(self.frame_config, text="LANCER LA PARTIE", command=self.start_game,
                             font=("Segoe UI", 12, "bold"), bg="#50fa7b", fg="#282a36",
                             activebackground="#40c463", cursor="hand2", 
                             bd=0, padx=40, pady=15)
        btn_play.pack(pady=30)

    def create_radio(self, parent, text, value, variable):
        """Helper pour créer des boutons radio stylisés"""
        rb = tk.Radiobutton(parent, text=text, variable=variable, value=value,
                            bg=parent["bg"], fg="#bd93f9", selectcolor="#44475a",
                            activebackground=parent["bg"], activeforeground="white",
                            font=self.FONT_MAIN, bd=0, highlightthickness=0)
        rb.pack(anchor="w", padx=20)

    def start_game(self):
        """Initialisation du jeu (Correction du bug initial_state incluse)"""
        if self.start_choice.get() == "human":
            self.human_is_max = True
            max_starting = True
        else:
            self.human_is_max = False
            max_starting = False
        
        self.game = generate_tictactoe_game(max_starting)
        self.state = self.game.state
        
        algo_name = self.algo_choice.get()
        if algo_name == "minimax":
            self.algorithm = Minimax(game=self.game, max_depth=9)
        elif algo_name == "alphabeta":
            self.algorithm = AlphaBeta(game=self.game, max_depth=9)
        else:
            self.algorithm = MonteCarlo(game=self.game, max_iterations=1200)
        
        self.frame_config.destroy()
        self.create_game_board()
        
        if (self.state.player == "MAX") != self.human_is_max:
            self.root.after(600, self.ai_move)
    
    def create_game_board(self):
        """Plateau de jeu épuré"""
        self.main_frame = tk.Frame(self.root, bg=self.BG_DARK, padx=20, pady=20)
        self.main_frame.pack()
        
        self.info_label = tk.Label(self.main_frame, text="", font=self.FONT_BOLD, 
                                   bg=self.BG_DARK, fg="white")
        self.info_label.pack(pady=(0, 20))
        
        size = self.SIZE * self.CELL_SIZE
        self.canvas = tk.Canvas(self.main_frame, width=size, height=size, 
                               bg=self.BG_CARD, bd=0, highlightthickness=2, 
                               highlightbackground=self.ACCENT)
        self.canvas.pack()
        
        self.draw_board()

        ctrl_frame = tk.Frame(self.main_frame, bg=self.BG_DARK)
        ctrl_frame.pack(pady=20)
        
        tk.Button(ctrl_frame, text="RETOUR MENU", command=self.reset_game, 
                  bg="#44475a", fg="white", bd=0, padx=15, pady=8).pack(side=tk.LEFT, padx=10)
        
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.update_info_label()

    def draw_board(self):
        self.canvas.delete("all")

        for i in range(1, self.SIZE):

            self.canvas.create_line(i * self.CELL_SIZE, 0, i * self.CELL_SIZE, self.SIZE * self.CELL_SIZE, fill="#44475a", width=2)
            self.canvas.create_line(0, i * self.CELL_SIZE, self.SIZE * self.CELL_SIZE, i * self.CELL_SIZE, fill="#44475a", width=2)
        
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                val = self.state.board[r][c]
                x_center = c * self.CELL_SIZE + self.CELL_SIZE // 2
                y_center = r * self.CELL_SIZE + self.CELL_SIZE // 2
                offset = 35
                
                if val == 'X':
                    self.canvas.create_line(x_center-offset, y_center-offset, x_center+offset, y_center+offset, fill=self.X_COLOR, width=10, capstyle=tk.ROUND)
                    self.canvas.create_line(x_center-offset, y_center+offset, x_center+offset, y_center-offset, fill=self.X_COLOR, width=10, capstyle=tk.ROUND)
                elif val == 'O':
                    self.canvas.create_oval(x_center-offset, y_center-offset, x_center+offset, y_center+offset, outline=self.O_COLOR, width=10)

    def on_canvas_click(self, event):
        if self.game_over or (self.state.player == "MAX") != self.human_is_max:
            return
        
        col, row = event.x // self.CELL_SIZE, event.y // self.CELL_SIZE
        action = (row, col)
        
        if action in self.state.get_possible_moves():
            self.state = self.state._apply_action(action)
            self.draw_board()
            if not self.check_game_over():
                self.update_info_label()
                self.root.after(500, self.ai_move)

    def ai_move(self):
        if self.game_over: return
        self.info_label.config(text="L'IA réfléchit...", fg=self.ACCENT)
        self.root.update()
        
        best_state = self.algorithm.choose_best_move(self.state)
        if best_state:
            self.state = best_state
            self.draw_board()
            if not self.check_game_over():
                self.update_info_label()

    def update_info_label(self):
        is_human = (self.state.player == "MAX") == self.human_is_max
        msg = "À VOUS DE JOUER" if is_human else "L'IA RÉFLECHIT..."
        color = self.O_COLOR if is_human else self.ACCENT
        self.info_label.config(text=msg, fg=color)

    def check_game_over(self):
        if self.state.is_game_over():
            self.game_over = True
            winner = self.state.get_winner()
            if winner is None:
                msg, color = "MATCH NUL !", "#f1fa8c"
            elif (winner == "MAX") == self.human_is_max:
                msg, color = "VICTOIRE !", self.O_COLOR
            else:
                msg, color = "DÉFAITE...", self.X_COLOR
            
            self.info_label.config(text=msg, fg=color)
            return True
        return False

    def reset_game(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    root.eval('tk::PlaceWindow . center')
    app = TicTacToeGUI(root)
    root.mainloop()