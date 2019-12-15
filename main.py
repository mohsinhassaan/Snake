import pygame, sys
from sys import argv
from pygame.locals import *
from random import randint
from collections import deque
from itertools import islice


def main():
    global screen, w, h, pieces, piece_size

    if "-h" in argv or "--help" in argv:
        print(f"Usage: {argv[0]} [options]")
        print("-h   --help          Show this help")
        print(
            "--height [height]    Set display height (default 600) (does nothing in fulscreen mode)"
        )
        print(
            "--width [width]      Set display width (default 600) (does nothing in fulscreen mode)"
        )
        print("--pieces             Set no. of pieces in width (default 20)")
        print("-f   --fullscreen    Start game in fullscreen mode")
        sys.exit()

    if "--pieces" in argv:
        pieces = int(argv[argv.index("--pieces") + 1])
    else:
        pieces = 20

    if "--width" in argv:
        w = int(argv[argv.index("--width") + 1])
        w = w - (w % pieces)
    else:
        w = 700

    if "--height" in argv:
        h = int(argv[argv.index("--height") + 1])
        h = h - (h % pieces)
    else:
        h = 700

    if "-f" in argv or "--fullscreen" in argv:
        info_object = pygame.display.Info()
        piece_size = info_object.current_w // pieces
        screen = pygame.display.set_mode(
            (
                info_object.current_w - (info_object.current_w % piece_size),
                info_object.current_h - (info_object.current_h % piece_size),
            ),
            pygame.FULLSCREEN,
        )
        w, h = screen.get_size()
    else:
        screen = pygame.display.set_mode((w, h))
        piece_size = w // pieces

    s = snake(pieces, h / piece_size)
    a = generate_apple(s)

    print(f"w = {s.width}, h = {s.height}")

    direction = "r"

    screen.fill([64, 64, 64])
    draw_snake(s)
    draw_apple(a)
    pygame.display.update()
    print(",".join(map(str, s.pieces)))

    paused = False

    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    break
                elif event.key == K_ESCAPE:
                    sys.exit()
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
                print(",".join(map(str, s.pieces)))
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
    def __init__(self, w: int, h: int):
        self.width = w
        self.height = h
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

        pos = self.__wall_collision(pos)

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
            return pos

    def __valid_pos(self, pos: tuple, eating: bool):
        start = 1 if eating else 0

        for piece in islice(self.pieces, start, len(self.pieces)):
            if piece.pos == pos:
                return False
        return True


class snake_bit(object):
    def __init__(self, pos):
        self.pos = pos

    def __str__(self):
        return str(self.pos)


class apple(object):
    def __init__(self, pos):
        self.pos = pos


pygame.init()


def draw_snake(s: snake):
    snake_color = (255, 255, 255) if s.alive else (0, 0, 200)
    for piece in s.pieces:
        pygame.draw.rect(
            screen,
            snake_color,
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

