# FILE: PyAdverseSearch/test/test_next_move.py

from PyAdverseSearch.classes.node import Node
from PyAdverseSearch.classes.minimax import Minimax
from .state_tictactoe import generate_tictactoe_game

def test_next_move():
    print("🔵 TESTING next_move() FROM Minimax 🔵")
    # 1. Créer la partie et récupérer l'état initial
    game = generate_tictactoe_game()
    state = game.state

    # 2. Construire le nœud racine et générer ses enfants
    root = Node(state, parent=None, depth=0)
    root._expand()

    # 3. Instancier Minimax avec la même profondeur
    minimax = Minimax(game=game, max_depth=6)

    # 4. Itérer : à chaque étape, choisir next_move et afficher
    current = root
    step = 1
    while current.children and not current.state._is_terminal():
        print(f"\n--- Étape {step} ---")
        current.state.display()

        next_node = minimax.next_move(current)
        if next_node is None:
            print("Aucun coup possible.")
            break

        print("Coup choisi :")
        next_node.state.display()

        current = next_node
        step += 1

    print("Fin du test (état terminal atteint ou pas d’enfants).")

# Permet d'exécuter ce test directement si pytest n'est pas installé
if __name__ == "__main__":
    test_next_move()
