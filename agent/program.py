# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent

from referee.game import PlayerColor, Action, PlaceAction, Coord

# Our imports
import numpy as np


class Shape:
    """
    This is the superclass that represents the basic tetris shape objects
    """

    def __init__(self, tokens, position=Coord(0, 0), rotation_index=0):
        self.tokens = tokens
        self.position = position
        self.rotation_index = rotation_index


class IShape(Shape):
    """
    I shape and its rotations, with a relative position at (0,0)
    """

    def __init__(self, position=Coord(0, 0)):
        tokens = [
            [Coord(0, 0), Coord(0, 1), Coord(0, 2), Coord(0, 3)],  # vertical state
            [Coord(0, 0), Coord(1, 0), Coord(2, 0), Coord(3, 0)]  # horizontal state
        ]
        super().__init__(tokens, position)


class OShape(Shape):
    """
    O shape and its rotations, with a relative position at (0,0)
    """

    def __init__(self, position=Coord(0, 0)):
        tokens = [
            [Coord(0, 0), Coord(0, 1), Coord(1, 0), Coord(1, 1)]
        ]
        super().__init__(tokens, position)


class TShape(Shape):
    """
    T shape and its rotations, with a relative position at (0,0)
    """

    def __init__(self, position=Coord(0, 0)):
        tokens = [
            [Coord(0, 0), Coord(0, 1), Coord(0, 2), Coord(1, 1)],
            [Coord(0, 0), Coord(0, 1), Coord(1, 1), Coord(10, 1)],
            [Coord(0, 0), Coord(1, 0), Coord(1, 1), Coord(2, 0)],
            [Coord(0, 0), Coord(0, 1), Coord(10, 1), Coord(0, 2)]
        ]
        super().__init__(tokens, position)


class JShape(Shape):
    """
    J shape and its rotations, with a relative position at (0,0)
    """

    def __init__(self, position=Coord(0, 0)):
        tokens = [
            [Coord(0, 0), Coord(0, 1), Coord(10, 1), Coord(9, 1)],
            [Coord(0, 0), Coord(1, 0), Coord(2, 0), Coord(0, 1)],
            [Coord(0, 0), Coord(1, 0), Coord(1, 1), Coord(1, 2)],
            [Coord(0, 0), Coord(0, 1), Coord(0, 2), Coord(1, 2)]
        ]
        super().__init__(tokens, position)


class LShape(Shape):
    """
    L shape and its rotations, with a relative position at (0,0)
    """

    def __init__(self, position=Coord(0, 0)):
        tokens = [
            [Coord(0, 0), Coord(1, 0), Coord(2, 0), Coord(2, 1)],
            [Coord(0, 0), Coord(0, 1), Coord(0, 2), Coord(1, 0)],
            [Coord(0, 0), Coord(0, 1), Coord(1, 1), Coord(2, 1)],
            [Coord(0, 0), Coord(0, 1), Coord(0, 2), Coord(10, 2)]
        ]
        super().__init__(tokens, position)


class ZShape(Shape):
    """
    Z shape and its rotations, with a relative position at (0,0)
    """

    def __init__(self, position=Coord(0, 0)):
        tokens = [
            [Coord(0, 0), Coord(0, 1), Coord(1, 1), Coord(1, 2)],
            [Coord(0, 0), Coord(0, 1), Coord(1, 0), Coord(10, 1)]
        ]
        super().__init__(tokens, position)


class SShape(Shape):
    """
    S shape and its rotations, with a relative position at (0,0)
    """

    def __init__(self, position=Coord(0, 0)):
        tokens = [
            [Coord(0, 0), Coord(1, 0), Coord(1, 1), Coord(2, 1)],
            [Coord(0, 0), Coord(0, 1), Coord(10, 1), Coord(10, 2)]
        ]
        super().__init__(tokens, position)


def generate_place_action(shape: Shape):
    """
    Returns: Shape's coordinates in PlaceAction form

    """
    return PlaceAction(shape.tokens[shape.rotation_index][0], shape.tokens[shape.rotation_index][1],
                       shape.tokens[shape.rotation_index][2], shape.tokens[shape.rotation_index][3])



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

        best_move = self.best_action()
        print(best_move.tokens[best_move.rotation_index])
        return generate_place_action(best_move)

    def does_shape_fit_on_board(self, shape: Shape) -> bool:
        for token in shape.tokens[shape.rotation_index]:
            if token in self.game_state:
                return False
        return True

########################
    def best_action(self):
        mobilities = self.find_mobilities()
        biggest_value = -float('inf')
        for val in mobilities.keys():
            if self.does_shape_fit_on_board(mobilities[val]):
                if val > biggest_value:
                    biggest_value = val
        if biggest_value == -float('inf'):
            mobilities = self.find_mobilities(1)
            for val in mobilities.keys():
                if self.does_shape_fit_on_board(mobilities[val]):
                    if val > biggest_value:
                        biggest_value = val
        best_move = mobilities[biggest_value]

        return best_move

    def find_mobilities(self, rotation_request=0):
        mobilities: dict[float, Shape] = {}
        for move in self.possible_moves(self.game_state, self._color, rotation_request):
            new_board = self.update_board(move)
            our_mobility = len(self.possible_moves(new_board, self._color, rotation_request))
            opponent_mobility = len(self.possible_moves(new_board, self._color.opponent, rotation_request))
            heuristic_mobility = 1 * our_mobility - 1.5 * opponent_mobility
            mobilities[heuristic_mobility] = move

        return mobilities

    def update_board(self, piece: Shape):
        new_board = self.copy_board()
        for token in piece.tokens[piece.rotation_index]:
            new_board[token] = self._color
        return new_board

    def copy_board(self) -> dict[Coord, PlayerColor]:
        new_board = {}
        for key, value in self.game_state.items():
            new_board[key] = value
        return new_board

    @staticmethod
    def find_adjacent_tokens(board: dict[Coord, PlayerColor], color: PlayerColor):
        available_adjacent_tokens = []

        def unanimous_checker():
            unanimous_list = []
            for coord, token_color in board.items():
                if token_color == color:
                    return []
                unanimous_list.append(coord)
            return unanimous_list

        if not board:
            for i in range(11):
                for j in range(11):
                    available_adjacent_tokens.append(Coord(i, j))
            return available_adjacent_tokens

        u_list = unanimous_checker()
        if u_list:
            for i in range(11):
                for j in range(11):
                    available_adjacent_tokens.append(Coord(i, j))
            for c in u_list:
                available_adjacent_tokens.remove(c)
            return available_adjacent_tokens
        else:
            for c, t_color in board.items():
                if t_color == color:
                    adjacency_tokens = [c.up(), c.left(), c.down(), c.right()]
                    for adjacency_token in adjacency_tokens:
                        if board.get(adjacency_token, None) is None:
                            available_adjacent_tokens.append(adjacency_token)
            return available_adjacent_tokens

    def possible_moves(self, board, color, rotation_request):
        """
        Returns: The list of all future states based on the current_state of the game

        """
        future_moves = []
        match rotation_request:
            case 0:
                for adjacent_token in self.find_adjacent_tokens(board, color):
                    list_of_shapes = [IShape(), OShape(), TShape(), JShape(), LShape(), ZShape(), SShape()]
                    for shape in list_of_shapes:
                        num_of_rotations = len(shape.tokens)
                        for i in range(num_of_rotations):
                            shape.rotation_index = i
                            if self.shape_checker(board, adjacent_token, shape) is True:
                                future_moves.append(shape)
            case 1:
                for adjacent_token in self.find_adjacent_tokens(board, color):
                    list_of_shapes = [IShape(), OShape(), TShape(), JShape(), LShape(), ZShape(), SShape()]
                    for shape in list_of_shapes:
                        num_of_rotations = len(shape.tokens)
                        for i in range(num_of_rotations):
                            shape.rotation_index = i
                            shapes = self.shape_checker_rotation(board, adjacent_token, shape)
                            if shapes:
                                for rotation in shapes:
                                    future_moves.append(rotation)
        return future_moves

    @staticmethod
    def shape_checker(board: dict[Coord, PlayerColor], adjacent_token: Coord, shape: Shape):
        new_piece_coords = []
        for coordinate in shape.tokens[shape.rotation_index]:
            coordinate = coordinate + adjacent_token
            if board.get(coordinate, None) is not None:
                return False
            new_piece_coords.append(coordinate)
        shape.tokens[shape.rotation_index] = new_piece_coords
        shape.position = adjacent_token
        return True
    
    @staticmethod
    def shape_checker_rotation(board: dict[Coord, PlayerColor], adjacent_token: Coord, shape: Shape):

        def rotate_piece(coords: list[Coord], pivot: Coord, clockwise=True):
            pivot_x, pivot_y = pivot.r, pivot.c
            new_coords = []

            for coord in coords:
                if clockwise:
                    new_x = pivot_x + (coord.c - pivot_y)
                    new_y = pivot_y - (coord.r - pivot_x)
                else:
                    new_x = pivot_x - (coord.c - pivot_y)
                    new_y = pivot_y + (coord.r - pivot_x)

                if new_x < 0:
                    new_x = new_x + 11
                if new_y < 0:
                    new_y = new_y + 11
                if new_x > 10:
                    new_x = new_x - 11
                if new_y > 10:
                    new_y = new_y - 11
                new_coords.append(Coord(new_x, new_y))

            return new_coords

        rotation1 = shape.tokens[shape.rotation_index]
        rotation2 = rotate_piece(rotation1, Coord(0,0))
        rotation3 = rotate_piece(rotation2, Coord(0,0))
        rotation4 = rotate_piece(rotation3, Coord(0,0))

        list_of_rotations = [rotation1, rotation2, rotation3, rotation4]

        list_of_valid_shapes = []
        for rotation in list_of_rotations:
            new_piece_coords = []
            for coordinate in rotation:
                coordinate = coordinate + adjacent_token
                if board.get(coordinate, None) is not None:
                    break
                new_piece_coords.append(coordinate)
            shape.tokens[shape.rotation_index] = new_piece_coords
            shape.position = adjacent_token
            list_of_valid_shapes.append(shape)

        return list_of_valid_shapes

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

        rows_to_delete = []
        columns_to_delete = []

        col_full = True
        row_full = True

        for coord in place_action.coords:
            r = coord.r
            c = coord.c
            for rows in range(11):
                if self.game_state.get(Coord(rows, c), None) is None:
                    col_full = False
                    break

            for cols in range(11):
                if self.game_state.get(Coord(r, cols), None) is None:
                    row_full = False
                    break

            if col_full is True:
                columns_to_delete.append(c)

            if row_full is True:
                rows_to_delete.append(r)

            col_full = True
            row_full = True

        if len(columns_to_delete) > 0:
            for c in columns_to_delete:
                for row in range(11):
                    self.game_state.pop(Coord(row, c), None)
                    # self.mcts_node.board.pop(Coord(row, c))

        if len(rows_to_delete) > 0:
            for r in rows_to_delete:
                for col in range(11):
                    self.game_state.pop(Coord(r, col), None)
                    # self.mcts_node.board.pop(Coord(r, col))

        # Here we are just printing out the PlaceAction coordinates for
        # demonstration purposes. You should replace this with your own logic
        # to update your agent's internal game state representation.
        print(f"Testing: {color} played PLACE action: {c1}, {c2}, {c3}, {c4}")