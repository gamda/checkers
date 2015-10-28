# Copyright (c) 2015 Gamda Software, LLC
#
# See the file LICENSE.txt for copying permission.

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
    class Gamestate(Enum):
        invalidMove = -1
        inProgress = 0
        whiteWon = 1
        blackWon = 2
        tie = 3

    def new_game(self):
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
            self.board.set_content(k,self.chips[k])
        self.turn = Chip.Color.white
        self._current_chip = None

    def _neighbor_in_direction(self, square, direction):
        neighborSquare = self.board.neighbor_in_direction(square, direction)
        return neighborSquare

    def _next_neighbor_in_direction(self, square, direction):
        neighbor_square = self.board.neighbor_in_direction(square, direction)
        if neighbor_square is not None: # check the next
            new_neighbor = \
                self.board.neighbor_in_direction(neighbor_square, direction)
            if new_neighbor is not None:
                return new_neighbor
        return None

    def _enemy_in_neighbor(self, square, direction):
        neighbor = self._neighbor_in_direction(square, direction)
        return neighbor is not None and \
               self.board.get_content(neighbor) is not None and \
               self.board.get_content(neighbor).color != self.turn

    def _directions_for_soldier(self):
        white_directions = [Direction.top_left, Direction.top_right]
        black_directions = [Direction.btm_left, Direction.btm_right]
        return white_directions \
               if self.turn == Chip.Color.white \
               else black_directions

    def _soldier_available_jumps(self, square):
        jumps = set()
        for direction in self._directions_for_soldier():
            if self._enemy_in_neighbor(square, direction):
                next_neighbor = \
                    self._next_neighbor_in_direction(square, direction)
                if next_neighbor is not None and \
                        self.board.get_content(next_neighbor) is None:
                    jumps.add((square, next_neighbor))
        return jumps

    def _soldier_available_regular_moves(self, square):
        moves = set()
        for direction in self._directions_for_soldier():
            neighbor = self._neighbor_in_direction(square, direction)
            if neighbor is not None and \
                    self.board.get_content(neighbor) is None: 
                # empty square, valid move
                moves.add((square, neighbor))
        return moves

    def _soldier_can_jump(self, square):
        return bool(self._soldier_available_jumps(square))

    def _soldier_chip_available_moves(self, square):
        moves = self._soldier_available_jumps(square)
        if len(moves) > 0:
            return moves, True

        return self._soldier_available_regular_moves(square), False

    def _queen_rival_found_moves(self, 
                                 origin, 
                                 square, 
                                 direction, 
                                 moves, 
                                 can_jump):
        my_moves = moves
        neighbor = self._neighbor_in_direction(square, direction)
        if neighbor is not None:
            content = self.board.get_content(neighbor)
            if content is None and can_jump: 
                # another empty square after a jump
                my_moves.add((origin, neighbor))
                return my_moves, True
            elif content is None and not can_jump:
                # just found out queen can jump
                my_moves = set([(origin, neighbor)])
                return my_moves, True
        return moves, can_jump # two chips in a row or out of bounds

    def _queen_moves_in_direction(self, square, direction):
        moves, can_jump = set(), False
        neighbor = self._neighbor_in_direction(square, direction)
        while neighbor is not None: 
            content = self.board.get_content(neighbor)
            if content is None: # empty
                moves.add((square, neighbor))
            elif content.color != self. turn: # rival
                # rival chip found
                old_moves = moves
                moves, can_jump = self._queen_rival_found_moves(square, 
                                                                neighbor, 
                                                                direction, 
                                                                moves, 
                                                                can_jump)
                neighbor = self._neighbor_in_direction(neighbor, direction)
                if moves == old_moves:
                    break # two chips in a row or out of bounds
            else:
                break # ally chip found
            neighbor = self._neighbor_in_direction(neighbor, direction)
        return moves, can_jump

    def _queen_can_jump(self, square):
        moves, can_jump = self._queen_chip_available_moves(square)
        return can_jump

    def _queen_chip_available_moves(self, square):
        directions = [Direction.top_left, Direction.top_right,
                      Direction.btm_left, Direction.btm_right]
        moves, can_jump = set(), False

        for d in directions:
            new_moves, new_can_jump = self._queen_moves_in_direction(square, d)
            if can_jump == new_can_jump: 
                moves = moves | new_moves
            elif not can_jump and new_can_jump: 
                moves = new_moves
                can_jump = True
        return moves, can_jump

    def _chip_can_jump(self, square):
        if square in self.chips:
            if self.chips[square].type == Chip.Type.soldier:
                return self._soldier_can_jump(square)
            else:
                return self._queen_can_jump(square)
        return False

    def chip_available_moves(self, square):
        """Return a tuple (set[available_moves], bool can_jump)

        Args:
            square (Coordinate): the square where the chip is/should be
        Returns:
            set: tuple of Coordinate values of valid moves for the chip. They 
            have the form (Coordinate.origin, Coordinate.destination)
            bool: True if the chip can jump, False otherwise

        """
        if not isinstance(square, Coordinate):
            raise TypeError("square variable must be from Coordinate enum")
        if square not in self.chips.keys() or \
                self.board.get_content(square) is None:
            # chip is not in the game anymore
            return set(), False
        chip = self.chips[square]
        if chip.color != self.turn:
            return set(), False
        if chip.type == Chip.Type.soldier:
            return self._soldier_chip_available_moves(square)
        return self._queen_chip_available_moves(square)

    def available_moves(self):
        """Return a set with tuples of Coordinate values of all available moves

        Returns:
            set: tuple of Coordinate values of valid moves for the chip. They 
            have the form (Coordinate.origin, Coordinate.destination)

        """
        moves = set()
        if self._current_chip is not None:
            moves, can_jump =  self.chip_available_moves(self._current_chip)
            return moves
        can_jump = False
        for coord, chip in self.chips.items(): 
            newMoves, newcan_jump = self.chip_available_moves(coord)
            if can_jump == newcan_jump: 
                moves = moves | newMoves
            elif not can_jump and newcan_jump: # found a jump, delete old moves
                moves = newMoves
                can_jump = True
            # else found regular move, but jump found previously
        return moves

    def _promote(self, square):
        startIndex = 0 if self.turn == Chip.Color.white else 7
        promo_squares = []
        for i in range(startIndex, 64, 8):
            promo_squares.append(Coordinate(i))
        if square in promo_squares:
            self.chips[square].promote()

    def _next_turn(self):
        self.turn = Chip.Color.black \
                    if self.turn == Chip.Color.white \
                    else Chip.Color.white

    def _gamestate(self):
        if len(self.available_moves()) == 0:
            return self.Gamestate.whiteWon \
                   if self.turn == Chip.Color.black \
                   else self.Gamestate.blackWon
        return self.Gamestate.inProgress

    def _remove_chips(self, origin, destination):
        removed = []
        direction = self._direction_of_move(origin, destination)
        squares_jumped = self.board.path_in_direction(origin, 
                                                      destination, 
                                                      direction)
        for s in squares_jumped:
            if self.board.get_content(s) != None:
                self.board.clear_square(s)
                del self.chips[s]
                removed.append(s)
        return removed

    def _direction_of_move(self, origin, destination):
        distance = destination - origin
        direction = None
        if distance < 0: # moved left
            if distance % 7 == 0: # moved top
                direction = Direction.top_left
            else: # distance % 9 == 0, moved btm
                direction = Direction.btm_left
        else: # moved right
            if distance % 9 == 0:
                direction = Direction.top_right
            else:
                direction = Direction.btm_right
        return direction

    def move(self, origin, destination):
        """Perform the requested move and returns a tuple (Gamestate, list)

        Args:
            origin (Coordinate): the square where the chip is currently
            destination (Direction): the square where the chip will end
        Returns:
            Gamestate: value from enum 
            list: Coordinate values indicating the chip(s) removed
        Raises:
            TypeError: if origin or destination is not Coordinate
            
        """
        if not isinstance(origin, Coordinate):
            raise TypeError("origin variable must be from Coordinate enum")
        if not isinstance(destination, Coordinate):
            raise TypeError("destination must be from Coordinate enum")
        if not (origin, destination) in self.available_moves():
            return self.Gamestate.invalidMove, []
        turnFinished = True
        _, jumped = self.chip_available_moves(origin)
        # move chip
        self.board.move(origin, destination)
        self.chips[destination] = self.chips[origin]
        del self.chips[origin]
        self._promote(destination)
        # remove chips if jump occured
        distance = destination - origin
        removed = []
        if jumped:
            removed = self._remove_chips(origin, destination)
            if self._chip_can_jump(destination):
                turnFinished = False
                self._current_chip = destination

        if turnFinished:
            self._next_turn()
            self._current_chip = None
            self._promote(destination)
        return (self._gamestate(), removed)

    def square_contains_teammate(self, square):
        """Returns True if the chip belongs to the team whose turn it is

        Args:
            square (Coordinate): the square to check for an ally chip
        Returns:
            bool: True if the chip belongs to the team whose turn it is
        Raises:
            TypeError: if square is not Coordinate

        """
        if not isinstance(square, Coordinate):
            raise TypeError("square variable must be from Coordinate enum")
        # Python's lazy evaluation makes sure this expression will never
        # throw KeyError because if the key is not in the dictionary, the
        # second expression will not be evaluated
        return square in self.chips.keys() and \
                self.chips[square].color == self.turn



