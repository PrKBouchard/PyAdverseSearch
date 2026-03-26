import unittest
from PyAdverseSearch.classes.game import Game
from PyAdverseSearch.test.state_connect4 import Connect4State, ROWS, COLS, possible_actions, is_terminal, winner_function, utility, heuristic
from PyAdverseSearch.classes.minimax import Minimax
from PyAdverseSearch.classes.alphabeta import AlphaBeta
from PyAdverseSearch.classes.negamax import NegamaxSolver
from PyAdverseSearch.classes.montecarlo import MonteCarlo
from PyAdverseSearch.classes.pnsearch import PNSearch
from PyAdverseSearch.classes.node import Node

class TestLogicAllAlgorithms(unittest.TestCase):
    
    def setUp(self):
        self.game = Game(
            initial_state=Connect4State(),
            possible_actions=possible_actions,
            is_terminal=is_terminal,
            winner_function=winner_function,
            utility=utility,
            heuristic=heuristic,
            isMaxStarting=True
        )
        # We test the major algorithms available in the library.
        self.algorithms = [
            "Minimax",
            "AlphaBeta",
            "Negamax",
            "MonteCarlo",
            "PNSearch"
        ]

    def _get_move_from_algo(self, algo_name, state):
        """
        Helper method to instantiate the correct algorithm and return the board result.
        Returns the board (list of lists) representing the state after the best move.
        """
        if algo_name == "Minimax":
            # Depth 2 is sufficient for the logic tests
            solver = Minimax(game=self.game, max_depth=2)
            best_state = solver.choose_best_move(state)
            return best_state.board if best_state else None
            
        elif algo_name == "AlphaBeta":
            solver = AlphaBeta(game=self.game, max_depth=2)
            best_state = solver.choose_best_move(state)
            return best_state.board if best_state else None
            
        elif algo_name == "Negamax":
            solver = NegamaxSolver(depth_limit=2)
            root = Node(state)
            # Negamax returns the board directly, not a state object
            return solver.get_best_move(root)
            
        elif algo_name == "MonteCarlo":
            # Needs enough iterations to confidently find obvious wins or blocks
            solver = MonteCarlo(game=self.game, max_iterations=5000)
            best_state = solver.choose_best_move(state)
            return best_state.board if best_state else None
            
        elif algo_name == "PNSearch":
            # PNSearch finds forced wins/blocks
            pn = PNSearch(game=self.game, max_nodes=5000)
            best_state = pn.choose_best_move(state)
            return best_state.board if best_state else None
            
        else:
            raise ValueError(f"Unknown algorithm: {algo_name}")

    def test_logic_constrained_column(self):
        """Test behavior when only ONE move is possible."""
        for algo in self.algorithms:
            with self.subTest(algo=algo):
                # Fill all columns except column 3
                board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
                for c in range(COLS):
                    if c == 3: continue
                    for r in range(ROWS):
                        board[r][c] = 'X' if (r+c)%2==0 else 'O'
                
                state = Connect4State(board=board, game=self.game, player='MAX')
                
                # Verify only col 3 is open
                actions = possible_actions(state)
                self.assertEqual(actions, [3], "Only column 3 should be open")
                
                best_board = self._get_move_from_algo(algo, state)
                self.assertIsNotNone(best_board)
                
                found_diff = False
                for r in range(ROWS):
                    if best_board[r][3] != ' ':
                        found_diff = True
                        break
                self.assertTrue(found_diff, f"{algo} did not play in the only available column (3)")

    def test_logic_immediate_win(self):
        """Test algorithm takes an immediate winning move."""
        for algo in self.algorithms:
            with self.subTest(algo=algo):
                board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
                # Row 5 (bottom) setup for MAX ('X') win in col 3
                board[5][0] = 'X'
                board[5][1] = 'X'
                board[5][2] = 'X'
                
                state = Connect4State(board=board, game=self.game, player='MAX')
                
                best_board = self._get_move_from_algo(algo, state)
                self.assertIsNotNone(best_board)
                self.assertEqual(best_board[5][3], 'X', f"{algo} should take the winning move at (5, 3)")

    def test_logic_block_opponent_win(self):
        """Test algorithm blocks an immediate opponent win."""
        for algo in self.algorithms:
            # MonteCarlo requires significant iterations to sometimes reliably block in this setup.
            # We already set it to 5000 which should be sufficient.
            with self.subTest(algo=algo):
                board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
                # Row 5 (bottom) setup for MIN ('O') win in col 3
                board[5][0] = 'O'
                board[5][1] = 'O'
                board[5][2] = 'O'
                
                state = Connect4State(board=board, game=self.game, player='MAX')
                
                best_board = self._get_move_from_algo(algo, state)
                self.assertIsNotNone(best_board, f"{algo} returned None, should find a blocking move")
                
                self.assertEqual(best_board[5][3], 'X', f"{algo} should block the opponent win at (5, 3)")

if __name__ == "__main__":
    unittest.main()
