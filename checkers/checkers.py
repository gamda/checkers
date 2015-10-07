import sys, pygame
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
blackSquare = 221, 164, 72
whiteSquare = 234, 249, 217

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

model = Model()

def main( ):
    drawSquares()
    drawChips()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

def drawSquares():
    screen.fill(board)
    for i in range(8):
        for j in range(8):
            index = i * 8 + j
            if i % 2 : #odd row, start with light square
                if j % 2 : #odd square, make it dark
                    pygame.draw.rect(screen, blackSquare, squareRects[index])
                else: #even square make it light
                    pygame.draw.rect(screen, whiteSquare, squareRects[index])
            else: #even row, start with dark square
                if j % 2 : #odd square, make it light
                    pygame.draw.rect(screen, whiteSquare, squareRects[index])
                else:# make it dark
                    pygame.draw.rect(screen, blackSquare, squareRects[index])
    pygame.display.flip()

def drawChips():
    for k, c in model.chips.items():
        center = squareRects[k].center
        color = whiteChip if c.color == Chip.Color.white else blackChip
        pygame.draw.circle(screen, color, center, 25)
    pygame.display.flip()


if __name__ == '__main__':
    main()
