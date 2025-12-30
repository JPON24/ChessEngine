import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import PGNReader as pgn

from ChessEngine import init

def model():
    pass

def train():
    pass

def analyzeGame(index):
    boardList = init()
    print(boardList)

    moves = pgn.getGame(index)


analyzeGame(0)