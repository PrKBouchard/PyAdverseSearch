"# FILE: PyAdverseSearch/test/Chess/piece.py"

piecesName=(' ','K','Q','R','N','B','P')
piecesValue=(0,0,9,5,3,3,1)

rook_movements = (-10,10,-1,1)
bishop_movements = (-11,-9,11,9)
knight_movements = (-12,-21,-19,-8,12,21,19,8)
queen_movements = rook_movements + bishop_movements

tab120 = (
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1,  0,  1,  2,  3,  4,  5,  6,  7, -1,
    -1,  8,  9, 10, 11, 12, 13, 14, 15, -1,
    -1, 16, 17, 18, 19, 20, 21, 22, 23, -1,
    -1, 24, 25, 26, 27, 28, 29, 30, 31, -1,
    -1, 32, 33, 34, 35, 36, 37, 38, 39, -1,
    -1, 40, 41, 42, 43, 44, 45, 46, 47, -1,
    -1, 48, 49, 50, 51, 52, 53, 54, 55, -1,
    -1, 56, 57, 58, 59, 60, 61, 62, 63, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1
    )
tab64 = (
    21, 22, 23, 24, 25, 26, 27, 28,
    31, 32, 33, 34, 35, 36, 37, 38,
    41, 42, 43, 44, 45, 46, 47, 48,
    51, 52, 53, 54, 55, 56, 57, 58,
    61, 62, 63, 64, 65, 66, 67, 68,
    71, 72, 73, 74, 75, 76, 77, 78,
    81, 82, 83, 84, 85, 86, 87, 88,
    91, 92, 93, 94, 95, 96, 97, 98
    )

class Piece:
    def __init__(self, name, color):
        self.name = name      # '.' 'K', 'Q', 'R', 'N', 'B', 'P'
        self.color = color    # 'WHITE' ou 'BLACK'
        self.value=piecesValue[piecesName.index(name)]

    def rook_possible_moves(self, from_pos_index ,board):
        possible_moves = []

        for i in rook_movements:
            j = 1
            while True:
                to_pos_tab120 = tab120[tab64[from_pos_index]+ i * j] 
                if(to_pos_tab120 !=-1):
                    if board.cases[to_pos_tab120].name == ' ':
                        possible_moves.append(to_pos_tab120)
                    elif board.cases[to_pos_tab120].color != self.color:
                        possible_moves.append(to_pos_tab120)
                        break
                    else:
                        break
                else:
                    break
                j=j+1
        return possible_moves
    
    
    def bishop_possible_moves(self, from_pos_index ,board):
        possible_moves = []

        for i in bishop_movements:
            j = 1
            while True:
                to_pos_tab120 = tab120[tab64[from_pos_index]+ i * j] 
                if(to_pos_tab120 !=-1):
                    if board.cases[to_pos_tab120].name == ' ':
                        possible_moves.append(to_pos_tab120)
                    elif board.cases[to_pos_tab120].color != self.color:
                        possible_moves.append(to_pos_tab120)
                        break
                    else:
                        break
                else:
                    break
                j=j+1
        return possible_moves
    
    
    def knight_possible_moves(self, from_pos_index ,board):
        possible_moves = []

        for i in knight_movements:
            to_pos_tab120 = tab120[tab64[from_pos_index]+ i] 
            if(to_pos_tab120 !=-1):
                if board.cases[to_pos_tab120].name == ' ':
                    possible_moves.append(to_pos_tab120)
                elif board.cases[to_pos_tab120].color != self.color:
                    possible_moves.append(to_pos_tab120)
        return possible_moves
    
    
    def queen_possible_moves(self, from_pos_index ,board):
        possible_moves = []

        for i in queen_movements:
            j = 1
            while True:
                to_pos_tab120 = tab120[tab64[from_pos_index]+ i * j] 
                if(to_pos_tab120 !=-1):
                    if board.cases[to_pos_tab120].name == ' ':
                        possible_moves.append(to_pos_tab120)
                    elif board.cases[to_pos_tab120].color != self.color:
                        possible_moves.append(to_pos_tab120)
                        break
                    else:
                        break
                else:
                    break
                j=j+1
        return possible_moves
    
    
    def king_possible_moves(self, from_pos_index ,board):
        possible_moves = []

        for i in queen_movements:
            to_pos_tab120 = tab120[tab64[from_pos_index]+ i] 
            if(to_pos_tab120 !=-1):
                if board.cases[to_pos_tab120].name == ' ':
                    possible_moves.append(to_pos_tab120)
                elif board.cases[to_pos_tab120].color != self.color:
                    possible_moves.append(to_pos_tab120)
        return possible_moves
    
    
    def king_possible_castling_moves(self, from_pos_index ,board):
        possible_moves = []
        
        if (self.color == 'WHITE'): # e1
            if board.white_can_castle_56 and board.cases[tab120[tab64[from_pos_index] - 1]].name == ' ' and board.cases[tab120[tab64[from_pos_index] - 2]].name == ' ' and board.cases[tab120[tab64[from_pos_index] - 3]].name == ' ' and board.cases[tab120[tab64[from_pos_index] - 4]].name == 'R':
                possible_moves.append(58) # c1
            if board.white_can_castle_63 and board.cases[tab120[tab64[from_pos_index] + 1]].name == ' ' and board.cases[tab120[tab64[from_pos_index] + 2]].name == ' ' and board.cases[tab120[tab64[from_pos_index] + 3]].name == 'R':
                possible_moves.append(62) # g1
    
        elif (self.color == 'BLACK'): # e8
            if board.black_can_castle_0 and board.cases[tab120[tab64[from_pos_index] - 1]].name == ' ' and board.cases[tab120[tab64[from_pos_index] - 2]].name == ' ' and board.cases[tab120[tab64[from_pos_index] - 3]].name == ' ' and board.cases[tab120[tab64[from_pos_index] - 4]].name == 'R':
                possible_moves.append(2) # c8
            if board.black_can_castle_7 and board.cases[tab120[tab64[from_pos_index] + 1]].name == ' ' and board.cases[tab120[tab64[from_pos_index] + 2]].name == ' ' and board.cases[tab120[tab64[from_pos_index] + 3]].name == 'R':
                possible_moves.append(6) # g8
        return possible_moves
    

    def pawn_possible_moves(self, from_pos_index ,board):
        possible_moves = []
        # Move forward
        if self.color == 'WHITE':
            to_pos_tab120 = tab120[tab64[from_pos_index] - 10]
            if to_pos_tab120 != -1 and board.cases[to_pos_tab120].name == ' ':
                if to_pos_tab120 >=7:
                    possible_moves.append(to_pos_tab120)
                # Double move from starting position
                if from_pos_index >= 48 and from_pos_index <= 55:
                    to_pos_tab120_double = tab120[tab64[from_pos_index] - 20]
                    if to_pos_tab120_double != -1 and board.cases[to_pos_tab120_double].name == ' ':
                        possible_moves.append(to_pos_tab120_double)
            for capture in [-9, -11]:
                to_pos_tab120 = tab120[tab64[from_pos_index] + capture]
                if to_pos_tab120 != -1 and board.cases[to_pos_tab120].color == 'BLACK':
                    if to_pos_tab120 >=7:
                        possible_moves.append(to_pos_tab120)
        else:  
            # Move forward
            to_pos_tab120 = tab120[tab64[from_pos_index] + 10]
            if to_pos_tab120 != -1 and board.cases[to_pos_tab120].name == ' ':
                possible_moves.append(to_pos_tab120)
                # Double move from starting position
                if from_pos_index >= 8 and from_pos_index <= 15:
                    to_pos_tab120_double = tab120[tab64[from_pos_index] + 20]
                    if to_pos_tab120_double != -1 and board.cases[to_pos_tab120_double].name == ' ':
                        possible_moves.append(to_pos_tab120_double)
            for capture in [9, 11]:
                to_pos_tab120 = tab120[tab64[from_pos_index] + capture]
                if to_pos_tab120 != -1 and board.cases[to_pos_tab120].color == 'WHITE':
                    possible_moves.append(to_pos_tab120)
        
        return possible_moves
    
    
    def pawn_possible_promotions(self, from_pos_index ,board):
        possible_moves = []
        if self.color == 'WHITE':
            
            to_pos_tab120 = tab120[tab64[from_pos_index] - 10]
            if to_pos_tab120 != -1 and board.cases[to_pos_tab120].name == ' ' and to_pos_tab120 < 8:
                possible_moves.append(to_pos_tab120)
            
            for capture in [-9, -11]:
                to_pos_tab120 = tab120[tab64[from_pos_index] + capture]
                if to_pos_tab120 != -1 and board.cases[to_pos_tab120].color == 'BLACK' and to_pos_tab120 < 8:
                    possible_moves.append(to_pos_tab120)
        else:  # BLACK
            to_pos_tab120 = tab120[tab64[from_pos_index] + 10]
            if to_pos_tab120 != -1 and board.cases[to_pos_tab120].name == ' ' and to_pos_tab120 >= 56:
                possible_moves.append(to_pos_tab120)
            
            for capture in [9, 11]:
                to_pos_tab120 = tab120[tab64[from_pos_index] + capture]
                if to_pos_tab120 != -1 and board.cases[to_pos_tab120].color == 'WHITE' and to_pos_tab120 >= 56:
                    possible_moves.append(to_pos_tab120)
        return possible_moves
       
            





