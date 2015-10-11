import sys, pygame
import pygame.locals
from model import Model, Chip
from gameboard.coordinate import Coordinate

pygame.init()
# set up fonts
basicFont = pygame.font.SysFont(None, 48)
infoFont = pygame.font.SysFont(None,20)

# window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
MARGIN = 40
SQR_WIDTH = 65
SQR_HEIGHT = 65

###### INITIALIZE DISPLAY #######
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT),0,32)
pygame.display.set_caption( 'Checkers!' )

board = 147, 75, 0
blackSquare = 211, 154, 62
whiteSquare = 234, 249, 217
highlight = 255, 215, 0

blackChip = 0, 0, 0
whiteChip = 255, 0, 0

btnPanel = pygame.Rect(WINDOW_HEIGHT,0,
                       WINDOW_WIDTH-WINDOW_HEIGHT,WINDOW_HEIGHT)
txtReset = basicFont.render( "Reset", True, (0,0,0), board )
btnReset = txtReset.get_rect()
btnReset.centerx = btnPanel.centerx
btnReset.top = WINDOW_HEIGHT // 2

# generate squares for the board
drawX, drawY = MARGIN - SQR_WIDTH, WINDOW_HEIGHT - MARGIN - SQR_HEIGHT

squareRects = {}
for i in range(64):
    if i % 8 == 0: # new row
        drawX += SQR_WIDTH
        drawY = WINDOW_HEIGHT - MARGIN - SQR_HEIGHT
    squareRects[Coordinate(i)] = pygame.Rect(drawX,drawY,SQR_WIDTH,SQR_HEIGHT)
    drawY -= SQR_HEIGHT
highlightedSquares = []

model = Model()
chosenChip = None
moveDestinations = set()
chipSelected = False

def main( ):
    drawScreen()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                # a click happened
                #-----------------
                handleClick(event.pos)

def handleClick(position):
    global model, chipSelected, chosenChip
    square, chipJustSelected = findSquareClicked(position)
    if square is None:
        # Check buttons, for now just reset
        model = Model()
        drawScreen()
    elif chipSelected and square in moveDestinations:
        move(chosenChip, square)
        chosenChip = None
        chipSelected = False
    else:
        highlightSquares(square)
        chosenChip = square
        chipSelected = chipJustSelected

def move(origin, destination):
    move, chips = model.move(origin, destination)
    unghighlightSquares()
    if len(chips) > 0:
        for c in chips:
            color = whiteOrBlackSquare(i)
            pygame.draw.rect(screen, color, squareRects[c])
        pygame.display.flip()

def findSquareClicked(pos):
    square = None
    for k, s in squareRects.items():
        if s.collidepoint(pos):
            square = k
    return (square, model.squareHasAllyChip(square)) if not square is None \
            else (None, False)

def drawScreen():
    drawSquares()
    drawChips()
    drawButtons()
    drawNotation()
    pygame.display.flip()

def drawSquares():
    screen.fill(board)
    for i in Coordinate:
        color = whiteOrBlackSquare(i)
        pygame.draw.rect(screen, color, squareRects[i])

def drawChips():
    for coord in model.chips.keys():
        drawChip(coord)

def drawChip(coord):
    chip = model.chips[coord]
    center = squareRects[coord].center
    color = whiteChip if chip.color == Chip.Color.white else blackChip
    pygame.draw.circle(screen, color, center, 25)

def drawButtons():
    screen.blit(txtReset, btnReset)

def drawNotation():
    for n in range(8):
        txt = basicFont.render(str(n + 1), True, (0,0,0), board)
        lbl = txt.get_rect()
        lbl.centerx = MARGIN // 2
        lbl.centery = squareRects[Coordinate(n)].centery
        screen.blit(txt, lbl)
    letters = ['a','b','c','d','e','f','g','h']
    for i in range(len(letters)):
        txt = basicFont.render(letters[i], True, (0,0,0), board)
        lbl = txt.get_rect()
        lbl.centery = WINDOW_HEIGHT - MARGIN // 2
        lbl.centerx = squareRects[Coordinate(i * 8)].centerx
        screen.blit(txt, lbl)
    # txtReset = basicFont.render( "Reset", True, (0,0,0), board )
    # btnReset = txtReset.get_rect()
    # btnReset.centerx = btnPanel.centerx
    # btnReset.top = WINDOW_HEIGHT // 2

def highlightSquares(coord):
    global moveDestinations
    unghighlightSquares()
    if coord in model.chips.keys() and \
            model.turn == model.chips[coord].color: # only highlight if there's a chip
        toHighlight = [coord]
        moves = model.availableMoves() & \
                model.chipAvailableMoves(coord)[0] # must be in both
        # if len(moves) > 0: # only highlight if there are available moves
        for m in moves:
            toHighlight.append(m[1])
            moveDestinations.add(m[1])
        for s in toHighlight:
            highlightOneSquare(s)

def highlightOneSquare(coord):
    highlightedSquares.append(coord)
    pygame.draw.rect(screen, highlight, squareRects[coord])
    height = SQR_HEIGHT - 8
    width = SQR_WIDTH - 8
    left = squareRects[coord].left + 4
    top = squareRects[coord].top + 4
    sqrColor = whiteOrBlackSquare(coord)
    highlightedRect = pygame.Rect(left,top,width,height)
    pygame.draw.rect(screen, sqrColor, highlightedRect)

    if coord in model.chips.keys():
        drawChip(coord)
    pygame.display.flip()

def unghighlightSquares():
    for s in highlightedSquares:
        unhighlightOneSquare(s)

def unhighlightOneSquare(coord):
    global highlightedSquares
    highlightedSquares = highlightedSquares[1:]
    color = whiteOrBlackSquare(coord)
    pygame.draw.rect(screen,color, squareRects[coord])
    
    # Redraw chip if there is one
    if coord in model.chips.keys():
        drawChip(coord)
    pygame.display.flip()

def whiteOrBlackSquare(coord):
    evenLetter = (coord // 8) % 2 == 1 # b, d, f, h are even letters
    evenSquare = coord % 2 == 1 # even squares have odd values
    if evenLetter and evenSquare:
        return blackSquare
    elif evenLetter and not evenSquare:
        return whiteSquare
    elif not evenLetter and evenSquare:
        return whiteSquare
    else: # not evenLetter and not evenSquare
        return blackSquare

if __name__ == '__main__':
    main()
