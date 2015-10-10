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

    def _neighborContentInDirection(self, square, direction):
        neighborSquare = self.board.neighborInDirection(square, direction)
        if not neighborSquare is None:
            return {"coordinate": neighborSquare, 
                    "content": self.board.getContent(neighborSquare)}
        return False

    def _nextNeighborContentInSquare(self, square, direction):
        neighborSquare = self.board.neighborInDirection(square, direction)
        if not neighborSquare is None: # check the next
            newNeighbor = self.board.neighborInDirection(neighborSquare, direction)
            if not newNeighbor is None:
                return {"coordinate": newNeighbor,
                        "content": self.board.getContent(newNeighbor)}
        return False

    def _soldierChipAvailableMoves(self, color, square):
        """Returns a list with tuples of Coordinate values of available moves for the chip

        This function is meant to be called by _chipAvailableMoves, which already
        checked that the chip exists in both the chips and board.squares dictionaries.
        For this reason, it doesn't check to see if square is a Coordinate, the check
        already happened in the previous function.

        Args:
            square (Coordinate): the square where the chip is/should be
        Returns:
            list: tuple of Coordinate values of valid moves for the chip. They have
            the form (Coordinate.origin, Coordinate.destination)

        """
        whiteDirections = [Direction.topLeft, Direction.topRight]
        blackDirections = [Direction.btmLeft, Direction.btmRight]
        directions = whiteDirections if color == Chip.Color.white else blackDirections

        moves = set()
        canJump = False
        for direction in directions:
            neighbor = self._neighborContentInDirection(square, direction)
            if neighbor is False: # outside the board
                pass 
            elif neighbor["content"] is None: # empty square, valid move
                if not canJump:
                    moves.add((square, neighbor["coordinate"]))
            elif neighbor["content"].color != color: # Check next square for jump
                nextNeighbor = self._nextNeighborContentInSquare(square, direction)
                if nextNeighbor and nextNeighbor["content"] is None:
                    if canJump:
                        moves.add((square, nextNeighbor["coordinate"]))
                    else: # first jump move found, delete previous moves
                        canJump = True
                        moves = set([(square, nextNeighbor["coordinate"])])
        return moves

    def chipAvailableMoves(self, square):
        if square not in self.chips.keys() or self.board.getContent(square) is None:
            # chip is not in the game anymore
            return set()
        chip = self.chips[square]
        if chip.color != self.turn:
            return set()
        if chip.type == Chip.Type.soldier:
            if chip.color == Chip.Color.white:
                return self._soldierChipAvailableMoves(Chip.Color.white, square)
            else: # chip.color = black
                return self._soldierChipAvailableMoves(Chip.Color.black, square)

    def availableMoves(self):
        """Returns a set with tuples of Coordinate values of all available moves

        This function is meant to be called by _chipAvailableMoves, which already
        checked that the chip exists in both the chips and board.squares dictionaries.
        For this reason, it doesn't check to see if square is a Coordinate, the check
        already happened in the previous function.

        Returns:
            set: tuple of Coordinate values of valid moves for the chip. They have
            the form (Coordinate.origin, Coordinate.destination)

        """
        moves = set()
        if self.turn == Chip.Color.white:
            for coord, chip in self.chips.items(): # soldiers
                moves = moves | self.chipAvailableMoves(coord)
        else: # self.turn = black
            for coord, chip in self.chips.items(): # soldiers
                moves = moves | self.chipAvailableMoves(coord)
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
        # move chip
        self.board.move(origin, destination)
        self.chips[destination] = self.chips[origin]
        del self.chips[origin]
        self.turn = Chip.Color.black \
                    if self.turn == Chip.Color.white \
                    else Chip.Color.white
        # remove chips if jump occured
        distance = destination - origin
        removed = []
        if abs(distance) != 7 and abs(distance) != 9:
            removed = self._removeChips(origin, destination)

        return (self._moveType(destination, removed), removed)

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



