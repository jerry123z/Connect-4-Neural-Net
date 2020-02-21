import unittest
import Connect4Board
import numpy as np


class BoardTests(unittest.TestCase):
    def test_init_empty(self):
        board = Connect4Board.Connect4GameBoard()
        self.assertTrue(np.array_equal(board.board, np.zeros((7, 6))))

    def test_place_in_col(self):
        board = Connect4Board.Connect4GameBoard()
        board = board.play(column=0)
        self.assertEqual(board.board[0, 0], 1)
        self.assertTrue(1 in board.cols)

    def test_check_row(self):
        board = Connect4Board.Connect4GameBoard()
        board = board.play(column=0)
        board = board.play(column=0)
        board = board.play(column=1)
        board = board.play(column=1)
        board = board.play(column=2)
        board = board.play(column=2)
        board = board.play(column=3)
        self.assertEqual(board.check_win(), 1)

    def test_check_col(self):
        board = Connect4Board.Connect4GameBoard()
        board = board.play(column=0)
        board = board.play(column=1)
        board = board.play(column=0)
        board = board.play(column=1)
        board = board.play(column=0)
        board = board.play(column=1)
        board = board.play(column=0)
        self.assertEqual(1, board.check_win())

    def test_check_continue(self):
        board = Connect4Board.Connect4GameBoard()
        board = board.play(column=0)
        board = board.play(column=0)
        board = board.play(column=0)
        board = board.play(column=0)
        self.assertEqual(0, board.check_win())

    def test_chec_diag(self):
        board = Connect4Board.Connect4GameBoard()
        board = board.play(column=0)
        board = board.play(column=1)
        board = board.play(column=1)
        board = board.play(column=6)
        board = board.play(column=2)
        board = board.play(column=2)
        board = board.play(column=2)
        board = board.play(column=3)
        board = board.play(column=3)
        board = board.play(column=3)
        board = board.play(column=3)
        self.assertEqual(1, board.check_win())


if __name__ == '__main__':
    unittest.main()
