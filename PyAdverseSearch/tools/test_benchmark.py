from PyAdverseSearch.test.state_tictactoe import generate_tictactoe_game
from PyAdverseSearch.classes.negamax import NegamaxSolver
from PyAdverseSearch.tools.benchmark import AIvsAIBenchmark

# 1. Define two different AI profiles
smart_ai = NegamaxSolver(depth_limit=4)  # Deeper search
fast_ai = NegamaxSolver(depth_limit=2)   # Shallower search

# 2. Setup Benchmark
benchmark = AIvsAIBenchmark(
    game_generator=generate_tictactoe_game,
    solver1=smart_ai,
    solver2=fast_ai
)

# 3. Run 20 games
benchmark.run_tournament(num_games=20)