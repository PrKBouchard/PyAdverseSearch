# FILE: PyAdverseSearch/test/Chess/state_chess.py

from .piece import Piece
from ...classes.state import State
from ...classes.game import Game
from .board import Board
import copy

from PyAdverseSearch.classes import state 
class ChessState(State):
    def __init__(self, board=None, parent=None, game=None, player='MAX', isMaxStarting=True):
        """
        Initializes a Chess game state.

        :param board: 8×8 list of lists representing the chess board (default starting position)
        :param player: 'MAX' or 'MIN'
        :param parent: parent state (previous move)
        :param game: reference to the Game instance (attached after init)
        """
        
        if board is None:
            board = Board()

        # Call to the base State initializer
        super().__init__(board, parent)
        # Ensure essential attributes are set
        self.board = board
        self.player = player
        self.parent = parent
        self.game = game 
        self.all_possible_moves = None
        self.isMaxStarting = isMaxStarting

    def _apply_action(self, action):
        """
        Applies the given action ((from_row, from_col), (to_row, to_col)) and returns a new ChessState.
        """
        action_from, action_to, type = action
        new_board = self.board.clone() 
        if type=='CASTLE':
            new_board.do_castling_move(action_from, action_to)
        elif type in ['Q', 'R', 'B', 'N']:
            new_board.do_pawn_promotion(action_from, action_to, type)
        else:
            new_board.do_move(action_from, action_to)
        new_board.player = 'BLACK' if self.board.player == 'WHITE' else 'WHITE'
        next_player = 'MIN' if self.player == 'MAX' else 'MAX'

        return ChessState(board=new_board, parent=self, game=self.game, player=next_player)
    
    def user_move(self, user_input):
        if (user_input == 'f'):
            self.board.undo_move()
            return ChessState(board=self.board, parent=self, game=self.game, player=self.player)
        action_from = user_input[0:2]
        action_to = user_input[2:4]
        type = user_input[4] if len(user_input) == 5 else ''
        
        new_board = self.board.clone() 
        piece = new_board.get_piece_at(action_from)
        all_possible_moves = new_board.get_all_possible_moves(new_board.player)

        if piece.color != new_board.player:
            raise ValueError(str(user_input) + " : incorrect move or let king in check")
        if (action_from, action_to, type) in all_possible_moves:
            if type in ['Q', 'R', 'B', 'N']:
                new_board.do_pawn_promotion(action_from, action_to, type)
            else:
                new_board.do_move(action_from, action_to)
        elif (action_from, action_to, 'CASTLE') in all_possible_moves:
            new_board.do_castling_move(action_from, action_to)
        else:             
            raise ValueError(str(user_input) + " : incorrect move or let king in check")

        new_board.player = 'BLACK' if self.board.player == 'WHITE' else 'WHITE'
        next_player = 'MIN' if self.player == 'MAX' else 'MAX'

        return ChessState(board=new_board, parent=self, game=self.game, player=next_player)

    def display(self):
        GRAY = "\033[90m"
        RESET = "\033[0m"

        print("  +" + "---+" * 8)
        for i in range(8):
            col = 8 - i
            row_pieces = self.board.cases[i*8 : (i+1)*8]
            
            display_row = []
            for piece in row_pieces:
                if piece.color == "BLACK":
                    char = f"{GRAY}{piece.name}{RESET}"
                else:
                    char = piece.name
                
                display_row.append(char)
            
            print(str(col) + " | " + " | ".join(display_row) + " |")
            print("  +" + "---+" * 8)
            
        print("    a   b   c   d   e   f   g   h")

        #TODO: Si MaxIsStarting est Faux, inverser le plateau pour que les pièces blanches soient en bas et les noires en haut, sinon laisser tel quel (blancs en haut, noirs en bas)

def possible_actions(state):
    """
    Returns a list of available (from_pos, to_pos) moves on the board.
    """
    if state.all_possible_moves is None:
        state.all_possible_moves = state.board.get_all_possible_moves(state.board.player)
    return state.all_possible_moves
    

def is_terminal(state):
    """
    Checks if the game has ended (win or stalemate).
    """
    if state.all_possible_moves is None:
        state.all_possible_moves = possible_actions(state)
    moves = state.all_possible_moves
    if len(moves) == 0:  
        return True
    return False
    

def utility(state):
    """
    Returns 1000 if MAX wins, -1000 if MIN wins, 0 otherwise.
    """
    b = state.board

    if state.all_possible_moves is None:
        state.all_possible_moves = possible_actions(state)
    
    if state.isMaxStarting:
        if b.is_checkmate('WHITE', state.all_possible_moves):
            return -1000
        if b.is_checkmate('BLACK', state.all_possible_moves):
            return 1000 
    else:
        if b.is_checkmate('WHITE', state.all_possible_moves):
            return 1000 
        if b.is_checkmate('BLACK', state.all_possible_moves):
            return -1000 

    return 0


def heuristic(state):
    """
    h(s) = 
    0.6 Points for Piece values (Q=9, R=5, B=3, N=3, P=1)
    0.2 Points for Control of the center (d4, d5, e4, e5)
    0.2 Points for Mobility (number of legal moves)
    
    """
                
    b = state.board
    WhiteScore=0
    BlackScore=0
    PiecesValue = 0
    MAX_MOVES = 80 # Approximate maximum number of legal moves in a chess position

    for pos1,piece in enumerate(b.cases):
        if(piece.color=='WHITE'):
            WhiteScore+=piece.value
        else:
            BlackScore+=piece.value
            
    if state.isMaxStarting:
        PiecesValue = (WhiteScore-BlackScore + 39)*0.0076
        moves = b.get_all_possible_moves('WHITE', DontCheck=True)
    else:
        PiecesValue = (BlackScore-WhiteScore + 39)*0.0076
        moves = b.get_all_possible_moves('BLACK', DontCheck=True)
    
    MobilityScore = min(len(moves) / MAX_MOVES, 1.0) * 0.2

    d4Control, d5Control, e4Control, e5Control = 0, 0, 0, 0
    for move in moves:
        if move[0] or move[1]  == 'd4':
            d4Control = 0.05
        elif move[0] or move[1]== 'd5':
            d5Control = 0.05
        elif move[0] or move[1]== 'e4':
            e4Control = 0.05
        elif move[0] or move[1]== 'e5':
            e5Control = 0.05
    CenterControlScore = (d4Control + d5Control + e4Control + e5Control)
    Score = PiecesValue + MobilityScore + CenterControlScore

    return Score


def winner_function(state):
    """
    Returns 'MAX' or 'MIN' if there is a winner, else None.
    """
    b = state.board

    if state.isMaxStarting:
        if b.is_checkmate('WHITE'):
            return "MIN" 
        if b.is_checkmate('BLACK'):
            return "MAX" 
    else:
        if b.is_checkmate('WHITE'):
            return "MAX" 
        if b.is_checkmate('BLACK'):
            return "MIN"
        
    return None                      

def generate_chess_game(isMaxStartingParameter=True):

    """
    Factory: builds a Game configured for Chess.
    """
    initial_state = ChessState(isMaxStarting=isMaxStartingParameter)
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
