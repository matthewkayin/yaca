import pygame
import sys
from pieces import Board

SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512
FPS = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_TILE = (255, 206, 158)
DARK_TILE = (209, 139, 71)

spritesheet = pygame.image.load("sprites.png")
spritesheet = pygame.transform.scale(spritesheet, (384, 128))

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
board = Board(sys.argv)

def renderPiece(piece):
    subimageY = 0
    if piece[0] == 0:
        subimageY = 64
    screen.blit(spritesheet, (piece[2] * 64, piece[3] * 64), ((6 - piece[1]) * 64, subimageY, 64, 64))

running = True

#game loop
while running:
    clock.tick(FPS)
    screen.fill(BLACK)
    for i in range(0, 8):
        for j in range(0, 8):
            if (i + j) % 2 == 0:
                pygame.draw.rect(screen, LIGHT_TILE, (i * 64, j * 64, 64, 64), False)
            else:
                pygame.draw.rect(screen, DARK_TILE, (i * 64, j * 64, 64, 64), False)
    if len(board.potentialMoves) > 0:
        for move in board.potentialMoves:
            pygame.draw.rect(screen, GREEN, (move[0] * 64, move[1] * 64, 64, 64), False)
    for piece in board.getPieces():
        renderPiece(piece)
    pygame.display.flip()
    board.blackMove()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mousex, mousey = pygame.mouse.get_pos()
            squareX = (mousex - (mousex % 64)) / 64
            squareY = (mousey - (mousey % 64)) / 64
            board.click(int(squareX), int(squareY))

#game over, deinit pygame
pygame.quit()
