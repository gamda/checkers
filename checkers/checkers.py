# Copyright (c) 2015 Gamda Software, LLC
#
# See the file LICENSE.txt for copying permission.

import sys, pygame
import pygame.locals
from model import Model, Chip
from gameboard.coordinate import Coordinate

pygame.init()
# set up font
basic_font = pygame.font.SysFont(None, 36)

# window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
MARGIN = 40
SQR_WIDTH = 65
SQR_HEIGHT = 65

###### INITIALIZE DISPLAY #######
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT),0,32)
pygame.display.set_caption( 'Checkers!' )

# generate squares for the board
draw_x, draw_y = MARGIN - SQR_WIDTH, WINDOW_HEIGHT - MARGIN - SQR_HEIGHT

board_tile_rects = {}
for i in range(64):
    if i % 8 == 0: # new row
        draw_x += SQR_WIDTH
        draw_y = WINDOW_HEIGHT - MARGIN - SQR_HEIGHT
    board_tile_rects[Coordinate(i)] = pygame.Rect(draw_x,draw_y,
                                                  SQR_WIDTH,
                                                  SQR_HEIGHT)
    draw_y -= SQR_HEIGHT

highlighted_squares = []
buttons = {}
model = Model()
chosen_chip = None
move_destinations = set()
chip_selected = False

def main( ):
    draw_screen()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
              (event.type == pygame.KEYDOWN and \
               event.key == pygame.K_ESCAPE):
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                handle_click(event.pos)

def handle_click(position):
    global model, chip_selected, chosen_chip
    square, chip_just_selected = find_square_clicked(position)
    if square is None:
        # Check buttons
        for k, b in buttons.items():
            if b.collidepoint(position):
                if k == 'reset':
                    model.new_game()
                    draw_screen()
                elif k == 'exit':
                    sys.exit()
    elif chip_selected and square in move_destinations:
        move(chosen_chip, square)
        chosen_chip = None
        chip_selected = False
    else:
        highlight_squares(square)
        chosen_chip = square
        chip_selected = chip_just_selected

def move(origin, destination):
    move, chips = model.move(origin, destination)
    unghighlight_squares()
    update_turn()
    # remove chip if necessary
    if len(chips) > 0:
        for c in chips:
            color = tile_color(i)
            pygame.draw.rect(screen, color, board_tile_rects[c])
    pygame.display.flip()

def find_square_clicked(pos):
    square = None
    for k, s in board_tile_rects.items():
        if s.collidepoint(pos):
            square = k
    return (square, model.square_contains_teammate(square)) \
            if not square is None \
            else (None, False)

def draw_screen():
    draw_squares()
    draw_chips()
    draw_buttons()
    draw_notation()
    update_turn()
    pygame.display.flip()

def draw_squares():
    board = 147, 75, 0
    screen.fill(board)
    for i in Coordinate:
        color = tile_color(i)
        pygame.draw.rect(screen, color, board_tile_rects[i])

def draw_chips():
    for coord in model.chips.keys():
        draw_chip(coord)

def draw_chip(coord):
    black_chip = 0, 0, 0
    white_chip = 255, 0, 0
    queen_center = 127, 127, 127

    chip = model.chips[coord]
    center = board_tile_rects[coord].center
    color = white_chip if chip.color == Chip.Color.white else black_chip
    pygame.draw.circle(screen, color, center, 25)
    if chip.type == Chip.Type.queen:
        pygame.draw.circle(screen, queen_center, center,15)

def update_turn():
    black_chip = 0, 0, 0
    white_chip = 255, 0, 0
    color = white_chip if model.turn == Chip.Color.white else black_chip
    center = buttons['chip'].center
    pygame.draw.circle(screen, color, center, 25)

def draw_buttons():
    background = 226, 132, 19
    btn_BG = 246, 152, 39
    btn_Panel = pygame.Rect(WINDOW_HEIGHT,
                            0,
                            WINDOW_WIDTH-WINDOW_HEIGHT,
                            WINDOW_HEIGHT)
    pygame.draw.rect(screen, background, btn_Panel)
    
    btn_Reset = pygame.Rect(btn_Panel.left + 10, 
                            board_tile_rects[Coordinate.a3].top, 
                            btn_Panel.width - 20,
                            SQR_HEIGHT)
    buttons['reset'] = btn_Reset
    pygame.draw.rect(screen, btn_BG, btn_Reset)
    txt_Reset = basic_font.render( "New Game", True, (0,0,0), btn_BG )
    reset_rect = txt_Reset.get_rect()
    reset_rect.center = btn_Reset.center
    screen.blit(txt_Reset, reset_rect)

    btn_Exit = pygame.Rect(btn_Panel.left + 10, 
                           board_tile_rects[Coordinate.a1].top, 
                           btn_Panel.width - 20,
                           SQR_HEIGHT)
    buttons['exit'] = btn_Exit
    pygame.draw.rect(screen, btn_BG, btn_Exit)
    txt_Exit = basic_font.render("Exit (Esc)", True, (0,0,0), btn_BG)
    exit_rect = txt_Exit.get_rect()
    exit_rect.center = btn_Exit.center
    screen.blit(txt_Exit, exit_rect)

    btn_turn = pygame.Rect(btn_Panel.left + 10,
                           board_tile_rects[Coordinate.a5].top,
                           btn_Panel.width - 20,
                           SQR_HEIGHT)
    pygame.draw.rect(screen, btn_BG, btn_turn)
    txt_turn = basic_font.render("Turn: ", True, (0,0,0), btn_BG)
    turn_rect = txt_turn.get_rect()
    turn_rect.left = btn_turn.left + MARGIN // 2
    turn_rect.centery = btn_turn.centery
    screen.blit(txt_turn, turn_rect)

    btn_chip = pygame.Rect(btn_turn.left + btn_turn.width // 2,
                           board_tile_rects[Coordinate.a5].top,
                           SQR_WIDTH,
                           SQR_HEIGHT)
    buttons['chip'] = btn_chip
    pygame.draw.rect(screen, btn_BG, btn_chip)

def draw_notation():
    board = 147, 75, 0
    for n in range(8):
        txt = basic_font.render(str(n + 1), True, (0,0,0), board)
        lbl = txt.get_rect()
        lbl.centerx = MARGIN // 2
        lbl.centery = board_tile_rects[Coordinate(n)].centery
        screen.blit(txt, lbl)
    letters = ['a','b','c','d','e','f','g','h']
    for i in range(len(letters)):
        txt = basic_font.render(letters[i], True, (0,0,0), board)
        lbl = txt.get_rect()
        lbl.centery = WINDOW_HEIGHT - MARGIN // 2
        lbl.centerx = board_tile_rects[Coordinate(i * 8)].centerx
        screen.blit(txt, lbl)

def highlight_squares(coord):
    global move_destinations
    unghighlight_squares()
    if coord in model.chips.keys() and \
            model.turn == model.chips[coord].color: 
        # only highlight if there's a chip
        toHighlight = [coord]
        chip_moves, _ = model.chip_available_moves(coord)
        all_moves = model.available_moves()
        moves = chip_moves & all_moves
        for m in moves:
            toHighlight.append(m[1])
            move_destinations.add(m[1])
        for s in toHighlight:
            highlight_one_square(s)

def highlight_one_square(coord):
    highlight = 255, 215, 0
    highlighted_squares.append(coord)
    pygame.draw.rect(screen, highlight, board_tile_rects[coord])
    height = SQR_HEIGHT - 8
    width = SQR_WIDTH - 8
    left = board_tile_rects[coord].left + 4
    top = board_tile_rects[coord].top + 4
    sqrColor = tile_color(coord)
    highlightedRect = pygame.Rect(left,top,width,height)
    pygame.draw.rect(screen, sqrColor, highlightedRect)

    if coord in model.chips.keys():
        draw_chip(coord)
    pygame.display.flip()

def unghighlight_squares():
    for s in highlighted_squares:
        unhighlight_one_square(s)

def unhighlight_one_square(coord):
    global highlighted_squares
    highlighted_squares = highlighted_squares[1:]
    color = tile_color(coord)
    pygame.draw.rect(screen, color, board_tile_rects[coord])
    
    # Redraw chip if there is one
    if coord in model.chips.keys():
        draw_chip(coord)
    pygame.display.flip()

def tile_color(coord):
    black_square = 211, 154, 62
    white_square = 234, 249, 217
    even_letter = (coord // 8) % 2 == 1 # b, d, f, h are even letters
    even_square = coord % 2 == 1 # even squares have odd values in Coordinate()
    if even_letter and even_square:
        return black_square
    elif even_letter and not even_square:
        return white_square
    elif not even_letter and even_square:
        return white_square
    else: # not evenLetter and not evenSquare
        return black_square

if __name__ == '__main__':
    main()
