import numpy as np
import scipy.signal


ACTIONS = [0, 1, 2, 3, 4, 5, 6]


class Connect4GameBoard:
    def __init__(self, board=np.zeros((7, 6)), cols=(0, 0, 0, 0, 0, 0, 0), curr_player=1):
        self.board = board
        self.cols = list(cols)
        self.winner = 0
        self.curr_player = curr_player

    def is_game_over(self):
        result = self.check_win()
        if result == 1 or result == -1:
            return True
        if len(self.get_legal_actions()) == 0:
            return True
        return False

    def game_result(self):
        return self.check_win()

    def _is_action_legal(self, column):
        if self.cols[column] < 6:
            return True
        return False

    def get_legal_actions(self):
        return list(filter(self._is_action_legal, range(7)))

    def play(self, column):
        if self.cols[column] < 6:
            new_board = np.copy(self.board)
            new_cols = np.copy(self.cols)
            new_board[column, self.cols[column]] = self.curr_player
            new_cols[column] += 1
            new_curr_player = self.curr_player * (-1)
            return Connect4GameBoard(new_board, new_cols, new_curr_player)
        raise Exception("Action is Not Valid")

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
            return 1 * self.curr_player
        if np.amin(row_check) == -4 or np.amin(col_check) == -4 or np.amin(diagonal_left_check) == -4 \
                or np.amin(diagonal_right_check) == -4:
            return -1 * self.curr_player
        return 0
