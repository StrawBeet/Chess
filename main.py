import pygame

pygame.init()

clock = pygame.time.Clock()
mouse_pos = pygame.mouse.get_pos()
screen = pygame.display.set_mode((1080, 864))
pygame.display.set_caption("Chess")

# Font sizes I might need for text
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 35)
smaller_font = pygame.font.Font(None, 20)
title_font = pygame.font.Font(None, 100)

# Colors of the game board and other things
brown = (54, 35, 18)
beige = (247, 232, 208)
green = (25, 120, 12) # Background color

running = True
mode = 0 # 0 will be for the menu, 1 will be for playing against a bot, everything else will be for the variants

def add_doubles(double1, double2, mult=1):
    # This will be useful because I will use tuples of length 2 to store positions
    return (mult * (double1[0] + double2[0]), mult * (double2[1] + double2[1]))

def outside(pos):
    # Checks whether something is outside the board
    if pos[0] < 0 or pos[0] > 7 or pos[1] < 0 or pos[1] > 7:
        return True
    else:
        return False

class Piece:
    def __init__(self, pos, move_rules, capture_rules, limited):
        """Move_rules will be a tuple of all possible moves represented by displacements
        capture_rules will be a tuple of all possible captures represented by displacements"""
        self.pos = pos
        self.moves = move_rules
        self.captures = capture_rules
        self.limit = limited

    def legal_moves(self):
        # Returns all possible moves without accounting for other pieces
        legal_moves = []

        if not self.limit:
            for moves in self.moves:
                if not outside(add_doubles(self.pos, moves)):
                    legal_moves.append(add_doubles(self.pos, moves))
                else:
                    pass
        else:
            for moves in self.moves:
                for mult in range(1, 8):
                    if not outside(add_doubles(self.pos, (moves[0] * mult, moves[1] * mult))):
                        legal_moves.append(add_doubles(self.pos, (moves[0] * mult, moves[1] * mult)))
                    else:
                        pass

        return legal_moves

    def legal_captures(self):
        # Returns all possible captures without accounting for other pieces
        legal_captures = []

        if not self.limit:
            for captures in self.captures:
                if not outside(add_doubles(self.pos, captures)):
                    legal_captures.append(add_doubles(self.pos, captures))
                else:
                    pass
        else:
            for captures in self.captures:
                for mult in range(1,8):
                    if not outside(add_doubles(self.pos, (captures[0] * mult, captures[1] * mult))):
                        legal_captures.append(add_doubles(self.pos, (captures[0] * mult, captures[1] * mult)))
                    else:
                        pass

        return legal_captures

# Rules for every piece so that I can easily reuse them for each piece
pawn_rules = [((0, 1)), ((1, 1), (-1, 1)), False]
knight_rules = [((1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1))]
knight_rules.append(knight_rules[0])
knight_rules.append(False)
bishop_rules = [((1, 1), (-1, 1), (-1, -1), (1, -1))]
bishop_rules.append(bishop_rules[0])
bishop_rules.append(True)
rook_rules = [(1, 0), (0, 1), (-1, 0), (0, -1)]
rook_rules.append(rook_rules[0])
rook_rules.append(True)
queen_rules = [bishop_rules[0] + rook_rules[0]]
queen_rules.append(queen_rules[0])
queen_rules.append(True)
king_rules = [bishop_rules[0] + rook_rules[0]]
king_rules.append(king_rules[0])
king_rules.append(False)

class Board:
    def __init__(self, board):
        """board is a dictionary of length 64 that contains the game board"""
        self.board = board

    def make_move(self, start, end):
        """This will return the board after a move was made.
        start is the position of the piece before the move
        end is the position of the piece after the move"""
        # Because of how this method is set up, there's no need for a separate function for captures
        # I will replace this with code to animate the piece moving
        while False:
            pass

        self.board[end] = [self.board[start]]
        self.board[start] = []

        return self.board

# This creates the standard board for the game
standard_board = {}
standard_board[(0, 0)] = [Piece((0, 0), rook_rules[0], rook_rules[1], rook_rules[2]), 5]
standard_board[(1, 0)] = [Piece((1, 0), knight_rules[0], knight_rules[1], knight_rules[2]), 3]
standard_board[(2, 0)] = [Piece((2, 0), bishop_rules[0], bishop_rules[1], bishop_rules[2]), 3]
standard_board[(3, 0)] = [Piece((3, 0), queen_rules[0], queen_rules[1], queen_rules[2]), 9]
standard_board[(4, 0)] = [Piece((4, 0), king_rules[0], king_rules[1], king_rules[1]), 99]
standard_board[(5, 0)] = [Piece((5, 0), bishop_rules[0], bishop_rules[1], bishop_rules[2]), 3]
standard_board[(6, 0)] = [Piece((6, 0), knight_rules[0], knight_rules[1], knight_rules[2]), 3]
standard_board[(7, 0)] = [Piece((7, 0), rook_rules[0], rook_rules[1], rook_rules[2]), 5]
for i in range(8):
    standard_board[(i, 0)] = [Piece((i, 0), pawn_rules[0], pawn_rules[1], pawn_rules[2]), 1]
for i in range(4):
    for k in range(8):
        standard_board[(k, 2 + i)] = [0, 0]
for i in range(8):
    standard_board[(i, 6)] = [Piece((i, 6), pawn_rules[0], pawn_rules[1], pawn_rules[2]), 1]
standard_board[(0, 7)] = [Piece((0, 7), rook_rules[0], rook_rules[1], rook_rules[2]), 5]
standard_board[(1, 7)] = [Piece((1, 7), knight_rules[0], knight_rules[1], knight_rules[2]), 3]
standard_board[(2, 7)] = [Piece((2, 7), bishop_rules[0], bishop_rules[1], bishop_rules[2]), 3]
standard_board[(3, 7)] = [Piece((3, 7), queen_rules[0], queen_rules[1], queen_rules[2]), 9]
standard_board[(4, 7)] = [Piece((4, 7), king_rules[0], king_rules[1], king_rules[1]), 99]
standard_board[(5, 7)] = [Piece((5, 7), bishop_rules[0], bishop_rules[1], bishop_rules[2]), 3]
standard_board[(6, 7)] = [Piece((6, 7), knight_rules[0], knight_rules[1], knight_rules[2]), 3]
standard_board[(7, 7)] = [Piece((7, 7), rook_rules[0], rook_rules[1], rook_rules[2]), 5]

GameBoard = Board(standard_board)

# Initial menu screen
screen.fill(green)

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()