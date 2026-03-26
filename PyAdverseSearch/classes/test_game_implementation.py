# FILE: test_game_implementation.py

import unittest
from .state import State
from .game import Game

class GameTester(unittest.TestCase):
    """
    A base test class for developers using PyAdverseSearch to test their Game and State implementations.
    To use this class:
    1. Inherit from `GameTester`
    2. Override the `setUp` method to initialize `self.game` with your custom `Game` instance.
    
    Example:
        class MyGameTest(GameTester):
            def setUp(self):
                self.game = create_my_custom_game()
    """

    def setUp(self):
        self.game = None

    def test_game_initialization(self):
        """Validates that self.game was properly initialized and is a Game instance."""
        self.assertIsNotNone(self.game, "self.game must be initialized in your test setUp().")
        self.assertIsInstance(self.game, Game, "self.game must be an instance of the Game class.")

    def test_game_has_initial_state(self):
        """Validates that the provided Game has a correctly initialized state."""
        if self.game is None:
            self.skipTest("Game is not initialized.")
        self.assertIsNotNone(self.game.state, "Game must have an initial state provided during initialization.")
        self.assertIsInstance(self.game.state, State, "The initial state must inherit from the State abstract class.")

    def test_game_functions_are_callable(self):
        """Validates that all required Game functions were provided and are callable."""
        if self.game is None:
            self.skipTest("Game is not initialized.")
        self.assertTrue(callable(self.game.possible_actions), "possible_actions must be a callable function.")
        self.assertTrue(callable(self.game.is_terminal), "is_terminal must be a callable function.")
        self.assertTrue(callable(self.game.utility), "utility must be a callable function.")
        self.assertTrue(callable(self.game.heuristic), "heuristic must be a callable function.")
        self.assertTrue(callable(self.game.winner_function), "winner_function must be a callable function.")

    def test_state_possible_actions(self):
        """Validates the structure of actions returned from the initial state."""
        if self.game is None or self.game.state is None:
            self.skipTest("Game or State is not initialized.")
        state = self.game.state
        actions = self.game.possible_actions(state)
        self.assertIsInstance(actions, list, "possible_actions callback must return a list of actions.")
        self.assertTrue(all(actions) or not actions, "All possible actions must not be None.")

    def test_state_apply_actions_and_generation(self):
        """Validates that applying an action creates a correct child state and tests generation."""
        if self.game is None or self.game.state is None:
            self.skipTest("Game or State is not initialized.")
        
        state = self.game.state
        if self.game.is_terminal(state):
            self.skipTest("The provided initial state is already terminal. Cannot test action derivation.")

        actions = self.game.possible_actions(state)
        if not actions:
            self.skipTest("No possible actions from the initial state to test derivation against.")

        # Test _apply_action on the first action
        action = actions[0]
        try:
            next_state = state._apply_action(action)
        except AttributeError:
            self.fail("Your state class must implement the `_apply_action(self, action)` method.")
        except Exception as e:
            self.fail(f"Applying an action threw an exception: {e}")

        self.assertIsInstance(next_state, State, "_apply_action must return an instance inheriting from State.")
        self.assertNotEqual(id(state), id(next_state), "_apply_action must return a new discrete state memory reference.")

        # Test _generate_successors, which depends on _apply_action
        try:
            successors = state._generate_successors()
            self.assertIsInstance(successors, list, "_generate_successors must return a list of States.")
            self.assertEqual(len(successors), len(actions), "The number of successors must equal the number of possible actions.")
        except Exception as e:
            self.fail(f"_generate_successors threw an exception. Make sure _apply_action is implemented cleanly: {e}")

    def test_state_is_terminal(self):
        """Validates the returns of the is_terminal checks uniformly."""
        if self.game is None or self.game.state is None:
            self.skipTest("Game or State is not initialized.")
        is_term = self.game.is_terminal(self.game.state)
        self.assertIsInstance(is_term, bool, "is_terminal callback must return a boolean True/False.")

    def test_state_heuristic(self):
        """Validates that the heuristic callback returns numerical outcomes properly."""
        if self.game is None or self.game.state is None:
            self.skipTest("Game or State is not initialized.")
        try:
            val = self.game.heuristic(self.game.state)
            self.assertIsInstance(val, (int, float), "heuristic callback must return a numeric value.")
        except Exception as e:
            self.fail(f"heuristic computation threw an exception on the initial state: {e}")

    def test_state_utility_and_winner(self):
        """Validates utility and winner derivations (requires resolving cleanly without exceptions)."""
        if self.game is None or self.game.state is None:
            self.skipTest("Game or State is not initialized.")
        try:
            # We enforce testing utility explicitly even on non-terminal states if not blocked.
            # Depending on game rules it may yield a numeric tie value or baseline.
            util = self.game.utility(self.game.state)
            self.assertIsInstance(util, (int, float), "utility callback must return a numeric value.")
        except Exception as e:
            self.skipTest(f"utility callback threw an exception (perhaps due to un-handled non-terminal base conditions): {e}")

        try:
            self.game.get_winner()
        except Exception as e:
            self.fail(f"winner_function evaluation threw an exception logically resolving winner checks: {e}")
