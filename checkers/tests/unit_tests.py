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
        # White chip with one move
        moves = self.model._chipAvailableMoves(Coordinate.a3)
        answer = set([(Coordinate.a3,Coordinate.b4)])
        self.assertEqual(moves, answer)
        # White chip with two moves
        moves = self.model._chipAvailableMoves(Coordinate.c3)
        answer = set([(Coordinate.c3,Coordinate.b4),
                        (Coordinate.c3,Coordinate.d4)])
        self.assertEqual(moves, answer)
        # Black chip, no moves
        moves = self.model._chipAvailableMoves(Coordinate.b6)
        answer = set()
        self.assertEqual(moves, answer)
        # Empty square, no moves
        moves = self.model._chipAvailableMoves(Coordinate.c6)
        self.assertEqual(moves, answer)

    def test_chip_available_moves_black_turn(self):
        self.model.move(Coordinate.a3,Coordinate.b4)
        # Black chip with one move
        moves = self.model._chipAvailableMoves(Coordinate.h6)
        answer = set([(Coordinate.h6,Coordinate.g5)])
        self.assertEqual(moves, answer)
        # Black chip with two moves
        moves = self.model._chipAvailableMoves(Coordinate.d6)
        answer = set([(Coordinate.d6,Coordinate.c5),
                        (Coordinate.d6,Coordinate.e5)])
        self.assertEqual(moves, answer)
        # White chip, no moves
        moves = self.model._chipAvailableMoves(Coordinate.b4)
        answer = set()
        self.assertEqual(moves, answer)
        # Empty square, no moves
        moves = self.model._chipAvailableMoves(Coordinate.c6)
        self.assertEqual(moves, answer)

    def test_available_moves_white(self):
        modelMoves = self.model.availableMoves()
        correctMoves = set([(Coordinate.a3,Coordinate.b4),
                            (Coordinate.c3,Coordinate.b4),
                            (Coordinate.c3,Coordinate.d4),
                            (Coordinate.e3,Coordinate.d4),
                            (Coordinate.e3,Coordinate.f4),
                            (Coordinate.g3,Coordinate.f4),
                            (Coordinate.g3,Coordinate.h4)])
        self.assertEqual(modelMoves, correctMoves)

    def test_available_moves_black(self):
        self.model.move(Coordinate.a3,Coordinate.b4)
        modelMoves = self.model.availableMoves()
        correctMoves = set([(Coordinate.b6,Coordinate.a5),
                            (Coordinate.b6,Coordinate.c5),
                            (Coordinate.d6,Coordinate.c5),
                            (Coordinate.d6,Coordinate.e5),
                            (Coordinate.f6,Coordinate.e5),
                            (Coordinate.f6,Coordinate.g5),
                            (Coordinate.h6,Coordinate.g5)])
        self.assertEqual(modelMoves, correctMoves)

    def test_move_raises_TypeError(self):
        self.assertRaises(TypeError, self.model.move,
            origin = "notCoordinate",
            destination = Coordinate.e3)
        self.assertRaises(TypeError, self.model.move,
            origin = Coordinate.a1,
            destination = "notCoordinate")

    def test_move_white_invalid(self):
        chip = self.model.board.getContent(Coordinate.a3)
        move = self.model.move(Coordinate.a3, Coordinate.c4)
        self.assertFalse(move)
        self.assertIs(chip, self.model.board.getContent(Coordinate.a3))
        self.assertNotIn(Coordinate.c4, self.model.chips.keys())
        self.assertIs(chip, self.model.chips[Coordinate.a3])

    def test_move_white_valid_no_jump(self):
        chip = self.model.board.getContent(Coordinate.a3)
        move = self.model.move(Coordinate.a3,Coordinate.b4)
        self.assertIs(self.model.board.getContent(Coordinate.a3), None)
        self.assertTrue(move)
        self.assertIs(self.model.board.getContent(Coordinate.b4), chip)
        self.assertIn(Coordinate.b4, self.model.chips.keys())
        self.assertIs(chip, self.model.chips[Coordinate.b4])
        self.assertEqual(self.model.turn, Chip.Color.black)

    def test_move_black_invalid(self):
        self.model.move(Coordinate.a3,Coordinate.b4)
        chip = self.model.board.getContent(Coordinate.h6)
        move = self.model.move(Coordinate.h6, Coordinate.g4)
        self.assertFalse(move)
        self.assertIs(chip, self.model.board.getContent(Coordinate.h6))
        self.assertNotIn(Coordinate.g4, self.model.chips.keys())
        self.assertIs(chip, self.model.chips[Coordinate.h6])

    def test_move_black_valid_no_jump(self):
        self.model.move(Coordinate.a3,Coordinate.b4)
        chip = self.model.board.getContent(Coordinate.h6)
        move = self.model.move(Coordinate.h6, Coordinate.g5)
        self.assertIs(self.model.board.getContent(Coordinate.h6), None)
        self.assertTrue(move)
        self.assertIs(self.model.board.getContent(Coordinate.g5), chip)
        self.assertIn(Coordinate.g5, self.model.chips.keys())
        self.assertIs(chip, self.model.chips[Coordinate.g5])
        self.assertIs(self.model.turn, Chip.Color.white)



if __name__ == '__main__':
    unittest.main()