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

def add_doubles(double1, double2):
    # This will be useful because I will use tuples of length 2 to store positions
    return [double1[0] + double2[0], double2[1] + double2[1]]

def outside(pos):
    # Checks whether something is outside the board
    if pos[0] < 0 or pos[0] > 7 or pos[1] < 0 or pos[1] > 7:
        return True
    else:
        return False

class Piece:
    def __init__(self, pos, move_rules, capture_rules):
        """Move_rules will be a tuple of all possible moves represented by displacements
        capture_rules will be a tuple of all possible captures represented by displacements"""
        self.pos = pos
        self.moves = move_rules
        self.captures = capture_rules

    def legal_moves(self):
        # Returns all possible moves without accounting for other pieces
        legal_moves = []

        for moves in self.moves:
            if not outside(add_doubles(self.pos, moves)):
                legal_moves.append(add_doubles(self.pos, moves))
            else:
                pass

        return legal_moves

    def legal_captures(self):
        # Returns all possible captures without accounting for other pieces
        legal_captures = []

        for captures in self.captures:
            if not outside(add_doubles(self.pos, captures)):
                legal_captures.append(add_doubles(self.pos, captures))
            else:
                pass

        return legal_captures

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