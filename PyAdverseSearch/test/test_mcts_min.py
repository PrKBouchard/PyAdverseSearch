from ..classes.montecarlo import MonteCarlo
from ..classes.game import Game
from ..classes.state import State
from ..classes.node import Node

# Mock State and Game
class MockState(State):
    def __init__(self, name, player, is_terminal=False, utility=0, game=None):
        self.name = name
        self.player = player
        self._is_terminal_val = is_terminal
        self._utility_val = utility
        self.children = []
        self.game = game # Attach game

    def _possible_actions(self):
        return list(range(len(self.children)))

    def _apply_action(self, action):
        return self.children[action]
    
    def _is_terminal(self):
        return self._is_terminal_val
    
    def _utility(self):
        return self._utility_val
    
    def _evaluate(self):
        return 0
        
    def __repr__(self):
        return f"State({self.name}, {self.player})"

def winner_function(state):
    if state._utility_val > 0: return "MAX"
    if state._utility_val < 0: return "MIN"
    return None

def test_mcts_min_logic():
    print("\n=== TEST: MCTS Minimization for MIN ===")
    # Root (MIN to move)
    #  |
    #  +-- Child A (Terminal, Utility = 100 (MAX wins))
    #  |
    #  +-- Child B (Terminal, Utility = -100 (MIN wins))

    game_obj = Game(isMaxStarting=True)
    root_state = MockState("Root", "MIN", game=game_obj)
    child_a = MockState("Child A", "MAX", is_terminal=True, utility=100, game=game_obj)
    child_b = MockState("Child B", "MAX", is_terminal=True, utility=-100, game=game_obj)

    root_state.children = [child_a, child_b]

    # Update game object
    game_obj.state = root_state
    game_obj.winner_function = winner_function
    game_obj.is_terminal = lambda s: s._is_terminal()
    game_obj.possible_actions = lambda s: s._possible_actions()
    game_obj.utility = lambda s: s._utility()
    game_obj.heuristic = lambda s: 0

    mcts = MonteCarlo(game=game_obj, max_iterations=100)
    best_state = mcts.choose_best_move(root_state)

    print(f"Root player: {root_state.player}")
    print(f"Child A utility: {child_a._utility_val}")
    print(f"Child B utility: {child_b._utility_val}")
    print(f"Selected state: {best_state.name}")

    if best_state.name == "Child A":
        print("BUG CONFIRMED: MCTS selected Child A (MAX win) for MIN player.")
    elif best_state.name == "Child B":
        print("SUCCESS: MCTS selected Child B (MIN win). Correct behavior.")
    else:
        print("Unknown result.")

if __name__ == "__main__":
    test_mcts_min_logic()
