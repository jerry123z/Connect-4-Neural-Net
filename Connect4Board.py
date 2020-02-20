import numpy as np
import scipy.signal


class GameBoard:
    def __init__(self):
        self.board = np.zeros((7, 6))
        self.openRows = [0, 0, 0, 0, 0, 0, 0]

    def play(self, player, column):
        if self.openRows[column] < 6:
            self.board[column, self.openRows[column]] = player
            self.openRows[column] += 1
            return True
        return False

    def check_win(self):
        row = np.ones((1, 4))
        col = np.ones((4, 1))
        diagonal_left = np.eye(4)
        diagonal_right = [[0, 0, 0, 1],
                          [0, 0, 1, 0],
                          [0, 1, 0, 0],
                          [1, 0, 0, 0]]
        row_check = scipy.signal.convolve2d(self.board, row, 'valid')
        col_check = scipy.signal.convolve2d(self.board, col, 'valid')
        diagonal_left_check = scipy.signal.convolve2d(self.board, diagonal_left, 'valid')
        diagonal_right_check = scipy.signal.convolve2d(self.board, diagonal_right, 'valid')

        if np.amax(row_check) == 4 or np.amax(col_check) == 4 or np.amax(diagonal_left_check) == 4 \
                or np.amax(diagonal_right_check) == 4:
            return 1
        if np.amin(row_check) == -4 or np.amin(col_check) == -4 or np.amin(diagonal_left_check) == -4 \
                or np.amin(diagonal_right_check) == -4:
            return -1
        return 0
