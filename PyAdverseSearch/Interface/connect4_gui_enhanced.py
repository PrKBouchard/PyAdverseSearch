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

        # Configuration du jeu
        self.ROWS = 6
        self.COLS = 7
        self.CELL_SIZE = 80
        self.MARGIN = 10

        # Couleurs
        self.BOARD_COLOR = "#0066cc"
        self.EMPTY_COLOR = "#ffffff"
        self.PLAYER_COLOR = "#ff0000"
        self.AI_COLOR = "#ffff00"
        self.HIGHLIGHT_COLOR = "#00ff00"
        self.WIN_COLOR = "#00cc44"

        # Cellules de l'alignement gagnant (liste de (row, col))
        self._winning_cells = []

        # Variables de jeu
        self.game = None
        self.state = None
        self.algorithm = None       # AutoSolver ou algo fixe
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
        config_frame = tk.Frame(self.root, padx=20, pady=20)
        config_frame.pack()

        tk.Label(config_frame, text="Puissance 4", font=("Arial", 24, "bold")).pack(pady=10)
        tk.Label(config_frame, text="Version Enhanced AI",
                 font=("Arial", 10, "italic"), fg="gray").pack()

        tk.Label(config_frame, text="Qui commence ?", font=("Arial", 14)).pack(pady=5)
        self.start_choice = tk.StringVar(value="human")
        tk.Radiobutton(config_frame, text="Vous (Rouge)", variable=self.start_choice,
                       value="human", font=("Arial", 12)).pack()
        tk.Radiobutton(config_frame, text="IA (Jaune)", variable=self.start_choice,
                       value="ai", font=("Arial", 12)).pack()

        tk.Label(config_frame, text="Algorithme IA", font=("Arial", 14)).pack(pady=(20, 5))
        self.algo_choice = tk.StringVar(value="fast")
        tk.Radiobutton(config_frame, text="Rapide (MTD(f) + PN-Search)", variable=self.algo_choice,
                       value="fast", font=("Arial", 12, "bold"), fg="green").pack()
        tk.Radiobutton(config_frame, text="Auto Equilibre (Tous les algos)", variable=self.algo_choice,
                       value="auto", font=("Arial", 12, "bold")).pack()
        tk.Label(config_frame, text="--- Algorithmes manuels ---",
                 font=("Arial", 10), fg="gray").pack(pady=(10, 0))
        for text, val in [
            ("Minimax (Classique)", "minimax"),
            ("Alpha-Beta (Elagage)", "alphabeta"),
            ("MTD(f) (Plus efficace)", "mtdf"),
            ("Negamax (Simplifie)", "negamax"),
            ("Monte Carlo (Simulations)", "montecarlo"),
            ("PN-Search (Preuve)", "pnsearch"),
        ]:
            tk.Radiobutton(config_frame, text=text, variable=self.algo_choice,
                           value=val, font=("Arial", 12)).pack()

        tk.Label(config_frame, text="Difficulte", font=("Arial", 14)).pack(pady=(20, 5))
        self.difficulty = tk.StringVar(value="medium")
        for text, val in [
            ("Facile (profondeur 3)", "easy"),
            ("Moyen (profondeur 5)", "medium"),
            ("Difficile (profondeur 7)", "hard"),
            ("Expert (profondeur 9)", "expert"),
        ]:
            tk.Radiobutton(config_frame, text=text, variable=self.difficulty,
                           value=val, font=("Arial", 12)).pack()

        tk.Button(config_frame, text="Commencer", command=self.start_game,
                  font=("Arial", 14, "bold"), bg="#4CAF50", fg="white",
                  padx=20, pady=10).pack(pady=20)

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
            self.algorithm = AutoSolver(
                game=self.game, depth=depth, mode="classic",
                rows=self.ROWS, cols=self.COLS
            )
            self.auto_mode = True
            self.fast_mode = False
            self.current_algo_name = "Auto"

        elif algo_name == "fast":
            self.algorithm = AutoSolver(
                game=self.game, depth=depth, mode="fast",
                rows=self.ROWS, cols=self.COLS
            )
            self.auto_mode = False
            self.fast_mode = True
            self.current_algo_name = "Rapide"

        elif algo_name == "minimax":
            self.algorithm = Minimax(game=self.game, max_depth=depth)
            self.auto_mode = False
            self.fast_mode = False
            self.current_algo_name = "Minimax"

        elif algo_name == "alphabeta":
            self.algorithm = AlphaBeta(game=self.game, max_depth=depth,
                                       use_transposition_table=True)
            self.auto_mode = False
            self.fast_mode = False
            self.current_algo_name = "Alpha-Beta+TT"

        elif algo_name == "mtdf":
            timeout_map = {3: 1.0, 5: 3.0, 7: 5.0, 9: 8.0}
            self.algorithm = MTDf(game=self.game, max_depth=depth,
                                  max_time_seconds=timeout_map.get(depth, 5.0),
                                  initial_guess=0)
            self.auto_mode = False
            self.fast_mode = False
            self.current_algo_name = "MTD(f)"

        elif algo_name == "negamax":
            self.algorithm = NegamaxSolver(depth_limit=depth)
            self.auto_mode = False
            self.fast_mode = False
            self.current_algo_name = "Negamax"

        elif algo_name == "pnsearch":
            self.algorithm = PNSearch(game=self.game, max_nodes=10000 * depth,
                                      use_transposition_table=True)
            self.auto_mode = False
            self.fast_mode = False
            self.current_algo_name = "PN-Search"

        else:  # montecarlo
            self.algorithm = MonteCarlo(game=self.game, max_iterations=2000 * depth)
            self.auto_mode = False
            self.fast_mode = False
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

        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10)

        top_frame = tk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=5)

        self.info_label = tk.Label(top_frame, text="", font=("Arial", 14, "bold"))
        self.info_label.pack(side=tk.LEFT, padx=10)

        self.algo_label = tk.Label(top_frame, text="", font=("Arial", 10), fg="purple")
        self.algo_label.pack(side=tk.LEFT, padx=10)

        self.time_label = tk.Label(top_frame, text="Temps IA: --",
                                   font=("Arial", 11), fg="blue")
        self.time_label.pack(side=tk.RIGHT, padx=10)

        self.update_info_label()

        progress_frame = tk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=5)

        tk.Label(progress_frame, text="Reflexion IA:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.progress_bar = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.progress_bar.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.progress_label = tk.Label(progress_frame, text="0%", font=("Arial", 10))
        self.progress_label.pack(side=tk.LEFT, padx=5)

        stats_frame = tk.Frame(main_frame)
        stats_frame.pack(fill=tk.X, pady=5)
        self.stats_label = tk.Label(stats_frame, text="", font=("Arial", 9), fg="gray")
        self.stats_label.pack()

        canvas_width = self.COLS * self.CELL_SIZE + 2 * self.MARGIN
        canvas_height = self.ROWS * self.CELL_SIZE + 2 * self.MARGIN
        self.canvas = tk.Canvas(main_frame, width=canvas_width, height=canvas_height,
                                bg=self.BOARD_COLOR)
        self.canvas.pack(pady=10)
        self.draw_board()

        history_frame = tk.Frame(main_frame)
        history_frame.pack(fill=tk.X, pady=5)
        tk.Label(history_frame, text="Historique:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.history_text = tk.Text(history_frame, height=3, width=50, font=("Courier", 9))
        self.history_text.pack(fill=tk.X)
        self.history_text.config(state=tk.DISABLED)

        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)
        self._button_frame = button_frame

        tk.Button(button_frame, text="Nouvelle Partie", command=self.reset_game,
                  font=("Arial", 12), padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Quitter", command=self.root.quit,
                  font=("Arial", 12), padx=10).pack(side=tk.LEFT, padx=5)

        # Le bouton PDF sera ajoute a la fin de la partie
        self._pdf_button = None

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Motion>", self.on_mouse_move)

    # ------------------------------------------------------------------
    # Dessin du plateau
    # ------------------------------------------------------------------

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
                padding = 5
                outline_w = 3 if (row, col) in winning_set else 2
                self.canvas.create_oval(
                    x + padding, y + padding,
                    x + self.CELL_SIZE - padding,
                    y + self.CELL_SIZE - padding,
                    fill=color, outline="black", width=outline_w
                )
        if self.highlight_col is not None and not self.game_over and not self.ai_thinking:
            x = self.MARGIN + self.highlight_col * self.CELL_SIZE
            self.canvas.create_rectangle(
                x, 0, x + self.CELL_SIZE,
                self.MARGIN + self.ROWS * self.CELL_SIZE,
                outline=self.HIGHLIGHT_COLOR, width=3, stipple="gray50"
            )

    # ------------------------------------------------------------------
    # Evenements souris
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Gestion des coups
    # ------------------------------------------------------------------

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
        recent_moves = self.move_history[-10:]
        self.history_text.insert(1.0, " | ".join(recent_moves))
        self.history_text.config(state=tk.DISABLED)

    # ------------------------------------------------------------------
    # Tour de l'IA
    # ------------------------------------------------------------------

    def ai_move(self):
        if self.game_over:
            return

        # Mettre a jour le nom de l'algo affiche si on est en mode auto/fast
        if self.auto_mode or self.fast_mode:
            # Le nom sera mis a jour apres le calcul via les records AutoSolver
            pass

        self.ai_thinking = True
        self.info_label.config(text=f"L'IA reflechit ({self.current_algo_name})...", fg="orange")
        self.progress_bar['value'] = 0
        self.progress_label.config(text="0%")
        self.root.update()

        def compute_move():
            start = time.time()
            best_state = None
            try:
                if isinstance(self.algorithm, AutoSolver):
                    best_state = self.algorithm.choose_best_move(self.state)
                elif isinstance(self.algorithm, NegamaxSolver):
                    from PyAdverseSearch.classes.node import Node
                    root_node = Node(self.state)
                    best_board = self.algorithm.get_best_move(root_node)
                    for c in self.state._possible_actions():
                        test_state = self.state._apply_action(c)
                        if test_state.board == best_board:
                            best_state = test_state
                            break
                else:
                    best_state = self.algorithm.choose_best_move(self.state)
            except Exception as e:
                print(f"Erreur dans compute_move: {e}")
                import traceback
                traceback.print_exc()

            elapsed = time.time() - start

            col = None
            if best_state:
                for c in range(self.COLS):
                    if c in self.state._possible_actions():
                        test_state = self.state._apply_action(c)
                        if test_state.board == best_state.board:
                            col = c
                            break

            self.root.after(0, lambda: self.finish_ai_move(best_state, col, elapsed))

        thread = threading.Thread(target=compute_move)
        thread.daemon = True
        thread.start()

    def finish_ai_move(self, best_state, col, elapsed):
        self.ai_thinking = False

        if best_state is None or col is None:
            messagebox.showerror("Erreur", "L'IA n'a pas trouve de coup valide")
            return

        self.time_label.config(text=f"Temps IA: {elapsed:.2f}s")
        self.progress_bar['value'] = 100
        self.progress_label.config(text="100%")

        # Mettre a jour le nom de l'algo courant depuis AutoSolver
        if isinstance(self.algorithm, AutoSolver):
            self.current_algo_name = self.algorithm.current_algo_name()
            mode_tag = "[RAPIDE]" if self.fast_mode else "[AUTO]"
            self.algo_label.config(text=f"{mode_tag} {self.current_algo_name}")
            reason = self.algorithm.current_reason()
            self.stats_label.config(
                text=f"{reason} | {elapsed:.2f}s",
                fg="green" if self.fast_mode else "purple"
            )
        elif isinstance(self.algorithm, (AlphaBeta, MTDf)):
            stats = self.algorithm.get_statistics()
            nodes = stats.get('nodes_explored', 0)
            cutoffs = stats.get('cutoffs', 0)
            tt_hit = stats.get('tt_hit_rate', None)
            tt_str = f", TT hit: {tt_hit:.0f}%" if tt_hit is not None else ""
            self.stats_label.config(
                text=f"[{self.current_algo_name}] {nodes:,} noeuds, "
                     f"{cutoffs:,} coupures{tt_str} en {elapsed:.2f}s",
                fg="gray"
            )
        elif isinstance(self.algorithm, PNSearch):
            stats = self.algorithm.get_statistics()
            nodes = stats.get('nodes_explored', 0)
            tt_size = stats.get('transposition_table_size', 0)
            self.stats_label.config(
                text=f"[{self.current_algo_name}] {nodes:,} noeuds, "
                     f"TT: {tt_size} entrees en {elapsed:.2f}s",
                fg="gray"
            )
        elif isinstance(self.algorithm, NegamaxSolver):
            nodes = getattr(self.algorithm, 'nodes_visited', 0)
            cutoffs = getattr(self.algorithm, 'cutoffs', 0)
            self.stats_label.config(
                text=f"[{self.current_algo_name}] {nodes:,} noeuds, "
                     f"{cutoffs:,} coupures en {elapsed:.2f}s",
                fg="gray"
            )
        elif isinstance(self.algorithm, Minimax):
            nodes = getattr(self.algorithm, 'nodes_explored', 0)
            self.stats_label.config(
                text=f"[{self.current_algo_name}] {nodes:,} noeuds en {elapsed:.2f}s "
                     f"(profondeur {self.algorithm.max_depth})",
                fg="gray"
            )
        elif isinstance(self.algorithm, MonteCarlo):
            self.stats_label.config(
                text=f"[{self.current_algo_name}] {self.algorithm.max_iterations} simulations "
                     f"en {elapsed:.2f}s",
                fg="gray"
            )
        else:
            self.stats_label.config(
                text=f"[{self.current_algo_name}] Calcul termine en {elapsed:.2f}s",
                fg="gray"
            )

        self.make_move(col, is_human=False)

    # ------------------------------------------------------------------
    # Info label
    # ------------------------------------------------------------------

    def update_info_label(self):
        if self.game_over:
            return
        if self.auto_mode:
            self.algo_label.config(text=f"[AUTO] {self.current_algo_name}")
        elif self.fast_mode:
            self.algo_label.config(text=f"[RAPIDE] {self.current_algo_name}")
        else:
            self.algo_label.config(text=f"Algo: {self.current_algo_name}")

        if self.ai_thinking:
            self.info_label.config(text="L'IA reflechit...", fg="orange")
            return

        current_is_max = (self.state.player == "MAX")
        if current_is_max != self.human_is_max:
            self.info_label.config(text="Tour de l'IA...", fg="orange")
        else:
            self.info_label.config(text="Votre tour (cliquez sur une colonne)", fg="green")

    # ------------------------------------------------------------------
    # Fin de partie
    # ------------------------------------------------------------------

    def check_game_over(self):
        if self.state._is_terminal():
            self.game_over = True
            winner = self.game.winner_function(self.state)

            # Calculer et stocker les cellules de l'alignement gagnant
            self._winning_cells = self._find_winning_cells(self.state) if winner else []
            # Redessiner avec les pieces gagnantes en vert
            self.draw_board()

            if winner is None:
                message = "Match nul !"
                self.info_label.config(text=message, fg="blue")
                self._winner_key = "Match nul"
            elif (winner == "MAX") == self.human_is_max:
                message = "Vous avez gagne ! Felicitations !"
                self.info_label.config(text=message, fg="green")
                self._winner_key = "Joueur"
            else:
                message = "L'IA a gagne !"
                self.info_label.config(text=message, fg="red")
                self._winner_key = "IA"

            # Ajouter le bouton de telechargement PDF
            self._add_pdf_button()

            messagebox.showinfo("Fin de partie", message)
            return True
        return False

    def _find_winning_cells(self, state):
        """Retourne la liste des (row, col) qui forment l'alignement gagnant."""
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
                        if not (0 <= nr < self.ROWS and 0 <= nc < self.COLS):
                            break
                        if state.board[nr][nc] != symbol:
                            break
                        cells.append((nr, nc))
                    if len(cells) == 4:
                        return cells
        return []

    def _add_pdf_button(self):
        """Ajoute le bouton d'export PDF dans la barre de boutons."""
        if self._pdf_button is not None:
            return
        self._pdf_button = tk.Button(
            self._button_frame,
            text="Telecharger le rapport PDF",
            command=self._export_pdf,
            font=("Arial", 12, "bold"),
            bg="#1565C0",
            fg="white",
            padx=10,
        )
        self._pdf_button.pack(side=tk.LEFT, padx=5)

    def _export_pdf(self):
        """Prepare les donnees et lance la generation du PDF."""
        duration = time.time() - self.game_start_time if self.game_start_time else 0.0

        algo_mode = self.algo_choice.get()  # "auto", "fast", "minimax", etc.

        game_summary = {
            "winner": self._winner_key,
            "total_moves": len(self.move_history),
            "duration": duration,
            "algo_mode": algo_mode,
            "difficulty": self.difficulty.get(),
            "human_starts": self.start_choice.get() == "human",
        }

        # Recuperer les records depuis AutoSolver ou construire un record simple
        if isinstance(self.algorithm, AutoSolver):
            algo_records = self.algorithm.get_records()
        else:
            # Pour les algos fixes, on construit un enregistrement synthetique
            # a partir de l'historique des coups IA
            algo_records = []
            move_num = 0
            for entry in self.move_history:
                if "IA" in entry:
                    move_num += 1
                    algo_records.append({
                        "move_number": move_num,
                        "algo_name": self.current_algo_name,
                        "reason": f"Algorithme fixe selectionne manuellement",
                        "elapsed": 0.0,
                        "stats": {},
                    })

        export_game_pdf(game_summary, self.move_history, algo_records)

    # ------------------------------------------------------------------
    # Reset
    # ------------------------------------------------------------------

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
