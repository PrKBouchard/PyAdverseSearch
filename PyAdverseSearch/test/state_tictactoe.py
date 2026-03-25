# FILE: PyAdverseSearch/test/state_tictactoe.py

from ..classes.state import State
from ..classes.game import Game

class TicTacToeState(State):
    def __init__(self, board=None, player='MAX', parent=None, game=None):
        """
        Initializes a Tic-Tac-Toe game state.

        :param board: 3×3 list of lists (default empty board)
        :param player: 'MAX' or 'MIN'
        :param parent: parent state (previous move)
        :param game: reference to the Game instance (attached after init)
        """
        if board is None:
            board = [[' ' for _ in range(3)] for _ in range(3)]

        # Call to the base State initializer
        super().__init__(board, player, parent)
        # Ensure essential attributes are set
        self.board = board
        self.player = player
        self.parent = parent
        self.game = game

    def _apply_action(self, action):
        """
        Applies the given action (row, col) and returns a new TicTacToeState.
        """
        row, col = action
        new_board = [r[:] for r in self.board]
        new_board[row][col] = 'X' if self.player == 'MAX' else 'O'
        next_player = 'MIN' if self.player == 'MAX' else 'MAX'

        # Create the child state and transfer game reference
        child = TicTacToeState(new_board, next_player, parent=self, game=self.game)
        return child

    def get_possible_moves(self):
        """Returns a list of available (row, col) moves on the board."""
        return possible_actions(self)

    def is_game_over(self):
        """Checks if the game has ended."""
        return is_terminal(self)

    def get_utility(self):
        """Returns the utility value for terminal states."""
        return utility(self)

    def get_winner(self):
        """Returns the winner if game is over."""
        return winner_function(self)

    def evaluate(self):
        """Returns heuristic evaluation of the state."""
        return heuristic(self)


def possible_actions(state):
    """
    Returns a list of available (row, col) moves on the board.
    """
    return [(i, j) for i in range(3) for j in range(3) if state.board[i][j] == ' ']


def is_terminal(state):
    """
    Checks if the game has ended (win or full board).
    """
    b = state.board
    lines = (
        b +
        [list(col) for col in zip(*b)] +
        [[b[i][i] for i in range(3)], [b[i][2-i] for i in range(3)]]
    )
    if any(line.count(line[0]) == 3 and line[0] != ' ' for line in lines):
        return True
    return all(cell != ' ' for row in b for cell in row)


def utility(state):
    """
    Returns 1 if MAX wins, -1 if MIN wins, 0 otherwise.
    """
    b = state.board
    lines = (
        b +
        [list(col) for col in zip(*b)] +
        [[b[i][i] for i in range(3)], [b[i][2-i] for i in range(3)]]
    )
    for line in lines:
        if line.count('X') == 3:
            return 1000
        if line.count('O') == 3:
            return -1000
    return 0


def heuristic(state):
    """
    h(s) = 0.5*(#2-en-ligne MAX)
         - 0.5*(#2-en-ligne MIN)
         + 0.2*(X au centre)
         - 0.2*(O au centre)
         + 0.1*(différence de mobilité)
    """
    b = state.board

    # 1) Rassembler toutes les lignes, colonnes, diagonales
    lines = (
        b +
        [list(col) for col in zip(*b)] +
        [[b[i][i] for i in range(3)], [b[i][2-i] for i in range(3)]]
    )

    # 2) Comptage des 2-en-ligne
    two_max = sum(1 for L in lines if L.count('X') == 2 and L.count(' ') == 1)
    two_min = sum(1 for L in lines if L.count('O') == 2 and L.count(' ') == 1)

    # 3) Possession du centre
    center = b[1][1]
    # +1 si X au centre, -1 si O, 0 sinon
    center_val = 1 if center == 'X' else -1 if center == 'O' else 0

    # 4) Mobilité = nombre de cases vides
    mobility = sum(1 for i in range(3) for j in range(3) if b[i][j] == ' ')
    # On peut choisir de donner la mobilité à MAX uniquement
    # ici on l'applique tel quel (toujours positif)
    diff_mobility = mobility

    # 5) Combinaison linéaire
    return (
        0.5 * two_max
      - 0.5 * two_min
      + 0.2 * center_val
      + 0.1 * diff_mobility
    )


def winner_function(state):
    """
    Returns 'MAX' or 'MIN' if there is a winner, else None.
    """
    b = state.board
    lines = (
        b +
        [list(col) for col in zip(*b)] +
        [[b[i][i] for i in range(3)], [b[i][2-i] for i in range(3)]]
    )
    for line in lines:
        if line.count('X') == 3:
            return 'MAX'
        if line.count('O') == 3:
            return 'MIN'
    return None


def generate_tictactoe_game(isMaxStartingParameter=True):
    """
    Factory: builds a Game configured for Tic-Tac-Toe.
    """
    initial_state = TicTacToeState()
    game = Game(
        initial_state=initial_state,
        possible_actions=possible_actions,
        is_terminal=is_terminal,
        winner_function=winner_function,
        utility=utility,
        heuristic=heuristic,
        isMaxStarting=isMaxStartingParameter
    )
    initial_state.game = game
    return game
