from enum import Enum
from gameboard.gameboard import Gameboard
from gameboard.gameboard import Direction as Direction
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
        for direction in directions:
            neighbor = self._neighborContentInDirection(square, direction)
            if neighbor is False: # outside the board
                pass 
            elif neighbor["content"] is None: # empty square, valid move
                moves.add((square, neighbor["coordinate"]))
            elif neighbor["content"].color == Chip.Color.black: # Check next square for jump
                nextNeighbor = self._nextNeighborContentInSquare(square, direction)
                if nextNeighbor["content"] is None:
                    moves.add((square, nextNeighbor["coordinate"]))
        return moves

    def _chipAvailableMoves(self, square):
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
        """Returns a list with tuples of Coordinate values of all available moves

        This function is meant to be called by _chipAvailableMoves, which already
        checked that the chip exists in both the chips and board.squares dictionaries.
        For this reason, it doesn't check to see if square is a Coordinate, the check
        already happened in the previous function.

        Returns:
            list: tuple of Coordinate values of valid moves for the chip. They have
            the form (Coordinate.origin, Coordinate.destination)

        """
        moves = set()
        if self.turn == Chip.Color.white:
            for coord, chip in self.chips.items():
                moves = moves | self._chipAvailableMoves(coord)
        return moves

    def move(self, origin, destination):
        """Returns a boolean. True if the move is successful, False if invalid

        Args:
            origin (Coordinate): the square where the chip is currently
            destination (Direction): the square where the chip will end
        Returns:
            Boolean: True if move is successful, False otherwise
        Raises:
            TypeError: if square is not Coordinate or if direction is not Direction
        """
        if not isinstance(origin, Coordinate):
            raise TypeError("origin variable must be from Coordinate enum")
        if not isinstance(destination, Coordinate):
            raise TypeError("destination must be from Direction enum")
        if not (origin, destination) in self.availableMoves():
            return False
        self.board.move(origin, destination)
        self.turn = Chip.Color.black \
                    if self.turn == Chip.Color.white \
                    else Chip.Color.white
        return True





