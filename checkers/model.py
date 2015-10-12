from enum import Enum
from gameboard.gameboard import Gameboard
from gameboard.gameboard import Direction
from gameboard.coordinate import Coordinate

class Chip:
    class Color(Enum):
        white = True
        black = False
    class Type(Enum):
        soldier = 0
        queen = 1 
    
    def __init__(self, color):
        if not isinstance(color, self.Color):
            raise ValueError("Use Chip.Color values")
        self.color = color
        self.type = self.Type.soldier

    def promote(self):
        self.type = self.Type.queen

class Model:
    class MoveType(Enum):
        invalid = -1
        soldierMove = 0
        soldierJump = 1
        queenMove = 2
        queenJump = 3

    def newGame(self):
        self.__init__()
    
    def __init__(self):
        self.board = Gameboard()
        self.chips = {Coordinate.a1: Chip(Chip.Color.white),
                    Coordinate.c1: Chip(Chip.Color.white),
                    Coordinate.e1: Chip(Chip.Color.white),
                    Coordinate.g1: Chip(Chip.Color.white),
                    Coordinate.b2: Chip(Chip.Color.white),
                    Coordinate.d2: Chip(Chip.Color.white),
                    Coordinate.f2: Chip(Chip.Color.white),
                    Coordinate.h2: Chip(Chip.Color.white),
                    Coordinate.a3: Chip(Chip.Color.white),
                    Coordinate.c3: Chip(Chip.Color.white),
                    Coordinate.e3: Chip(Chip.Color.white),
                    Coordinate.g3: Chip(Chip.Color.white),
                    Coordinate.b6: Chip(Chip.Color.black),
                    Coordinate.d6: Chip(Chip.Color.black),
                    Coordinate.f6: Chip(Chip.Color.black),
                    Coordinate.h6: Chip(Chip.Color.black),
                    Coordinate.a7: Chip(Chip.Color.black),
                    Coordinate.c7: Chip(Chip.Color.black),
                    Coordinate.e7: Chip(Chip.Color.black),
                    Coordinate.g7: Chip(Chip.Color.black),
                    Coordinate.b8: Chip(Chip.Color.black),
                    Coordinate.d8: Chip(Chip.Color.black),
                    Coordinate.f8: Chip(Chip.Color.black),
                    Coordinate.h8: Chip(Chip.Color.black)}
        for k in self.chips.keys():
            self.board.setContent(k,self.chips[k])
        self.turn = Chip.Color.white
        self.currentChip = None

    def _neighborInDirection(self, square, direction):
        neighborSquare = self.board.neighborInDirection(square, direction)
        if neighborSquare is not None:
            return neighborSquare
        return False

    def _nextNeighborInDirection(self, square, direction):
        neighborSquare = self.board.neighborInDirection(square, direction)
        if neighborSquare is not None: # check the next
            newNeighbor = self.board.neighborInDirection(neighborSquare, direction)
            if newNeighbor is not None:
                return newNeighbor
        return False

    def _enemyInNeighbor(self, square, direction):
        neighbor = self._neighborInDirection(square, direction)
        return neighbor is not False and\
                self.board.getContent(neighbor) is not None and \
                self.board.getContent(neighbor).color != self.turn

    def _directions(self):
        whiteDirections = [Direction.topLeft, Direction.topRight]
        blackDirections = [Direction.btmLeft, Direction.btmRight]
        return whiteDirections if self.turn == Chip.Color.white else blackDirections

    def _soldierAvailableJumps(self, square):
        jumps = set()
        for direction in self._directions():
            if self._enemyInNeighbor(square, direction):
                nextNeighbor = self._nextNeighborInDirection(square, direction)
                if nextNeighbor is not False \
                        and self.board.getContent(nextNeighbor) is None:
                    jumps.add((square, nextNeighbor))
        return jumps

    def _soldierAvailableRegularMoves(self, square):
        moves = set()
        for direction in self._directions():
            neighbor = self._neighborInDirection(square, direction)
            if neighbor is False: # outside the board
                pass 
            elif self.board.getContent(neighbor) is None: # empty square, valid move
                moves.add((square, neighbor))
        return moves

    def _soldierCanJump(self, square):
        return len(self._soldierAvailableJumps(square)) > 0

    def _soldierChipAvailableMoves(self, square):
        moves = self._soldierAvailableJumps(square)
        if len(moves) > 0:
            return moves, True

        return self._soldierAvailableRegularMoves(square), False

    def _queenRivalFound(self, origin, square, direction, moves, canJump):
        myMoves = moves
        neighbor = self._neighborInDirection(square, direction)
        if neighbor is not False:
            content = self.board.getContent(neighbor)
            if content is None and canJump:
                myMoves.add((origin, neighbor))
                return myMoves, True
            elif content is None and not canJump:
                myMoves = set([(origin, neighbor)])
                return myMoves, True
        return moves, canJump # two chips in a row or out of bounds

    def _queenMovesInDirection(self, square, direction):
        moves, canJump = set(), False
        neighbor = self._neighborInDirection(square, direction)
        while neighbor is not False: 
            content = self.board.getContent(neighbor)
            if content is None: # empty
                moves.add((square, neighbor))
            elif content.color != self. turn: # rival
                # rival chip found
                oldMoves = moves
                moves, canJump = self._queenRivalFound(square, 
                                                        neighbor, 
                                                        direction, 
                                                        moves, 
                                                        canJump)
                neighbor = self._neighborInDirection(neighbor, direction)
                if moves == oldMoves:
                    break # two chips in a row or out of bounds
            else:
                break # ally chip found
            neighbor = self._neighborInDirection(
                        neighbor, direction)
        return moves, canJump

    def _queenCanJump(self, square):
        moves, canJump = self._queenChipAvailableMoves(square)
        return canJump

    def _queenChipAvailableMoves(self, square):
        directions = [Direction.topLeft, Direction.topRight,
                      Direction.btmLeft, Direction.btmRight]
        moves, canJump = set(), False

        for d in directions:
            newMoves, newCanJump = self._queenMovesInDirection(square, d)
            if canJump == newCanJump: 
                moves = moves | newMoves
            elif not canJump and newCanJump: # found a jump, delete old moves
                moves = newMoves
                canJump = True
        return moves, canJump

    def _chipCanJump(self, square):
        if square in self.chips.keys():
            if self.chips[square].type == Chip.Type.soldier:
                return self._soldierCanJump(square)
            else:
                return self._queenCanJump(square)
        return False

    def chipAvailableMoves(self, square):
        """Returns a tuple (set[availableMoves], bool canJump)

        Args:
            square (Coordinate): the square where the chip is/should be
        Returns:
            set: tuple of Coordinate values of valid moves for the chip. They have
            the form (Coordinate.origin, Coordinate.destination)
            bool: True if the chip can jump, False otherwise

        """
        if not isinstance(square, Coordinate):
            raise TypeError("square variable must be from Coordinate enum")
        if square not in self.chips.keys() or self.board.getContent(square) is None:
            # chip is not in the game anymore
            return set(), False
        chip = self.chips[square]
        if chip.color != self.turn:
            return set(), False
        if chip.type == Chip.Type.soldier:
            return self._soldierChipAvailableMoves(square)
        return self._queenChipAvailableMoves(square)

    # def _availableMoves(self, color):

    def availableMoves(self):
        """Returns a set with tuples of Coordinate values of all available moves

        Returns:
            set: tuple of Coordinate values of valid moves for the chip. They have
            the form (Coordinate.origin, Coordinate.destination)

        """
        moves = set()
        if self.currentChip is not None:
            moves, canJump =  self.chipAvailableMoves(self.currentChip)
            return moves
        canJump = False
        for coord, chip in self.chips.items(): 
            newMoves, newCanJump = self.chipAvailableMoves(coord)
            if canJump == newCanJump: 
                moves = moves | newMoves
            elif not canJump and newCanJump: # found a jump, delete old moves
                moves = newMoves
                canJump = True
            # else found regular move, but jump found previously
        return moves

    def move(self, origin, destination):
        """Performs the requested move and returns a tuple (MoveType, list)

        Args:
            origin (Coordinate): the square where the chip is currently
            destination (Direction): the square where the chip will end
        Returns:
            tuple: (MoveType, list)
                MoveType: value from enum
                list: Coordinate values indicating the chips removed
        Raises:
            TypeError: if origin or destination is not Coordinate
        """
        if not isinstance(origin, Coordinate):
            raise TypeError("origin variable must be from Coordinate enum")
        if not isinstance(destination, Coordinate):
            raise TypeError("destination must be from Coordinate enum")
        if not (origin, destination) in self.availableMoves():
            return self.MoveType.invalid, []
        turnFinished = True
        # move chip
        self.board.move(origin, destination)
        self.chips[destination] = self.chips[origin]
        del self.chips[origin]
        self._promote(destination)
        # remove chips if jump occured
        distance = destination - origin
        removed = []
        if abs(distance) != 7 and abs(distance) != 9: 
            removed = self._removeChips(origin, destination)
            if self._chipCanJump(destination):
                turnFinished = False
                self.currentChip = destination

        if turnFinished:
            self._nextTurn()
            self.currentChip = None
            self._promote(destination)
        return (self._moveType(destination, removed), removed)

    def _promote(self, square):
        startIndex = 0 if self.turn == Chip.Color.white else 7
        promoSquares = []
        for i in range(startIndex, 64, 8):
            promoSquares.append(Coordinate(i))
        if square in promoSquares:
            self.chips[square].promote()

    def _nextTurn(self):
        self.turn = Chip.Color.black \
                    if self.turn == Chip.Color.white \
                    else Chip.Color.white

    def _moveType(self, destination, removed):
        if len(removed) > 0:
            if self.chips[destination].type == Chip.Type.soldier:
                return self.MoveType.soldierJump
            else:
                return self.MoveType.queenJump
        else:
            if self.chips[destination].type == Chip.Type.soldier:
                return self.MoveType.soldierMove
            else:
                return self.MoveType.queenMove

    def _removeChips(self, origin, destination):
        removed = []
        direction = self._moveDirection(origin, destination)
        squaresJumped = self.board.pathInDirection(origin, destination, direction)
        for s in squaresJumped:
            if self.board.getContent(s) != None:
                self.board.clearSquare(s)
                del self.chips[s]
                removed.append(s)
        return removed

    def _moveDirection(self, origin, destination):
        distance = destination - origin
        direction = None
        if distance < 0: # moved left
            if distance % 7 == 0: # moved top
                direction = Direction.topLeft
            else: # distance % 9 == 0, moved btm
                direction = Direction.btmLeft
        else: # moved right
            if distance % 9 == 0:
                direction = Direction.topRight
            else:
                direction = Direction.btmRight
        return direction

    def squareHasAllyChip(self, square):
        """Returns True if the chip belongs to the team whose turn it is, False otherwise

        Args:
            square (Coordinate): the square to check for an ally chip
        Returns:
            Boolean: True if the chip belongs to the team whose turn it is, False otherwise
        Raises:
            TypeError: if square is not Coordinate
        """
        if not isinstance(square, Coordinate):
            raise TypeError("square variable must be from Coordinate enum")
        # Python's lazy evaluation makes sure this expression will never
        #   throw KeyError because if the key is not in the dictionary, the
        #   second expression will not be evaluated
        return square in self.chips.keys() and \
                self.chips[square].color == self.turn



