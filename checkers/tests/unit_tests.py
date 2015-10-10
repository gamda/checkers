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
        moves, canJump = self.model.chipAvailableMoves(Coordinate.a3)
        answer = set([(Coordinate.a3,Coordinate.b4)])
        self.assertEqual(moves, answer)
        self.assertFalse(canJump)
        # White chip with two moves
        moves, canJump = self.model.chipAvailableMoves(Coordinate.c3)
        answer = set([(Coordinate.c3,Coordinate.b4),
                        (Coordinate.c3,Coordinate.d4)])
        self.assertEqual(moves, answer)
        self.assertFalse(canJump)
        # Black chip, no moves
        moves, canJump = self.model.chipAvailableMoves(Coordinate.b6)
        answer = set()
        self.assertEqual(moves, answer)
        self.assertFalse(canJump)
        # Empty square, no moves
        moves, canJump = self.model.chipAvailableMoves(Coordinate.c6)
        self.assertEqual(moves, answer)     
        self.assertFalse(canJump)

    def test_chip_available_moves_black_turn(self):
        self.model.move(Coordinate.a3,Coordinate.b4)
        # Black chip with one move
        moves, canJump = self.model.chipAvailableMoves(Coordinate.h6)
        answer = set([(Coordinate.h6,Coordinate.g5)])
        self.assertEqual(moves, answer)
        self.assertFalse(canJump)
        # Black chip with two moves
        moves, canJump = self.model.chipAvailableMoves(Coordinate.d6)
        answer = set([(Coordinate.d6,Coordinate.c5),
                        (Coordinate.d6,Coordinate.e5)])
        self.assertEqual(moves, answer)
        self.assertFalse(canJump)
        # White chip, no moves
        moves, canJump = self.model.chipAvailableMoves(Coordinate.b4)
        answer = set()
        self.assertEqual(moves, answer)
        self.assertFalse(canJump)
        # Empty square, no moves
        moves, canJump = self.model.chipAvailableMoves(Coordinate.c6)
        self.assertEqual(moves, answer)
        self.assertFalse(canJump)

    def test_chip_available_moves_white_one_jump(self):
        self.model.move(Coordinate.g3, Coordinate.f4)
        self.model.move(Coordinate.h6, Coordinate.g5)
        moves, canJump = self.model.chipAvailableMoves(Coordinate.f4)
        answer = set([(Coordinate.f4, Coordinate.h6)])
        self.assertEqual(moves, answer)
        self.assertTrue(canJump)

    def test_chip_available_moves_black_one_jump(self):
        self.model.move(Coordinate.c3, Coordinate.d4)
        self.model.move(Coordinate.d6, Coordinate.e5)
        self.model.move(Coordinate.a3, Coordinate.b4)
        moves, canJump = self.model.chipAvailableMoves(Coordinate.e5)
        answer = set([(Coordinate.e5, Coordinate.c3)])
        self.assertEqual(moves, answer)
        self.assertTrue(canJump)

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

    def test_available_moves_white_one_jump(self):
        self.model.move(Coordinate.g3, Coordinate.f4)
        self.model.move(Coordinate.h6, Coordinate.g5)
        moves = self.model.availableMoves()
        answer = set([(Coordinate.f4, Coordinate.h6)])
        self.assertEqual(moves, answer)

    def test_available_moves_black_one_jump(self):
        self.model.move(Coordinate.c3, Coordinate.d4)
        self.model.move(Coordinate.d6, Coordinate.e5)
        self.model.move(Coordinate.a3, Coordinate.b4)
        moves = self.model.availableMoves()
        answer = set([(Coordinate.e5, Coordinate.c3)])
        self.assertEqual(moves, answer)

    def test_move_raises_TypeError(self):
        self.assertRaises(TypeError, self.model.move,
            origin = "notCoordinate",
            destination = Coordinate.e3)
        self.assertRaises(TypeError, self.model.move,
            origin = Coordinate.a1,
            destination = "notCoordinate")

    def test_move_white_invalid(self):
        chip = self.model.board.getContent(Coordinate.a3)
        move, removed = self.model.move(Coordinate.a3, Coordinate.c4)
        self.assertEqual(move, self.model.MoveType.invalid)
        self.assertIs(chip, self.model.board.getContent(Coordinate.a3))
        self.assertNotIn(Coordinate.c4, self.model.chips.keys())
        self.assertIs(chip, self.model.chips[Coordinate.a3])
        self.assertEqual(len(removed),0)

    def test_move_black_invalid(self):
        self.model.move(Coordinate.a3,Coordinate.b4)
        chip = self.model.board.getContent(Coordinate.h6)
        move, removed = self.model.move(Coordinate.h6, Coordinate.g4)
        self.assertEqual(move, self.model.MoveType.invalid)
        self.assertIs(chip, self.model.board.getContent(Coordinate.h6))
        self.assertNotIn(Coordinate.g4, self.model.chips.keys())
        self.assertIs(chip, self.model.chips[Coordinate.h6])
        self.assertEqual(len(removed),0)

    def test_move_white_valid_no_jump(self):
        chip = self.model.board.getContent(Coordinate.a3)
        move, removed = self.model.move(Coordinate.a3,Coordinate.b4)
        self.assertIs(self.model.board.getContent(Coordinate.a3), None)
        self.assertEqual(move, self.model.MoveType.soldierMove)
        self.assertIs(self.model.board.getContent(Coordinate.b4), chip)
        self.assertIn(Coordinate.b4, self.model.chips.keys())
        self.assertIs(chip, self.model.chips[Coordinate.b4])
        self.assertEqual(self.model.turn, Chip.Color.black)
        self.assertEqual(len(removed),0)

    def test_move_black_valid_no_jump(self):
        self.model.move(Coordinate.a3,Coordinate.b4)
        chip = self.model.board.getContent(Coordinate.h6)
        move, removed = self.model.move(Coordinate.h6, Coordinate.g5)
        self.assertIs(self.model.board.getContent(Coordinate.h6), None)
        self.assertEqual(move, self.model.MoveType.soldierMove)
        self.assertIs(self.model.board.getContent(Coordinate.g5), chip)
        self.assertIn(Coordinate.g5, self.model.chips.keys())
        self.assertIs(chip, self.model.chips[Coordinate.g5])
        self.assertIs(self.model.turn, Chip.Color.white)
        self.assertEqual(len(removed),0)

    def test_move_white_valid_jump(self):
        self.model.move(Coordinate.g3, Coordinate.f4)
        self.model.move(Coordinate.h6, Coordinate.g5)
        eater = self.model.chips[Coordinate.f4]
        move, removed = self.model.move(Coordinate.f4, Coordinate.h6)
        self.assertEqual(move, self.model.MoveType.soldierJump)
        self.assertIs(eater, self.model.board.getContent(Coordinate.h6))
        self.assertIn(Coordinate.h6, self.model.chips.keys())
        self.assertIs(eater, self.model.chips[Coordinate.h6])
        self.assertIsNone(self.model.board.getContent(Coordinate.g5))
        self.assertNotIn(Coordinate.g5, self.model.chips.keys())
        self.assertEqual(removed, [Coordinate.g5])

    def test_move_black_valid_jump(self):
        self.model.move(Coordinate.c3, Coordinate.b4)
        self.model.move(Coordinate.b6, Coordinate.a5)
        self.model.move(Coordinate.e3, Coordinate.d4)
        eater = self.model.chips[Coordinate.a5]
        move, removed = self.model.move(Coordinate.a5, Coordinate.c3)
        self.assertEqual(move, self.model.MoveType.soldierJump)
        self.assertIs(eater, self.model.board.getContent(Coordinate.c3))
        self.assertIn(Coordinate.c3, self.model.chips.keys())
        self.assertIs(eater, self.model.chips[Coordinate.c3])
        self.assertIsNone(self.model.board.getContent(Coordinate.b4))
        self.assertNotIn(Coordinate.b4, self.model.chips.keys())
        self.assertEqual(removed, [Coordinate.b4])

    def test_square_has_ally_chip_raises_TypeError(self):
        self.assertRaises(TypeError, self.model.squareHasAllyChip, "notCoordinate")

    def test_square_has_ally_chip_empty(self):
        self.assertFalse(self.model.squareHasAllyChip(Coordinate.a4))

    def test_square_has_ally_chip_enemy(self):
        self.assertFalse(self.model.squareHasAllyChip(Coordinate.a7))

    def test_square_has_ally_chip_ally(self):
        self.assertTrue(self.model.squareHasAllyChip(Coordinate.a3))


if __name__ == '__main__':
    unittest.main()