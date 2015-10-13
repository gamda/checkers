Checkers
========

Checkers is a package containing the game of checkers. The file 'checkers.py'
contains a graphic implementation using Pygame. The file 'model.py' is the 
logic implementation that can be used anywhere to play the game.

Copyright (c) 2015 Daniel Garcia

See the file LICENSE.txt for copying permission.

Chip
----

Color - Enum:
    * Color.white
    * Color.black

Type - Enum:
    * Type.soldier
    * Type.queen

promote():

Model
-----

chipAvailableMoves(square):
    Args:

    *square* (**Coordinate**): the square where the chip is/should be
    
    Returns:

    *set*: tuple of **Coordinate** values of valid moves for the chip. They have
    the form (**Coordinate**.origin, **Coordinate**.destination)
    bool: **True** if the chip can jump, **False** otherwise



availableMoves():
    Returns:

    *set*: tuple of **Coordinate** values of valid moves for the chip. They have
    the form (*origin*: **Coordinate**, *destination*: **Coordinate**)



move(origin, destination):
    Args:

    *origin* (**Coordinate**): the square where the chip is currently
    *destination* (**Direction**): the square where the chip will end

    Returns:

    *Gamestate*: value from enum 
    *list*: **Coordinate** values indicating the chip(s) removed

    Raises:

    *TypeError*: if *origin* or *destination* is not **Coordinate**

**Gamestate** - Enum:
    Gamestate.invalidMove 
    Gamestate.inProgress 
    Gamestate.whiteWon 
    Gamestate.blackWon 
    Gamestate.tie 



squareHasAllyChip(square):
    Args:

    *square* (**Coordinate**): the square to check for an ally chip

    Returns:

    *bool*: **True** if the chip belongs to the team whose turn it is, **False** otherwise

    Raises:

    *TypeError*: if *square* is not **Coordinate**
