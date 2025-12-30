from BoardData import *
import chess.pgn

file_1 = open("PGNDATA/lichess_Jpon24_2025-12-19.pgn")
file_2 = open("PGNDATA/chess_com_games_2025-12-28.pgn")
file_3 = open("PGNDATA/chess_com_games_2025-12-28 (1).pgn")
file_4 = open("PGNDATA/chess_com_games_2025-12-28 (2).pgn")
file_5 = open("PGNDATA/chess_com_games_2025-12-28 (3).pgn")
file_6 = open("PGNDATA/chess_com_games_2025-12-28 (4).pgn")
file_7 = open("PGNDATA/chess_com_games_2025-12-28 (5).pgn")
file_8 = open("PGNDATA/chess_com_games_2025-12-28 (6).pgn")
file_9 = open("PGNDATA/chess_com_games_2025-12-28 (7).pgn")
file_10 = open("PGNDATA/chess_com_games_2025-12-28 (8).pgn")

fileList = []

fileList.append(file_1)
fileList.append(file_2)
fileList.append(file_3)
fileList.append(file_4)
fileList.append(file_5)
fileList.append(file_6)
fileList.append(file_7)
fileList.append(file_8)
fileList.append(file_9)
fileList.append(file_10)

gameList = []

def generateGameList():
    outputList = []
    for i in range(10):
        while True:
            game = chess.pgn.read_game(fileList[i])
            if game is None:
                break

            outputList.append(game)
    return outputList

gameList = generateGameList()

xPos = {'a': 0, 'b': 1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7} 

def convertToMoveClass(move):
    splitMove = [x for x in move]
    splitMove[0] = xPos[splitMove[0]]
    splitMove[1] = 8 - int(splitMove[1])
    splitMove[2] = xPos[splitMove[2]]
    splitMove[3] = 8 - int(splitMove[3])

    splitMove = Move(splitMove[0], splitMove[1], splitMove[2], splitMove[3])
    return splitMove

def getGame(index):
    moveList = []
    for move in gameList[index].mainline_moves():
        move = convertToMoveClass(str(move))
        moveList.append(move)
    
    return moveList