import sys, pygame
import pygame.locals
from model import Model, Chip
from gameboard.coordinate import Coordinate

######### SAMPLE BOARD ###########
##
##   initial state
##
##  x _ x _ x _ x _
##  _ x _ x _ x _ x
##  x _ x _ x _ x _ 
##  _ e _ e _ e _ e 
##  e _ e _ e _ e _
##  _ o _ o _ o _ o
##  o _ o _ o _ o _
##  _ o _ o _ o _ o

# window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 570
MARGIN = 25
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
    drawSquares()
    drawChips()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                # a click happened
                #-----------------
                handleClick(event.pos)

def handleClick(position):
    global chipSelected, chosenChip
    square, chipJustSelected = findSquareClicked(position)
    if chipSelected and square in moveDestinations:
        move(chosenChip, square)
        chosenChip = None
        chipSelected = False
    else:
        highlightSquares(square)
        chosenChip = square
        chipSelected = chipJustSelected

def move(origin, destination):
    model.move(origin, destination)
    unghighlightSquares()

def findSquareClicked(pos):
    square = None
    for k, s in squareRects.items():
        if s.collidepoint(pos):
            square = k
    return (square, model.squareHasAllyChip(square))

def drawSquares():
    screen.fill(board)
    for i in Coordinate:
        color = whiteOrBlackSquare(i)
        pygame.draw.rect(screen, color, squareRects[i])
    pygame.display.flip()

def drawChips():
    for coord in model.chips.keys():
        drawChip(coord)
    pygame.display.flip()

def drawChip(coord):
    chip = model.chips[coord]
    center = squareRects[coord].center
    color = whiteChip if chip.color == Chip.Color.white else blackChip
    pygame.draw.circle(screen, color, center, 25)

def highlightSquares(coord):
    global moveDestinations
    unghighlightSquares()
    if coord in model.chips.keys() and \
            model.turn == model.chips[coord].color: # only highlight if there's a chip
        toHighlight = [coord]
        moves = model.chipAvailableMoves(coord) # (origin, destination)
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
    for i in range(8):
        for j in range(8):
            index = i * 8 + j
            if Coordinate(index) == coord:
                if i % 2 : #odd row, start with light square
                    if j % 2 : #odd square, make it dark
                        return blackSquare
                    else: #even square make it light
                        return whiteSquare
                else: #even row, start with dark square
                    if j % 2 : #odd square, make it light
                        return whiteSquare
                    else:# make it dark
                        return blackSquare

if __name__ == '__main__':
    main()
