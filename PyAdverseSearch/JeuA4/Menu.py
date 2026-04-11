import tkinter as tk

class Menu:
    def __init__(self, root):
        self.root = root
        self.root.title("Configuration du jeu")

        self.frame = tk.Frame(root)
        self.frame.pack(padx=20, pady=20)

        tk.Label(self.frame, text="Nombre de joueurs humains :", font=("Arial", 14)).pack(pady=10)

        self.player_count = tk.IntVar(value=1)

        for i in range(1, 5):
            tk.Radiobutton(
                self.frame,
                text=f"{i} joueur(s)",
                variable=self.player_count,
                value=i
            ).pack(anchor="w")

        tk.Button(self.frame, text="Lancer le jeu", command=self.start_game).pack(pady=20)

    def start_game(self):
        human_count = self.player_count.get()

        human_players = PLAYERS[:human_count]

        self.frame.destroy()

        TerritoryWindow(self.root, human_players)