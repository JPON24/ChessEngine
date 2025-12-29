import numpy as np
import pygame
from BoardData import *
import math
import copy

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
                drawPawn(340 + 75 * j, 60 + i * 75, boardList[i][j].color)
            elif (piece == 'r'):
                drawRook(340 + 75 * j, 60 + i * 75, boardList[i][j].color)
            elif (piece == 'n'):
                drawKnight(340 + 75 * j, 60 + i * 75, boardList[i][j].color)
            elif (piece == 'k'):
                drawKing(340 + 75 * j, 60 + i * 75, boardList[i][j].color)
            elif (piece == 'q'):
                drawQueen(340 + 75 * j, 60 + i * 75, boardList[i][j].color)
            elif (piece == 'b'):
                drawBishop(340 + 75 * j, 60 + i * 75, boardList[i][j].color)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

def drawPawn(x,y,color):
    pawnSize = pieceW * 2 / 3
    if color == 'b':
        pygame.draw.rect(screen,pieceDark, (x+38-pawnSize/2, y+38-pawnSize/2, pawnSize,pawnSize))
    elif color == 'w':
        pygame.draw.rect(screen,pieceLight, (x+38-pawnSize/2, y+38-pawnSize/2, pawnSize,pawnSize))

def drawRook(x,y,color):
    if color == 'b':
        pygame.draw.rect(screen,pieceDark, (x + pieceW//4, y+5, pieceW,65))
    elif color == 'w':
        pygame.draw.rect(screen,pieceLight, (x + pieceW//4, y+5, pieceW,65))

def drawBishop(x,y,color):
    points = [(x+38,y+38+pieceH/2),(x+38+pieceW/2,y+38),(x+38-pieceW/2,y+38),(x+38,y+38-pieceH/2)]
    if color == 'b':
        pygame.draw.polygon(screen,pieceDark,points)
    elif color == 'w':
        pygame.draw.polygon(screen,pieceLight,points)

def drawQueen(x,y,color):
    if color == 'b':
        pygame.draw.circle(screen,pieceDark, (x+75//2, y+75//2),pieceW/2)
    elif color == 'w':
        pygame.draw.circle(screen,pieceLight, (x+75//2, y+75//2),pieceW/2)

def drawKing(x,y,color):
    pawnSize = pieceW * 3 / 4
    if color == 'b':
        pygame.draw.rect(screen,pieceDark, (x+38-pawnSize/2, y+38-pawnSize/2, pawnSize,pawnSize))
        pygame.draw.circle(screen,pieceDark, (x+75//2, y+75//2),pieceW*5.25/12)
    elif color == 'w':
        pygame.draw.rect(screen,pieceLight, (x+38-pawnSize/2, y+38-pawnSize/2, pawnSize,pawnSize))
        pygame.draw.circle(screen,pieceLight, (x+75//2, y+75//2),pieceW*5.25/12)

def drawKnight(x,y,color):
    knightSize = pieceW * 2 / 3
    if color == 'b':
        pygame.draw.ellipse(screen,pieceDark, (x + 13, y + 22, pieceW,knightSize))
    elif color == 'w':
        pygame.draw.ellipse(screen,pieceLight, (x + 13, y + 22, pieceW,knightSize))

def selectSquare(x,y):
    for i in range(8):
        for j in range(8):
            if (x > 340 + 75 * j and x < 415 + 75 * j and
                y > 60 + i * 75 and y < 60 + 75 + i * 75):
                return j,i
    return -1, -1

def calculatePossibleMoves(boardList, x, y, color):
    position = boardList[y][x]
    piece = position.typeOfPiece
    # color = position.color
    validMoves = []

    if piece == 'p':
        positions = []

        if y == 2 and color == 'b':
            positions.append((x,y+1))
            positions.append((x,y+2))
        elif y == 6 and color == 'w':
            positions.append((x,y-1))
            positions.append((x,y-2))
            
        elif color == 'b':
            positions.append((x,y+1))
            if x+1 <= 7 and y+1 <= 7:
                if boardList[y+1][x+1].color == 'b':
                    validMoves.append(move(x, y, x+1, y+1))
            if x-1 >= 0 and y+1 <= 7:
                if boardList[y+1][x-1].color == 'b':
                    validMoves.append(move(x, y, x-1, y+1))

        elif color == 'w':
            positions.append((x,y-1))
            if x+1 <= 7 and y-1 >= 0:
                if boardList[y-1][x+1].color == 'b':
                    validMoves.append(move(x, y, x+1, y-1))
            if x-1 >= 0 and y-1 >= 0:
                if boardList[y-1][x-1].color == 'b':
                    validMoves.append(move(x,y,x-1, y-1))

        for i in positions:
            if i[0] > 7 or i[0] < 0 or i[1] > 7 or i[1] < 0:
                continue
            if boardList[i[1]][i[0]].typeOfPiece != '-':
                continue
            validMoves.append(move(x, y, i[0], i[1]))
    
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
                    validMoves.append(move(x, y, i[0], i[1]))
                continue 
            validMoves.append(move(x, y, i[0], i[1]))

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
                    validMoves.append(move(x, y, i[0], i[1]))
                continue 
            validMoves.append(move(x, y, i[0], i[1]))

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
            validMoves.append(move(x, y, i[0], i[1]))

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
            validMoves.append(move(x, y, i[0], i[1]))

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
            validMoves.append(move(x, y, i[0], i[1]))
    
    return validMoves

def movePiece(board,x,y,tgtX,tgtY,piece,color):
    global playerTurn,kingHasMoved
    
    if piece == 'k':
        kingHasMoved = True

    board[y][x].typeOfPiece = '-'
    board[y][x].color = '-'

    board[tgtY][tgtX].typeOfPiece = piece
    board[tgtY][tgtX].color = color

    playerTurn = not playerTurn

def getLegalMoves(board, white):
    legalMoves = []
    color = ''
    
    if white:
        color == 'w'
    else:
        color = 'b'
    
    count = 0
    for r in range(8):
        for c in range(8):
            if board[c][r].color == 'w':
                count += 1
            # legalMoves.extend(calculatePossibleMoves(board, r, c, color))
    print(count)
    return legalMoves

def checkGameOver(board, white):
    if len(getLegalMoves(board,white)) == 0:
        return True
    return False

def evaluate(board):
    whiteScore = 0
    blackScore = 0

    for i in range(8):
        for j in range(8):
            color = board[i][j].color
            if (color == 'w'):
                whiteScore += material[board[i][j].typeOfPiece]
            elif (color == 'b'):
                blackScore += material[board[i][j].typeOfPiece]

    score = whiteScore - blackScore

    return score

def minimax(board, depth, alpha, beta, white):
    if checkGameOver(board, white) or depth == 0:
        return evaluate(board)

    if white:
        maxEval = -math.inf
        possibleMoves = getLegalMoves(board, white)

        print(len(possibleMoves))

        # for i in possibleMoves:
        #     print(f'x : {i.x}, y : {i.y}, tgtX : {i.tgtX}, tgtY : {i.tgtY}')

        for move in possibleMoves:
            copiedBoard = copy.deepcopy(board)
            movePiece(copiedBoard,move.x,move.y,move.tgtX,move.tgtY,copiedBoard[move.y][move.x].typeOfPiece,'w')
            eval = minimax(copiedBoard, depth-1, alpha, beta, False)
            maxEval = max(maxEval, eval)
            if beta <= alpha:
                break

        return maxEval
    else:
        minEval = math.inf
        possibleMoves = getLegalMoves(board, white)

        for move in possibleMoves:
            copiedBoard = copy.deepcopy(board)
            movePiece(copiedBoard,move.x,move.y,move.tgtX,move.tgtY,copiedBoard[move.y][move.x].typeOfPiece,'b')
            eval = minimax(copiedBoard, depth-1, alpha, beta, True)
            minEval = min(minEval, eval)
            if beta <= alpha:
                break
            
        return minEval

material = {'p':1, 'n':3, 'b':3.1, 'r':5, 'q': 9, 'k':0, '-':0}

selectedPieceX = -1
selectedPieceY = -1

selectedX = -1
selectedY = -1

playerTurn = True
turnNumber = 0

kingHasMoved = False

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # print(evaluate(boardList))

    if (playerTurn):

        if event.type == pygame.MOUSEBUTTONDOWN:
            
            eval = minimax(boardList, 1, -math.inf, math.inf, True)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            selectedX, selectedY = selectSquare(mouse_x,mouse_y)

            if boardList[selectedY][selectedX].typeOfPiece != '-' and boardList[selectedY][selectedX].color == 'w':
                selectedPieceX, selectedPieceY = selectSquare(mouse_x,mouse_y)        
                validMoves = calculatePossibleMoves(boardList, selectedPieceX, selectedPieceY, 'w')

                for i in validMoves:
                    print(f'x : {i.x}, y : {i.y}, tgtX : {i.tgtX}, tgtY : {i.tgtY}')            
            else:
                validMoves = calculatePossibleMoves(boardList, selectedPieceX, selectedPieceY, 'w')

                # for i in validMoves:
                #     print(f'x : {i.x}, y : {i.y}, tgtX : {i.tgtX}, tgtY : {i.tgtY}')
                # print(f'selx : {selectedPieceX}, sely : {selectedPieceY}, seltgtX : {selectedX}, seltgtY : {selectedY}')
                
                unpacked = []
                for i in validMoves:
                    unpacked.append(i.unpack())

                if (selectedPieceX,selectedPieceY,selectedX,selectedY) in unpacked:
                    movePiece(boardList,selectedPieceX,selectedPieceY,
                                selectedX,selectedY,boardList[selectedPieceY][selectedPieceX].typeOfPiece,'w')
    else:
        selectedPieceX = -1
        selectedPieceY = -1
        selectedX = -1
        selectedY = -1

        if (turnNumber > 7):
            movePiece(boardList,turnNumber-8,2,
                                turnNumber-8,3,boardList[2][turnNumber-8].typeOfPiece,'b') 
        else:
            movePiece(boardList,turnNumber-8,1,
                                turnNumber-8,2,boardList[1][turnNumber-8].typeOfPiece,'b') 
        
        # minimax(boardList, 5, -math.inf, math.inf, False)
        turnNumber += 1

    rendering() 
    
pygame.quit()