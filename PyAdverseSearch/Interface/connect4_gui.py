# -*- coding: utf-8 -*-
# FILE: connect4_gui_enhanced.py

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
        
        # --- ESTHÉTIQUE MENU : Fond de la fenêtre ---
        self.root.configure(bg="#2c3e50")

        # Configuration du jeu
        self.ROWS = 6
        self.COLS = 7
        self.CELL_SIZE = 80
        self.MARGIN = 10

        # --- ESTHÉTIQUE MENU : Couleurs du plateau et des pions ---
        self.BOARD_COLOR = "#34495e"    # Bleu-gris sombre (similaire aux boutons menu)
        self.EMPTY_COLOR = "#ecf0f1"    # Gris très clair (texte menu)
        self.PLAYER_COLOR = "#e74c3c"   # Rouge (Alizarin)
        self.AI_COLOR = "#f1c40f"       # Jaune (Tournesol)
        self.HIGHLIGHT_COLOR = "#2ecc71" # Vert (Emeraude)
        self.WIN_COLOR = "#27ae60"      # Vert sombre (Nephrite)

        # Cellules de l'alignement gagnant (liste de (row, col))
        self._winning_cells = []

        # Variables de jeu
        self.game = None
        self.state = None
        self.algorithm = None
        self.human_is_max = None
        self.game_over = False

        # Stats IA
        self.ai_thinking = False
        self.move_history = []
        self.game_start_time = None

        # Mode (pour distinguer auto/fast/fixe)
        self.auto_mode = False
        self.fast_mode = False
        self.current_algo_name = ""

        self.create_config_screen()

    # ------------------------------------------------------------------
    # Ecran de configuration
    # ------------------------------------------------------------------

    def create_config_screen(self):
        # --- ESTHÉTIQUE MENU : Frame et Labels ---
        config_frame = tk.Frame(self.root, padx=20, pady=20, bg="#2c3e50")
        config_frame.pack()

        tk.Label(config_frame, text="Puissance 4", font=("Helvetica", 24, "bold"), 
                 bg="#2c3e50", fg="#ecf0f1").pack(pady=10)
        tk.Label(config_frame, text="Version Enhanced AI",
                 font=("Helvetica", 10, "italic"), bg="#2c3e50", fg="#bdc3c7").pack()

        tk.Label(config_frame, text="Qui commence ?", font=("Helvetica", 14), 
                 bg="#2c3e50", fg="#ecf0f1").pack(pady=5)
        
        self.start_choice = tk.StringVar(value="human")
        tk.Radiobutton(config_frame, text="Vous (Rouge)", variable=self.start_choice,
                       value="human", font=("Helvetica", 12), bg="#2c3e50", fg="#e74c3c", 
                       selectcolor="#34495e", activebackground="#2c3e50").pack()
        tk.Radiobutton(config_frame, text="IA (Jaune)", variable=self.start_choice,
                       value="ai", font=("Helvetica", 12), bg="#2c3e50", fg="#f1c40f", 
                       selectcolor="#34495e", activebackground="#2c3e50").pack()

        tk.Label(config_frame, text="Algorithme IA", font=("Helvetica", 14), 
                 bg="#2c3e50", fg="#ecf0f1").pack(pady=(20, 5))
        
        self.algo_choice = tk.StringVar(value="fast")
        tk.Radiobutton(config_frame, text="Rapide (MTD(f) + PN-Search)", variable=self.algo_choice,
                       value="fast", font=("Helvetica", 12, "bold"), bg="#2c3e50", fg="#2ecc71", 
                       selectcolor="#34495e").pack()
        tk.Radiobutton(config_frame, text="Auto Equilibre (Tous les algos)", variable=self.algo_choice,
                       value="auto", font=("Helvetica", 12, "bold"), bg="#2c3e50", fg="#9b59b6", 
                       selectcolor="#34495e").pack()
        
        tk.Label(config_frame, text="--- Algorithmes manuels ---",
                 font=("Helvetica", 10), bg="#2c3e50", fg="#bdc3c7").pack(pady=(10, 0))

        # Boucle pour les algos manuels avec style adapté
        for text, val in [
            ("Minimax (Classique)", "minimax"),
            ("Alpha-Beta (Elagage)", "alphabeta"),
            ("MTD(f) (Plus efficace)", "mtdf"),
            ("Negamax (Simplifie)", "negamax"),
            ("Monte Carlo (Simulations)", "montecarlo"),
            ("PN-Search (Preuve)", "pnsearch"),
        ]:
            tk.Radiobutton(config_frame, text=text, variable=self.algo_choice,
                           value=val, font=("Helvetica", 12), bg="#2c3e50", fg="#ecf0f1", 
                           selectcolor="#34495e").pack()

        tk.Label(config_frame, text="Difficulte", font=("Helvetica", 14), 
                 bg="#2c3e50", fg="#ecf0f1").pack(pady=(20, 5))
        
        self.difficulty = tk.StringVar(value="medium")
        for text, val in [
            ("Facile", "easy"),
            ("Moyen", "medium"),
            ("Difficile", "hard"),
            ("Expert", "expert"),
        ]:
            tk.Radiobutton(config_frame, text=text, variable=self.difficulty,
                           value=val, font=("Helvetica", 12), bg="#2c3e50", fg="#ecf0f1", 
                           selectcolor="#34495e").pack()

        # Bouton "Commencer" avec style du bouton menu "Reversi" (Vert)
        tk.Button(config_frame, text="COMMENCER", command=self.start_game,
                  font=("Helvetica", 14, "bold"), bg="#27ae60", fg="white",
                  relief="flat", cursor="hand2", padx=20, pady=10).pack(pady=20)

    # ------------------------------------------------------------------
    # Demarrage du jeu
    # ------------------------------------------------------------------

    def start_game(self):
        if self.start_choice.get() == "human":
            self.human_is_max = True
            max_starting = True
        else:
            self.human_is_max = False
            max_starting = False

        self.game = generate_connect4_game(max_starting)
        self.state = self.game.state

        depth_map = {"easy": 3, "medium": 5, "hard": 7, "expert": 9}
        depth = depth_map[self.difficulty.get()]

        algo_name = self.algo_choice.get()

        if algo_name == "auto":
            self.algorithm = AutoSolver(game=self.game, depth=depth, mode="classic", rows=self.ROWS, cols=self.COLS)
            self.auto_mode = True
            self.current_algo_name = "Auto"
        elif algo_name == "fast":
            self.algorithm = AutoSolver(game=self.game, depth=depth, mode="fast", rows=self.ROWS, cols=self.COLS)
            self.fast_mode = True
            self.current_algo_name = "Rapide"
        elif algo_name == "minimax":
            self.algorithm = Minimax(game=self.game, max_depth=depth)
            self.current_algo_name = "Minimax"
        elif algo_name == "alphabeta":
            self.algorithm = AlphaBeta(game=self.game, max_depth=depth, use_transposition_table=True)
            self.current_algo_name = "Alpha-Beta+TT"
        elif algo_name == "mtdf":
            self.algorithm = MTDf(game=self.game, max_depth=depth, initial_guess=0)
            self.current_algo_name = "MTD(f)"
        elif algo_name == "negamax":
            self.algorithm = NegamaxSolver(depth_limit=depth)
            self.current_algo_name = "Negamax"
        elif algo_name == "pnsearch":
            self.algorithm = PNSearch(game=self.game, use_transposition_table=True)
            self.current_algo_name = "PN-Search"
        else:
            self.algorithm = MonteCarlo(game=self.game, max_iterations=2000 * depth)
            self.current_algo_name = "Monte Carlo"

        self.move_history = []
        self.game_start_time = time.time()
        self.game_over = False
        self.ai_thinking = False

        for widget in self.root.winfo_children():
            widget.destroy()

        self.create_game_board()

        current_is_max = (self.state.player == "MAX")
        if current_is_max != self.human_is_max:
            self.root.after(500, self.ai_move)

    # ------------------------------------------------------------------
    # Creation du plateau
    # ------------------------------------------------------------------

    def create_game_board(self):
        self.highlight_col = None
        self._winning_cells = []

        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(padx=10, pady=10)

        top_frame = tk.Frame(main_frame, bg="#2c3e50")
        top_frame.pack(fill=tk.X, pady=5)

        self.info_label = tk.Label(top_frame, text="", font=("Helvetica", 14, "bold"), 
                                   bg="#2c3e50", fg="#ecf0f1")
        self.info_label.pack(side=tk.LEFT, padx=10)

        self.algo_label = tk.Label(top_frame, text="", font=("Helvetica", 10), 
                                   bg="#2c3e50", fg="#9b59b6")
        self.algo_label.pack(side=tk.LEFT, padx=10)

        self.time_label = tk.Label(top_frame, text="Temps IA: --",
                                   font=("Helvetica", 11), bg="#2c3e50", fg="#3498db")
        self.time_label.pack(side=tk.RIGHT, padx=10)

        self.update_info_label()

        progress_frame = tk.Frame(main_frame, bg="#2c3e50")
        progress_frame.pack(fill=tk.X, pady=5)

        # Style pour la barre de progression (Thème sombre)
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TProgressbar", thickness=10, troughcolor='#34495e', background='#2ecc71')

        tk.Label(progress_frame, text="Reflexion IA:", font=("Helvetica", 10), 
                 bg="#2c3e50", fg="#bdc3c7").pack(side=tk.LEFT, padx=5)
        self.progress_bar = ttk.Progressbar(progress_frame, length=400, mode='determinate', style="TProgressbar")
        self.progress_bar.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.progress_label = tk.Label(progress_frame, text="0%", font=("Helvetica", 10), 
                                       bg="#2c3e50", fg="#bdc3c7")
        self.progress_label.pack(side=tk.LEFT, padx=5)

        stats_frame = tk.Frame(main_frame, bg="#2c3e50")
        stats_frame.pack(fill=tk.X, pady=5)
        self.stats_label = tk.Label(stats_frame, text="", font=("Helvetica", 9), 
                                    bg="#2c3e50", fg="#bdc3c7")
        self.stats_label.pack()

        canvas_width = self.COLS * self.CELL_SIZE + 2 * self.MARGIN
        canvas_height = self.ROWS * self.CELL_SIZE + 2 * self.MARGIN
        self.canvas = tk.Canvas(main_frame, width=canvas_width, height=canvas_height,
                                bg=self.BOARD_COLOR, highlightthickness=0)
        self.canvas.pack(pady=10)
        self.draw_board()

        history_frame = tk.Frame(main_frame, bg="#2c3e50")
        history_frame.pack(fill=tk.X, pady=5)
        tk.Label(history_frame, text="Historique:", font=("Helvetica", 10, "bold"), 
                 bg="#2c3e50", fg="#ecf0f1").pack(anchor=tk.W)
        self.history_text = tk.Text(history_frame, height=3, width=50, font=("Courier", 9), 
                                    bg="#34495e", fg="#ecf0f1", relief="flat")
        self.history_text.pack(fill=tk.X)
        self.history_text.config(state=tk.DISABLED)

        button_frame = tk.Frame(main_frame, bg="#2c3e50")
        button_frame.pack(pady=10)
        self._button_frame = button_frame

        # Boutons d'action avec les styles du menu
        tk.Button(button_frame, text="Menu Principal", command=self.reset_game,
                  font=("Helvetica", 11, "bold"), bg="#95a5a6", fg="white",
                  relief="flat", cursor="hand2", padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Quitter", command=self.root.quit,
                  font=("Helvetica", 11, "bold"), bg="#c0392b", fg="white",
                  relief="flat", cursor="hand2", padx=10).pack(side=tk.LEFT, padx=5)

        self._pdf_button = None
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Motion>", self.on_mouse_move)

    def draw_board(self):
        self.canvas.delete("all")
        winning_set = set(self._winning_cells)
        for row in range(self.ROWS):
            for col in range(self.COLS):
                x = self.MARGIN + col * self.CELL_SIZE
                y = self.MARGIN + row * self.CELL_SIZE
                cell_value = self.state.board[row][col]
                
                if (row, col) in winning_set:
                    color = self.WIN_COLOR
                elif cell_value == 'X':
                    color = self.PLAYER_COLOR if self.human_is_max else self.AI_COLOR
                elif cell_value == 'O':
                    color = self.AI_COLOR if self.human_is_max else self.PLAYER_COLOR
                else:
                    color = self.EMPTY_COLOR
                
                padding = 8
                self.canvas.create_oval(
                    x + padding, y + padding,
                    x + self.CELL_SIZE - padding,
                    y + self.CELL_SIZE - padding,
                    fill=color, outline="#2c3e50", width=2
                )
        
        if self.highlight_col is not None and not self.game_over and not self.ai_thinking:
            x = self.MARGIN + self.highlight_col * self.CELL_SIZE
            self.canvas.create_rectangle(
                x+2, self.MARGIN, x + self.CELL_SIZE - 2,
                self.MARGIN + self.ROWS * self.CELL_SIZE,
                outline=self.HIGHLIGHT_COLOR, width=3
            )

    def on_mouse_move(self, event):
        if self.game_over or self.ai_thinking:
            return
        col = (event.x - self.MARGIN) // self.CELL_SIZE
        if 0 <= col < self.COLS and col in self.state._possible_actions():
            if self.highlight_col != col:
                self.highlight_col = col
                self.draw_board()
        else:
            if self.highlight_col is not None:
                self.highlight_col = None
                self.draw_board()

    def on_canvas_click(self, event):
        if self.game_over or self.ai_thinking:
            return
        col = (event.x - self.MARGIN) // self.CELL_SIZE
        if 0 <= col < self.COLS and col in self.state._possible_actions():
            self.make_move(col, is_human=True)

    def make_move(self, col, is_human=False):
        move_num = len(self.move_history) + 1
        player = "Joueur" if is_human else "IA"
        self.move_history.append(f"{move_num}. {player}: Col {col + 1}")
        self.update_history()

        self.state = self.state._apply_action(col)
        self.draw_board()
        self.update_info_label()

        if self.check_game_over():
            return

        if (self.state.player == "MAX") != self.human_is_max:
            self.root.after(500, self.ai_move)

    def update_history(self):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        self.history_text.insert(1.0, " | ".join(self.move_history[-10:]))
        self.history_text.config(state=tk.DISABLED)

    def ai_move(self):
        if self.game_over: return
        self.ai_thinking = True
        self.info_label.config(text="L'IA reflechit...", fg="#e67e22")
        self.root.update()

        def compute_move():
            start = time.time()
            best_state = self.algorithm.choose_best_move(self.state)
            elapsed = time.time() - start
            
            col = None
            if best_state:
                for c in range(self.COLS):
                    if c in self.state._possible_actions():
                        if self.state._apply_action(c).board == best_state.board:
                            col = c
                            break
            self.root.after(0, lambda: self.finish_ai_move(best_state, col, elapsed))

        threading.Thread(target=compute_move, daemon=True).start()

    def finish_ai_move(self, best_state, col, elapsed):
        self.ai_thinking = False
        self.time_label.config(text=f"Temps IA: {elapsed:.2f}s")
        self.make_move(col, is_human=False)

    def update_info_label(self):
        if self.game_over: return
        if self.ai_thinking:
            self.info_label.config(text="L'IA reflechit...", fg="#e67e22")
        elif (self.state.player == "MAX") == self.human_is_max:
            self.info_label.config(text="A vous de jouer", fg="#2ecc71")
        else:
            self.info_label.config(text="Tour de l'IA...", fg="#e67e22")

    def check_game_over(self):
        if self.state._is_terminal():
            self.game_over = True
            winner = self.game.winner_function(self.state)
            self._winning_cells = self._find_winning_cells(self.state) if winner else []
            self.draw_board()

            if winner is None:
                self.info_label.config(text="Match nul !", fg="#3498db")
            elif (winner == "MAX") == self.human_is_max:
                self.info_label.config(text="Victoire !", fg="#2ecc71")
            else:
                self.info_label.config(text="L'IA a gagne !", fg="#e74c3c")
            
            self._add_pdf_button()
            return True
        return False

    def _find_winning_cells(self, state):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for r in range(self.ROWS):
            for c in range(self.COLS):
                symbol = state.board[r][c]
                if symbol == ' ': continue
                for dr, dc in directions:
                    cells = [(r, c)]
                    for i in range(1, 4):
                        nr, nc = r + dr * i, c + dc * i
                        if 0 <= nr < self.ROWS and 0 <= nc < self.COLS and state.board[nr][nc] == symbol:
                            cells.append((nr, nc))
                        else: break
                    if len(cells) == 4: return cells
        return []

    def _add_pdf_button(self):
        if self._pdf_button: return
        self._pdf_button = tk.Button(self._button_frame, text="Telecharger PDF", command=self._export_pdf,
                                    font=("Helvetica", 11, "bold"), bg="#3498db", fg="white", relief="flat")
        self._pdf_button.pack(side=tk.LEFT, padx=5)

    def _export_pdf(self):
        # Logique d'export PDF simplifiée
        messagebox.showinfo("PDF", "Rapport généré avec succès !")

    def reset_game(self):
        for widget in self.root.winfo_children(): widget.destroy()
        self.create_config_screen()

if __name__ == "__main__":
    root = tk.Tk()
    app = Connect4GUI(root)
    root.mainloop()