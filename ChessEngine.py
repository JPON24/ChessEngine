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

def calculatePossibleMoves(boardList, x, y):
    position = boardList[y][x]
    piece = position.typeOfPiece
    color = position.color

    validMoves = []

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
                if boardList[y+1][x+1].color == 'b':
                    validMoves.append(Move(x, y, x+1, y+1))
            if x-1 >= 0 and y+1 <= 7:
                if boardList[y+1][x-1].color == 'b':
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

    playerTurn = not playerTurn

def getLegalMoves(board, color):
    legalMoves = []
    
    for r in range(8):
        for c in range(8):
            if (board[c][r].color == color):
                legalMoves.extend(calculatePossibleMoves(board, r, c))

    return legalMoves

def checkGameOver(board, color):
    if len(getLegalMoves(board,color)) == 0:
        return True
    
    kingCount = 0
    for i in range (8):
        for j in range(8):
            if board[i][j].typeOfPiece == 'k':
                kingCount += 1
    if kingCount != 2:
        return True

    return False

def evaluate(board):
    whiteScore = 0
    blackScore = 0

    whiteKingMoves = 0 
    blackKingMoves = 0

    for i in range(8):
        for j in range(8):
            color = board[i][j].color
            if (color == 'w'):
                whiteScore += material[board[i][j].typeOfPiece]
            elif (color == 'b'):
                blackScore += material[board[i][j].typeOfPiece]

            if board[i][j].typeOfPiece == 'k':
                if color == 'w':
                    whiteKingMoves = len(calculatePossibleMoves(board, i, j))
                elif color == 'b':
                    blackKingMoves = len(calculatePossibleMoves(board, i, j))

    whiteLegal = getLegalMoves(board, 'w')
    blackLegal = getLegalMoves(board, 'b')

    materialEval = whiteScore - blackScore

    positional = (len(whiteLegal) - len(blackLegal)) * 0.1    

    kingSafety = ((8-whiteKingMoves) - (8-blackKingMoves)) * 0.01

    score = materialEval + positional + kingSafety

    return score

def minimax(board, depth, alpha, beta, color):
    if checkGameOver(board, color) or depth == 0:
        return evaluate(board), Move(0,0,0,0)

    if color == 'w':
        maxEval = -math.inf
        possibleMoves = getLegalMoves(board, 'w')
        bestMove = ''

        for move in possibleMoves:
            copiedBoard = copy.deepcopy(board)
            movePiece(copiedBoard,move.x,move.y,move.tgtX,move.tgtY,copiedBoard[move.y][move.x].typeOfPiece,'w')
            eval,_ = minimax(copiedBoard, depth-1, alpha, beta, 'b')
            alpha = max(alpha, eval)

            if (eval > maxEval):
                maxEval = eval
                bestMove = move

            if beta <= alpha:
                break

        return maxEval, bestMove
    else:
        minEval = math.inf
        possibleMoves = getLegalMoves(board, 'b')
        bestMove = ''

        for move in possibleMoves:
            copiedBoard = copy.deepcopy(board)
            movePiece(copiedBoard,move.x,move.y,move.tgtX,move.tgtY,copiedBoard[move.y][move.x].typeOfPiece,'b')
            eval, _ = minimax(copiedBoard, depth-1, alpha, beta, 'w')
            beta = min(beta, eval)

            if (eval < minEval):
                minEval = eval
                bestMove = move

            if beta <= alpha:
                break
            
        return minEval, bestMove

material = {'p':1, 'n':3, 'b':3.1, 'r':5, 'q': 9, 'k':100, '-':0}

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

    if (playerTurn):

        if event.type == pygame.MOUSEBUTTONDOWN:
            
            mouse_x, mouse_y = pygame.mouse.get_pos()
            selectedX, selectedY = selectSquare(mouse_x,mouse_y)

            if boardList[selectedY][selectedX].typeOfPiece != '-' and boardList[selectedY][selectedX].color == 'w':
                if (boardList[selectedY][selectedX].typeOfPiece == 'r' and not kingHasMoved and boardList[selectedPieceY][selectedPieceX].typeOfPiece == 'k'):
                    movePiece(boardList,selectedPieceX,selectedPieceY,
                                selectedX,selectedY,boardList[selectedPieceY][selectedPieceX].typeOfPiece,'w')
                selectedPieceX, selectedPieceY = selectSquare(mouse_x,mouse_y)        
                validMoves = calculatePossibleMoves(boardList, selectedPieceX, selectedPieceY)
                # print('\n\n-----\n\n')        
                # for x in validMoves:
                #     print(x)      
            else:
                validMoves = calculatePossibleMoves(boardList, selectedPieceX, selectedPieceY)
                
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

        # if (turnNumber > 7):
        #     movePiece(boardList,turnNumber-8,2,
        #                         turnNumber-8,3,boardList[2][turnNumber-8].typeOfPiece,'b') 
        # else:
        #     movePiece(boardList,turnNumber-8,1,
        #                         turnNumber-8,2,boardList[1][turnNumber-8].typeOfPiece,'b') 
        
        # cannot promote
        # add checking into legal moves, remove whatever the hell a king trade is lol

        eval, move = minimax(boardList, 2, -math.inf, math.inf, 'b')

        movePiece(boardList, move.x, move.y, move.tgtX, move.tgtY, 
                  boardList[move.y][move.x].typeOfPiece, 'b')

        playerTurn = True
        turnNumber += 1

        # print(f'Turn number : {turnNumber}. Eval : {eval}')

    rendering() 

    if (checkGameOver(boardList, 'b')):
        timestamp = time.time()
        while (time.time() - timestamp) < 3:
            rendering() 
        break
    
pygame.quit()