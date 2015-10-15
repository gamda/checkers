Checkers
========

Checkers is a package containing the game of checkers. The file 'checkers.py'
contains a graphic implementation using Pygame. The file 'model.py' is the 
logic implementation that can be used anywhere to play the game.

Depends on the package 'gameboard' found at https://github.com/gamda/gameboard

* All references to **Coordinate** are to **Gameboard.Coordinate**

Copyright (c) 2015 Gamda Software, LLC

See the file LICENSE.txt for copying permission.

Chip
----

Color - Enum:
    * Color.white
    * Color.black

Type - Enum:
    * Type.soldier
    * Type.queen

*color* - read-only property

*type* - read-only property

Model
-----

*board* - property:
    Instance of **Gameboard** managed by Model. 

*chips* - property:
    *Dictionary* where *keys* are **Coordinate** values and *items* are
    **Chip** instances with *Color* and *Type* correctly set. When a move
    is made, this property is updated to reflect the current gamestate.

*turn* - property:
    **Chip.Color** value to reflect whose turn it is in the current gamestate.

* All three properties are provided to read the gamestate, but should not be
modified by the user.

chipAvailableMoves(square):
    Args:

    *square* (**Coordinate**): the square where the chip is/should be
    
    Returns:

    * *set*: tuple of **Coordinate** values of valid moves for the chip. They have
    the form (**Coordinate**.origin, **Coordinate**.destination)
    * *bool*: **True** if the chip can jump, **False** otherwise


availableMoves():
    Returns:

    *set*: tuple of **Coordinate** values of valid moves for the chip. They have
    the form (*origin*: **Coordinate**, *destination*: **Coordinate**)


move(origin, destination):
    Args:

    * *origin* (**Coordinate**): the square where the chip is currently
    * *destination* (**Direction**): the square where the chip will end

    Returns:

    * *Gamestate*: value from enum 
    * *list*: **Coordinate** values indicating the chip(s) removed

    Raises:

    *TypeError*: if *origin* or *destination* is not **Coordinate**


**Gamestate** - Enum:
    * Gamestate.invalidMove 
    * Gamestate.inProgress 
    * Gamestate.whiteWon 
    * Gamestate.blackWon 
    * Gamestate.tie - *currently unused*


squareHasAllyChip(square):
    Used by checkers.py to highlight squares

    Args:

    *square* (**Coordinate**): the square to check for an ally chip

    Returns:

    *bool*: **True** if the chip belongs to the team whose turn it is, **False** otherwise

    Raises:

    *TypeError*: if *square* is not **Coordinate**