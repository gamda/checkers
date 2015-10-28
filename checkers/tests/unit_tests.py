# Copyright (c) 2015 Gamda Software, LLC
#
# See the file LICENSE.txt for copying permission.

import unittest
import random
from checkers.model import Model, Chip
from gameboard.coordinate import Coordinate

class TestChip(unittest.TestCase):

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
        self.assertEqual(self.model.board.get_content(Coordinate.a1).color, 
            Chip.Color.white)
        self.assertEqual(self.model.board.get_content(Coordinate.c1).color, 
            Chip.Color.white)
        self.assertEqual(self.model.board.get_content(Coordinate.e1).color, 
            Chip.Color.white)
        self.assertEqual(self.model.board.get_content(Coordinate.g1).color, 
            Chip.Color.white)
        self.assertEqual(self.model.board.get_content(Coordinate.b2).color, 
            Chip.Color.white)
        self.assertEqual(self.model.board.get_content(Coordinate.d2).color, 
            Chip.Color.white)
        self.assertEqual(self.model.board.get_content(Coordinate.f2).color, 
            Chip.Color.white)
        self.assertEqual(self.model.board.get_content(Coordinate.h2).color, 
            Chip.Color.white)
        self.assertEqual(self.model.board.get_content(Coordinate.a3).color, 
            Chip.Color.white)
        self.assertEqual(self.model.board.get_content(Coordinate.c3).color, 
            Chip.Color.white)
        self.assertEqual(self.model.board.get_content(Coordinate.e3).color, 
            Chip.Color.white)
        self.assertEqual(self.model.board.get_content(Coordinate.g3).color, 
            Chip.Color.white)
        self.assertEqual(self.model.board.get_content(Coordinate.b6).color, 
            Chip.Color.black)
        self.assertEqual(self.model.board.get_content(Coordinate.d6).color, 
            Chip.Color.black)
        self.assertEqual(self.model.board.get_content(Coordinate.f6).color, 
            Chip.Color.black)
        self.assertEqual(self.model.board.get_content(Coordinate.h6).color, 
            Chip.Color.black)
        self.assertEqual(self.model.board.get_content(Coordinate.a7).color, 
            Chip.Color.black)
        self.assertEqual(self.model.board.get_content(Coordinate.c7).color, 
            Chip.Color.black)
        self.assertEqual(self.model.board.get_content(Coordinate.e7).color, 
            Chip.Color.black)
        self.assertEqual(self.model.board.get_content(Coordinate.g7).color, 
            Chip.Color.black)
        self.assertEqual(self.model.board.get_content(Coordinate.b8).color, 
            Chip.Color.black)
        self.assertEqual(self.model.board.get_content(Coordinate.d8).color, 
            Chip.Color.black)
        self.assertEqual(self.model.board.get_content(Coordinate.f8).color, 
            Chip.Color.black)
        self.assertEqual(self.model.board.get_content(Coordinate.h8).color, 
            Chip.Color.black)

    def test_chip_available_moves_raises_TypeError(self):
        self.assertRaises(TypeError, 
                          self.model.chip_available_moves, 
                          "notCoordinate")

    def test_chip_available_moves_white_turn(self):
        # White chip with one move
        moves, can_jump = self.model.chip_available_moves(Coordinate.a3)
        answer = set([(Coordinate.a3,Coordinate.b4)])
        self.assertEqual(moves, answer)
        self.assertFalse(can_jump)
        # White chip with two moves
        moves, can_jump = self.model.chip_available_moves(Coordinate.c3)
        answer = set([(Coordinate.c3,Coordinate.b4),
                        (Coordinate.c3,Coordinate.d4)])
        self.assertEqual(moves, answer)
        self.assertFalse(can_jump)
        # Black chip, no moves
        moves, can_jump = self.model.chip_available_moves(Coordinate.b6)
        answer = set()
        self.assertEqual(moves, answer)
        self.assertFalse(can_jump)
        # Empty square, no moves
        moves, can_jump = self.model.chip_available_moves(Coordinate.c6)
        self.assertEqual(moves, answer)     
        self.assertFalse(can_jump)

    def test_chip_available_moves_black_turn(self):
        self.model.move(Coordinate.a3,Coordinate.b4)
        # Black chip with one move
        moves, can_jump = self.model.chip_available_moves(Coordinate.h6)
        answer = set([(Coordinate.h6,Coordinate.g5)])
        self.assertEqual(moves, answer)
        self.assertFalse(can_jump)
        # Black chip with two moves
        moves, can_jump = self.model.chip_available_moves(Coordinate.d6)
        answer = set([(Coordinate.d6,Coordinate.c5),
                        (Coordinate.d6,Coordinate.e5)])
        self.assertEqual(moves, answer)
        self.assertFalse(can_jump)
        # White chip, no moves
        moves, can_jump = self.model.chip_available_moves(Coordinate.b4)
        answer = set()
        self.assertEqual(moves, answer)
        self.assertFalse(can_jump)
        # Empty square, no moves
        moves, can_jump = self.model.chip_available_moves(Coordinate.c6)
        self.assertEqual(moves, answer)
        self.assertFalse(can_jump)

    def test_chip_available_moves_white_one_jump(self):
        self.model.move(Coordinate.g3, Coordinate.f4)
        self.model.move(Coordinate.h6, Coordinate.g5)
        moves, can_jump = self.model.chip_available_moves(Coordinate.f4)
        answer = set([(Coordinate.f4, Coordinate.h6)])
        self.assertEqual(moves, answer)
        self.assertTrue(can_jump)

    def test_chip_available_moves_black_one_jump(self):
        self.model.move(Coordinate.c3, Coordinate.d4)
        self.model.move(Coordinate.d6, Coordinate.e5)
        self.model.move(Coordinate.a3, Coordinate.b4)
        moves, can_jump = self.model.chip_available_moves(Coordinate.e5)
        answer = set([(Coordinate.e5, Coordinate.c3)])
        self.assertEqual(moves, answer)
        self.assertTrue(can_jump)

    def test_available_moves_white(self):
        moves = self.model.available_moves()
        answer = set([(Coordinate.a3,Coordinate.b4),
                      (Coordinate.c3,Coordinate.b4),
                      (Coordinate.c3,Coordinate.d4),
                      (Coordinate.e3,Coordinate.d4),
                      (Coordinate.e3,Coordinate.f4),
                      (Coordinate.g3,Coordinate.f4),
                      (Coordinate.g3,Coordinate.h4)])
        self.assertEqual(moves, answer)

    def test_available_moves_black(self):
        self.model.move(Coordinate.a3,Coordinate.b4)
        moves = self.model.available_moves()
        answer = set([(Coordinate.b6,Coordinate.a5),
                      (Coordinate.b6,Coordinate.c5),
                      (Coordinate.d6,Coordinate.c5),
                      (Coordinate.d6,Coordinate.e5),
                      (Coordinate.f6,Coordinate.e5),
                      (Coordinate.f6,Coordinate.g5),
                      (Coordinate.h6,Coordinate.g5)])
        self.assertEqual(moves, answer)

    def test_available_moves_white_one_jump(self):
        self.model.move(Coordinate.g3, Coordinate.f4)
        self.model.move(Coordinate.h6, Coordinate.g5)
        moves = self.model.available_moves()
        answer = set([(Coordinate.f4, Coordinate.h6)])
        self.assertEqual(moves, answer)

    def test_available_moves_black_one_jump(self):
        self.model.move(Coordinate.c3, Coordinate.d4)
        self.model.move(Coordinate.d6, Coordinate.e5)
        self.model.move(Coordinate.a3, Coordinate.b4)
        moves = self.model.available_moves()
        answer = set([(Coordinate.e5, Coordinate.c3)])
        self.assertEqual(moves, answer)

    def test_available_moves_white_two_jumps(self):
        self.model.move(Coordinate.e3, Coordinate.f4)
        self.model.move(Coordinate.f6, Coordinate.e5)
        self.model.move(Coordinate.d2, Coordinate.e3)
        self.model.move(Coordinate.e5, Coordinate.d4)
        moves = self.model.available_moves()
        answer = set([(Coordinate.c3, Coordinate.e5),
                      (Coordinate.e3, Coordinate.c5)])
        self.assertEqual(moves, answer)

    def test_available_moves_black_two_jumps(self):
        self.model.move(Coordinate.c3, Coordinate.d4)
        self.model.move(Coordinate.d6, Coordinate.c5)
        self.model.move(Coordinate.g3, Coordinate.h4)
        self.model.move(Coordinate.c7, Coordinate.d6)
        self.model.move(Coordinate.f2, Coordinate.g3)
        self.model.move(Coordinate.d6, Coordinate.e5)
        self.model.move(Coordinate.e3, Coordinate.f4)
        moves = self.model.available_moves()
        answer = set([(Coordinate.c5, Coordinate.e3),
                      (Coordinate.e5, Coordinate.c3)])
        self.assertEqual(moves, answer)

    def test_available_moves_white_double_jump(self):
        self.model.move(Coordinate.c3, Coordinate.d4)
        self.model.move(Coordinate.d6, Coordinate.c5)
        self.model.move(Coordinate.b2, Coordinate.c3)
        self.model.move(Coordinate.c7, Coordinate.d6)
        self.model.move(Coordinate.c3, Coordinate.b4)
        self.model.move(Coordinate.d8, Coordinate.c7)
        self.model.move(Coordinate.d2, Coordinate.c3)
        self.model.move(Coordinate.f6, Coordinate.e5)
        # ^ this set of moves can also be used to test crowning
        moves = self.model.available_moves()
        answer = set([(Coordinate.d4, Coordinate.f6)])
        self.assertEqual(moves, answer)
        self.model.move(Coordinate.d4, Coordinate.f6)
        self.assertEqual(self.model.turn, Chip.Color.white)
        moves = self.model.available_moves()
        answer = set([(Coordinate.f6, Coordinate.d8)])
        self.assertEqual(moves, answer)

    def test_available_moves_white_double_jump_with_other_jump_available(self):
        self.model.move(Coordinate.c3, Coordinate.d4)
        self.model.move(Coordinate.d6, Coordinate.c5)
        self.model.move(Coordinate.b2, Coordinate.c3)
        self.model.move(Coordinate.c7, Coordinate.d6)
        self.model.move(Coordinate.c3, Coordinate.b4)
        self.model.move(Coordinate.d8, Coordinate.c7)
        self.model.move(Coordinate.d2, Coordinate.c3)
        self.model.move(Coordinate.f6, Coordinate.g5)
        self.model.move(Coordinate.g3, Coordinate.h4)
        self.model.move(Coordinate.d6, Coordinate.e5)
        moves = self.model.available_moves()
        answer = set([(Coordinate.d4, Coordinate.f6),
                      (Coordinate.h4, Coordinate.f6),
                      (Coordinate.b4, Coordinate.d6)])
        self.assertEqual(moves, answer)
        self.model.move(Coordinate.d4, Coordinate.f6)
        moves = self.model.available_moves()
        answer = set([(Coordinate.f6, Coordinate.d8)])
        self.assertEqual(moves, answer)

    def test_move_raises_TypeError(self):
        self.assertRaises(TypeError, self.model.move,
            origin = "notCoordinate",
            destination = Coordinate.e3)
        self.assertRaises(TypeError, self.model.move,
            origin = Coordinate.a1,
            destination = "notCoordinate")

    def test_move_white_invalid(self):
        chip = self.model.board.get_content(Coordinate.a3)
        move, removed = self.model.move(Coordinate.a3, Coordinate.c4)
        self.assertEqual(move, self.model.Gamestate.invalidMove)
        self.assertIs(chip, self.model.board.get_content(Coordinate.a3))
        self.assertNotIn(Coordinate.c4, self.model.chips.keys())
        self.assertIs(chip, self.model.chips[Coordinate.a3])
        self.assertEqual(len(removed),0)

    def test_move_black_invalid(self):
        self.model.move(Coordinate.a3,Coordinate.b4)
        chip = self.model.board.get_content(Coordinate.h6)
        move, removed = self.model.move(Coordinate.h6, Coordinate.g4)
        self.assertEqual(move, self.model.Gamestate.invalidMove)
        self.assertIs(chip, self.model.board.get_content(Coordinate.h6))
        self.assertNotIn(Coordinate.g4, self.model.chips.keys())
        self.assertIs(chip, self.model.chips[Coordinate.h6])
        self.assertEqual(len(removed),0)

    def test_move_white_valid_no_jump(self):
        chip = self.model.board.get_content(Coordinate.a3)
        move, removed = self.model.move(Coordinate.a3,Coordinate.b4)
        self.assertIs(self.model.board.get_content(Coordinate.a3), None)
        self.assertEqual(move, self.model.Gamestate.inProgress)
        self.assertIs(self.model.board.get_content(Coordinate.b4), chip)
        self.assertIn(Coordinate.b4, self.model.chips.keys())
        self.assertIs(chip, self.model.chips[Coordinate.b4])
        self.assertEqual(self.model.turn, Chip.Color.black)
        self.assertEqual(len(removed),0)

    def test_move_black_valid_no_jump(self):
        self.model.move(Coordinate.a3,Coordinate.b4)
        chip = self.model.board.get_content(Coordinate.h6)
        move, removed = self.model.move(Coordinate.h6, Coordinate.g5)
        self.assertIs(self.model.board.get_content(Coordinate.h6), None)
        self.assertEqual(move, self.model.Gamestate.inProgress)
        self.assertIs(self.model.board.get_content(Coordinate.g5), chip)
        self.assertIn(Coordinate.g5, self.model.chips.keys())
        self.assertIs(chip, self.model.chips[Coordinate.g5])
        self.assertIs(self.model.turn, Chip.Color.white)
        self.assertEqual(len(removed),0)

    def test_move_white_valid_jump(self):
        self.model.move(Coordinate.g3, Coordinate.f4)
        self.model.move(Coordinate.h6, Coordinate.g5)
        eater = self.model.chips[Coordinate.f4]
        move, removed = self.model.move(Coordinate.f4, Coordinate.h6)
        self.assertEqual(move, self.model.Gamestate.inProgress)
        self.assertIs(eater, self.model.board.get_content(Coordinate.h6))
        self.assertIn(Coordinate.h6, self.model.chips.keys())
        self.assertIs(eater, self.model.chips[Coordinate.h6])
        self.assertIsNone(self.model.board.get_content(Coordinate.g5))
        self.assertNotIn(Coordinate.g5, self.model.chips.keys())
        self.assertEqual(removed, [Coordinate.g5])

    def test_move_black_valid_jump(self):
        self.model.move(Coordinate.c3, Coordinate.b4)
        self.model.move(Coordinate.b6, Coordinate.a5)
        self.model.move(Coordinate.e3, Coordinate.d4)
        eater = self.model.chips[Coordinate.a5]
        move, removed = self.model.move(Coordinate.a5, Coordinate.c3)
        self.assertEqual(move, self.model.Gamestate.inProgress)
        self.assertIs(eater, self.model.board.get_content(Coordinate.c3))
        self.assertIn(Coordinate.c3, self.model.chips.keys())
        self.assertIs(eater, self.model.chips[Coordinate.c3])
        self.assertIsNone(self.model.board.get_content(Coordinate.b4))
        self.assertNotIn(Coordinate.b4, self.model.chips.keys())
        self.assertEqual(removed, [Coordinate.b4])

    def get_white_queen(self):
        self.model.move(Coordinate.c3, Coordinate.d4)
        self.model.move(Coordinate.d6, Coordinate.c5)
        self.model.move(Coordinate.b2, Coordinate.c3)
        self.model.move(Coordinate.c7, Coordinate.d6)
        self.model.move(Coordinate.c3, Coordinate.b4)
        self.model.move(Coordinate.d8, Coordinate.c7)
        self.model.move(Coordinate.d2, Coordinate.c3)
        self.model.move(Coordinate.f6, Coordinate.e5)
        self.model.move(Coordinate.d4, Coordinate.f6)
        self.model.move(Coordinate.f6, Coordinate.d8)

    def get_black_queen(self):
        self.model.move(Coordinate.e3, Coordinate.f4)
        self.model.move(Coordinate.d6, Coordinate.c5)
        self.model.move(Coordinate.g3, Coordinate.h4)
        self.model.move(Coordinate.e7, Coordinate.d6)
        self.model.move(Coordinate.h2, Coordinate.g3)
        self.model.move(Coordinate.d8, Coordinate.e7)
        self.model.move(Coordinate.g1, Coordinate.h2)
        self.model.move(Coordinate.b6, Coordinate.a5)
        self.model.move(Coordinate.c3, Coordinate.d4)
        self.model.move(Coordinate.c5, Coordinate.e3)
        self.model.move(Coordinate.e3, Coordinate.g1)

    def test_white_promotion(self):
        self.get_white_queen()
        chip = self.model.chips[Coordinate.d8]
        self.assertEqual(chip.type, Chip.Type.queen)

    def test_black_promotion(self):
        self.get_black_queen()
        chip = self.model.chips[Coordinate.g1]
        self.assertEqual(chip.type, Chip.Type.queen)

    def test_chip_available_moves_white_queen_no_jump(self):
        self.get_white_queen()
        self.model.move(Coordinate.d6, Coordinate.e5)
        chip = self.model.chips[Coordinate.d8]
        moves, can_jump = self.model.chip_available_moves(Coordinate.d8)
        answer = set([(Coordinate.d8, Coordinate.e7),
                      (Coordinate.d8, Coordinate.f6),
                      (Coordinate.d8, Coordinate.g5),
                      (Coordinate.d8, Coordinate.h4)])
        self.assertEqual(moves, answer)

    def test_chip_available_moves_white_queen_jump(self):
        self.get_white_queen()
        self.model.move(Coordinate.f8, Coordinate.e7)
        chip = self.model.chips[Coordinate.d8]
        moves, can_jump = self.model.chip_available_moves(Coordinate.d8)
        answer = set([(Coordinate.d8, Coordinate.f6),
                      (Coordinate.d8, Coordinate.g5),
                      (Coordinate.d8, Coordinate.h4)])
        self.assertEqual(moves, answer)
        #------------------------------
        self.model.new_game()
        self.get_white_queen()
        self.model.move(Coordinate.g7, Coordinate.f6)
        moves, can_jump = self.model.chip_available_moves(Coordinate.d8)
        answer = set([(Coordinate.d8, Coordinate.g5),
                      (Coordinate.d8, Coordinate.h4)])
        self.assertEqual(moves, answer)
        #------------------------------
        self.model.new_game()
        self.get_white_queen()
        self.model.move(Coordinate.h6, Coordinate.g5)
        moves, can_jump = self.model.chip_available_moves(Coordinate.d8)
        answer = set([(Coordinate.d8, Coordinate.h4)])
        self.assertEqual(moves, answer)
        #------------------------------
        self.model.new_game()
        self.get_white_queen()
        self.model.move(Coordinate.b6, Coordinate.a5)
        moves, can_jump = self.model.chip_available_moves(Coordinate.d8)
        answer = set([(Coordinate.d8, Coordinate.b6)])
        self.assertEqual(moves, answer)
        self.model.move(Coordinate.d8, Coordinate.b6)
        moves, can_jump = self.model.chip_available_moves(Coordinate.b6)
        answer = set([(Coordinate.b6, Coordinate.d4)])
        self.assertEqual(moves, answer)
        # Since the function used to find queen moves make no distinction
        # between white and black queens, there is no need to test
        # black chips' behavior separately.

    def test_square_has_ally_chip_raises_TypeError(self):
        self.assertRaises(TypeError, 
                          self.model.square_contains_teammate, 
                          "notCoordinate")

    def test_square_has_ally_chip_empty(self):
        self.assertFalse(self.model.square_contains_teammate(Coordinate.a4))

    def test_square_has_ally_chip_enemy(self):
        self.assertFalse(self.model.square_contains_teammate(Coordinate.a7))

    def test_square_has_ally_chip_ally(self):
        self.assertTrue(self.model.square_contains_teammate(Coordinate.a3))

    def test_gamestate_white_won(self):
        self.get_white_queen()
        self.model.move(Coordinate.h6, Coordinate.g5)
        self.model.move(Coordinate.d8, Coordinate.h4)
        self.model.move(Coordinate.g7, Coordinate.f6)
        self.model.move(Coordinate.h4, Coordinate.d8)
        self.model.move(Coordinate.h8, Coordinate.g7)
        self.model.move(Coordinate.g3, Coordinate.h4)
        self.model.move(Coordinate.b6, Coordinate.a5)
        self.model.move(Coordinate.d8, Coordinate.b6)
        self.model.move(Coordinate.b6, Coordinate.d4)
        self.model.move(Coordinate.d4, Coordinate.h8)
        self.model.move(Coordinate.f8, Coordinate.g7) 
        # ^ (1) new queen double jump test case
        self.model.move(Coordinate.h8, Coordinate.e5)
        self.model.move(Coordinate.e5, Coordinate.c7)
        self.model.move(Coordinate.b8, Coordinate.d6)
        self.model.move(Coordinate.b4, Coordinate.c5)
        self.model.move(Coordinate.d6, Coordinate.b4)
        self.model.move(Coordinate.b4, Coordinate.d2)
        self.model.move(Coordinate.e1, Coordinate.c3)
        self.model.move(Coordinate.a7, Coordinate.b6)
        self.model.move(Coordinate.e3, Coordinate.d4)
        self.model.move(Coordinate.a5, Coordinate.b4)
        self.model.move(Coordinate.c3, Coordinate.a5)
        move, removed = self.model.move(Coordinate.a5, Coordinate.c7)
        self.assertEqual(move, self.model.Gamestate.whiteWon)

    def test_gamestate_black_won(self):
        self.get_black_queen()
        self.model.move(Coordinate.e1, Coordinate.f2) 
        # ^ (1) other queen double jump test
        self.model.move(Coordinate.g1, Coordinate.e3)
        self.model.move(Coordinate.e3, Coordinate.g5)
        self.model.move(Coordinate.a3, Coordinate.b4)
        self.model.move(Coordinate.a5, Coordinate.c3)
        self.model.move(Coordinate.c3, Coordinate.e1)
        self.model.move(Coordinate.c1, Coordinate.d2)
        self.model.move(Coordinate.g5, Coordinate.c1)
        self.model.move(Coordinate.c1, Coordinate.a3)
        self.model.move(Coordinate.h4, Coordinate.g5)
        self.model.move(Coordinate.f6, Coordinate.h4)
        self.model.move(Coordinate.h4, Coordinate.f2)
        self.model.move(Coordinate.a1, Coordinate.b2)
        self.model.move(Coordinate.a3, Coordinate.c1)
        self.model.move(Coordinate.h2, Coordinate.g3)
        self.model.move(Coordinate.h6, Coordinate.g5)
        self.model.move(Coordinate.g3, Coordinate.f4)
        move, removed = self.model.move(Coordinate.g5, Coordinate.e3)
        self.assertEqual(move, self.model.Gamestate.blackWon)

# (1) Originally, tests would be added to make sure that a queen takes
#     a double jump if available. However, no source could be found
#     to confim that a queen must take a double jump over a single
#     jump. Therefore, this model allows a queen to choose a single
#     jump over a double jump if the circumstance presents itself.

if __name__ == '__main__':
    unittest.main()