# FILE: PyAdverseSearch/tools/test_tools.py
import matplotlib.pyplot as plt
from PyAdverseSearch.test.state_tictactoe import generate_tictactoe_game
from PyAdverseSearch.classes.negamax import NegamaxSolver
from PyAdverseSearch.classes.node import Node
from PyAdverseSearch.tools.tracer import SearchTracer
from PyAdverseSearch.tools.visualizer import TreeVisualizer

def run_test():
    # 1. Setup the game
    game = generate_tictactoe_game(isMaxStartingParameter=True)
    root_state = game.state
    root_node = Node(state=root_state)

    # 2. Initialize the Tracer
    tracer = SearchTracer()

    # 3. Initialize Solver with Tracer
    # Use a small depth (2 or 3) so the graph isn't too crowded at first
    solver = NegamaxSolver(depth_limit=3, tracer=tracer)
    
    print("AI is thinking...")
    solver.get_best_move(root_node)
    print(f"Done! Captured {len(tracer.history)} steps.")

    # 4. Launch Visualizer
    viz = TreeVisualizer(tracer)
    plt.show()

if __name__ == "__main__":
    run_test()