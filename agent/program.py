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
            self.position + coord
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
            [Coord(0, 0), Coord(1, 0), Coord(1, 10), Coord(0, 1)],
            [Coord(0, 0), Coord(1, 0), Coord(0, 10), Coord(10, 10)]
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
    
    def __init__(self, board: dict[Coord, PlayerColor] = None, current_player : PlayerColor = None, turn_count: int = 0):
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
    
    def _find_valid_coords(self, color: PlayerColor) -> set:
        """
        Finds all viable coordinates, after the first move, where a player can potentially lay a piece

        Args: 
            color: Player's color

        Returns:
            Set of valid adjacent coords for a token to be placed
        """

        # Get all board pieces of the agents color
        same_colour_pieces = {coord for coord, piece_color in self.board.items() if piece_color == color}

        valid_surrounding_spaces = set()
        for coord in same_colour_pieces:
            valid_surrounding_spaces = self._find_adjacent_coords(coord, valid_surrounding_spaces)
        
        return valid_surrounding_spaces
    
    def _find_adjacent_coords(self, coord: Coord, surrounding_spaces : set) -> set:
        """
        Helper method to find valid adjacent coords next to a coord of its own color

        Args:
            coord: coordinate to check surroundings of
            surrounding_spaces: set of coordinates to append valid tokens to

        Returns:
            Updated set of valid surrounding spaces
        """

        directions = [coord.up(), coord.left(), coord.right(), coord.down()]
        for direction in directions:
            if direction not in self.board:
                surrounding_spaces.add(direction)
        
        return surrounding_spaces
    
    def _first_turn_valid_coords(self) -> set:
        valid_coords = set()
        for r in range(11):
            for c in  range(11):
                valid_coords.add(Coord(r,c))
        
        return valid_coords

    def find_all_valid_moves(self, color: PlayerColor) -> list[tuple[Shape, Coord]]:
        """
        Finds all valid moves for every shape and rotation at each valid coordinate.
        A move is considered valid

        Args:
            color: The color of the player making the move

        Returns:
            A list of tuples containing (Shape, Coord) pairs representing valid moves
        """
        valid_moves = []
        if self.turn_count == 0:
            valid_coords = self._first_turn_valid_coords()
        else:
            valid_coords = self._find_valid_coords(color)
        
        # Define all possible shapes
        shapes = [
            IShape(position=Coord(0, 0)),
            OShape(position=Coord(0, 0)),
            TShape(position=Coord(0, 0)),
            JShape(position=Coord(0, 0)),
            LShape(position=Coord(0, 0)),
            ZShape(position=Coord(0, 0)),
            SShape(position=Coord(0, 0))
        ]
        
        # For each valid coordinate
        for valid_coord in valid_coords:
            # For each shape type
            for shape in shapes:
                # For each possible rotation
                for rotation in range(len(shape.shapes)):
                    # Get the relative coordinates for this rotation
                    relative_coords = shape.shapes[rotation]
                    
                    # For each coordinate in the shape
                    for rel_coord in relative_coords:
                        # Calculate the position that would place this coordinate at the valid position
                        # This is: valid_coord - rel_coord
                        base_position = valid_coord - rel_coord
                        
                        # Create a new shape at the calculated base position
                        test_shape = type(shape)(position=base_position, rotation_index=rotation)
                        
                        # Get the coordinates this shape would occupy
                        place_action = test_shape.get_place_action()
                        shape_coords = set(place_action.coords)
                        
                        # Check if any coordinates overlap with existing pieces
                        if not any(coord in self.board for coord in shape_coords):
                            valid_moves.append((test_shape, valid_coord))
        
        return valid_moves
    
    def is_game_over(self):
        valid_moves = self.find_all_valid_moves(self.current_player)
        if not valid_moves:
            return True
        return False


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

