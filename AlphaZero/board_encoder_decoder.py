#!/usr/bin/env python

import numpy as np
from Connect4Board import Connect4GameBoard


def encode_board(board):
    encoded = np.zeros([7, 6, 2]).astype(int)
    encoded[:, :, 0] = board.board
    encoded[:, :, 1] = board.curr_player
    return encoded


def decode_board(encoded):
    cols = []
    for row in range(7):
        cols.append(np.argmax(np.nonzero(encoded[row])))
    return Connect4GameBoard(encoded[:, :, 0], cols, encoded[0, 0, 1])