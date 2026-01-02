import numpy as np
import pygame
from BoardData import *
import math
import copy
import time

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# rendering stuff
bgColor = (210, 210, 210)

boardRenderSize = (600, 600)
boardDark = (137, 81, 41)
boardLight = (211, 182, 131)

pieceDark = (30, 30, 30)
pieceLight = (220, 220, 220)
boardList = []

pieceW = 50
pieceH = 50 

#images
king_white = pygame.image.load('Images/white_king.png').convert_alpha()
king_white_scaled = pygame.transform.scale(king_white, (75, 75))

king_black = pygame.image.load('Images/black_king.png').convert_alpha()
king_black_scaled = pygame.transform.scale(king_black, (75, 75))

pawn_white = pygame.image.load('Images/white_pawn.png').convert_alpha()
pawn_white_scaled = pygame.transform.scale(pawn_white, (75, 75))

pawn_black = pygame.image.load('Images/black_pawn.png').convert_alpha()
pawn_black_scaled = pygame.transform.scale(pawn_black, (75, 75))

bishop_white = pygame.image.load('Images/white_bishop.png').convert_alpha()
bishop_white_scaled = pygame.transform.scale(bishop_white, (75, 75))

bishop_black = pygame.image.load('Images/black_bishop.png').convert_alpha()
bishop_black_scaled = pygame.transform.scale(bishop_black, (75, 75))
    
queen_white = pygame.image.load('Images/white_queen.png').convert_alpha()
queen_white_scaled = pygame.transform.scale(queen_white, (75, 75))

queen_black = pygame.image.load('Images/black_queen.png').convert_alpha()
queen_black_scaled = pygame.transform.scale(queen_black, (75, 75))

rook_white = pygame.image.load('Images/white_rook.png').convert_alpha()
rook_white_scaled = pygame.transform.scale(rook_white, (75, 75))

rook_black = pygame.image.load('Images/black_rook.png').convert_alpha()
rook_black_scaled = pygame.transform.scale(rook_black, (75, 75))

knight_white = pygame.image.load('Images/white_knight.png').convert_alpha()
knight_white_scaled = pygame.transform.scale(knight_white, (75, 75))

knight_black = pygame.image.load('Images/black_knight.png').convert_alpha()
knight_black_scaled = pygame.transform.scale(knight_black, (75, 75))

def init():
    outputList = []
    for i in range(8):
        newRow = []
        for j in range(8):
            occupied_piece = ''
            if (i == 1 or i == 6):
                occupied_piece = 'p'
            elif (i == 0 or i == 7):
                if (j == 0 or j == 7):
                    occupied_piece = 'r'
                if (j == 1 or j == 6):
                    occupied_piece = 'n'
                if (j == 2 or j == 5):
                    occupied_piece = 'b'
                if (j == 3):
                    occupied_piece = 'q'
                if (j == 4):
                    occupied_piece = 'k'
            else:
                occupied_piece = '-'
            if (i < 2):
                newRow.append(square(j, i, occupied_piece, 'b'))
            elif (i > 5):
                newRow.append(square(j, i, occupied_piece, 'w'))
            else:
                newRow.append(square(j, i, occupied_piece, '-'))

        outputList.append(newRow)
    return outputList

boardList = init()

def rendering():
    screen.fill(bgColor)

    for i in range(8):
        for j in range(8):
            if (j + i) % 2 == 1:
                pygame.draw.rect(screen, boardDark, (340 + 75 * j, 60 + i * 75,75,75))
            else:
                pygame.draw.rect(screen, boardLight, (340 + 75 * j, 60 + i * 75,75,75))

            piece = boardList[i][j].typeOfPiece

            if (piece == 'p'):
                drawPawnImg(340 + 75 * j, 60 + i * 75, boardList[i][j].color)
            elif (piece == 'r'):
                drawRookImg(340 + 75 * j, 60 + i * 75, boardList[i][j].color)
            elif (piece == 'n'):
                drawKnightImg(340 + 75 * j, 60 + i * 75, boardList[i][j].color)
            elif (piece == 'k'):
                drawKingImg(340 + 75 * j, 60 + i * 75, boardList[i][j].color)
            elif (piece == 'q'):
                drawQueenImg(340 + 75 * j, 60 + i * 75, boardList[i][j].color)
            elif (piece == 'b'):
                drawBishopImg(340 + 75 * j, 60 + i * 75, boardList[i][j].color)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

def drawPawnImg(x,y,color):
    if color == 'w':
        screen.blit(pawn_white_scaled, (x,y))
    elif color == 'b':
        pass
        screen.blit(pawn_black_scaled, (x,y))

def drawRookImg(x,y,color):
    if color == 'w':
        screen.blit(rook_white_scaled, (x,y))
    elif color == 'b':
        screen.blit(rook_black_scaled, (x,y))

def drawBishopImg(x,y,color):
    if color == 'w':
        screen.blit(bishop_white_scaled, (x,y))
    elif color == 'b':
        screen.blit(bishop_black_scaled, (x,y))

def drawQueenImg(x,y,color):
    if color == 'w':
        screen.blit(queen_white_scaled, (x,y))
    elif color == 'b':
        screen.blit(queen_black_scaled, (x,y))

def drawKingImg(x,y,color):
    if color == 'w':
        screen.blit(king_white_scaled, (x,y))
    elif color == 'b':
        screen.blit(king_black_scaled, (x,y))

def drawKnightImg(x,y,color):
    if color == 'w':
        screen.blit(knight_white_scaled, (x,y))
    elif color == 'b':
        screen.blit(knight_black_scaled, (x,y))

def selectSquare(x,y):
    for i in range(8):
        for j in range(8):
            if (x > 340 + 75 * j and x < 415 + 75 * j and
                y > 60 + i * 75 and y < 60 + 75 + i * 75):
                return j,i
    return -1, -1

calls = 0

def calculatePossibleMoves(boardList, x, y, check):
    global calls

    calls += 1
    position = boardList[y][x]
    piece = position.typeOfPiece
    color = position.color

    validMoves = []
    attackingMoves = []

    if piece == 'p':
        positions = []

        if y == 1 and color == 'b':
            if (boardList[y+1][x].typeOfPiece == '-'):
                positions.append((x,y+2))
        elif y == 6 and color == 'w':
            if (boardList[y-1][x].typeOfPiece == '-'):
                positions.append((x,y-2))
            
        if color == 'b':
            positions.append((x,y+1))
            if x+1 <= 7 and y+1 <= 7:
                if boardList[y+1][x+1].color == 'w':
                    validMoves.append(Move(x, y, x+1, y+1))
            if x-1 >= 0 and y+1 <= 7:
                if boardList[y+1][x-1].color == 'w':
                    validMoves.append(Move(x, y, x-1, y+1))

        elif color == 'w':
            positions.append((x,y-1))
            if x+1 <= 7 and y-1 >= 0:
                if boardList[y-1][x+1].color == 'b':
                    validMoves.append(Move(x, y, x+1, y-1))
            if x-1 >= 0 and y-1 >= 0:
                if boardList[y-1][x-1].color == 'b':
                    validMoves.append(Move(x,y,x-1, y-1))

        for i in positions:
            if i[0] > 7 or i[0] < 0 or i[1] > 7 or i[1] < 0:
                continue
            if boardList[i[1]][i[0]].typeOfPiece != '-':
                continue
            validMoves.append(Move(x, y, i[0], i[1]))
    
    if piece == 'n':
        positions = []
        
        positions.append((x+1,y+2))
        positions.append((x+1,y-2))
        positions.append((x-1,y-2))
        positions.append((x-1,y+2))

        positions.append((x+2,y+1))
        positions.append((x+2,y-1))
        positions.append((x-2,y-1))
        positions.append((x-2,y+1))

        for i in positions:
            if i[0] > 7 or i[0] < 0 or i[1] > 7 or i[1] < 0:
                continue
            if boardList[i[1]][i[0]].typeOfPiece != '-':
                if boardList[i[1]][i[0]].color != color:
                    validMoves.append(Move(x, y, i[0], i[1]))
                continue 
            validMoves.append(Move(x, y, i[0], i[1]))

    if piece == 'k':
        positions = []
        
        positions.append((x+1,y+1))
        positions.append((x+1,y-1))
        positions.append((x-1,y-1))
        positions.append((x-1,y+1))

        positions.append((x+1,y))
        positions.append((x-1,y))
        positions.append((x,y+1))
        positions.append((x,y-1))

        for i in positions:
            if i[0] > 7 or i[0] < 0 or i[1] > 7 or i[1] < 0:
                continue
            if boardList[i[1]][i[0]].typeOfPiece != '-':
                if boardList[i[1]][i[0]].color != color:
                    validMoves.append(Move(x, y, i[0], i[1]))
                if boardList[i[1]][i[0]].typeOfPiece == 'r':
                    if color == 'b':
                        if boardList[0][3] == '-' and boardList[0][2] == '-' and boardList[0][1] == '-':    
                            validMoves.append(Move(x,y,0,0))
                        if boardList[0][5] == '-' and boardList[0][6] == '-':    
                            validMoves.append(Move(x,y,7,0))
                    elif color == 'w':
                        if boardList[7][3] == '-' and boardList[7][2] == '-' and boardList[7][1] == '-':    
                            validMoves.append(Move(x,y,0,7))
                        if boardList[7][5] == '-' and boardList[7][6] == '-':    
                            validMoves.append(Move(x,y,7,7))
                continue 
            validMoves.append(Move(x, y, i[0], i[1]))

        # if not kingHasMoved:
        #     if tgtX == 0 and tgtY == 7:
        #         for i in range(1,4):
        #             if boardList[y][x-i].typeOfPiece != '-':
        #                 break
        #         if boardList[7][0].typeOfPiece == 'r':
        #             movePiece(boardList,x,y,x-2,y, piece,color)
        #             movePiece(boardList,0,7,x-1,y, 'r',color)
        #     elif tgtX == 7 and tgtY == 7:
        #         for i in range(1,3):
        #             if boardList[y][x+i].typeOfPiece != '-':
        #                 break
        #         if boardList[7][7].typeOfPiece == 'r':
        #             movePiece(boardList,x,y,x+2,y, piece,color)
        #             movePiece(boardList,7,7,x+1,y, 'r',color)
        #             global playerTurn

        #             playerTurn = not playerTurn

    if piece == 'r':
        positions = []

        for i in range(1,8):
            if x + i > 7:
                break
            if boardList[y][x+i].typeOfPiece != '-':
                if (boardList[y][x+i].color != color):
                    positions.append((x+i,y))
                break
            positions.append((x+i, y))

        for i in range(1,8):
            if x - i < 0:
                break
            if boardList[y][x-i].typeOfPiece != '-':
                if (boardList[y][x-i].color != color):
                    positions.append((x-i,y))
                break
            positions.append((x-i, y))

        for i in range(1,8):
            if y + i > 7:
                break
            if boardList[y+i][x].typeOfPiece != '-':
                if (boardList[y+i][x].color != color):
                    positions.append((x,y+i))
                break
            positions.append((x, y+i))

        for i in range(1,8):
            if y - i < 0:
                break
            if boardList[y-i][x].typeOfPiece != '-':
                if (boardList[y-i][x].color != color):
                    positions.append((x,y-i))
                break
            positions.append((x, y-i))

        for i in positions:
            if i[0] > 7 or i[0] < 0 or i[1] > 7 or i[1] < 0:
                continue
            validMoves.append(Move(x, y, i[0], i[1]))

    if piece == 'b':
        positions = []

        for i in range(1,8):
            if x + i > 7 or y + i > 7:
                break
            if boardList[y+i][x+i].typeOfPiece != '-':
                if (boardList[y+i][x+i].color != color):
                    positions.append((x+i,y+i))
                break
            positions.append((x+i, y+i))

        for i in range(1,8):
            if x - i < 0 or y - i < 0:
                break
            if boardList[y-i][x-i].typeOfPiece != '-':
                if (boardList[y-i][x-i].color != color):
                    positions.append((x-i,y-i))
                break
            positions.append((x-i, y-i))

        for i in range(1,8):
            if y + i > 7 or x - i < 0:
                break
            if boardList[y+i][x-i].typeOfPiece != '-':
                if (boardList[y+i][x-i].color != color):
                    positions.append((x-i,y+i))
                break
            positions.append((x-i, y+i))

        for i in range(1,8):
            if y - i < 0 or x + i > 7:
                break
            if boardList[y-i][x+i].typeOfPiece != '-':
                if (boardList[y-i][x+i].color != color):
                    positions.append((x+i,y-i))
                break
            positions.append((x+i, y-i))

        for i in positions:
            if i[0] > 7 or i[0] < 0 or i[1] > 7 or i[1] < 0:
                continue
            validMoves.append(Move(x, y, i[0], i[1]))

    if piece == 'q':
        positions = []

        for i in range(1,8):
            if x + i > 7 or y + i > 7:
                break
            if boardList[y+i][x+i].typeOfPiece != '-':
                if (boardList[y+i][x+i].color != color):
                    positions.append((x+i,y+i))
                break
            positions.append((x+i, y+i))

        for i in range(1,8):
            if x - i < 0 or y - i < 0:
                break
            if boardList[y-i][x-i].typeOfPiece != '-':
                if (boardList[y-i][x-i].color != color):
                    positions.append((x-i,y-i))
                break
            positions.append((x-i, y-i))

        for i in range(1,8):
            if y + i > 7 or x - i < 0:
                break
            if boardList[y+i][x-i].typeOfPiece != '-':
                if (boardList[y+i][x-i].color != color):
                    positions.append((x-i,y+i))
                break
            positions.append((x-i, y+i))

        for i in range(1,8):
            if y - i < 0 or x + i > 7:
                break
            if boardList[y-i][x+i].typeOfPiece != '-':
                if (boardList[y-i][x+i].color != color):
                    positions.append((x+i,y-i))
                break
            positions.append((x+i, y-i))

        for i in range(1,8):
            if x + i > 7:
                break
            if boardList[y][x+i].typeOfPiece != '-':
                if (boardList[y][x+i].color != color):
                    positions.append((x+i,y))
                break
            positions.append((x+i, y))

        for i in range(1,8):
            if x - i < 0:
                break
            if boardList[y][x-i].typeOfPiece != '-':
                if (boardList[y][x-i].color != color):
                    positions.append((x-i,y))
                break
            positions.append((x-i, y))

        for i in range(1,8):
            if y + i > 7:
                break
            if boardList[y+i][x].typeOfPiece != '-':
                if (boardList[y+i][x].color != color):
                    positions.append((x,y+i))
                break
            positions.append((x, y+i))

        for i in range(1,8):
            if y - i < 0:
                break
            if boardList[y-i][x].typeOfPiece != '-':
                if (boardList[y-i][x].color != color):
                    positions.append((x,y-i))
                break
            positions.append((x, y-i))

        for i in positions:
            if i[0] > 7 or i[0] < 0 or i[1] > 7 or i[1] < 0:
                continue
            validMoves.append(Move(x, y, i[0], i[1]))
    
    out = []

    if check:
        for move in validMoves:
            copiedBoard = copy.deepcopy(boardList)

            movePiece(copiedBoard, move.x, move.y, move.tgtX, move.tgtY, 
                                copiedBoard[move.y][move.x].typeOfPiece, copiedBoard[move.y][move.x].color)

            legalMovesOther = ''
            color = copiedBoard[move.tgtY][move.tgtX].color

            if color == 'w':
                legalMovesOther = getLegalMoves(copiedBoard, 'b', False, validMoves)
            elif color == 'b':
                legalMovesOther = getLegalMoves(copiedBoard, 'w', False, validMoves)

            illegal = False
            for i in legalMovesOther:
                if copiedBoard[i.tgtY][i.tgtX].typeOfPiece == 'k' and copiedBoard[i.tgtY][i.tgtX].color == color:
                    illegal = True
                    break

            if not illegal:
                out.append(move)

        return out
    return validMoves

def movePiece(board,x,y,tgtX,tgtY,piece,color):
    global playerTurn
    
    if board[y][x].typeOfPiece == 'k':
        if (y == 7 or y == 0) and x == 4:
            if (board[tgtY][tgtX].typeOfPiece == 'r'):
                if tgtX == 0: # queenside
                    board[y][4].typeOfPiece = '-'
                    board[y][4].color = '-'
                    
                    board[y][2].typeOfPiece = 'k'
                    board[y][2].color = color

                    board[y][0].typeOfPiece = '-'
                    board[y][0].color = '-'

                    board[y][3].typeOfPiece = 'r'
                    board[y][3].color = color
                elif tgtX == 7: # kingside
                    board[y][x].typeOfPiece = '-'
                    board[y][x].color = '-'
                    
                    board[y][6].typeOfPiece = 'k'
                    board[y][6].color = color

                    board[y][7].typeOfPiece = '-'
                    board[y][7].color = '-'
                    
                    board[y][5].typeOfPiece = 'r'
                    board[y][5].color = color
                return

    board[y][x].typeOfPiece = '-'
    board[y][x].color = '-'

    board[tgtY][tgtX].typeOfPiece = piece
    board[tgtY][tgtX].color = color

    promote(board)

def getLegalMoves(board, color, check, legalMovesPrev=[]):
    legalMoves = []
    
    for r in range(8):
        for c in range(8):
            if (board[c][r].typeOfPiece == '-'):
                continue

            if (board[c][r].color == color):
                legalMoves.extend(calculatePossibleMoves(board, r, c, check))

    return legalMoves

def checkGameOver(board, color):
    if len(getLegalMoves(board,color,True)) == 0:
        return True

    return False

def getMaterial(board):
    whiteScore = 0
    blackScore = 0

    for i in range(8):
        for j in range(8):
            color = board[i][j].color
            if (color == 'w'):
                whiteScore += material[board[i][j].typeOfPiece]
            elif (color == 'b'):
                blackScore += material[board[i][j].typeOfPiece]
    
    return whiteScore - blackScore

def evaluate(board, possibleMovesB, possibleMovesW, training = False):
    whiteScore = 0
    blackScore = 0

    for i in range(8):
        for j in range(8):
            if training:
                if board[i*8 + j].typeOfPiece == '-':
                    continue

                color = board[i*8+j].color
                if (color == 'w'):
                    whiteScore += material[board[i*8+j].typeOfPiece]
                elif (color == 'b'):
                    blackScore += material[board[i*8+j].typeOfPiece]
            else:
                if board[i][j].typeOfPiece == '-':
                    continue

                color = board[i][j].color
                if (color == 'w'):
                    whiteScore += material[board[i][j].typeOfPiece]
                elif (color == 'b'):
                    blackScore += material[board[i][j].typeOfPiece]
    
    materialEval = whiteScore - blackScore

    positional = (len(possibleMovesW) - len(possibleMovesB)) * 0.1

    score = materialEval + positional

    return score

def promote(board):
    for i in range(8):
        if board[0][i].typeOfPiece == 'p':
            board[0][i].typeOfPiece = 'q'
        if board[7][i].typeOfPiece == 'p':
            board[7][i].typeOfPiece = 'q'

def minimax(board, depth, alpha, beta, color, possibleMovesB, possibleMovesW):
    global maxDepth
    if checkGameOver(board, color) or depth == 0:
        return evaluate(board, possibleMovesB, possibleMovesW), Move(0,0,0,0)

    if color == 'w':
        maxEval = -math.inf
        possibleMoves = getLegalMoves(board, 'w', True)
        possibleMovesW = possibleMoves
        bestMove = ''

        for move in possibleMoves:
            copiedBoard = copy.deepcopy(board)
            movePiece(copiedBoard,move.x,move.y,move.tgtX,move.tgtY,copiedBoard[move.y][move.x].typeOfPiece,'w')
            eval,_ = minimax(copiedBoard, depth-1, alpha, beta, 'b', possibleMovesB, possibleMovesW)
            alpha = max(alpha, eval)

            if (eval > maxEval):
                maxEval = eval
                bestMove = move

            if beta <= alpha:
                break

        return maxEval, bestMove
    else:
        minEval = math.inf
        possibleMoves = getLegalMoves(board, 'b', True)
        possibleMovesB = possibleMoves
        bestMove = ''

        for move in possibleMoves:
            copiedBoard = copy.deepcopy(board)
            movePiece(copiedBoard,move.x,move.y,move.tgtX,move.tgtY,copiedBoard[move.y][move.x].typeOfPiece,'b')
            eval, _ = minimax(copiedBoard, depth-1, alpha, beta, 'w', possibleMovesB, possibleMovesW)
            beta = min(beta, eval)

            if (eval < minEval):
                minEval = eval
                bestMove = move

            if beta <= alpha:
                break
            
        return minEval, bestMove

material = {'p':100, 'n':300, 'b':310, 'r':500, 'q': 900, 'k':10000, '-':0}

selectedPieceX = -1
selectedPieceY = -1

selectedX = -1
selectedY = -1

playerTurn = True
turnNumber = 0

kingHasMoved = False

import pandas as pd
import PGNReader as pgn

from sklearn.preprocessing import OrdinalEncoder
from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

model = LogisticRegression()

def inference(boardList, color):
    newOrdinal = OrdinalEncoder()
    categories = [
        ['p'],['n'],['b'],['r'],['k'],['q'],['-']
    ]

    newOrdinal.fit(categories)
    
    isWhite = 1
    colorOther = 'b'

    if color == 'w':
        colorOther = 'b'
        isWhite = 1
    elif color == 'b':
        colorOther = 'w'
        isWhite = 0

    possibleMoves = getLegalMoves(boardList, color, True)
    possibleMovesOther = getLegalMoves(boardList, colorOther, True)

    possibleMovesW = ''
    possibleMovesB = ''
    
    if color == 'w':
        possibleMovesW = possibleMoves
        possibleMovesB = possibleMovesOther
    elif color == 'b':
        possibleMovesW = possibleMovesOther
        possibleMovesB = possibleMoves

    pieces = []
    for i in possibleMoves:
        pieces.append([boardList[i.y][i.x].typeOfPiece]) 

    piecesConverted = newOrdinal.transform(pieces)

    flattenedBoard = []
    flattenedBoardPieces = []
    flattenedBoardColors = []
    
    boardPieces = []
    
    for i, val in enumerate(boardList):
        flattenedBoard.extend(val)
        tempPiece = []

        for j in range(8):
            tempPiece.append([boardList[i][j].typeOfPiece])
            if boardList[i][j].color == 'w':
                flattenedBoardColors.extend([1.0])
            elif boardList[i][j].color == 'b':
                flattenedBoardColors.extend([-1.0])
            else:
                flattenedBoardColors.extend([0.0])

        boardPieces.extend(tempPiece)

    flattenedBoardPieces = newOrdinal.transform(boardPieces)

    bestMove = ''
    maxProb = 0
    maxLogit = 0

    if (len(possibleMoves) == 0):
        return '','','',False

    for i, move in enumerate(possibleMoves):
        inputFeatures = []
        inputFeatures += [isWhite % 2,
                            evaluate(boardList, possibleMovesB, possibleMovesW),
                            move.x,
                            move.y,
                            move.tgtX,
                            move.tgtY,
                            piecesConverted[i][0]]
        
        inputFeatures += flattenedBoardPieces.T[0].tolist()
        inputFeatures += flattenedBoardColors

        x = pd.DataFrame(inputFeatures)

        scaler = preprocessing.StandardScaler().fit(x.T)

        x_scaled = scaler.transform(x.T)

        probability = model.predict_proba(x_scaled)[0, 1]
        rawLogit = model.decision_function(x_scaled)

        if probability > maxProb:
            maxProb = probability
            bestMove = move
            maxLogit = rawLogit

    return maxProb, maxLogit, bestMove, True

def train(model, gamesToAnalyze):
    for i in range(min(len(pgn.gameList), gamesToAnalyze)):
        x_train, y_train = analyzeGame(i)
        trainGame(model, x_train, y_train)

gamesTrained = 0

def trainGame(model, x_train, y_train):
    global gamesTrained
    gamesTrained += 1
    print(gamesTrained)

    scaler = preprocessing.StandardScaler().fit(x_train)
    
    x_scaled = scaler.transform(x_train)

    # xTrain, yTrain, xTest, yTest = train_test_split(x_scaled, y_train, test_size=0.2, random_state=42)

    model.fit(x_scaled, y_train)

def analyzeGame(index): 
    newOrdinal = OrdinalEncoder()
    categories = [
        ['p'],['n'],['b'],['r'],['k'],['q'],['-']
    ]

    newOrdinal.fit(categories)

    boardList = init()
    moves = pgn.getGame(index)
    isWhite = 1
    color = 'w'
    colorOther = 'b'

    x_train = pd.DataFrame([])
    y_train = []

    for move in moves:
        if isWhite%2 == 1:
            color = 'w'
            colorOther = 'b'
        else:
            color = 'b'
            colorOther = 'w'

        possibleMoves = getLegalMoves(boardList, color, True)
        possibleMovesOther = getLegalMoves(boardList, colorOther, True)

        possibleMovesW = ''
        possibleMovesB = ''
        
        if color == 'w':
            possibleMovesW = possibleMoves
            possibleMovesB = possibleMovesOther
        elif color == 'b':
            possibleMovesW = possibleMovesOther
            possibleMovesB = possibleMoves

        xOut = ''
        yOut = []

        pieces = []
        
        if( len(possibleMoves) == 0 or len(possibleMovesOther) == 0):
            continue
        
        for i in possibleMoves:
            pieces.append([boardList[i.y][i.x].typeOfPiece]) 

        piecesConverted = newOrdinal.transform(pieces)

        flattenedBoard = []
        flattenedBoardPieces = []
        flattenedBoardColors = []
        
        boardPieces = []
        
        for i, val in enumerate(boardList):
            flattenedBoard.extend(val)
            tempPiece = []

            for j in range(8):
                tempPiece.append([boardList[i][j].typeOfPiece])
                if boardList[i][j].color == 'w':
                    flattenedBoardColors.extend([1.0])
                elif boardList[i][j].color == 'b':
                    flattenedBoardColors.extend([-1.0])
                else:
                    flattenedBoardColors.extend([0.0])

            boardPieces.extend(tempPiece)

        flattenedBoardPieces = newOrdinal.transform(boardPieces)

        # print(flattenedBoardPieces.T[0].tolist())
        # print(flattenedBoardColors)

        for i, pos in enumerate(possibleMoves):
            inputFeatures = []
            inputFeatures += [isWhite % 2,
                              evaluate(flattenedBoard, possibleMovesB, possibleMovesW, True),
                              pos.x,
                              pos.y,
                              pos.tgtX,
                              pos.tgtY,
                              piecesConverted[i][0]]
            
            inputFeatures += flattenedBoardPieces.T[0].tolist()
            inputFeatures += flattenedBoardColors

            x = pd.DataFrame(inputFeatures)

            if type(xOut) != pd.DataFrame:
                xOut = x.T
            else:
                xOut = pd.concat([xOut, x.T], axis=0)

            y = 0

            if (move.x == pos.x and move.y == pos.y and 
            move.tgtX == pos.tgtX and move.tgtY == pos.tgtY):
                y = 1

            yOut.append(y)

        movePiece(boardList,move.x,move.y,move.tgtX,move.tgtY,boardList[move.y][move.x].typeOfPiece,color)
        isWhite += 1

        x_train = pd.concat([x_train, xOut], axis=0)
        y_train.extend(yOut)

    pd_x = x_train
    pd_y = y_train

    return pd_x, pd_y
    
gamesToAnalyze = 10
train(model, gamesToAnalyze)

import pickle

# Save the model to a file
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

# To load the model later:
# with open('model.pkl', 'rb') as f:
#     model = pickle.load(f)

lambdaVal = 0
maxDepth = 2

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if (playerTurn):
        if event.type == pygame.MOUSEBUTTONDOWN:
            calls = 0
            mouse_x, mouse_y = pygame.mouse.get_pos()
            selectedX, selectedY = selectSquare(mouse_x,mouse_y)

            if boardList[selectedY][selectedX].typeOfPiece != '-' and boardList[selectedY][selectedX].color == 'w':
                if (boardList[selectedY][selectedX].typeOfPiece == 'r' and not kingHasMoved and boardList[selectedPieceY][selectedPieceX].typeOfPiece == 'k'):
                    movePiece(boardList,selectedPieceX,selectedPieceY,
                                selectedX,selectedY,boardList[selectedPieceY][selectedPieceX].typeOfPiece,'w')
                    playerTurn = False
                selectedPieceX, selectedPieceY = selectSquare(mouse_x,mouse_y)        
                validMoves = (boardList, selectedPieceX, selectedPieceY, True)
                # print('\n\n-----\n\n')        
                # for x in validMoves:
                #     print(x)      
            else:
                validMoves = calculatePossibleMoves(boardList, selectedPieceX, selectedPieceY, True)
                
                unpacked = []
                for i in validMoves:
                    unpacked.append(i.unpack())

                if (selectedPieceX,selectedPieceY,selectedX,selectedY) in unpacked:
                    movePiece(boardList,selectedPieceX,selectedPieceY,
                                selectedX,selectedY,boardList[selectedPieceY][selectedPieceX].typeOfPiece,'w')
                    playerTurn = False
    else:
        selectedPieceX = -1
        selectedPieceY = -1
        selectedX = -1
        selectedY = -1

        # if (turnNumber > 7):
        #     movePiece(boardList,turnNumber-8,2,
        #                         turnNumber-8,3,boardList[2][turnNumber-8].typeOfPiece,'b') 
        # else:
        #     movePiece(boardList,turnNumber-8,1,
        #                         turnNumber-8,2,boardList[1][turnNumber-8].typeOfPiece,'b') 

        startingTimestamp = time.time()

        confidence, evalInf, moveInf, valid = inference(boardList, 'b')

        evalInf *= lambdaVal

        # print(f'confidence : {confidence}, evalInf : {evalInf}, evalMini : {eval}')

        if valid:
            print("inference move")
            movePiece(boardList, moveInf.x, moveInf.y, moveInf.tgtX, moveInf.tgtY, 
                    boardList[moveInf.y][moveInf.x].typeOfPiece, 'b')
        else:
            eval, move = minimax(boardList, maxDepth, -math.inf, math.inf, 'b', [], [])
            print("minimax move")
            movePiece(boardList, move.x, move.y, move.tgtX, move.tgtY, 
                boardList[move.y][move.x].typeOfPiece, 'b')

        playerTurn = True
        turnNumber += 1

        print(f'Turn number : {turnNumber}. Eval : {evalInf}. Move time : {time.time()-startingTimestamp}. Calls : {calls}')

    rendering() 

    if (checkGameOver(boardList, 'b')):
        timestamp = time.time()
        while (time.time() - timestamp) < 3:
            rendering() 
        break
    
pygame.quit()