import pygame
import copy
import sys
import os

pygame.init()

# The function below and the definition of music_path were made using AI
def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

music_path = get_resource_path(os.path.join("sfx", "piece_moving.ogg"))
pygame.mixer.music.load(music_path)

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

# Title for the menu
title_surf = pygame.Surface((810, 162))
title_surf.fill(brown)
title_rect = title_surf.get_rect(center=(screen.get_rect().centerx, screen.get_rect().centery - 324))
title_text = title_font.render("Chess Game", True, 'White')
title_text_rect = title_text.get_rect(center=title_rect.center)

# Buttons and text for the menu to exit a game mode
exit_surf = pygame.Surface((675, 162))
exit_surf.fill(brown)
exit_rect = exit_surf.get_rect(center=(screen.get_rect().centerx, screen.get_rect().centery - 324))
exit_title = title_font.render("Are You Sure?", True, 'White')
exit_title_rect = exit_title.get_rect(center = exit_rect.center)

exit_button = pygame.Surface((540, 270))
exit_button.fill('Brown')
exit_button_rect = exit_button.get_rect(center=(screen.get_rect().centerx - 324, screen.get_rect().centery))
exit_button_text = font.render("Exit", True, 'White')
exit_button_text_rect = exit_button_text.get_rect(center=exit_button_rect.center)

return_button = pygame.Surface((540, 270))
return_button.fill(brown)
return_button_rect = exit_button.get_rect(center=(screen.get_rect().centerx + 324, screen.get_rect().centery))
return_button_text = font.render("Return", True, 'White')
return_button_text_rect = return_button_text.get_rect(center=return_button_rect.center)

info_surf = pygame.Surface((540, 100))
info_rect = info_surf.get_rect(topleft=screen.get_rect().topleft)
info_text = small_font.render("Press 'Esc' to exit to the menu", True, 'Black')
info_text_rect = info_text.get_rect(topleft=info_rect.topleft)

# Button for playing against a bot
bot_surf = pygame.Surface((540, 135))
bot_surf.fill(brown)
bot_rect = bot_surf.get_rect(center=(screen.get_rect().centerx, screen.get_rect().centery - 108))
bot_text = font.render("Play Against A Bot", True, 'White')
bot_text_rect = bot_text.get_rect(center=bot_rect.center)

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
    def __init__(self, pos, move_rules, capture_rules, limited, type, first):
        """Move_rules will be a tuple of all possible moves represented by displacements
        capture_rules will be a tuple of all possible captures represented by displacements"""
        self.pos = pos
        self.moves = move_rules
        self.captures = capture_rules
        self.limit = limited
        self.type = type
        self.first = first

    def legal_moves(self, Board):
        # Returns the list of all possible moves for a piece accounting for other pieces
        legal_moves = []

        if not self.limit:
            for moves in self.moves():
                if not outside(add_doubles(self.pos, moves)):
                    if Board.board[add_doubles(self.pos, moves)][0] == 0:
                        legal_moves.append(add_doubles(self.pos, moves))
                    else:
                        pass
                else:
                    break

        else:
            for moves in self.moves():
                for mult in range(1, 8):
                    if not outside(add_doubles(self.pos, (moves[0] * mult, moves[1] * mult))):
                        if Board.board[add_doubles(self.pos, (moves[0] * mult, moves[1] * mult))][0] == 0:
                            legal_moves.append(add_doubles(self.pos, (moves[0] * mult, moves[1] * mult)))
                        else:
                            pass
                    else:
                        break

        return legal_moves

    def legal_captures(self, Board):
        # Returns the list of all possible captures for a piece
        legal_captures = []

        if not self.limit:
            for captures in self.captures():
                if not outside(add_doubles(self.pos, captures)):
                    if Board.board[add_doubles(self.pos, captures)][0].first ^ self.first:
                        legal_captures.append(add_doubles(self.pos, captures))
                    else:
                        pass
                else:
                    break

        else:
            for captures in self.captures():
                for mult in range(1, 8):
                    if not outside(add_doubles(self.pos, (captures[0] * mult, captures[1] * mult))):
                        if Board.board[add_doubles(self.pos, (captures[0] * mult, captures[1] * mult))][0].first ^ self.first:
                            legal_captures.append(add_doubles(self.pos, (captures[0] * mult, captures[1] * mult)))
                        else:
                            pass
                    else:
                        break

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
            clock.tick(60)


        self.board[end] = [self.board[start]]
        self.board[start] = []

        return self.board

# This creates the standard board for the game
standard_board = {}
standard_board[(0, 0)] = [Piece((0, 0), rook_rules[0], rook_rules[1], rook_rules[2], "R", True), 5]
standard_board[(1, 0)] = [Piece((1, 0), knight_rules[0], knight_rules[1], knight_rules[2], "N", True), 3]
standard_board[(2, 0)] = [Piece((2, 0), bishop_rules[0], bishop_rules[1], bishop_rules[2], "B", True), 3]
standard_board[(3, 0)] = [Piece((3, 0), queen_rules[0], queen_rules[1], queen_rules[2], "Q", True), 9]
standard_board[(4, 0)] = [Piece((4, 0), king_rules[0], king_rules[1], king_rules[1], "K", True), 99]
standard_board[(5, 0)] = [Piece((5, 0), bishop_rules[0], bishop_rules[1], bishop_rules[2], "B", True), 3]
standard_board[(6, 0)] = [Piece((6, 0), knight_rules[0], knight_rules[1], knight_rules[2], "N", True), 3]
standard_board[(7, 0)] = [Piece((7, 0), rook_rules[0], rook_rules[1], rook_rules[2], "R", True), 5]
for i in range(8):
    standard_board[(i, 0)] = [Piece((i, 0), pawn_rules[0], pawn_rules[1], pawn_rules[2], "", True), 1]
for i in range(4):
    for k in range(8):
        standard_board[(k, 2 + i)] = [0, 0]
for i in range(8):
    standard_board[(i, 6)] = [Piece((i, 6), pawn_rules[0], pawn_rules[1], pawn_rules[2], "", False), 1]
standard_board[(0, 7)] = [Piece((0, 7), rook_rules[0], rook_rules[1], rook_rules[2], "R", False), 5]
standard_board[(1, 7)] = [Piece((1, 7), knight_rules[0], knight_rules[1], knight_rules[2], "N", False), 3]
standard_board[(2, 7)] = [Piece((2, 7), bishop_rules[0], bishop_rules[1], bishop_rules[2], "B", False), 3]
standard_board[(3, 7)] = [Piece((3, 7), queen_rules[0], queen_rules[1], queen_rules[2], "Q", False), 9]
standard_board[(4, 7)] = [Piece((4, 7), king_rules[0], king_rules[1], king_rules[1], "K", False), 99]
standard_board[(5, 7)] = [Piece((5, 7), bishop_rules[0], bishop_rules[1], bishop_rules[2], "B", False), 3]
standard_board[(6, 7)] = [Piece((6, 7), knight_rules[0], knight_rules[1], knight_rules[2], "N", False), 3]
standard_board[(7, 7)] = [Piece((7, 7), rook_rules[0], rook_rules[1], rook_rules[2], "R", False), 5]

GameBoard = Board(standard_board)

board_rects = []

for i in range(8):
    for k in range(8):
        board_rects.append(pygame.Rect(140 + k * 100, 732 - i * 100, 100, 100))

def draw_board(Board):
    # The variable Board will eventually be used to draw the pieces
    for i in range(8):
        for k in range(8):
            if i % 2 == 0 and k % 2 == 0 or i % 2 == 1 and k % 2 == 1:
                pygame.draw.rect(screen, brown, board_rects[i * 8 + k])
            else:
                pygame.draw.rect(screen, beige, board_rects[i * 8 + k])

# Initial menu screen
screen.fill(green)
screen.blit(title_surf, title_rect)
screen.blit(title_text, title_text_rect)
screen.blit(bot_surf, bot_rect)
screen.blit(bot_text, bot_text_rect)

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mode == 0:
                if bot_rect.collidepoint(mouse_pos):
                    mode = 1
                    screen.fill(green)
                    current_board = copy.deepcopy(GameBoard)
                    draw_board(current_board)

                    screen.blit(info_text, info_text_rect)
            if mode == -1:
                if exit_button_rect.collidepoint(mouse_pos):
                    mode = 0

                    screen.fill(green)
                    screen.blit(title_surf, title_rect)
                    screen.blit(title_text, title_text_rect)
                    screen.blit(bot_surf, bot_rect)
                    screen.blit(bot_text, bot_text_rect)

                elif return_button_rect.collidepoint(mouse_pos):
                    mode = 1
                    screen.fill(green)
                    current_board = standard_board.copy()
                    draw_board(current_board)

                    screen.blit(info_text, info_text_rect)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("Pressed")
                if mode > 0:
                    mode = -1 # Mode for the menu where you can exit whichever mode you are playing
                    screen.fill(green)

                    screen.blit(exit_surf, exit_rect)
                    screen.blit(exit_title, exit_title_rect)
                    screen.blit(exit_button, exit_button_rect)
                    screen.blit(exit_button_text, exit_button_text_rect)
                    screen.blit(return_button, return_button_rect)
                    screen.blit(return_button_text, return_button_text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()