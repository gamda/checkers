import unittest
import random
from checkers.model import Model, Chip
from gameboard.coordinate import Coordinate

class TestChip(unittest.TestCase):

    # def setUp(self):
    #     self.chip = Chip(Chip.Color.white)

    def test_init_raises_color_exception(self):
        self.assertRaises(ValueError, Chip, "invalid color")

    def test_correct_color(self):
        newChip = Chip(Chip.Color.white)
        self.assertEqual(newChip.color, Chip.Color.white)
        newChip = Chip(Chip.Color.black)
        self.assertEqual(newChip.color, Chip.Color.black)

    def test_promote(self):
        chip = Chip(Chip.Color.white)
        chip.promote()
        self.assertEqual(chip.type, Chip.Type.queen)

class TestModel(unittest.TestCase):

    def setUp(self):
        self.model = Model()

    def test_initial_state(self):
        self.assertEqual(len(self.model.chips.keys()), 24)
        self.assertEqual(self.model.board.getContent(Coordinate.a1).color, 
            Chip.Color.white)
        self.assertEqual(self.model.board.getContent(Coordinate.c1).color, 
            Chip.Color.white)
        self.assertEqual(self.model.board.getContent(Coordinate.e1).color, 
            Chip.Color.white)
        self.assertEqual(self.model.board.getContent(Coordinate.g1).color, 
            Chip.Color.white)
        self.assertEqual(self.model.board.getContent(Coordinate.b2).color, 
            Chip.Color.white)
        self.assertEqual(self.model.board.getContent(Coordinate.d2).color, 
            Chip.Color.white)
        self.assertEqual(self.model.board.getContent(Coordinate.f2).color, 
            Chip.Color.white)
        self.assertEqual(self.model.board.getContent(Coordinate.h2).color, 
            Chip.Color.white)
        self.assertEqual(self.model.board.getContent(Coordinate.a3).color, 
            Chip.Color.white)
        self.assertEqual(self.model.board.getContent(Coordinate.c3).color, 
            Chip.Color.white)
        self.assertEqual(self.model.board.getContent(Coordinate.e3).color, 
            Chip.Color.white)
        self.assertEqual(self.model.board.getContent(Coordinate.g3).color, 
            Chip.Color.white)
        self.assertEqual(self.model.board.getContent(Coordinate.b6).color, 
            Chip.Color.black)
        self.assertEqual(self.model.board.getContent(Coordinate.d6).color, 
            Chip.Color.black)
        self.assertEqual(self.model.board.getContent(Coordinate.f6).color, 
            Chip.Color.black)
        self.assertEqual(self.model.board.getContent(Coordinate.h6).color, 
            Chip.Color.black)
        self.assertEqual(self.model.board.getContent(Coordinate.a7).color, 
            Chip.Color.black)
        self.assertEqual(self.model.board.getContent(Coordinate.c7).color, 
            Chip.Color.black)
        self.assertEqual(self.model.board.getContent(Coordinate.e7).color, 
            Chip.Color.black)
        self.assertEqual(self.model.board.getContent(Coordinate.g7).color, 
            Chip.Color.black)
        self.assertEqual(self.model.board.getContent(Coordinate.b8).color, 
            Chip.Color.black)
        self.assertEqual(self.model.board.getContent(Coordinate.d8).color, 
            Chip.Color.black)
        self.assertEqual(self.model.board.getContent(Coordinate.f8).color, 
            Chip.Color.black)
        self.assertEqual(self.model.board.getContent(Coordinate.h8).color, 
            Chip.Color.black)

    def test_chip_available_moves_white_turn(self):
        # None white chip with one move
        moves = self.model._chipAvailableMoves(Coordinate.a3)
        answer = set([Coordinate.b4])
        self.assertEqual(moves, answer)
        # None white chip with two moves
        moves = self.model._chipAvailableMoves(Coordinate.c3)
        answer = set([Coordinate.b4, Coordinate.d4])
        self.assertEqual(moves, answer)
        # None black chip, no moves
        moves = self.model._chipAvailableMoves(Coordinate.b6)
        answer = set()
        self.assertEqual(moves, answer)
        # None empty square, no moves
        moves = self.model._chipAvailableMoves(Coordinate.c6)
        self.assertEqual(moves, answer)

    # def test_available_moves_raises_TypeError(self):
    #     self.assertRaises(TypeError,self.model._chipAvailableMoves,"notCoordinate")

    # def test_available_moves_white(self):
    #     modelMoves = self.model.validMoves()
    #     correctMoves = set([(Coordinate.a3,Coordinate.b4),
    #                         (Coordinate.c3,Coordinate.b4),
    #                         (Coordinate.c3,Coordinate.d4),
    #                         (Coordinate.e3,Coordinate.d4),
    #                         (Coordinate.e3,Coordinate.f4),
    #                         (Coordinate.g3,Coordinate.f4),
    #                         (Coordinate.g3,Coordinate.h4)])
    #     self.assertEqual(modelMoves, correctMoves)

    # def test_move_chip(self):
    #     model.move()

    # def test_white_turn(self):
    #     self.assertEqual(self.model.whoseTurn(), Chip.Color.white)

    # def test_black_turn(self):

if __name__ == '__main__':
    unittest.main()