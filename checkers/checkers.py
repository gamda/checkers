import sys, pygame
import pygame.locals
from model import Model, Chip
from gameboard.coordinate import Coordinate

pygame.init()
# set up fonts
basicFont = pygame.font.SysFont(None, 36)

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
drawX, drawY = MARGIN - SQR_WIDTH, WINDOW_HEIGHT - MARGIN - SQR_HEIGHT

squareRects = {}
for i in range(64):
    if i % 8 == 0: # new row
        drawX += SQR_WIDTH
        drawY = WINDOW_HEIGHT - MARGIN - SQR_HEIGHT
    squareRects[Coordinate(i)] = pygame.Rect(drawX,drawY,SQR_WIDTH,SQR_HEIGHT)
    drawY -= SQR_HEIGHT
highlightedSquares = []

buttons = {}

model = Model()
chosenChip = None
moveDestinations = set()
chipSelected = False

def main( ):
    drawScreen()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
              (event.type == pygame.KEYDOWN and \
               event.key == pygame.K_ESCAPE):
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                # a click happened
                #-----------------
                handleClick(event.pos)

def handleClick(position):
    global model, chipSelected, chosenChip
    square, chipJustSelected = findSquareClicked(position)
    if square is None:
        # Check buttons
        for k, b in buttons.items():
            if b.collidepoint(position):
                if k == 'reset':
                    model.newGame()
                    drawScreen()
                elif k == 'exit':
                    sys.exit()
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
    board = 147, 75, 0
    screen.fill(board)
    for i in Coordinate:
        color = whiteOrBlackSquare(i)
        pygame.draw.rect(screen, color, squareRects[i])

def drawChips():
    for coord in model.chips.keys():
        drawChip(coord)

def drawChip(coord):
    blackChip = 0, 0, 0
    whiteChip = 255, 0, 0
    queenCenter = 127, 127, 127

    chip = model.chips[coord]
    center = squareRects[coord].center
    color = whiteChip if chip.color == Chip.Color.white else blackChip
    pygame.draw.circle(screen, color, center, 25)
    if chip.type == Chip.Type.queen:
        pygame.draw.circle(screen, queenCenter, center,15)

def drawButtons():
    background = 226, 132, 19
    btnBG = 246, 152, 39
    btnPanel = pygame.Rect(WINDOW_HEIGHT,0,
                       WINDOW_WIDTH-WINDOW_HEIGHT,WINDOW_HEIGHT)
    pygame.draw.rect(screen, background, btnPanel)
    
    btnReset = pygame.Rect(btnPanel.left + 10, 
                            squareRects[Coordinate.a3].top, 
                            btnPanel.width - 20,
                            SQR_HEIGHT)
    buttons['reset'] = btnReset
    pygame.draw.rect(screen, btnBG, btnReset)
    txtReset = basicFont.render( "New Game", True, (0,0,0), btnBG )
    resetRect = txtReset.get_rect()
    resetRect.center = btnReset.center
    screen.blit(txtReset, resetRect)

    btnExit = pygame.Rect(btnPanel.left + 10, 
                            squareRects[Coordinate.a1].top, 
                            btnPanel.width - 20,
                            SQR_HEIGHT)
    buttons['exit'] = btnExit
    pygame.draw.rect(screen, btnBG, btnExit)
    txtExit = basicFont.render("Exit (Esc)", True, (0,0,0), btnBG)
    exitRect = txtExit.get_rect()
    exitRect.center = btnExit.center
    screen.blit(txtExit, exitRect)

def drawNotation():
    board = 147, 75, 0
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
    highlight = 255, 215, 0
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
    blackSquare = 211, 154, 62
    whiteSquare = 234, 249, 217
    evenLetter = (coord // 8) % 2 == 1 # b, d, f, h are even letters
    evenSquare = coord % 2 == 1 # even squares have odd values in Coordinate()
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
