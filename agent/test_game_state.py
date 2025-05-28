import unittest
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.program import GameState, PlaceAction, Coord
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

if __name__ == '__main__':
    unittest.main() 