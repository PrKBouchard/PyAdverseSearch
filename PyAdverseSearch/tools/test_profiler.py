from PyAdverseSearch.test.state_tictactoe import generate_tictactoe_game
from PyAdverseSearch.classes.negamax import NegamaxSolver
from PyAdverseSearch.classes.node import Node
from PyAdverseSearch.tools.profiler import SearchProfiler

def run_profile_test():
    game = generate_tictactoe_game()
    solver = NegamaxSolver(depth_limit=4)
    profiler = SearchProfiler(solver)
    
    state = game.state
    move_count = 0

    # Play a full game
    while not game.is_terminal(state):
        move_count += 1
        root_node = Node(state=state)
        
        best_board = solver.get_best_move(root_node)
        
        profiler.capture_metrics(f"M{move_count}")

        successors = state._generate_successors()
        state = next(s for s in successors if s.board == best_board)

    # Generate Graph
    profiler.plot()

if __name__ == "__main__":
    run_profile_test()