# FILE: connect4_gui.py

import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os

# Ajouter le chemin parent pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyAdverseSearch.test.state_connect4 import generate_connect4_game
from PyAdverseSearch.classes.minimax import Minimax
from PyAdverseSearch.classes.alphabeta import AlphaBeta
from PyAdverseSearch.classes.montecarlo import MonteCarlo

class Connect4GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Puissance 4")
        self.root.resizable(False, False)
        
        self.ROWS = 6
        self.COLS = 7
        self.CELL_SIZE = 80
        self.MARGIN = 10

        self.BOARD_COLOR = "#0066cc"
        self.EMPTY_COLOR = "#ffffff"
        self.PLAYER_COLOR = "#ff0000"
        self.AI_COLOR = "#ffff00"
        self.HIGHLIGHT_COLOR = "#00ff00"
        
        self.game = None
        self.state = None
        self.algorithm = None
        self.human_is_max = None
        self.game_over = False
        
        # Interface de configuration
        self.create_config_screen()
        
    def create_config_screen(self):
        """Écran de configuration initiale"""
        config_frame = tk.Frame(self.root, padx=20, pady=20)
        config_frame.pack()
        
        # Titre
        title = tk.Label(config_frame, text="Puissance 4", font=("Arial", 24, "bold"))
        title.pack(pady=10)
        
        # Choix du joueur qui commence
        tk.Label(config_frame, text="Qui commence ?", font=("Arial", 14)).pack(pady=5)
        self.start_choice = tk.StringVar(value="human")
        tk.Radiobutton(config_frame, text="Vous (Rouge)", variable=self.start_choice, 
                      value="human", font=("Arial", 12)).pack()
        tk.Radiobutton(config_frame, text="IA (Jaune)", variable=self.start_choice, 
                      value="ai", font=("Arial", 12)).pack()
        
        # Choix de l'algorithme
        tk.Label(config_frame, text="Algorithme IA", font=("Arial", 14)).pack(pady=(20, 5))
        self.algo_choice = tk.StringVar(value="minimax")
        tk.Radiobutton(config_frame, text="Minimax", variable=self.algo_choice, 
                      value="minimax", font=("Arial", 12)).pack()
        tk.Radiobutton(config_frame, text="Alpha-Beta", variable=self.algo_choice, 
                      value="alphabeta", font=("Arial", 12)).pack()
        tk.Radiobutton(config_frame, text="Monte Carlo", variable=self.algo_choice, 
                      value="montecarlo", font=("Arial", 12)).pack()
        
        # Choix de la difficulté
        tk.Label(config_frame, text="Difficulté", font=("Arial", 14)).pack(pady=(20, 5))
        self.difficulty = tk.StringVar(value="medium")
        tk.Radiobutton(config_frame, text="Facile (profondeur 3)", variable=self.difficulty, 
                      value="easy", font=("Arial", 12)).pack()
        tk.Radiobutton(config_frame, text="Moyen (profondeur 5)", variable=self.difficulty, 
                      value="medium", font=("Arial", 12)).pack()
        tk.Radiobutton(config_frame, text="Difficile (profondeur 7)", variable=self.difficulty, 
                      value="hard", font=("Arial", 12)).pack()
        
        # Bouton de démarrage
        start_btn = tk.Button(config_frame, text="Commencer", command=self.start_game,
                             font=("Arial", 14, "bold"), bg="#4CAF50", fg="white",
                             padx=20, pady=10)
        start_btn.pack(pady=20)
        
    def start_game(self):
        """Initialise et démarre le jeu"""
        # Déterminer qui commence
        if self.start_choice.get() == "human":
            self.human_is_max = True
            max_starting = True
        else:
            self.human_is_max = False
            max_starting = False
        
        self.game = generate_connect4_game(max_starting)
        self.state = self.game.state
        
        depth_map = {"easy": 3, "medium": 5, "hard": 7}
        depth = depth_map[self.difficulty.get()]
        
        # Créer l'algorithme
        algo_name = self.algo_choice.get()
        if algo_name == "minimax":
            self.algorithm = Minimax(game=self.game, max_depth=depth)
        elif algo_name == "alphabeta":
            self.algorithm = AlphaBeta(game=self.game, max_depth=depth)
        else:  # montecarlo
            iterations = 1000 * depth  # Plus de profondeur = plus d'itérations
            self.algorithm = MonteCarlo(game=self.game, max_iterations=iterations)
        
        # Détruire l'écran de configuration et créer le plateau
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.create_game_board()
        
        # Si l'IA commence, faire son coup
        current_is_max = (self.state.player == "MAX")
        if current_is_max != self.human_is_max:
            self.root.after(500, self.ai_move)
    
    def create_game_board(self):
        """Crée l'interface du plateau de jeu"""
        # Initialiser highlight_col avant tout
        self.highlight_col = None
        
        # Frame principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10)
        
        # Label d'information
        self.info_label = tk.Label(main_frame, text="", font=("Arial", 14, "bold"))
        self.info_label.pack(pady=10)
        self.update_info_label()
        
        # Canvas pour le plateau
        canvas_width = self.COLS * self.CELL_SIZE + 2 * self.MARGIN
        canvas_height = self.ROWS * self.CELL_SIZE + 2 * self.MARGIN
        
        self.canvas = tk.Canvas(main_frame, width=canvas_width, height=canvas_height,
                               bg=self.BOARD_COLOR)
        self.canvas.pack()
        
        # Dessiner la grille
        self.draw_board()
        
        # Boutons en bas
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Nouvelle Partie", command=self.reset_game,
                 font=("Arial", 12), padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Quitter", command=self.root.quit,
                 font=("Arial", 12), padx=10).pack(side=tk.LEFT, padx=5)
        
        # Bind pour les clics de colonne
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Motion>", self.on_mouse_move)
    
    def draw_board(self):
        """Dessine le plateau de jeu"""
        self.canvas.delete("all")
        
        # Dessiner les cercles
        for row in range(self.ROWS):
            for col in range(self.COLS):
                x = self.MARGIN + col * self.CELL_SIZE
                y = self.MARGIN + row * self.CELL_SIZE
                
                # Déterminer la couleur
                cell_value = self.state.board[row][col]
                if cell_value == 'X':
                    # X est joué par MAX
                    # Si human_is_max est True, alors le joueur est MAX (rouge)
                    # Sinon l'IA est MAX (jaune)
                    color = self.PLAYER_COLOR if self.human_is_max else self.AI_COLOR
                elif cell_value == 'O':
                    # O est joué par MIN
                    # Si human_is_max est True, alors l'IA est MIN (jaune)
                    # Sinon le joueur est MIN (rouge)
                    color = self.AI_COLOR if self.human_is_max else self.PLAYER_COLOR
                else:
                    color = self.EMPTY_COLOR
                
                # Dessiner le cercle
                padding = 5
                self.canvas.create_oval(x + padding, y + padding,
                                       x + self.CELL_SIZE - padding,
                                       y + self.CELL_SIZE - padding,
                                       fill=color, outline="black", width=2)
        
        # Surligner la colonne si la souris est dessus
        if self.highlight_col is not None and not self.game_over:
            x = self.MARGIN + self.highlight_col * self.CELL_SIZE
            self.canvas.create_rectangle(x, 0, x + self.CELL_SIZE, 
                                        self.MARGIN + self.ROWS * self.CELL_SIZE,
                                        outline=self.HIGHLIGHT_COLOR, width=3, 
                                        stipple="gray50")
    
    def on_mouse_move(self, event):
        """Gère le survol de la souris"""
        if self.game_over:
            return
        
        # Vérifier si c'est le tour du joueur humain
        current_is_max = (self.state.player == "MAX")
        if current_is_max != self.human_is_max:
            # C'est le tour de l'IA, pas de surlignage
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
        """Gère les clics sur le canvas"""
        if self.game_over:
            return
        
        # Déterminer si c'est le tour de l'humain
        current_is_max = (self.state.player == "MAX")
        if current_is_max != self.human_is_max:
            return  # C'est le tour de l'IA, on n'accepte pas les clics
        
        # Déterminer la colonne cliquée
        col = (event.x - self.MARGIN) // self.CELL_SIZE
        
        if 0 <= col < self.COLS and col in self.state._possible_actions():
            self.make_move(col)
    
    def make_move(self, col):
        """Applique un coup humain"""
        # Appliquer l'action
        self.state = self.state._apply_action(col)
        self.draw_board()
        self.update_info_label()
        
        # Vérifier fin de partie
        if self.check_game_over():
            return
        
        # Tour de l'IA - vérifier que c'est bien son tour maintenant
        current_is_max = (self.state.player == "MAX")
        if current_is_max != self.human_is_max:
            self.root.after(500, self.ai_move)
    
    def ai_move(self):
        """Fait jouer l'IA"""
        if self.game_over:
            return
        
        self.info_label.config(text="L'IA réfléchit...")
        self.root.update()
        
        # L'IA choisit son coup
        best_state = self.algorithm.choose_best_move(self.state)
        
        if best_state is None:
            messagebox.showerror("Erreur", "L'IA n'a pas trouvé de coup valide")
            return
        
        self.state = best_state
        self.draw_board()
        self.update_info_label()
        
        # Vérifier fin de partie
        self.check_game_over()
    
    def update_info_label(self):
        """Met à jour le label d'information"""
        if self.game_over:
            return
        
        current_is_max = (self.state.player == "MAX")
        if current_is_max != self.human_is_max:
            self.info_label.config(text="Tour de l'IA...", fg="orange")
        else:
            self.info_label.config(text="Votre tour (cliquez sur une colonne)", fg="green")
    
    def check_game_over(self):
        """Vérifie si le jeu est terminé"""
        if self.state._is_terminal():
            self.game_over = True
            winner = self.game.winner_function(self.state)
            
            if winner is None:
                message = "Match nul !"
                self.info_label.config(text=message, fg="blue")
            elif (winner == "MAX") == self.human_is_max:
                message = "Vous avez gagné ! Félicitations !"
                self.info_label.config(text=message, fg="green")
            else:
                message = "L'IA a gagné !"
                self.info_label.config(text=message, fg="red")
            
            messagebox.showinfo("Fin de partie", message)
            return True
        
        return False
    
    def reset_game(self):
        """Réinitialise le jeu"""
        self.game_over = False
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_config_screen()

def main():
    root = tk.Tk()
    app = Connect4GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()