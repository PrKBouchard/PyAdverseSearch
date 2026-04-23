# -*- coding: utf-8 -*-
# FILE: connect4_gui.py

import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os
import time
import threading

# Ajouter le chemin parent pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyAdverseSearch.test.state_connect4 import generate_connect4_game
from PyAdverseSearch.classes.minimax import Minimax
from PyAdverseSearch.classes.alphabeta import AlphaBeta
from PyAdverseSearch.classes.montecarlo import MonteCarlo
from PyAdverseSearch.classes.mtdf import MTDf
from PyAdverseSearch.classes.negamax import NegamaxSolver
from PyAdverseSearch.classes.pnsearch import PNSearch
from PyAdverseSearch.classes.autosolver import AutoSolver
from PyAdverseSearch.Interface.pdf_report import export_game_pdf


class Connect4GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Puissance 4 - Enhanced AI")
        self.root.resizable(False, False)
        
        # --- STYLE MENU : Fond de fenetre ---
        self.root.configure(bg="#2c3e50")

        # Configuration du jeu
        self.ROWS = 6
        self.COLS = 7
        self.CELL_SIZE = 80
        self.MARGIN = 10

        # --- STYLE MENU : Palette de couleurs ---
        self.BOARD_COLOR = "#34495e"    # Bleu-gris sombre
        self.EMPTY_COLOR = "#ecf0f1"    # Gris tres clair
        self.PLAYER_COLOR = "#e74c3c"   # Rouge (Alizarin)
        self.AI_COLOR = "#f1c40f"       # Jaune (Tournesol)
        self.HIGHLIGHT_COLOR = "#2ecc71" # Vert (Emeraude)
        self.WIN_COLOR = "#27ae60"      # Vert sombre (Nephrite)

        self._winning_cells = []
        self.game = None
        self.state = None
        self.algorithm = None
        self.human_is_max = None
        self.game_over = False
        self.ai_thinking = False
        self.move_history = []
        self.game_start_time = None
        self.auto_mode = False
        self.fast_mode = False
        self.current_algo_name = ""

        self.create_config_screen()

    def create_config_screen(self):
        config_frame = tk.Frame(self.root, padx=20, pady=20, bg="#2c3e50")
        config_frame.pack()

        tk.Label(config_frame, text="PUISSANCE 4", font=("Helvetica", 24, "bold"),
                 bg="#2c3e50", fg="#ecf0f1").pack(pady=10)
        
        tk.Label(config_frame, text="Qui commence ?", font=("Helvetica", 14),
                 bg="#2c3e50", fg="#ecf0f1").pack(pady=5)
        
        self.start_choice = tk.StringVar(value="human")
        tk.Radiobutton(config_frame, text="Joueur (Rouge)", variable=self.start_choice,
                       value="human", font=("Helvetica", 12),
                       bg="#2c3e50", fg="#e74c3c", selectcolor="#34495e",
                       activebackground="#2c3e50").pack()
        tk.Radiobutton(config_frame, text="IA (Jaune)", variable=self.start_choice,
                       value="ai", font=("Helvetica", 12),
                       bg="#2c3e50", fg="#f1c40f", selectcolor="#34495e",
                       activebackground="#2c3e50").pack()

        tk.Label(config_frame, text="Algorithme", font=("Helvetica", 14),
                 bg="#2c3e50", fg="#ecf0f1").pack(pady=(20, 5))
        
        self.algo_choice = tk.StringVar(value="fast")
        tk.Radiobutton(config_frame, text="Mode Rapide", variable=self.algo_choice,
                       value="fast", font=("Helvetica", 12, "bold"),
                       bg="#2c3e50", fg="#2ecc71", selectcolor="#34495e").pack()
        tk.Radiobutton(config_frame, text="Mode Auto", variable=self.algo_choice,
                       value="auto", font=("Helvetica", 12, "bold"),
                       bg="#2c3e50", fg="#9b59b6", selectcolor="#34495e").pack()

        tk.Button(config_frame, text="LANCER LA PARTIE", command=self.start_game,
                  font=("Helvetica", 12, "bold"), bg="#27ae60", fg="white",
                  relief="flat", cursor="hand2", padx=20, pady=10).pack(pady=30)

    def start_game(self):
        if self.start_choice.get() == "human":
            self.human_is_max = True
            max_starting = True
        else:
            self.human_is_max = False
            max_starting = False

        self.game = generate_connect4_game(max_starting)
        self.state = self.game.state
        depth = 6 # Profondeur par defaut

        algo_name = self.algo_choice.get()
        if algo_name == "auto":
            self.algorithm = AutoSolver(game=self.game, depth=depth, mode="classic")
            self.auto_mode = True
            self.current_algo_name = "Auto"
        else:
            self.algorithm = AutoSolver(game=self.game, depth=depth, mode="fast")
            self.fast_mode = True
            self.current_algo_name = "Rapide"

        self.move_history = []
        self.game_start_time = time.time()
        self.game_over = False
        
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_game_board()

        if (self.state.player == "MAX") != self.human_is_max:
            self.root.after(500, self.ai_move)

    def create_game_board(self):
        self.highlight_col = None
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(padx=10, pady=10)

        self.info_label = tk.Label(main_frame, text="A vous de jouer", font=("Helvetica", 14, "bold"),
                                   bg="#2c3e50", fg="#ecf0f1")
        self.info_label.pack(pady=5)

        canvas_width = self.COLS * self.CELL_SIZE + 2 * self.MARGIN
        canvas_height = self.ROWS * self.CELL_SIZE + 2 * self.MARGIN
        self.canvas = tk.Canvas(main_frame, width=canvas_width, height=canvas_height,
                                bg=self.BOARD_COLOR, highlightthickness=0)
        self.canvas.pack(pady=10)
        
        self.draw_board()

        btn_frame = tk.Frame(main_frame, bg="#2c3e50")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Menu Principal", command=self.reset_game,
                  bg="#95a5a6", fg="white", relief="flat", font=("Helvetica", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Quitter", command=self.root.quit,
                  bg="#c0392b", fg="white", relief="flat", font=("Helvetica", 10, "bold")).pack(side=tk.LEFT, padx=5)

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Motion>", self.on_mouse_move)

    def draw_board(self):
        self.canvas.delete("all")
        win_set = set(self._winning_cells)
        for r in range(self.ROWS):
            for c in range(self.COLS):
                x = self.MARGIN + c * self.CELL_SIZE
                y = self.MARGIN + r * self.CELL_SIZE
                val = self.state.board[r][c]
                
                if (r, c) in win_set: color = self.WIN_COLOR
                elif val == 'X': color = self.PLAYER_COLOR if self.human_is_max else self.AI_COLOR
                elif val == 'O': color = self.AI_COLOR if self.human_is_max else self.PLAYER_COLOR
                else: color = self.EMPTY_COLOR
                
                self.canvas.create_oval(x+5, y+5, x+self.CELL_SIZE-5, y+self.CELL_SIZE-5,
                                        fill=color, outline="#2c3e50", width=2)

    def on_mouse_move(self, event):
        if self.game_over or self.ai_thinking: return
        col = (event.x - self.MARGIN) // self.CELL_SIZE
        if 0 <= col < self.COLS and self.highlight_col != col:
            self.highlight_col = col
            self.draw_board()
            x = self.MARGIN + col * self.CELL_SIZE
            self.canvas.create_rectangle(x+2, self.MARGIN, x+self.CELL_SIZE-2, 
                                         self.MARGIN+self.ROWS*self.CELL_SIZE, 
                                         outline=self.HIGHLIGHT_COLOR, width=2)

    def on_canvas_click(self, event):
        if self.game_over or self.ai_thinking: return
        col = (event.x - self.MARGIN) // self.CELL_SIZE
        if 0 <= col < self.COLS and col in self.state._possible_actions():
            self.make_move(col, True)

    def make_move(self, col, is_human):
        self.state = self.state._apply_action(col)
        self.move_history.append(f"{'Joueur' if is_human else 'IA'}: Col {col+1}")
        self.draw_board()
        
        if self.state._is_terminal():
            self.game_over = True
            winner = self.game.winner_function(self.state)
            if winner:
                self.info_label.config(text="FIN DE PARTIE", fg="#f1c40f")
                messagebox.showinfo("Resultat", "Gagne !")
            else:
                self.info_label.config(text="MATCH NUL", fg="#ecf0f1")
            return

        if is_human:
            self.ai_move()

    def ai_move(self):
        self.ai_thinking = True
        self.info_label.config(text="L'IA reflechit...", fg="#e67e22")
        self.root.update()
        
        def compute():
            best_state = self.algorithm.choose_best_move(self.state)
            col = None
            for c in range(self.COLS):
                if c in self.state._possible_actions():
                    if self.state._apply_action(c).board == best_state.board:
                        col = c
                        break
            self.root.after(0, lambda: self.finish_ai_move(col))

        threading.Thread(target=compute, daemon=True).start()

    def finish_ai_move(self, col):
        self.ai_thinking = False
        self.info_label.config(text="A vous de jouer", fg="#2ecc71")
        if col is not None:
            self.make_move(col, False)

    def reset_game(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_config_screen()

if __name__ == "__main__":
    root = tk.Tk()
    Connect4GUI(root)
    root.mainloop()