from PyAdverseSearch.test.state_tictactoe import generate_tictactoe_game
from PyAdverseSearch.classes.negamax import NegamaxSolver
from PyAdverseSearch.tools.random_solver import RandomSolver
from PyAdverseSearch.tools.benchmark import AIvsAIBenchmark

smart_ai = NegamaxSolver(depth_limit=3)
random_ai = RandomSolver()

benchmark = AIvsAIBenchmark(
    game_generator=generate_tictactoe_game,
    solver1=smart_ai,
    solver2=random_ai
)

benchmark.run_tournament(num_games=50)