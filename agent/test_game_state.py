import unittest
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.program import GameState, PlaceAction, Coord, IShape, OShape, TShape, JShape, LShape, ZShape, SShape
from referee.game import PlayerColor

class TestGameState(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.game_state = GameState(board={}, current_player=PlayerColor.RED)

    def test_empty_board_no_full_lines(self):
        """Test that no lines are detected as full on an empty board."""
        action = PlaceAction(Coord(0, 0), Coord(0, 1), Coord(0, 2), Coord(0, 3))
        full_rows, full_cols = self.game_state.is_line_full(action)
        self.assertEqual(full_rows, [])
        self.assertEqual(full_cols, [])

    def test_full_row_detection(self):
        """Test that a full row is properly detected."""
        # Fill row 5 completely
        for c in range(11):
            self.game_state.board[Coord(5, c)] = PlayerColor.RED
        
        # Place a piece that includes row 5
        action = PlaceAction(Coord(5, 0), Coord(5, 1), Coord(5, 2), Coord(5, 3))
        full_rows, full_cols = self.game_state.is_line_full(action)
        self.assertIn(5, full_rows)
        self.assertEqual(full_cols, [])

    def test_full_column_detection(self):
        """Test that a full column is properly detected."""
        # Fill column 3 completely
        for r in range(11):
            self.game_state.board[Coord(r, 3)] = PlayerColor.RED
        
        # Place a piece that includes column 3
        action = PlaceAction(Coord(0, 3), Coord(1, 3), Coord(2, 3), Coord(3, 3))
        full_rows, full_cols = self.game_state.is_line_full(action)
        self.assertIn(3, full_cols)
        self.assertEqual(full_rows, [])

    def test_partial_line_not_detected(self):
        """Test that partially filled lines are not detected as full."""
        # Fill only part of row 4
        for c in range(5):  # Only fill first 5 columns
            self.game_state.board[Coord(4, c)] = PlayerColor.RED
        
        action = PlaceAction(Coord(4, 0), Coord(4, 1), Coord(4, 2), Coord(4, 3))
        full_rows, full_cols = self.game_state.is_line_full(action)
        self.assertEqual(full_rows, [])
        self.assertEqual(full_cols, [])

    def test_multiple_full_lines(self):
        """Test detection of multiple full lines."""
        # Fill row 2 and column 7 completely
        for c in range(11):
            self.game_state.board[Coord(2, c)] = PlayerColor.RED
        for r in range(11):
            self.game_state.board[Coord(r, 7)] = PlayerColor.RED
        
        action = PlaceAction(Coord(2, 7), Coord(2, 8), Coord(3, 7), Coord(3, 8))
        full_rows, full_cols = self.game_state.is_line_full(action)
        self.assertIn(2, full_rows)
        self.assertIn(7, full_cols)

    def test_clear_single_row(self):
        """Test clearing a single full row."""
        # Fill row 3 completely
        for c in range(11):
            self.game_state.board[Coord(3, c)] = PlayerColor.RED
        
        # Add some other pieces that shouldn't be cleared
        self.game_state.board[Coord(4, 0)] = PlayerColor.RED
        self.game_state.board[Coord(4, 1)] = PlayerColor.RED
        
        # Clear row 3
        self.game_state.clear_lines([3], [])
        
        # Verify row 3 is empty
        for c in range(11):
            self.assertNotIn(Coord(3, c), self.game_state.board)
        
        # Verify other pieces remain
        self.assertIn(Coord(4, 0), self.game_state.board)
        self.assertIn(Coord(4, 1), self.game_state.board)

    def test_clear_single_column(self):
        """Test clearing a single full column."""
        # Fill column 5 completely
        for r in range(11):
            self.game_state.board[Coord(r, 5)] = PlayerColor.RED
        
        # Add some other pieces that shouldn't be cleared
        self.game_state.board[Coord(0, 6)] = PlayerColor.RED
        self.game_state.board[Coord(1, 6)] = PlayerColor.RED
        
        # Clear column 5
        self.game_state.clear_lines([], [5])
        
        # Verify column 5 is empty
        for r in range(11):
            self.assertNotIn(Coord(r, 5), self.game_state.board)
        
        # Verify other pieces remain
        self.assertIn(Coord(0, 6), self.game_state.board)
        self.assertIn(Coord(1, 6), self.game_state.board)

    def test_clear_multiple_lines(self):
        """Test clearing multiple rows and columns simultaneously."""
        # Fill row 2 and column 3 completely
        for c in range(11):
            self.game_state.board[Coord(2, c)] = PlayerColor.RED
        for r in range(11):
            self.game_state.board[Coord(r, 3)] = PlayerColor.RED
        
        # Add some pieces that shouldn't be cleared
        self.game_state.board[Coord(4, 4)] = PlayerColor.RED
        self.game_state.board[Coord(5, 5)] = PlayerColor.RED
        
        # Clear row 2 and column 3
        self.game_state.clear_lines([2], [3])
        
        # Verify row 2 is empty
        for c in range(11):
            self.assertNotIn(Coord(2, c), self.game_state.board)
        
        # Verify column 3 is empty
        for r in range(11):
            self.assertNotIn(Coord(r, 3), self.game_state.board)
        
        # Verify other pieces remain
        self.assertIn(Coord(4, 4), self.game_state.board)
        self.assertIn(Coord(5, 5), self.game_state.board)

    def test_clear_empty_lines(self):
        """Test that clearing empty lines doesn't affect the board."""
        # Add some pieces
        self.game_state.board[Coord(0, 0)] = PlayerColor.RED
        self.game_state.board[Coord(1, 1)] = PlayerColor.RED
        
        # Try to clear empty lines
        self.game_state.clear_lines([5], [5])
        
        # Verify original pieces remain
        self.assertIn(Coord(0, 0), self.game_state.board)
        self.assertIn(Coord(1, 1), self.game_state.board)

class TestShapePlacement(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        pass

    def test_ishape_placement(self):
        """Test I-shape placement in different positions and rotations."""
        # Test horizontal I-shape
        shape = IShape(position=Coord(5, 3), rotation_index=0)
        action = shape.get_place_action()
        expected_coords = {
            Coord(5, 3), Coord(5, 4), Coord(5, 5), Coord(5, 6)
        }
        self.assertEqual(set(action.coords), expected_coords)

        # Test vertical I-shape
        shape = IShape(position=Coord(2, 4), rotation_index=1)
        action = shape.get_place_action()
        expected_coords = {
            Coord(2, 4), Coord(3, 4), Coord(4, 4), Coord(5, 4)
        }
        self.assertEqual(set(action.coords), expected_coords)

    def test_oshape_placement(self):
        """Test O-shape placement (rotation doesn't matter for O-shape)."""
        shape = OShape(position=Coord(3, 3))
        action = shape.get_place_action()
        expected_coords = {
            Coord(3, 3), Coord(3, 4), Coord(4, 3), Coord(4, 4)
        }
        self.assertEqual(set(action.coords), expected_coords)

    def test_tshape_placement(self):
        """Test T-shape placement in different rotations."""
        # Test T-shape pointing down
        shape = TShape(position=Coord(4, 4), rotation_index=0)
        action = shape.get_place_action()
        expected_coords = {
            Coord(4, 4), Coord(4, 5), Coord(4, 6), Coord(5, 5)
        }
        self.assertEqual(set(action.coords), expected_coords)

        # Test T-shape pointing left
        shape = TShape(position=Coord(4, 4), rotation_index=1)
        action = shape.get_place_action()
        expected_coords = {
            Coord(4, 4), Coord(5, 4), Coord(6, 4), Coord(5, 3)
        }
        self.assertEqual(set(action.coords), expected_coords)

        # Test T-shape pointing up
        shape = TShape(position=Coord(4, 4), rotation_index=2)
        action = shape.get_place_action()
        expected_coords = {
            Coord(4, 4), Coord(4, 3), Coord(4, 2), Coord(3, 3)
        }
        self.assertEqual(set(action.coords), expected_coords)

        # Test T-shape pointing right
        shape = TShape(position=Coord(4, 4), rotation_index=3)
        action = shape.get_place_action()
        expected_coords = {
            Coord(4, 4), Coord(3, 4), Coord(2, 4), Coord(3, 5)
        }
        self.assertEqual(set(action.coords), expected_coords)

    def test_jshape_placement(self):
        """Test J-shape placement in different rotations."""
        # Test J-shape pointing up
        shape = JShape(position=Coord(4, 4), rotation_index=0)
        action = shape.get_place_action()
        expected_coords = {
            Coord(4, 4), Coord(4, 5), Coord(3, 5), Coord(2, 5)
        }
        self.assertEqual(set(action.coords), expected_coords)

        # Test J-shape pointing right
        shape = JShape(position=Coord(4, 4), rotation_index=1)
        action = shape.get_place_action()
        expected_coords = {
            Coord(4, 4), Coord(5, 4), Coord(5, 5), Coord(5, 6)
        }
        self.assertEqual(set(action.coords), expected_coords)

        # Test J-shape pointing down
        shape = JShape(position=Coord(4, 4), rotation_index=2)
        action = shape.get_place_action()
        expected_coords = {
            Coord(4, 4), Coord(4, 3), Coord(5, 3), Coord(6, 3)
        }
        self.assertEqual(set(action.coords), expected_coords)

        # Test J-shape pointing left
        shape = JShape(position=Coord(4, 4), rotation_index=3)
        action = shape.get_place_action()
        expected_coords = {
            Coord(4, 4), Coord(3, 4), Coord(3, 3), Coord(3, 2)
        }
        self.assertEqual(set(action.coords), expected_coords)

    def test_lshape_placement(self):
        """Test L-shape placement in different rotations."""
        # Test L-shape pointing up
        shape = LShape(position=Coord(4, 4), rotation_index=0)
        action = shape.get_place_action()
        expected_coords = {
            Coord(4, 4), Coord(4, 3), Coord(3, 3), Coord(2, 3)
        }
        self.assertEqual(set(action.coords), expected_coords)

        # Test L-shape pointing right
        shape = LShape(position=Coord(4, 4), rotation_index=1)
        action = shape.get_place_action()
        expected_coords = {
            Coord(4, 4), Coord(3, 4), Coord(3, 5), Coord(3, 6)
        }
        self.assertEqual(set(action.coords), expected_coords)

        # Test L-shape pointing down
        shape = LShape(position=Coord(4, 4), rotation_index=2)
        action = shape.get_place_action()
        expected_coords = {
            Coord(4, 4), Coord(4, 5), Coord(5, 5), Coord(6, 5)
        }
        self.assertEqual(set(action.coords), expected_coords)

        # Test L-shape pointing left
        shape = LShape(position=Coord(4, 4), rotation_index=3)
        action = shape.get_place_action()
        expected_coords = {
            Coord(4, 4), Coord(5, 4), Coord(5, 3), Coord(5, 2)
        }
        self.assertEqual(set(action.coords), expected_coords)

    def test_zshape_placement(self):
        """Test Z-shape placement in different rotations."""
        # Test Z-shape horizontal
        shape = ZShape(position=Coord(4, 4), rotation_index=0)
        action = shape.get_place_action()
        expected_coords = {
            Coord(4, 4), Coord(5, 4), Coord(5, 5), Coord(4, 3)
        }
        self.assertEqual(set(action.coords), expected_coords)

        # Test Z-shape vertical
        shape = ZShape(position=Coord(4, 4), rotation_index=1)
        action = shape.get_place_action()
        expected_coords = {
            Coord(4, 4), Coord(4, 3), Coord(5, 3), Coord(3, 4)
        }
        self.assertEqual(set(action.coords), expected_coords)

    def test_sshape_placement(self):
        """Test S-shape placement in different rotations."""
        # Test S-shape horizontal
        shape = SShape(position=Coord(4, 4), rotation_index=0)
        action = shape.get_place_action()
        expected_coords = {
            Coord(4, 4), Coord(5, 4), Coord(5, 3), Coord(4, 5)
        }
        self.assertEqual(set(action.coords), expected_coords)

        # Test S-shape vertical
        shape = SShape(position=Coord(4, 4), rotation_index=1)
        action = shape.get_place_action()
        expected_coords = {
            Coord(4, 4), Coord(5, 4), Coord(4, 3), Coord(3, 3)
        }
        self.assertEqual(set(action.coords), expected_coords)

    def test_edge_positions(self):
        """Test shape placement at board edges."""
        # Test I-shape at top-left corner
        shape = IShape(position=Coord(9, 0), rotation_index=1)
        action = shape.get_place_action()
        expected_coords = {
            Coord(9, 0), Coord(10, 0), Coord(0, 0), Coord(1, 0)
        }
        self.assertEqual(set(action.coords), expected_coords)

        # Test O-shape at bottom-right corner
        shape = OShape(position=Coord(10, 10))
        action = shape.get_place_action()
        expected_coords = {
            Coord(10, 10), Coord(10, 0), Coord(0, 0), Coord(0, 10)
        }
        self.assertEqual(set(action.coords), expected_coords)

class TestValidCoords(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.game_state = GameState(board={}, current_player=PlayerColor.RED)

    def test_empty_board(self):
        """Test that an empty board returns an empty set of valid coordinates."""
        valid_coords = self.game_state.find_valid_coords(PlayerColor.RED)
        self.assertEqual(valid_coords, set())

    def test_single_piece_valid_coords(self):
        """Test finding valid coordinates around a single piece."""
        # Place a single piece
        self.game_state.board[Coord(5, 5)] = PlayerColor.RED
        
        valid_coords = self.game_state.find_valid_coords(PlayerColor.RED)
        expected_coords = {
            Coord(4, 5),  # up
            Coord(6, 5),  # down
            Coord(5, 4),  # left
            Coord(5, 6)   # right
        }
        self.assertEqual(valid_coords, expected_coords)

    def test_multiple_pieces_valid_coords(self):
        """Test finding valid coordinates around multiple connected pieces."""
        # Place multiple connected pieces
        self.game_state.board[Coord(5, 5)] = PlayerColor.RED
        self.game_state.board[Coord(5, 6)] = PlayerColor.RED
        self.game_state.board[Coord(5, 7)] = PlayerColor.RED
        
        valid_coords = self.game_state.find_valid_coords(PlayerColor.RED)
        expected_coords = {
            Coord(4, 5),  # up of first piece
            Coord(6, 5),  # down of first piece
            Coord(5, 4),  # left of first piece
            Coord(4, 6),  # up of middle piece
            Coord(6, 6),  # down of middle piece
            Coord(4, 7),  # up of last piece
            Coord(6, 7),  # down of last piece
            Coord(5, 8)   # right of last piece
        }
        self.assertEqual(valid_coords, expected_coords)

    def test_edge_pieces_valid_coords(self):
        """Test finding valid coordinates for pieces at board edges."""
        # Place pieces at edges
        self.game_state.board[Coord(0, 0)] = PlayerColor.RED  # top-left
        self.game_state.board[Coord(10, 10)] = PlayerColor.RED  # bottom-right
        
        valid_coords = self.game_state.find_valid_coords(PlayerColor.RED)
        expected_coords = {
            Coord(1, 0),   # down of top-left
            Coord(0, 1),   # right of top-left
            Coord(0, 10),  # left of top-left and down of bottom-right
            Coord(10, 0),  # up of top-left and right of bottom-right
            Coord(9, 10),  # up of bottom-right
            Coord(10, 9)   # left of bottom-right

        }
        self.assertEqual(valid_coords, expected_coords)

    def test_opponent_pieces_ignored(self):
        """Test that opponent's pieces are ignored when finding valid coordinates."""
        # Place pieces of both colors
        self.game_state.board[Coord(5, 5)] = PlayerColor.RED
        self.game_state.board[Coord(5, 6)] = PlayerColor.BLUE
        
        valid_coords = self.game_state.find_valid_coords(PlayerColor.RED)
        expected_coords = {
            Coord(4, 5),  # up
            Coord(6, 5),  # down
            Coord(5, 4)   # left
            # Coord(5, 6) is occupied by BLUE, so should not be included
        }
        self.assertEqual(valid_coords, expected_coords)

    def test_occupied_spaces_excluded(self):
        """Test that occupied spaces are not included in valid coordinates."""
        # Create a small cluster of pieces
        self.game_state.board[Coord(5, 5)] = PlayerColor.RED
        self.game_state.board[Coord(5, 6)] = PlayerColor.RED
        self.game_state.board[Coord(6, 5)] = PlayerColor.RED
        self.game_state.board[Coord(6, 6)] = PlayerColor.RED
        
        valid_coords = self.game_state.find_valid_coords(PlayerColor.RED)
        expected_coords = {
            Coord(4, 5),  # up of top-left
            Coord(4, 6),  # up of top-right
            Coord(5, 4),  # left of top-left
            Coord(6, 4),  # left of bottom-left
            Coord(5, 7),  # right of top-right
            Coord(6, 7),  # right of bottom-right
            Coord(7, 5),  # down of bottom-left
            Coord(7, 6)   # down of bottom-right
        }
        self.assertEqual(valid_coords, expected_coords)

    def test_different_color_valid_coords(self):
        """Test finding valid coordinates for different player colors."""
        # Place pieces for both colors
        self.game_state.board[Coord(5, 5)] = PlayerColor.RED
        self.game_state.board[Coord(7, 7)] = PlayerColor.BLUE
        
        # Test for RED player
        red_valid_coords = self.game_state.find_valid_coords(PlayerColor.RED)
        red_expected = {
            Coord(4, 5),  # up
            Coord(6, 5),  # down
            Coord(5, 4),  # left
            Coord(5, 6)   # right
        }
        self.assertEqual(red_valid_coords, red_expected)
        
        # Test for BLUE player
        blue_valid_coords = self.game_state.find_valid_coords(PlayerColor.BLUE)
        blue_expected = {
            Coord(6, 7),  # up
            Coord(8, 7),  # down
            Coord(7, 6),  # left
            Coord(7, 8)   # right
        }
        self.assertEqual(blue_valid_coords, blue_expected)

class TestValidMoves(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.game_state = GameState(board={}, current_player=PlayerColor.RED)

    def test_empty_board_first_move(self):
        """Test valid moves on an empty board (first move)."""
        valid_moves = self.game_state.find_all_valid_moves(PlayerColor.RED)
        # First move should have no valid moves as there are no pieces to be adjacent to
        self.assertEqual(len(valid_moves), 0)

    def test_single_piece_valid_moves(self):
        """Test valid moves with a single piece on the board."""
        # Place a single piece
        self.game_state.board[Coord(5, 5)] = PlayerColor.RED
        valid_moves = self.game_state.find_all_valid_moves(PlayerColor.RED)
        # Should have valid moves adjacent to the piece
        self.assertGreater(len(valid_moves), 0)

    def test_corner_piece_valid_moves(self):
        """Test valid moves with a piece in the corner."""
        # Place a piece in the corner
        self.game_state.board[Coord(0, 0)] = PlayerColor.RED
        valid_moves = self.game_state.find_all_valid_moves(PlayerColor.RED)
        # Should have valid moves only in valid directions from corner
        self.assertGreater(len(valid_moves), 0)

    def test_multiple_pieces_valid_moves(self):
        """Test valid moves with multiple connected pieces."""
        # Create a small cluster of pieces
        self.game_state.board[Coord(5, 5)] = PlayerColor.RED
        self.game_state.board[Coord(5, 6)] = PlayerColor.RED
        self.game_state.board[Coord(6, 5)] = PlayerColor.RED
        valid_moves = self.game_state.find_all_valid_moves(PlayerColor.RED)
        # Should have valid moves around the cluster
        self.assertGreater(len(valid_moves), 0)

    def test_opponent_pieces_valid_moves(self):
        """Test valid moves with opponent pieces on the board."""
        # Place pieces of both colors
        self.game_state.board[Coord(5, 5)] = PlayerColor.RED
        self.game_state.board[Coord(5, 6)] = PlayerColor.BLUE
        valid_moves = self.game_state.find_all_valid_moves(PlayerColor.RED)
        # Should have valid moves that don't overlap with opponent pieces
        self.assertGreater(len(valid_moves), 0)

    def test_edge_pieces_valid_moves(self):
        """Test valid moves with pieces at board edges."""
        # Place pieces at edges
        self.game_state.board[Coord(0, 5)] = PlayerColor.RED  # top edge
        self.game_state.board[Coord(10, 5)] = PlayerColor.RED  # bottom edge
        self.game_state.board[Coord(5, 0)] = PlayerColor.RED  # left edge
        self.game_state.board[Coord(5, 10)] = PlayerColor.RED  # right edge
        valid_moves = self.game_state.find_all_valid_moves(PlayerColor.RED)
        # Should have valid moves that respect board boundaries
        self.assertGreater(len(valid_moves), 0)

    def test_nearly_filled_board_no_valid_moves(self):
        """Test valid moves on a nearly filled board with no valid moves possible."""
        # Fill the board almost completely with RED pieces
        for r in range(11):
            for c in range(11):
                self.game_state.board[Coord(r, c)] = PlayerColor.RED
        
        # Create a few isolated empty slots that are too small for any shape
        # These slots are chosen to be isolated and too small for any shape to fit
        empty_slots = [
            Coord(3, 3),  # Single isolated slot
            Coord(7, 7),  # Single isolated slot
            Coord(0, 0),  # Corner slot
            Coord(10, 10)  # Corner slot
        ]
        
        # Remove pieces from the empty slots
        for coord in empty_slots:
            self.game_state.board.pop(coord, None)
        
        valid_moves = self.game_state.find_all_valid_moves(PlayerColor.RED)
        
        # Verify that no valid moves are found since the empty slots are too small
        # and isolated for any shape to fit
        self.assertEqual(len(valid_moves), 0)

if __name__ == '__main__':
    unittest.main() 