# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent

from referee.game import PlayerColor, Action, PlaceAction, Coord

import numpy as np

class Shape:
    """
    This is the superclass that represents the basic tetris shape objects
    """

    def __init__(self, shapes, position=Coord(0, 0), rotation_index=0):
        self.shapes = shapes
        self.position = position
        self.rotation_index = rotation_index

    def get_place_action(self) -> PlaceAction:
        """
        Generates a PlaceAction based on the shape's current position and rotation.
        
        Returns:
            PlaceAction: A PlaceAction object representing the shape's placement
        """
        # Get the coordinates for the current rotation
        relative_coords = self.shapes[self.rotation_index]
        
        # Convert relative coordinates to absolute coordinates
        absolute_coords = [
            Coord(self.position.r + coord.r, self.position.c + coord.c)
            for coord in relative_coords
        ]
        
        # Create and return the PlaceAction
        return PlaceAction(*absolute_coords)


class IShape(Shape):
    """
    I shape and its rotations, with a relative position at (0,0)
    """

    def __init__(self, position=Coord(0, 0), rotation_index=0):
        shapes = [
            [Coord(0, 0), Coord(0, 1), Coord(0, 2), Coord(0, 3)],  # horizontal state
            [Coord(0, 0), Coord(1, 0), Coord(2, 0), Coord(3, 0)]   # vertical state
        ]
        super().__init__(shapes, position, rotation_index)


class OShape(Shape):
    """
    O shape and its rotations, with a relative position at (0,0)
    """

    def __init__(self, position=Coord(0, 0), rotation_index=0):
        shapes = [
            [Coord(0, 0), Coord(0, 1), Coord(1, 0), Coord(1, 1)]
        ]
        super().__init__(shapes, position, rotation_index)


class TShape(Shape):
    """
    T shape and its rotations, with a relative position at (0,0)
    """

    def __init__(self, position=Coord(0, 0), rotation_index=0):
        shapes = [
            [Coord(0, 0), Coord(0, 1), Coord(0, 2), Coord(1, 1)],   # Pointing Down
            [Coord(0, 0), Coord(1, 0), Coord(2, 0), Coord(1, 10)],  # Pointing Left
            [Coord(0, 0), Coord(0, 10), Coord(0, 9), Coord(10, 10)], # Pointing Up
            [Coord(0, 0), Coord(10, 0), Coord(9, 0), Coord(10, 1)]   # Pointing Right
        ]
        super().__init__(shapes, position, rotation_index)


class JShape(Shape):
    """
    J shape and its rotations, with a relative position at (0,0)
    """

    def __init__(self, position=Coord(0, 0), rotation_index=0):
        shapes = [
            [Coord(0, 0), Coord(0, 1), Coord(10, 1), Coord(9, 1)], # Pointing Up
            [Coord(0, 0), Coord(1, 0), Coord(1, 1), Coord(1, 2)],  # Pointing Right
            [Coord(0, 0), Coord(0, 10), Coord(1, 10), Coord(2, 10)],  # Pointing Down
            [Coord(0, 0), Coord(10, 0), Coord(10, 10), Coord(10, 9)]   # Pointing Left
        ]
        super().__init__(shapes, position, rotation_index)


class LShape(Shape):
    """
    L shape and its rotations, with a relative position at (0,0)
    """

    def __init__(self, position=Coord(0, 0), rotation_index=0):
        shapes = [
            [Coord(0, 0), Coord(0, 10), Coord(10, 10), Coord(9, 10)],   # Pointing Up
            [Coord(0, 0), Coord(10, 0), Coord(10, 1), Coord(10, 2)],    # Pointing Right
            [Coord(0, 0), Coord(0, 1), Coord(1, 1), Coord(2, 1)],       # Pointing Down
            [Coord(0, 0), Coord(1, 0), Coord(1, 10), Coord(1, 9)]       # Pointing Left
        ]
        super().__init__(shapes, position, rotation_index)


class ZShape(Shape):
    """
    Z shape and its rotations, with a relative position at (0,0)
    """

    def __init__(self, position=Coord(0, 0), rotation_index=0):
        shapes = [
            [Coord(0, 0), Coord(1, 0), Coord(1, 1), Coord(0, 10)],
            [Coord(0, 0), Coord(0, 10), Coord(1, 10), Coord(10, 0)]
        ]
        super().__init__(shapes, position, rotation_index)


class SShape(Shape):
    """
    S shape and its rotations, with a relative position at (0,0)
    """

    def __init__(self, position=Coord(0, 0), rotation_index=0):
        shapes = [
            [Coord(0, 0), Coord(1, 0), Coord(1, 1), Coord(2, 1)],
            [Coord(0, 0), Coord(0, 1), Coord(10, 1), Coord(10, 2)]
        ]
        super().__init__(shapes, position, rotation_index)

class GameState:
    """
    This class is the core environment abstraction that holds the board state
    and functions

    Args:
            board: A dictionary mapping Coord objects to PlayerColor, representing the occupied cells.
            current_player: The player whose turn it is (PlayerColor.RED or PlayerColor.BLUE).
    """
    
    def __init__(self, board: dict[Coord, PlayerColor] = None, current_player : PlayerColor = None, turn_count: int = None):
        self.board = board
        self.current_player = current_player
        self.turn_count = turn_count
    
    def is_line_full(self, action : PlaceAction) -> tuple[list[int], list[int]]:
        """
        This method returns a tuple containing two lists, each 
        holding the row and columns that are full

        Args:
                action: The last move that was made by an agent before updating the board
        """
        rows_to_check = set()
        cols_to_check = set()
        for coord in action.coords:
            rows_to_check.add(coord.r)
            cols_to_check.add(coord.c)

        full_rows = []
        full_cols = []
        
        for target_row in rows_to_check:
            is_row_full = True
            for c in range(0,11):
                if not self.board.get(Coord(target_row, c)):
                    is_row_full = False
                    break
            if is_row_full:
                full_rows.append(target_row)
                
        for target_col in cols_to_check:
            is_col_full = True
            for r in range(0,11):
                if not self.board.get(Coord(r, target_col)):
                    is_col_full = False
                    break
            if is_col_full:
                full_cols.append(target_col)
                
        return full_rows, full_cols
    
    def clear_lines(self, rows, cols):
        """
        Method responsible for clearing a line that is full

        Args:
                rows: List of rows that need to be cleared
                cols: List of columns that need to be cleared
        """

        if rows:
            for row in rows:
                for c in range(0,11):
                    if Coord(row, c) in self.board:
                        self.board.pop(Coord(row, c), None)
        
        if cols:
            for col in cols:
                for r in range(0,11):
                    if Coord(r, col) in self.board:
                        self.board.pop(Coord(r, col), None)
    

class Agent:
    """
    This class is the "entry point" for your agent, providing an interface to
    respond to various Tetress game events.
    """

    def __init__(self, color: PlayerColor, **referee: dict):
        """
        This constructor method runs when the referee instantiates the agent.
        Any setup and/or precomputation should be done here.
        """

        self.game_state: dict[Coord, PlayerColor] = {}  # board represented by a dictionary
        self.turn_count = 0

        self._color = color
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as RED")
            case PlayerColor.BLUE:
                print("Testing: I am playing as BLUE")

    def action(self, **referee: dict) -> Action:
        """
        This method is called by the referee each time it is the agent's turn
        to take an action. It must always return an action object.
        """

    def update(self, color: PlayerColor, action: Action, **referee: dict):
        """
        This method is called by the referee after an agent has taken their
        turn. You should use it to update the agent's internal game state.
        """

        # There is only one action type, PlaceAction
        place_action: PlaceAction = action
        c1, c2, c3, c4 = place_action.coords

        self.game_state[c1] = color
        self.game_state[c2] = color
        self.game_state[c3] = color
        self.game_state[c4] = color

        self.turn_count += 1

        print(f"{color} played PLACE action: {c1}, {c2}, {c3}, {c4}")

