EMPTY = 0
PAWN = 1
ROOKE = 2
KNIGHT = 3
BISHOP = 4
QUEEN = 5
KING = 6

class Board():
    def __init__(self):
        self.squares = []
        for i in range(0, 8):
            self.squares.append([])
            for j in range(0, 8):
                self.squares[i].append(EMPTY)
        self.enPassant = [-1, -1]
        self.canCastle = [[True, True], [True, True]]
        self.turn = True
        self.pieceToMove = (-1, -1)
        self.potentialMoves = []
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

    def click(self, x, y):
        if self.isAlly(x, y, self.turn):
            self.potentialMoves = self.getPotentialMoves(x, y)
            self.pieceToMove = (x, y)
        else:
            for move in self.potentialMoves:
                if move == (x, y):
                    self.move(self.pieceToMove[0], self.pieceToMove[1], x, y)
                    self.turn = not self.turn
                    break
            self.potentialMoves = []

