import pygame, sys
from pygame.locals import *
from random import randint
from collections import deque


class snake(object):
    def __init__(self, h: int, w: int, piece_size: int):
        self.height = h
        self.width = w
        self.PIECE_SIZE = piece_size
        self.pieces = deque([snake_bit((0, 0))])
        self.alive = True

    def move(self, dir, ap):
        head = self.pieces[-1]

        if dir == "r":
            pos = (head.pos[0] + self.PIECE_SIZE, head.pos[1])
        elif dir == "l":
            pos = (head.pos[0] - self.PIECE_SIZE, head.pos[1])
        elif dir == "u":
            pos = (head.pos[0], head.pos[1] - self.PIECE_SIZE)
        elif dir == "d":
            pos = (head.pos[0], head.pos[1] + self.PIECE_SIZE)

        eating = True if pos == ap.pos else False

        if self.__valid_pos(pos, eating):
            if eating:
                self.pieces.append(snake_bit(pos))
                return True
            else:
                self.pieces.popleft()
                self.pieces.append(snake_bit(pos))
                return False
        else:
            self.alive = False

    def __valid_pos(self, pos: tuple, eating: bool):
        start = 1 if eating else 0

        for piece in list(self.pieces)[start:]:
            if piece.pos == pos:
                return False

        return (
            True
            if pos[0] >= 0
            and pos[0] + self.PIECE_SIZE <= self.width
            and pos[1] >= 0
            and pos[1] + self.PIECE_SIZE <= self.width
            else False
        )


class snake_bit(object):
    def __init__(self, pos):
        self.pos = pos


class apple(object):
    def __init__(self, pos):
        self.pos = pos


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
    font = pygame.font.Font(None, 60)
    text = font.render("GAME OVER. Press 'r' to restart", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (w // 2, h // 2)
    screen.blit(text, text_rect)


w, h = 800, 800
screen = pygame.display.set_mode((w, h))
piece_size = w / 20
s = snake(w, h, piece_size)
a = generate_apple()

direction = "r"

screen.fill([64, 64, 64])
draw_snake()
draw_apple()
pygame.display.update()

paused = False

while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_SPACE:
            break
    else:
        continue
    break

while True:
    lastdir = direction
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_LEFT and lastdir != "r":
                direction = "l"
            elif event.key == K_RIGHT and lastdir != "l":
                direction = "r"
            elif event.key == K_DOWN and lastdir != "u":
                direction = "d"
            elif event.key == K_UP and lastdir != "d":
                direction = "u"
            elif event.key == K_ESCAPE:
                sys.exit()
            elif event.key == K_r:
                s = snake(h, w, piece_size)
                a = generate_apple()
                direction = "r"
            elif event.key == K_p:
                paused = True if paused == False else False
    if not paused:
        if s.alive:
            eaten = s.move(direction, a)
            if eaten:
                a = generate_apple()
            screen.fill([64, 64, 64])
            draw_snake()
            draw_apple()
        else:
            gameover()

        pygame.display.update()
    pygame.time.wait(100)
