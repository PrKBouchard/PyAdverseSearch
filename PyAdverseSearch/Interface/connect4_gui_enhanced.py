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

try:
    from PyAdverseSearch.classes.mtdf import MTDf
    from PyAdverseSearch.classes.negamax import NegamaxSolver
    from PyAdverseSearch.classes.pnsearch import PNSearch
    from PyAdverseSearch.classes.autosolver import AutoSolver
    ADVANCED_ALGOS = True
except ImportError:
    ADVANCED_ALGOS = False


class EnhancedAlgorithm:
    """Wrapper pour suivre les performances de l'algorithme"""
    def __init__(self, algorithm, callback=None, algo_name=""):
        self.algorithm = algorithm
        self.callback = callback
        self.algo_name = algo_name
        self.nodes_explored = 0
        self.start_time = None
        self.elapsed_time = 0
        
    def choose_best_move(self, state):
        self.nodes_explored = 0
        self.start_time = time.time()
        
        # Pour Monte Carlo, on peut suivre les itérations
        if isinstance(self.algorithm, MonteCarlo):
            return self._choose_best_move_mcts(state)
        else:
            return self._choose_best_move_standard(state)
    
    def _choose_best_move_mcts(self, state):
        """Version avec suivi pour Monte Carlo"""
        max_iterations = self.algorithm.max_iterations
        step = max(1, max_iterations // 50)  # Updates tous les 2%
        
        best_state = None
        for i in range(0, max_iterations, step):
            remaining = max_iterations - i
            self.algorithm.max_iterations = min(step, remaining)
            best_state = self.algorithm.choose_best_move(state)
            
            self.nodes_explored = min(i + step, max_iterations)
            progress = min(100, (self.nodes_explored / max_iterations) * 100)
            
            if self.callback:
                self.callback(progress, self.nodes_explored, max_iterations)
        
        self.algorithm.max_iterations = max_iterations
        self.elapsed_time = time.time() - self.start_time
        return best_state
    
    def _choose_best_move_standard(self, state):
        """Version standard pour les autres algorithmes"""
        best_state = None
        finished = False
        
        # Lancer dans un thread pour ne pas bloquer l'UI
        def compute():
            nonlocal best_state, finished
            best_state = self.algorithm.choose_best_move(state)
            finished = True
        
        thread = threading.Thread(target=compute)
        thread.daemon = True
        thread.start()
        
        # Simuler la progression pendant le calcul
        start = time.time()
        while not finished:
            elapsed = time.time() - start
            # Estimation basée sur le temps (max 10s attendu pour difficulté normale)
            estimated_time = 10.0
            progress = min(95, (elapsed / estimated_time) * 100)
            
            if self.callback:
                self.callback(progress, 0, 0)
            
            time.sleep(0.05)
        
        # Terminer à 100%
        if self.callback:
            self.callback(100, 0, 0)
        
        self.elapsed_time = time.time() - start
        return best_state


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
        self.BOARD_COLOR = "#34495e"    # Bleu-gris sombre
        self.EMPTY_COLOR = "#ecf0f1"    # Gris très clair
        self.PLAYER_COLOR = "#e74c3c"   # Rouge
        self.AI_COLOR = "#f1c40f"       # Jaune
        self.HIGHLIGHT_COLOR = "#2ecc71" # Vert
        self.WIN_COLOR = "#27ae60"      # Vert sombre

        # Cellules de l'alignement gagnant
        self._winning_cells = []

        # Variables de jeu
        self.game = None
        self.state = None
        self.algorithm = None
        self.enhanced_algo = None
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
        
        self.algo_choice = tk.StringVar(value="alphabeta")
        
        # Algorithmes de base
        tk.Radiobutton(config_frame, text="Minimax (Classique)", variable=self.algo_choice,
                       value="minimax", font=("Helvetica", 12), bg="#2c3e50", fg="#ecf0f1", 
                       selectcolor="#34495e").pack()
        tk.Radiobutton(config_frame, text="Alpha-Beta (Recommandé)", variable=self.algo_choice,
                       value="alphabeta", font=("Helvetica", 12, "bold"), bg="#2c3e50", fg="#2ecc71", 
                       selectcolor="#34495e").pack()
        tk.Radiobutton(config_frame, text="Monte Carlo (Simulations)", variable=self.algo_choice,
                       value="montecarlo", font=("Helvetica", 12), bg="#2c3e50", fg="#ecf0f1", 
                       selectcolor="#34495e").pack()
        
        # Algorithmes avancés si disponibles
        if ADVANCED_ALGOS:
            tk.Label(config_frame, text="--- Algorithmes avancés ---",
                     font=("Helvetica", 10), bg="#2c3e50", fg="#bdc3c7").pack(pady=(10, 0))
            
            tk.Radiobutton(config_frame, text="Rapide (Auto-optimisé)", variable=self.algo_choice,
                           value="fast", font=("Helvetica", 12, "bold"), bg="#2c3e50", fg="#9b59b6", 
                           selectcolor="#34495e").pack()
            tk.Radiobutton(config_frame, text="Auto Équilibré", variable=self.algo_choice,
                           value="auto", font=("Helvetica", 12), bg="#2c3e50", fg="#9b59b6", 
                           selectcolor="#34495e").pack()
            tk.Radiobutton(config_frame, text="MTD(f)", variable=self.algo_choice,
                           value="mtdf", font=("Helvetica", 12), bg="#2c3e50", fg="#ecf0f1", 
                           selectcolor="#34495e").pack()
            tk.Radiobutton(config_frame, text="Negamax", variable=self.algo_choice,
                           value="negamax", font=("Helvetica", 12), bg="#2c3e50", fg="#ecf0f1", 
                           selectcolor="#34495e").pack()
            tk.Radiobutton(config_frame, text="PN-Search", variable=self.algo_choice,
                           value="pnsearch", font=("Helvetica", 12), bg="#2c3e50", fg="#ecf0f1", 
                           selectcolor="#34495e").pack()

        tk.Label(config_frame, text="Difficulté", font=("Helvetica", 14), 
                 bg="#2c3e50", fg="#ecf0f1").pack(pady=(20, 5))
        
        self.difficulty = tk.StringVar(value="medium")
        for text, val in [
            ("Facile (Prof. 3)", "easy"),
            ("Moyen (Prof. 5)", "medium"),
            ("Difficile (Prof. 7)", "hard"),
            ("Expert (Prof. 9)", "expert"),
        ]:
            tk.Radiobutton(config_frame, text=text, variable=self.difficulty,
                           value=val, font=("Helvetica", 12), bg="#2c3e50", fg="#ecf0f1", 
                           selectcolor="#34495e").pack()

        tk.Button(config_frame, text="COMMENCER", command=self.start_game,
                  font=("Helvetica", 14, "bold"), bg="#27ae60", fg="white",
                  relief="flat", cursor="hand2", padx=20, pady=10).pack(pady=20)

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

        # Créer l'algorithme selon le choix
        if ADVANCED_ALGOS and algo_name == "auto":
            self.algorithm = AutoSolver(game=self.game, depth=depth, mode="classic", rows=self.ROWS, cols=self.COLS)
            self.current_algo_name = "Auto"
        elif ADVANCED_ALGOS and algo_name == "fast":
            self.algorithm = AutoSolver(game=self.game, depth=depth, mode="fast", rows=self.ROWS, cols=self.COLS)
            self.current_algo_name = "Rapide"
        elif algo_name == "minimax":
            self.algorithm = Minimax(game=self.game, max_depth=depth)
            self.current_algo_name = "Minimax"
        elif algo_name == "alphabeta":
            self.algorithm = AlphaBeta(game=self.game, max_depth=depth)
            self.current_algo_name = "Alpha-Beta"
        elif ADVANCED_ALGOS and algo_name == "mtdf":
            self.algorithm = MTDf(game=self.game, max_depth=depth, initial_guess=0)
            self.current_algo_name = "MTD(f)"
        elif ADVANCED_ALGOS and algo_name == "negamax":
            self.algorithm = NegamaxSolver(depth_limit=depth)
            self.current_algo_name = "Negamax"
        elif ADVANCED_ALGOS and algo_name == "pnsearch":
            self.algorithm = PNSearch(game=self.game, use_transposition_table=True)
            self.current_algo_name = "PN-Search"
        else:  # montecarlo
            self.algorithm = MonteCarlo(game=self.game, max_iterations=2000 * depth)
            self.current_algo_name = "Monte Carlo"

        # Wrapper pour suivre les performances
        self.enhanced_algo = EnhancedAlgorithm(
            self.algorithm, 
            callback=self.update_ai_progress,
            algo_name=self.current_algo_name
        )

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

        self.algo_label = tk.Label(top_frame, text=f"Algorithme: {self.current_algo_name}", 
                                   font=("Helvetica", 10), bg="#2c3e50", fg="#9b59b6")
        self.algo_label.pack(side=tk.LEFT, padx=10)

        self.time_label = tk.Label(top_frame, text="Temps IA: --",
                                   font=("Helvetica", 11), bg="#2c3e50", fg="#3498db")
        self.time_label.pack(side=tk.RIGHT, padx=10)

        self.update_info_label()

        progress_frame = tk.Frame(main_frame, bg="#2c3e50")
        progress_frame.pack(fill=tk.X, pady=5)

        style = ttk.Style()
        style.theme_use('default')
        style.configure("TProgressbar", thickness=15, troughcolor='#34495e', background='#2ecc71')

        tk.Label(progress_frame, text="Réflexion IA:", font=("Helvetica", 10), 
                 bg="#2c3e50", fg="#bdc3c7").pack(side=tk.LEFT, padx=5)
        self.progress_bar = ttk.Progressbar(progress_frame, length=400, mode='determinate', style="TProgressbar")
        self.progress_bar.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.progress_label = tk.Label(progress_frame, text="0%", font=("Helvetica", 10), 
                                       bg="#2c3e50", fg="#bdc3c7")
        self.progress_label.pack(side=tk.LEFT, padx=5)

        stats_frame = tk.Frame(main_frame, bg="#2c3e50")
        stats_frame.pack(fill=tk.X, pady=5)
        self.stats_label = tk.Label(stats_frame, text="Prêt à jouer", font=("Helvetica", 9), 
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
        current_is_max = (self.state.player == "MAX")
        if current_is_max != self.human_is_max:
            if self.highlight_col is not None:
                self.highlight_col = None
                self.draw_board()
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
        current_is_max = (self.state.player == "MAX")
        if current_is_max != self.human_is_max:
            return
        
        col = (event.x - self.MARGIN) // self.CELL_SIZE
        if 0 <= col < self.COLS and col in self.state._possible_actions():
            self.make_move(col, is_human=True)

    def make_move(self, col, is_human=False):
        move_num = len(self.move_history) + 1
        player = "Vous" if is_human else "IA"
        self.move_history.append(f"{move_num}. {player}: Col {col + 1}")
        self.update_history()

        self.state = self.state._apply_action(col)
        self.draw_board()
        self.update_info_label()

        if self.check_game_over():
            return

        current_is_max = (self.state.player == "MAX")
        if current_is_max != self.human_is_max:
            self.root.after(500, self.ai_move)

    def update_history(self):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        self.history_text.insert(1.0, " | ".join(self.move_history[-10:]))
        self.history_text.config(state=tk.DISABLED)

    def ai_move(self):
        if self.game_over:
            return
        
        self.ai_thinking = True
        self.info_label.config(text="L'IA réfléchit...", fg="#e67e22")
        self.progress_bar['value'] = 0
        self.progress_label.config(text="0%")
        self.stats_label.config(text="Calcul en cours...")
        self.root.update()

        # Utiliser l'algorithme amélioré avec callback
        def compute_move():
            best_state = self.enhanced_algo.choose_best_move(self.state)
            elapsed = self.enhanced_algo.elapsed_time
            
            col = None
            if best_state:
                for c in range(self.COLS):
                    if c in self.state._possible_actions():
                        if self.state._apply_action(c).board == best_state.board:
                            col = c
                            break
            
            self.root.after(0, lambda: self.finish_ai_move(best_state, col, elapsed))

        thread = threading.Thread(target=compute_move, daemon=True)
        thread.start()

    def update_ai_progress(self, progress, nodes, total):
        """Callback pour mettre à jour la progression de l'IA"""
        self.progress_bar['value'] = progress
        self.progress_label.config(text=f"{int(progress)}%")
        
        if isinstance(self.algorithm, MonteCarlo):
            if total > 0:
                self.stats_label.config(text=f"Simulations: {nodes}/{total}")
        else:
            self.stats_label.config(text=f"Exploration en cours... ({progress:.1f}%)")
        
        self.root.update()

    def finish_ai_move(self, best_state, col, elapsed):
        self.ai_thinking = False
        self.time_label.config(text=f"Temps IA: {elapsed:.2f}s")
        self.progress_bar['value'] = 100
        self.progress_label.config(text="100%")
        
        if isinstance(self.algorithm, MonteCarlo):
            self.stats_label.config(
                text=f"✓ {self.algorithm.max_iterations} simulations en {elapsed:.2f}s"
            )
        else:
            depth = getattr(self.algorithm, 'max_depth', '?')
            self.stats_label.config(
                text=f"✓ Calcul terminé en {elapsed:.2f}s (prof. {depth})"
            )
        
        if best_state and col is not None:
            self.make_move(col, is_human=False)

    def update_info_label(self):
        if self.game_over:
            return
        if self.ai_thinking:
            self.info_label.config(text="L'IA réfléchit...", fg="#e67e22")
        else:
            current_is_max = (self.state.player == "MAX")
            if current_is_max == self.human_is_max:
                self.info_label.config(text="À vous de jouer", fg="#2ecc71")
            else:
                self.info_label.config(text="Tour de l'IA...", fg="#e67e22")

    def check_game_over(self):
        if self.state._is_terminal():
            self.game_over = True
            winner = self.game.winner_function(self.state)
            self._winning_cells = self._find_winning_cells(self.state) if winner else []
            self.draw_board()

            if winner is None:
                message = "Match nul !"
                self.info_label.config(text=message, fg="#3498db")
            elif (winner == "MAX") == self.human_is_max:
                message = "Vous avez gagné ! Félicitations !"
                self.info_label.config(text=message, fg="#2ecc71")
            else:
                message = "L'IA a gagné !"
                self.info_label.config(text=message, fg="#e74c3c")
            
            messagebox.showinfo("Fin de partie", message)
            return True
        return False

    def _find_winning_cells(self, state):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for r in range(self.ROWS):
            for c in range(self.COLS):
                symbol = state.board[r][c]
                if symbol == ' ':
                    continue
                for dr, dc in directions:
                    cells = [(r, c)]
                    for i in range(1, 4):
                        nr, nc = r + dr * i, c + dc * i
                        if 0 <= nr < self.ROWS and 0 <= nc < self.COLS and state.board[nr][nc] == symbol:
                            cells.append((nr, nc))
                        else:
                            break
                    if len(cells) == 4:
                        return cells
        return []

    def reset_game(self):
        self.game_over = False
        self.ai_thinking = False
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_config_screen()


def main():
    root = tk.Tk()
    app = Connect4GUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()