from enum import Enum
from gameboard.gameboard import Gameboard
from gameboard.coordinate import Coordinate

class Chip:
    class Color(Enum):
        white = 0
        black = 1
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







