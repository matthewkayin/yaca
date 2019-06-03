import random
from datetime import datetime

EMPTY = 0
PAWN = 1
ROOKE = 2
KNIGHT = 3
BISHOP = 4
QUEEN = 5
KING = 6

class Board():
    def __init__(self, arguments):
        random.seed(datetime.now())
        self.squares = []
        for i in range(0, 8):
            self.squares.append([])
            for j in range(0, 8):
                self.squares[i].append(EMPTY)
        self.enPassant = [-1, -1]
        self.canCastle = [[True, True], [True, True]]
        self.turn = True
        self.turnCount = 1
        self.pieceToMove = (-1, -1)
        self.potentialMoves = []
        self.gameover = False
        self.fakeMoveStack = []
        self.verbose = False
        self.depth = 1
        self.parseArgs(arguments)
        for i in range(0, 8):
            self.squares[i][1] = PAWN
            self.squares[i][6] = PAWN + 6

        self.squares[0][0] = ROOKE
        self.squares[7][0] = ROOKE
        self.squares[0][7] = ROOKE + 6
        self.squares[7][7] = ROOKE + 6

        self.squares[1][0] = KNIGHT
        self.squares[6][0] = KNIGHT
        self.squares[1][7] = KNIGHT + 6
        self.squares[6][7] = KNIGHT + 6

        self.squares[2][0] = BISHOP
        self.squares[5][0] = BISHOP
        self.squares[2][7] = BISHOP + 6
        self.squares[5][7] = BISHOP + 6

        self.squares[3][0] = QUEEN
        self.squares[3][7] = QUEEN + 6
        self.squares[4][0] = KING
        self.squares[4][7] = KING + 6

    def parseArgs(self, args):
        for arg in args:
            if arg.startswith("-depth="):
                index = arg.index("=")
                self.depth = int(arg[(index+1):])
            elif arg == "-verbose" or arg == "-v":
                self.verbose = True

    def strFromCoords(self, x, y):
        letters = "abcdefgh"
        numbers = "87654321"

        return letters[x] + numbers[y]

    def strFromPiece(self, code):
        colorMod = 0
        if code > 6:
            colorMod = 6

        if code - colorMod == PAWN:
            return "pawn"
        elif code - colorMod == KNIGHT:
            return "knight"
        elif code - colorMod == ROOKE:
            return "rooke"
        elif code - colorMod == BISHOP:
            return "bishop"
        elif code - colorMod == QUEEN:
            return "queen"
        elif code - colorMod == KING:
            return "king"
        else:
            return "invalid piece"

    def printMove(self, piece, move, white):
        player = "black"
        if white:
            player = "white"
        pieceString = self.strFromPiece(self.squares[piece[0]][piece[1]])
        squareString = self.strFromCoords(move[0], move[1])
        if pieceString == "king" and abs(move[0] - piece[0]) == 2:
            if move[0] - piece[0] > 0:
                print(player + " castles kingside")
            else:
                print(player + " castles queenside")
        elif pieceString == "pawn" and abs(move[0] - piece[0]) == 1 and self.squares[move[0]][move[1]] == EMPTY and self.isEnemy(move[0], piece[1], white):
            print(player + " " + pieceString + " to " + squareString + " and captures with en passant")
        else:
            captures = self.isEnemy(move[0], move[1], white)
            if captures:
                print(player + " " + pieceString + " captures on " + squareString)
            else:
                print(player + " " + pieceString + " to " + squareString)

    def getPieces(self):
        pieces = []
        for i in range(0, 8):
            for j in range(0, 8):
                if self.squares[i][j] != EMPTY:
                    color = 1
                    if self.isAlly(i, j, False):
                        color = 0
                    colorMod = 6 * color
                    pieces.append([color, self.squares[i][j] - colorMod, i, j])
        return pieces

    def squareOccupied(self, x, y):
        return self.squares[x][y] != EMPTY

    def isAlly(self, x, y, white):
        if white:
            return self.squares[x][y] > 6
        else:
            return self.squares[x][y] > 0 and self.squares[x][y] < 7

    def isEnemy(self, x, y, white):
        return self.isAlly(x, y, not white)

    def inBounds(self, position):
        return position[0] >= 0 and position[0] < 8 and position[1] >= 0 and position[1] < 8

    def getPotentialMoves(self, x, y):
        moves = []
        if self.squares[x][y] == PAWN or self.squares[x][y] == PAWN + 6:
            moves = self.getPotentialMovesPawn(x, y)
        elif self.squares[x][y] == ROOKE or self.squares[x][y] == ROOKE + 6:
            moves = self.getPotentialMovesRooke(x, y)
        elif self.squares[x][y] == KNIGHT or self.squares[x][y] == KNIGHT + 6:
            moves = self.getPotentialMovesKnight(x, y)
        elif self.squares[x][y] == BISHOP or self.squares[x][y] == BISHOP + 6:
            moves = self.getPotentialMovesBishop(x, y)
        elif self.squares[x][y] == QUEEN or self.squares[x][y] == QUEEN + 6:
            moves = self.getPotentialMovesRooke(x, y) + self.getPotentialMovesBishop(x, y)
        elif self.squares[x][y] == KING or self.squares[x][y] == KING + 6:
            moves = self.getPotentialMovesKing(x, y)
        removeCount = 0
        for i in range(0, len(moves)):
            if self.wouldCheck(x, y, moves[i - removeCount][0], moves[i - removeCount][1], self.squares[x][y] > 6):
                del moves[i - removeCount]
                removeCount += 1
        return moves

    def getPotentialMovesPawn(self, x, y):
        moves = []
        white = self.squares[x][y] > 6
        direction = 1
        if white:
            direction = -1

        if self.inBounds((x, y + direction)):
            if not self.squareOccupied(x, y + direction):
                moves.append((x, y + direction))
        if self.inBounds((x, y + direction)) and self.inBounds((x, y + (2*direction))):
            if ((y == 1 and not white) or (y == 6 and white)) and not self.squareOccupied(x, y + direction) and not self.squareOccupied(x, y + (2*direction)):
                moves.append((x, y + (2*direction)))
        if self.inBounds((x - 1, y + direction)):
            if self.isEnemy(x - 1, y + direction, white) or (self.isEnemy(x - 1, y, white) and self.enPassant[0] == x - 1 and self.enPassant[1] == y):
                moves.append((x - 1, y + direction))
        if self.inBounds((x + 1, y + direction)):
            if self.isEnemy(x + 1, y + direction, white) or (self.isEnemy(x + 1, y, white) and self.enPassant[0] == x + 1 and self.enPassant[1] == y):
                moves.append((x + 1, y + direction))

        return moves

    def getPotentialMovesRooke(self, x, y):
        moves = []
        white = self.squares[x][y] > 6
        checkX = x - 1
        checkY = y
        while self.inBounds((checkX, checkY)):
            if self.isAlly(checkX, checkY, white) or self.isEnemy(checkX + 1, checkY, white):
                break
            moves.append((checkX, checkY))
            checkX -= 1

        checkX = x + 1
        checkY = y
        while self.inBounds((checkX, checkY)):
            if self.isAlly(checkX, checkY, white) or self.isEnemy(checkX - 1, checkY, white):
                break
            moves.append((checkX, checkY))
            checkX += 1

        checkX = x
        checkY = y - 1
        while self.inBounds((checkX, checkY)):
            if self.isAlly(checkX, checkY, white) or self.isEnemy(checkX, checkY + 1, white):
                break
            moves.append((checkX, checkY))
            checkY -= 1

        checkX = x
        checkY = y + 1
        while self.inBounds((checkX, checkY)):
            if self.isAlly(checkX, checkY, white) or self.isEnemy(checkX, checkY - 1, white):
                break
            moves.append((checkX, checkY))
            checkY += 1

        return moves

    def getPotentialMovesKnight(self, x, y):
        moves = []
        white = self.squares[x][y] > 6
        offsets = [[2, 1], [2, -1], [-2, 1], [-2, -1],
                   [1, 2], [1, -2], [-1, 2], [-1, -2]]
        for offset in offsets:
            checkX = x + offset[0]
            checkY = y + offset[1]
            if self.inBounds((checkX, checkY)):
                if not self.isAlly(checkX, checkY, white):
                    moves.append((checkX, checkY))

        return moves

    def getPotentialMovesBishop(self, x, y):
        moves = []
        white = self.squares[x][y] > 6
        checkX = x - 1
        checkY = y - 1
        while self.inBounds((checkX, checkY)):
            if self.isAlly(checkX, checkY, white) or self.isEnemy(checkX + 1, checkY + 1, white):
                break
            moves.append((checkX, checkY))
            checkX -= 1
            checkY -= 1

        checkX = x + 1
        checkY = y - 1
        while self.inBounds((checkX, checkY)):
            if self.isAlly(checkX, checkY, white) or self.isEnemy(checkX - 1, checkY + 1, white):
                break
            moves.append((checkX, checkY))
            checkX += 1
            checkY -= 1

        checkX = x - 1
        checkY = y + 1
        while self.inBounds((checkX, checkY)):
            if self.isAlly(checkX, checkY, white) or self.isEnemy(checkX + 1, checkY - 1, white):
                break
            moves.append((checkX, checkY))
            checkX -= 1
            checkY += 1

        checkX = x + 1
        checkY = y + 1
        while self.inBounds((checkX, checkY)):
            if self.isAlly(checkX, checkY, white) or self.isEnemy(checkX - 1, checkY - 1, white):
                break
            moves.append((checkX, checkY))
            checkX += 1
            checkY += 1

        return moves

    def getPotentialMovesKing(self, x, y):
        moves = []
        white = self.squares[x][y] > 6
        checkX = x - 1
        checkY = y - 1
        for i in range(0, 3):
            for j in range(0, 3):
                if self.inBounds((checkX + i, checkY + j)):
                    if not self.isAlly(checkX + i, checkY + j, white):
                        moves.append((checkX + i, checkY + j))
        color = 0
        if white:
            color = 1
        if self.canCastle[color][0] and not self.inCheck(self.squares, white):
            append = True
            checkX = x - 1
            while checkX != 0:
                if self.squareOccupied(checkX, y):
                    append = False
                    break
                checkX -= 1
            if append:
                moves.append((x - 2, y))
        if self.canCastle[color][1] and not self.inCheck(self.squares, white):
            append = True
            checkX = x + 1
            while checkX != 7:
                if self.squareOccupied(checkX, y):
                    append = False
                    break
                checkX += 1
            if append:
                moves.append((x + 2, y))

        return moves

    def inCheck(self, theBoard, white):
        colorMod = 0
        if white:
            colorMod = 6
        x = -1
        y = -1
        for i in range(0, 8):
            for j in range(0, 8):
                if theBoard[i][j] == KING + colorMod:
                    x = i
                    y = j
                    break

        enemyMod = 0
        if not white:
            enemyMod = 6

        direction = 1
        if white:
            direction = -1
        if self.inBounds((x - 1, y + direction)):
            if theBoard[x - 1][y + direction] == PAWN + enemyMod:
                return True
        if self.inBounds((x + 1, y + direction)):
            if theBoard[x + 1][y + direction] == PAWN + enemyMod:
                return True

        offsets = [[2, 1], [2, -1], [-2, 1], [-2, -1],
                   [1, 2], [1, -2], [-1, 2], [-1, -2]]
        for offset in offsets:
            checkX = x + offset[0]
            checkY = y + offset[1]
            if self.inBounds((checkX, checkY)):
                if theBoard[checkX][checkY] == KNIGHT + enemyMod:
                    return True

        #rooke stuff
        checkX = x - 1
        checkY = y
        while self.inBounds((checkX, checkY)):
            if theBoard[checkX][checkY] == ROOKE + enemyMod or theBoard[checkX][checkY] == QUEEN + enemyMod:
                return True
            if theBoard[checkX][checkY] != EMPTY:
                break
            checkX -= 1

        checkX = x + 1
        checkY = y
        while self.inBounds((checkX, checkY)):
            if theBoard[checkX][checkY] == ROOKE + enemyMod or theBoard[checkX][checkY] == QUEEN + enemyMod:
                return True
            if theBoard[checkX][checkY] != EMPTY:
                break
            checkX += 1

        checkX = x
        checkY = y - 1
        while self.inBounds((checkX, checkY)):
            if theBoard[checkX][checkY] == ROOKE + enemyMod or theBoard[checkX][checkY] == QUEEN + enemyMod:
                return True
            if theBoard[checkX][checkY] != EMPTY:
                break
            checkY -= 1

        checkX = x
        checkY = y + 1
        while self.inBounds((checkX, checkY)):
            if theBoard[checkX][checkY] == ROOKE + enemyMod or theBoard[checkX][checkY] == QUEEN + enemyMod:
                return True
            if theBoard[checkX][checkY] != EMPTY:
                break
            checkY += 1

        checkX = x - 1
        checkY = y - 1
        while self.inBounds((checkX, checkY)):
            if theBoard[checkX][checkY] == BISHOP + enemyMod or theBoard[checkX][checkY] == QUEEN + enemyMod:
                return True
            if theBoard[checkX][checkY] != EMPTY:
                break
            checkX -= 1
            checkY -= 1

        checkX = x - 1
        checkY = y + 1
        while self.inBounds((checkX, checkY)):
            if theBoard[checkX][checkY] == BISHOP + enemyMod or theBoard[checkX][checkY] == QUEEN + enemyMod:
                return True
            if theBoard[checkX][checkY] != EMPTY:
                break
            checkX -= 1
            checkY += 1

        checkX = x + 1
        checkY = y - 1
        while self.inBounds((checkX, checkY)):
            if theBoard[checkX][checkY] == BISHOP + enemyMod or theBoard[checkX][checkY] == QUEEN + enemyMod:
                return True
            if theBoard[checkX][checkY] != EMPTY:
                break
            checkX += 1
            checkY -= 1

        checkX = x + 1
        checkY = y + 1
        while self.inBounds((checkX, checkY)):
            if theBoard[checkX][checkY] == BISHOP + enemyMod or theBoard[checkX][checkY] == QUEEN + enemyMod:
                return True
            if theBoard[checkX][checkY] != EMPTY:
                break
            checkX += 1
            checkY += 1

        checkX = x - 1
        checkY = y - 1
        for i in range(0, 3):
            for j in range(0, 3):
                if checkX + i == x and checkY + j == y:
                    continue
                if self.inBounds((checkX + i, checkY + j)):
                    if theBoard[checkX + i][checkY + j] == KING + enemyMod:
                        return True

        return False

    def wouldCheck(self, x, y, nx, ny, white):
        tempSquares = []
        for i in range(0, 8):
            tempSquares.append([])
            for j in range(0, 8):
                tempSquares[i].append(EMPTY)
        for i in range(0, 8):
            for j in range(0, 8):
                tempSquares[i][j] = self.squares[i][j]
        if tempSquares[x][y] == KING or tempSquares[x][y] == KING + 6:
            if abs(x - nx) == 2:
                rookeOldX = 0
                if nx - x > 0:
                    rookeOldX = 7
                tempSquares[x + int((nx - x) / 2)][y] = tempSquares[rookeOldX][y]
                tempSquares[rookeOldX][y] = EMPTY
        tempSquares[nx][ny] = tempSquares[x][y]
        tempSquares[x][y] = EMPTY

        return self.inCheck(tempSquares, white)

    def isMate(self, white):
        for i in range(0, 8):
            for j in range(0, 8):
                if self.isAlly(i, j, white):
                    moves = self.getPotentialMoves(i, j)
                    if len(moves) > 0:
                        return False
        return True

    def move(self, x, y, nx, ny):
        self.enPassant = [-1, -1]
        if self.squares[x][y] == PAWN or self.squares[x][y] == PAWN + 6:
            if abs(y - ny) == 2:
                self.enPassant = [nx, ny]
            elif abs(x - nx) == 1 and not self.squareOccupied(nx, ny):
                self.squares[nx][y] = EMPTY
        elif self.squares[x][y] == ROOKE or self.squares[x][y] == ROOKE + 6:
            color = 0
            if self.squares[x][y] == ROOKE + 6:
                color = 1
            self.canCastle[color][int(x / 7)] = False
        elif self.squares[x][y] == KING or self.squares[x][y] == KING + 6:
            color = 0
            if self.squares[x][y] == KING + 6:
                color = 1
            self.canCastle[color][0] = False
            self.canCastle[color][1] = False
            if abs(x - nx) == 2:
                rookeOldX = 0
                if nx - x > 0:
                    rookeOldX = 7
                self.squares[x + int((nx - x) / 2)][y] = self.squares[rookeOldX][y]
                self.squares[rookeOldX][y] = EMPTY
        self.squares[nx][ny] = self.squares[x][y]
        self.squares[x][y] = EMPTY
        if self.squares[nx][ny] == PAWN and ny == 7:
            self.squares[nx][ny] = QUEEN
        elif self.squares[nx][ny] == PAWN + 6 and ny == 0:
            self.squares[nx][ny] = QUEEN + 6

    def fakeMove(self, x, y, nx, ny):
        entry = []
        entry.append((x, y, self.squares[x][y]))
        entry.append((nx, ny, self.squares[nx][ny]))
        if abs(x - nx) == 2 and (self.squares[x][y] == KING or self.squares[x][y] == KING + 6):
            rookeOldX = 0
            direction = -1
            if nx - x > 0:
                rookeOldX = 7
                direction = 1
            entry.append((rookeOldX, y, self.squares[rookeOldX][y]))
            entry.append((x + direction, y, EMPTY))
        elif abs(x - nx) == 1 and (self.squares[x][y] == PAWN or self.squares[x][y] == PAWN + 6):
            entry.append((nx, y, self.squares[nx][y]))
        entry.append((self.enPassant[0], self.enPassant[1]))
        entry.append((self.canCastle[0][0], self.canCastle[0][1], self.canCastle[1][0], self.canCastle[1][1]))
        self.fakeMoveStack.append(entry)

        self.move(x, y, nx, ny)

    def undoFakeMove(self):
        entry = self.fakeMoveStack.pop()
        for undo in entry:
            if len(undo) == 2:
                self.enPassant[0] = undo[0]
                self.enPassant[1] = undo[1]
            elif len(undo) == 3:
                self.squares[undo[0]][undo[1]] = undo[2]
            elif len(undo) == 4:
                self.canCastle[0][0] = undo[0]
                self.canCastle[0][1] = undo[1]
                self.canCastle[1][0] = undo[2]
                self.canCastle[1][1] = undo[3]

    def click(self, x, y):
        if self.gameover:
            return
        if self.isAlly(x, y, self.turn):
            self.potentialMoves = self.getPotentialMoves(x, y)
            self.pieceToMove = (x, y)
        else:
            for move in self.potentialMoves:
                if move == (x, y):
                    self.printMove(self.pieceToMove, [x, y], True)
                    self.move(self.pieceToMove[0], self.pieceToMove[1], x, y)
                    self.turn = not self.turn
                    self.turnCount += 1
                    if self.inCheck(self.squares, self.turn) and self.isMate(self.turn):
                        print("Checkmate")
                        self.gameover = True
                    elif self.isMate(self.turn) and not self.inCheck(self.squares, self.turn):
                        print("Stalemate")
                        self.gameover = True
                    break
            self.potentialMoves = []

    def blackMove(self):
        if self.gameover:
            return
        if self.turn == False:
            bestMove = self.chooseMove(False, self.depth)
            if bestMove[0] != -1:
                self.printMove([bestMove[0], bestMove[1]], [bestMove[2], bestMove[3]], False)
                self.move(bestMove[0], bestMove[1], bestMove[2], bestMove[3])
            else:
                print("ERROR received invalid best move for black player despite no gameover")
            self.turn = not self.turn
            self.turnCount += 1
        if self.inCheck(self.squares, self.turn) and self.isMate(self.turn):
            print("Checkmate")
            self.gameover = True
        elif self.isMate(self.turn) and not self.inCheck(self.squares, self.turn):
            print("Stalemate")
            self.gameover = True

    def chooseMove(self, white, depth):
        pieces = []
        moves = []
        scores = []
        best = []
        for i in range(0, 8):
            for j in range(0, 8):
                if self.isAlly(i, j, white):
                    potMoves = self.getPotentialMoves(i, j)
                    for move in potMoves:
                        pieces.append((i, j))
                        moves.append(move)
                        scores.append(0)
        lowScore = 10000000000000000
        highScore = -10000
        for i in range(0, len(pieces)):
            scores[i] = self.considerMove(pieces[i], moves[i], white, depth)
            if scores[i] > highScore:
                highScore = scores[i]
            if scores[i] < lowScore:
                lowScore = scores[i]
        if self.verbose:
            print("Done considering moves, score range: " + str(lowScore) + " - " + str(highScore))

        bestMoves = []
        for i in range(0, len(pieces)):
            if scores[i] == highScore:
                bestMoves.append((pieces[i][0], pieces[i][1], moves[i][0], moves[i][1]))

        if len(bestMoves) == 0:
            return (-1, -1, -1, -1)
        return random.choice(bestMoves)

    def considerMove(self, piece, move, white, depth):
        if self.verbose:
            player = "black"
            if white:
                player = "white"
            print("considering move @depth=" + str(depth) + ": " + player + " " + self.strFromPiece(self.squares[piece[0]][piece[1]]) + " to " + self.strFromCoords(move[0], move[1]))
        self.fakeMove(piece[0], piece[1], move[0], move[1])
        score = 0

        if depth == 1:
            score = self.quantify(white)
        else:
            whiteMove = self.chooseMove(not white, 1)
            self.fakeMove(whiteMove[0], whiteMove[1], whiteMove[2], whiteMove[3])
            highScore = -100
            for i in range(0, 8):
                for j in range(0, 8):
                    if self.isAlly(i, j, white):
                        potMoves = self.getPotentialMoves(i, j)
                        for pMove in potMoves:
                            theScore = self.considerMove((i, j), pMove, white, depth - 1)
                            if theScore > highScore:
                                highScore = theScore
            score = highScore
            self.undoFakeMove()

        self.undoFakeMove()
        return score

    def quantify(self, white):

        if self.isMate(not white):
            return 1000000

        score = 0
        score += self.getPieceScore(white)
        score += (3900 - self.getPieceScore(not white))
        selfControlled = self.getSquaresControlled(white)
        enemyControlled = self.getSquaresControlled(not white)

        threatenedPieces = []
        for piece in enemyControlled:
            piecePos = piece[0]
            for square in piece[1:]:
                if self.isAlly(square[0], square[1], white):
                    threatenedPieces.append((piecePos[0], piecePos[1], square[0], square[1]))
                    i = square[0]
                    j = square[1]
                    if self.squares[i][j] == PAWN or self.squares[i][j] == PAWN + 6:
                        score -= 100
                    if self.squares[i][j] == KNIGHT or self.squares[i][j] == KNIGHT + 6:
                        score -= 300
                    if self.squares[i][j] == ROOKE or self.squares[i][j] == ROOKE + 6:
                        score -= 500
                    if self.squares[i][j] == BISHOP or self.squares[i][j] == BISHOP + 6:
                        score -= 300
                    if self.squares[i][j] == QUEEN or self.squares[i][j] == QUEEN + 6:
                        score -= 900

        for piece in selfControlled:
            piecePos = piece[0]
            for square in piece[1:]:
                controlScore = 0
                controlScore += 20
                if self.turnCount < 15:
                    if (white and square[1] < 6) or (white and square[1] > 1):
                        controlScore += 20
                        if square[0] > 2 and square[0] < 6:
                            controlScore += 20
                if controlScore >= 300:
                    controlScore = 300
                score += controlScore
                if self.isAlly(square[0], square[1], white):
                    isThreatened = (-1, -1)
                    for tp in threatenedPieces:
                        if tp[2] == square[0] and tp[3] == square[1]:
                            isThreatened = (tp[0], tp[1])
                            break
                    colorMod = -6
                    if white:
                        colorMod = 6
                    if isThreatened[0] != -1 and self.squares[isThreatened[0]][isThreatened[1]] + colorMod >= self.squares[square[0]][square[1]]:
                        i = square[0]
                        j = square[1]
                        if self.squares[i][j] == PAWN or self.squares[i][j] == PAWN + 6:
                            score += 100
                        if self.squares[i][j] == KNIGHT or self.squares[i][j] == KNIGHT + 6:
                            score += 300
                        if self.squares[i][j] == ROOKE or self.squares[i][j] == ROOKE + 6:
                            score += 500
                        if self.squares[i][j] == BISHOP or self.squares[i][j] == BISHOP + 6:
                            score += 300
                        if self.squares[i][j] == QUEEN or self.squares[i][j] == QUEEN + 6:
                            score += 900
                if self.isAlly(square[0], square[1], white):
                        i = square[0]
                        j = square[1]
                        if self.squares[i][j] == PAWN or self.squares[i][j] == PAWN + 6:
                            score += 50
                        if self.squares[i][j] == KNIGHT or self.squares[i][j] == KNIGHT + 6:
                            score += 150
                        if self.squares[i][j] == ROOKE or self.squares[i][j] == ROOKE + 6:
                            score += 250
                        if self.squares[i][j] == BISHOP or self.squares[i][j] == BISHOP + 6:
                            score += 150
                        if self.squares[i][j] == QUEEN or self.squares[i][j] == QUEEN + 6:
                            score += 450
                        if self.squares[i][j] == KING or self.squares[i][j] == KING + 6:
                            score = 500

        return score

    def getSquaresControlled(self, white):
        controlled = []
        index = -1
        for i in range(0, 8):
            for j in range(0, 8):
                if self.isAlly(i, j, white):
                    controlled.append([])
                    index += 1
                    controlled[index].append((i, j))
                    moves = self.getPotentialMoves(i, j)
                    for move in moves:
                        if self.squares[i][j] == PAWN or self.squares[i][j] == PAWN + 6:
                            if move[0] == i:
                                continue
                        if self.squares[i][j] == KING or self.squares[i][j] == KING + 6:
                            if abs(move[0] - i) == 2:
                                continue
                        controlled[index].append(move)

        return controlled

    def getPieceScore(self, white):
        score = 0
        for i in range(0, 8):
            for j in range(0, 8):
                if self.isAlly(i, j, white):
                    if self.squares[i][j] == PAWN or self.squares[i][j] == PAWN + 6:
                        score += 1
                    if self.squares[i][j] == KNIGHT or self.squares[i][j] == KNIGHT + 6:
                        score += 3
                    if self.squares[i][j] == ROOKE or self.squares[i][j] == ROOKE + 6:
                        score += 5
                    if self.squares[i][j] == BISHOP or self.squares[i][j] == BISHOP + 6:
                        score += 3
                    if self.squares[i][j] == QUEEN or self.squares[i][j] == QUEEN + 6:
                        score += 9
        return score
