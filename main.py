import pygame, sys
from pygame.locals import *
from random import randint
from objects import snake, apple

pygame.init()


def draw_snake():
    for piece in s.pieces:
        pygame.draw.rect(
            screen, (255, 255, 255), pygame.Rect(piece.pos, (piece_size, piece_size))
        )
        pygame.draw.rect(
            screen, (0, 0, 0), pygame.Rect(piece.pos, (piece_size, piece_size)), 1
        )


def draw_apple():
    pygame.draw.rect(screen, (200, 0, 0), pygame.Rect(a.pos, (piece_size, piece_size)))
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(a.pos, (piece_size, piece_size)), 1)


def generate_apple():
    pos = None
    while True:
        pos = (
            randint(0, w // piece_size - 1) * piece_size,
            randint(0, h // piece_size - 1) * piece_size,
        )
        valid = True
        for piece in s.pieces:
            if piece.pos == pos:
                valid = False

        if valid:
            break

    return apple(pos)


def gameover():
    font = pygame.font.Font(None, 72)
    text = font.render("GAME OVER", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (w // 2, h // 2)
    screen.blit(text, text_rect)


w, h = 750, 750
screen = pygame.display.set_mode((w, h))
piece_size = w / 20
s = snake(w, h, piece_size)
a = generate_apple()

dir = "r"

screen.fill([64, 64, 64])
draw_snake()
draw_apple()
pygame.display.update()


while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_SPACE:
            break
    else:
        continue
    break

while True:
    lastdir = dir
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_LEFT and lastdir != "r":
                dir = "l"
            elif event.key == K_RIGHT and lastdir != "l":
                dir = "r"
            elif event.key == K_DOWN and lastdir != "u":
                dir = "d"
            elif event.key == K_UP and lastdir != "d":
                dir = "u"
            elif event.key == K_ESCAPE:
                sys.exit()
    if s.alive:
        eaten = s.move(dir, a)
        if eaten:
            a = generate_apple()
        screen.fill([64, 64, 64])
        draw_snake()
        draw_apple()
    else:
        gameover()

    pygame.display.update()
    pygame.time.wait(100)
