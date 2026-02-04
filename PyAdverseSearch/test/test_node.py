from ..classes.node import Node
from ..classes.game import Game
from ..classes.state import State

# Mock State
class MockState(State):
    def __init__(self, game, player=None):
        self.game = game
        self.player = player # Simulate state knowing the player
    def _possible_actions(self): return []
    def _is_terminal(self): return False
    def _utility(self): return 0
    def _evaluate(self): return 0

def test_node_player_logic():
    print("=== TEST 1: MAX Starts (Standard Depth Logic) ===")
    game_max = Game(isMaxStarting=True)
    state_max = MockState(game_max)
    
    for depth in range(4):
        node = Node(state_max, depth=depth)
        expected = "MAX" if depth % 2 == 0 else "MIN"
        status = "OK" if node.player == expected else "BUG"
        print(f"Depth {depth}: Got {node.player}, Expected {expected} -> {status}")

    print("\n=== TEST 2: MIN Starts (Standard Depth Logic) ===")
    game_min = Game(isMaxStarting=False)
    state_min = MockState(game_min)
    
    for depth in range(4):
        node = Node(state_min, depth=depth)
        # If MIN starts:
        # Depth 0: MIN Depth 1: MAX
        expected = "MIN" if depth % 2 == 0 else "MAX"
        status = "OK" if node.player == expected else "BUG"
        print(f"Depth {depth}: Got {node.player}, Expected {expected} -> {status}")

    print("\n=== TEST 3: State Override (MCTS Scenario) ===")
    # Scenario: We are at depth 0 of the search tree.
    # The buggy logic says it's MIN's turn at depth 0 (if MAX starts).
    # But let's say the state explicitly says it's MAX's turn.
    # If Node respects the state, it should say MAX. If it uses the buggy logic, it will say MIN.
    game_override = Game(isMaxStarting=True) 
    state_override = MockState(game_override, player="MAX") 
    
    node_override = Node(state_override, depth=0)
    print(f"State says MAX. Node depth is 0 (Buggy logic says MIN).")
    print(f"Node decided: {node_override.player}")
    
    if node_override.player == "MAX":
        print("SUCCESS: Node respected state.player.")
    else:
        print("BUG: Node ignored state.player (or calculated wrong).")

if __name__ == "__main__":
    test_node_player_logic()
