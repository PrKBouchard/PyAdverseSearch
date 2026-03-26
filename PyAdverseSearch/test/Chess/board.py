# FILE: PyAdverseSearch/test/Chess/board.py

from .piece import Piece 

coord=[
    'a8','b8','c8','d8','e8','f8','g8','h8',
    'a7','b7','c7','d7','e7','f7','g7','h7',
    'a6','b6','c6','d6','e6','f6','g6','h6',
    'a5','b5','c5','d5','e5','f5','g5','h5',
    'a4','b4','c4','d4','e4','f4','g4','h4',
    'a3','b3','c3','d3','e3','f3','g3','h3',
    'a2','b2','c2','d2','e2','f2','g2','h2',
    'a1','b1','c1','d1','e1','f1','g1','h1',
    ]

class Board:
    def __init__(self, cases=None, player='WHITE'):
        """
        Initializes the chess board.

        :param board: 8×8 list of lists representing the chess board (default starting position)
        """
        if cases is None:
            self.cases = [
                Piece('R','BLACK'), Piece('N','BLACK'), Piece('B','BLACK'), Piece('Q','BLACK'), Piece('K','BLACK'), Piece('B','BLACK'), Piece('N','BLACK'), Piece('R','BLACK'),
                Piece('P','BLACK'), Piece('P','BLACK'), Piece('P','BLACK'), Piece('P','BLACK'), Piece('P','BLACK'), Piece('P','BLACK'), Piece('P','BLACK'), Piece('P','BLACK'),
                Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'),
                Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'),
                Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'),
                Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'),
                Piece('P','WHITE'), Piece('P','WHITE'), Piece('P','WHITE'), Piece('P','WHITE'), Piece('P','WHITE'), Piece('P','WHITE'), Piece('P','WHITE'), Piece('P','WHITE'),
                Piece('R','WHITE'), Piece('N','WHITE'), Piece('B','WHITE'), Piece('Q','WHITE'), Piece('K','WHITE'), Piece('B','WHITE'), Piece('N','WHITE'), Piece('R','WHITE')
            ]
        else:
            self.cases = cases
        
        self.player = player
        self.history = []
        self.white_can_castle_56=True
        self.white_can_castle_63=True
        self.black_can_castle_0=True
        self.black_can_castle_7=True 


    def get_all_possible_moves(self, color, DontCheck=False):
        """
        Returns a list of all possible moves for a given color in the format [(from_pos, to_pos, type), ...].

        :param color: The color of the pieces to get moves for ('WHITE' or 'BLACK').
        :return: A list of possible moves for the specified color.
        """
        all_possible_moves = []
        for index, piece in enumerate(self.cases):
            if piece.color == color:
                from_pos = coord[index]
                possible_moves = []
                possible_promotions = []
                possible_castling_moves = []
                
                match piece.name:
                    case 'P':
                        possible_moves = piece.pawn_possible_moves(index, self) 
                        possible_promotions = piece.pawn_possible_promotions(index, self)
                    case 'R':
                        possible_moves = piece.rook_possible_moves(index, self)
                    case 'N':
                        possible_moves = piece.knight_possible_moves(index, self)
                    case 'B':
                        possible_moves = piece.bishop_possible_moves(index, self)
                    case 'Q':
                        possible_moves = piece.queen_possible_moves(index, self)
                    case 'K':
                        possible_moves = piece.king_possible_moves(index, self)
                        if DontCheck:
                            possible_castling_moves = piece.king_possible_castling_moves(index, self)
                        elif not self.is_in_check(color):
                            possible_castling_moves = piece.king_possible_castling_moves(index, self)

                for move in possible_moves:
                    to_pos = coord[move]
                    all_possible_moves.append((from_pos, to_pos, ''))

                for promotion in possible_promotions:
                    to_pos = coord[promotion]
                    for promotion_piece in ['Q', 'R', 'B', 'N']:
                        all_possible_moves.append((from_pos, to_pos, promotion_piece))

                for castling_move in possible_castling_moves:
                    to_pos = coord[castling_move]
                    all_possible_moves.append((from_pos, to_pos, 'CASTLE'))

        if not DontCheck:
            in_check_move=[] 
            for move in all_possible_moves:
                #new_board = self.clone()
                action_from, action_to, type = move
                if type=='CASTLE':
                    self.do_castling_move(action_from, action_to)
                elif type in ['Q', 'R', 'B', 'N']:
                    self.do_pawn_promotion(action_from, action_to, type)
                else:
                    self.do_move(action_from, action_to)
                if self.is_in_check(color):
                    in_check_move.append(move)
                self.undo_move()

            for move in in_check_move:
                all_possible_moves.remove(move)

        return all_possible_moves
        

    def do_move(self, from_pos, to_pos):
        """
        Applies a move from from_pos to to_pos.

        :param from_pos: The position of the piece to move.
        :param to_pos: The position where the piece is being moved.
        """
        self.log_move(from_pos, to_pos)
        piece = self.cases[coord.index(from_pos)]
        self.cases[coord.index(to_pos)] = piece
        self.cases[coord.index(from_pos)] = Piece(' ','NONE')

    def undo_move(self):
        if not self.history:
            print("No moves to undo.")
            return
        
        last_move = self.history.pop()
        if last_move[8]:  # If it was a castling move
            from_pos, to_pos, white_can_castle_56, white_can_castle_63, black_can_castle_0, black_can_castle_7, rook_from_pos, rook_to_pos, _ = last_move
            #print(f"Undoing castling move from {from_pos} to {to_pos}")
            self.cases[coord.index(from_pos)] = self.cases[coord.index(to_pos)]
            self.cases[coord.index(to_pos)] = Piece(' ','NONE')
            self.cases[coord.index(rook_from_pos)] = self.cases[coord.index(rook_to_pos)]
            self.cases[coord.index(rook_to_pos)] = Piece(' ','NONE')
            self.white_can_castle_56 = white_can_castle_56
            self.white_can_castle_63 = white_can_castle_63
            self.black_can_castle_0 = black_can_castle_0
            self.black_can_castle_7 = black_can_castle_7
        else:
            from_pos, to_pos, piece_from, piece_to, white_can_castle_56, white_can_castle_63, black_can_castle_0, black_can_castle_7, _ = last_move
            #print(f"Undoing move from {from_pos} to {to_pos}")
            self.cases[coord.index(from_pos)] = piece_from
            self.cases[coord.index(to_pos)] = piece_to
            self.white_can_castle_56 = white_can_castle_56
            self.white_can_castle_63 = white_can_castle_63
            self.black_can_castle_0 = black_can_castle_0
            self.black_can_castle_7 = black_can_castle_7


    def do_pawn_promotion(self, from_pos, to_pos, promotion_piece):
        """
        Applies a pawn promotion move.

        :param from_pos: The position of the pawn to promote.
        :param to_pos: The position where the pawn is being promoted.
        :param promotion_piece: The piece to promote to (e.g., 'Q' for queen).
        """
        self.log_move(from_pos, to_pos)
        piece = self.cases[coord.index(from_pos)]
        self.cases[coord.index(to_pos)] = Piece(promotion_piece, piece.color)
        self.cases[coord.index(from_pos)] = Piece(' ','NONE')
        

    def do_castling_move(self,from_pos, to_pos):
        """
        Applies a castling move between the king and rook.

        :param from_pos: The position of the king to move.
        :param to_pos: The position where the king is being moved for castling.
        """
        self.log_move(from_pos, to_pos, True)
        from_pos_index = coord.index(from_pos)
        to_pos_index = coord.index(to_pos)
        
        if from_pos == 'e1' and to_pos == 'c1':
            self.cases[coord.index('c1')] = self.cases[coord.index('e1')]
            self.cases[coord.index('e1')] = Piece(' ','NONE')
            self.cases[coord.index('a1')] = Piece(' ','NONE')
            self.cases[coord.index('d1')] = Piece('R','WHITE')
            self.white_can_castle_56=False
            self.white_can_castle_63=False
        elif from_pos == 'e1' and to_pos == 'g1':
            self.cases[coord.index('g1')] = self.cases[coord.index('e1')]
            self.cases[coord.index('e1')] = Piece(' ','NONE')
            self.cases[coord.index('h1')] = Piece(' ','NONE')
            self.cases[coord.index('f1')] = Piece('R','WHITE')
            self.white_can_castle_56=False
            self.white_can_castle_63=False
        elif from_pos == 'e8' and to_pos == 'c8':
            self.cases[coord.index('c8')] = self.cases[coord.index('e8')]
            self.cases[coord.index('e8')] = Piece(' ','NONE')
            self.cases[coord.index('a8')] = Piece(' ','NONE')
            self.cases[coord.index('d8')] = Piece('R','BLACK')
            self.black_can_castle_0=False
            self.black_can_castle_7=False
        elif from_pos == 'e8' and to_pos == 'g8':
            self.cases[coord.index('g8')] = self.cases[coord.index('e8')]
            self.cases[coord.index('e8')] = Piece(' ','NONE')
            self.cases[coord.index('h8')] = Piece(' ','NONE')
            self.cases[coord.index('f8')] = Piece('R','BLACK')
            self.black_can_castle_0=False
            self.black_can_castle_7=False


    def get_piece_at(self, position):
        return self.cases[coord.index(position)]
    
    
    def clone(self):
        new_cases = [Piece(p.name, p.color) for p in self.cases]
        new_board = Board(cases=new_cases, player=self.player)
        new_board.white_can_castle_56 = self.white_can_castle_56
        new_board.white_can_castle_63 = self.white_can_castle_63
        new_board.black_can_castle_0 = self.black_can_castle_0
        new_board.black_can_castle_7 = self.black_can_castle_7
        return new_board
    

    def is_in_check(self, color):
        all_moves = self.get_all_possible_moves('BLACK' if color == 'WHITE' else 'WHITE', DontCheck=True)

        for piece in self.cases:
            if piece.name == 'K' and piece.color == color:
                king_position = coord[self.cases.index(piece)]
                for move in all_moves:
                    if move[1] == king_position:
                        return True
                    
        return False
    

    def is_checkmate(self, moves=None, color=None):
        if moves is None:
            moves = self.get_all_possible_moves(color)
        if len(moves) == 0 and self.is_in_check(color):
            return True
        return False
    

    def log_move(self, from_pos, to_pos, is_castling=False):
        #print(f"Move from {from_pos} to {to_pos}")
        if is_castling:
            if from_pos == 'e1' and to_pos == 'c1':
                move = [from_pos, to_pos, self.white_can_castle_56, self.white_can_castle_63, self.black_can_castle_0, self.black_can_castle_7, 'a1', 'd1', True]
            elif from_pos == 'e1' and to_pos == 'g1':
                move = [from_pos, to_pos, self.white_can_castle_56, self.white_can_castle_63, self.black_can_castle_0, self.black_can_castle_7, 'h1', 'f1', True]
            elif from_pos == 'e8' and to_pos == 'c8':
                move = [from_pos, to_pos, self.white_can_castle_56, self.white_can_castle_63, self.black_can_castle_0, self.black_can_castle_7, 'a8', 'd8', True]
            elif from_pos == 'e8' and to_pos == 'g8':
                move = [from_pos, to_pos, self.white_can_castle_56, self.white_can_castle_63, self.black_can_castle_0, self.black_can_castle_7, 'h8', 'f8', True]
        else:
            piece_from = self.get_piece_at(from_pos)
            piece_to = self.get_piece_at(to_pos)
            move = [from_pos, to_pos, piece_from, piece_to, self.white_can_castle_56, self.white_can_castle_63, self.black_can_castle_0, self.black_can_castle_7, False]
            self.history.append(move)

    
    
    