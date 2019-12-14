import pygame, sys
from sys import argv
from pygame.locals import *
from random import randint
from collections import deque


def main():
    if len(argv) > 4 or len(argv) == 2 and (argv[1] == "--help" or argv[1] == "-h"):
        print(f"Usage: {argv[0]} [width] [height] [pieces]")

    global screen, w, h, pieces, piece_size

    w, h = (int(argv[1]), int(argv[2])) if len(argv) >= 3 else (700, 700)
    pieces = int(argv[3]) if len(argv) == 4 else 20
    screen = pygame.display.set_mode((w, h))
    piece_size = w / pieces
    s = snake(pieces, int((pieces / w) * h))
    a = generate_apple(s)

    direction = "r"

    screen.fill([64, 64, 64])
    draw_snake(s)
    draw_apple(a)
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
                if not paused:
                    if event.key == K_LEFT and lastdir != "r":
                        direction = "l"
                    elif event.key == K_RIGHT and lastdir != "l":
                        direction = "r"
                    elif event.key == K_DOWN and lastdir != "u":
                        direction = "d"
                    elif event.key == K_UP and lastdir != "d":
                        direction = "u"
                if event.key == K_ESCAPE:
                    sys.exit()
                elif event.key == K_r:
                    s = snake(pieces, int((pieces / w) * h))
                    a = generate_apple(s)
                    direction = "r"
                elif event.key == K_p:
                    paused = True if paused == False else False
        if not paused:
            if s.alive:
                eaten = s.move(direction, a)
                if eaten:
                    a = generate_apple(s)
                screen.fill([64, 64, 64])
                draw_snake(s)
                draw_apple(a)
            else:
                gameover()

            pygame.display.update()
        pygame.time.delay(100)


class snake(object):
    def __init__(self, h: int, w: int):
        self.height = h
        self.width = w
        self.pieces = deque([snake_bit((0, 0))])
        self.alive = True

    def move(self, dir, ap):
        head = self.pieces[-1]

        if dir == "r":
            pos = (head.pos[0] + 1, head.pos[1])
        elif dir == "l":
            pos = (head.pos[0] - 1, head.pos[1])
        elif dir == "u":
            pos = (head.pos[0], head.pos[1] - 1)
        elif dir == "d":
            pos = (head.pos[0], head.pos[1] + 1)

        eating = True if pos == ap.pos else False

        if self.__valid_pos(pos, eating):
            collision = self.__wall_collision(pos)
            pos = collision if collision is not None else pos

            if eating:
                self.pieces.append(snake_bit(pos))
                return True
            else:
                self.pieces.popleft()
                self.pieces.append(snake_bit(pos))
                return False
        else:
            self.alive = False

    def __wall_collision(self, pos: tuple):
        if pos[0] < 0:
            return (self.width - 1, pos[1])
        elif pos[0] + 1 > self.width:
            return (0, pos[1])
        elif pos[1] < 0:
            return (pos[0], self.height - 1)
        elif pos[1] + 1 > self.height:
            return (pos[0], 0)
        else:
            return None

    def __valid_pos(self, pos: tuple, eating: bool):
        start = 2 if eating else 1

        for piece in list(self.pieces)[start:]:
            if piece.pos == pos:
                return False
        return True


class snake_bit(object):
    def __init__(self, pos):
        self.pos = pos


class apple(object):
    def __init__(self, pos):
        self.pos = pos


pygame.init()


def draw_snake(s: snake):
    for piece in s.pieces:
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            pygame.Rect(
                (piece.pos[0] * piece_size, piece.pos[1] * piece_size),
                (piece_size, piece_size),
            ),
        )
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            pygame.Rect(
                (piece.pos[0] * piece_size, piece.pos[1] * piece_size),
                (piece_size, piece_size),
            ),
            1,
        )


def draw_apple(a: apple):
    pygame.draw.rect(
        screen,
        (200, 0, 0),
        pygame.Rect(
            (a.pos[0] * piece_size, a.pos[1] * piece_size), (piece_size, piece_size)
        ),
    )
    pygame.draw.rect(
        screen,
        (0, 0, 0),
        pygame.Rect(
            (a.pos[0] * piece_size, a.pos[1] * piece_size), (piece_size, piece_size)
        ),
        1,
    )


def generate_apple(s: snake):
    pos = None
    while True:
        pos = (randint(0, w // piece_size - 1), randint(0, h // piece_size - 1))
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


if __name__ == "__main__":
    main()
