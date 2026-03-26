import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

def launch_module(module_path):
    """
    Lance un module Python en utilisant l'argument -m.
    C'est la méthode correcte pour ta structure de dossier.
    """
    try:
        subprocess.Popen([sys.executable, "-m", module_path])
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de lancer {module_path}\nErreur : {e}")

root = tk.Tk()
root.title("PyAdverseSearch Launcher")
root.geometry("400x550")
root.configure(bg="#2c3e50")

tk.Label(
    root, text="SÉLECTIONNEZ UN JEU", font=("Helvetica", 16, "bold"),
    bg="#2c3e50", fg="#ecf0f1", pady=30
).pack()
apps = [
    ("Connect 4 (Basic)", "PyAdverseSearch.Interface.connect4_gui", "#3498db"),
    ("Connect 4 (Enhanced)", "PyAdverseSearch.Interface.connect4_gui_enhanced", "#2980b9"),
    ("Reversi", "PyAdverseSearch.Interface.Reversi", "#27ae60"),
    ("Tic Tac Toe", "PyAdverseSearch.Interface.tictactoe_gui", "#e67e22"),
    ("Générateur PDF", "PyAdverseSearch.Interface.pdf_report", "#95a5a6")
]

for text, mod, color in apps:
    btn = tk.Button(
        root,
        text=text,
        command=lambda m=mod: launch_module(m),
        width=25,
        font=("Helvetica", 11, "bold"),
        bg=color,
        fg="white",
        relief="flat",
        pady=10,
        cursor="hand2"
    )
    btn.pack(pady=10)

root.mainloop()