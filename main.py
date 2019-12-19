import pygame, sys
from sys import argv
from pygame.locals import *
from random import randint
from objects import snake, apple


def main():
    pygame.init()
    global screen, w, h, pieces, piece_size

    if "-h" in argv or "--help" in argv:
        print_help()
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

    player_game()


def player_game():
    global s, a, direction, paused
    s = snake(pieces, h / piece_size)
    a = generate_apple(s)

    direction = "r"

    draw(s, a)

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
        handle_key()
        if not paused:
            if s.alive:
                eaten = s.move(direction, a)
                if eaten:
                    a = generate_apple(s)
                draw(s, a)
            else:
                gameover()
            pygame.display.update()
        pygame.time.delay(100)


def handle_key():
    global s, a, direction, paused
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


def print_help():
    print(f"Usage: {argv[0]} [options]")
    print()
    print("-h   --help          Show this help")
    print(
        "--height [height]    Set display height (default 600) (does nothing in fulscreen mode)"
    )
    print(
        "--width [width]      Set display width (default 600) (does nothing in fulscreen mode)"
    )
    print("--pieces             Set no. of pieces in width (default 20)")
    print("-f   --fullscreen    Start game in fullscreen mode")
    print("--ai                 AI player")


def draw(s: snake, a: apple):
    draw_background()
    draw_snake(s)
    draw_apple(a)
    pygame.display.update()


def draw_snake(s: snake):
    snake_color = (47, 139, 211)
    border_color = (0, 0, 0)
    snake_pieces = list(s.pieces)
    for i, piece in enumerate(snake_pieces):
        pygame.draw.rect(
            screen,
            snake_color,
            pygame.Rect(
                (piece.pos[0] * piece_size, piece.pos[1] * piece_size),
                (piece_size, piece_size),
            ),
        )
        next_pos = snake_pieces[i + 1].pos if i + 1 < len(snake_pieces) else (-1, -1)
        prev_pos = snake_pieces[i - 1].pos if i > 0 else (-1, -1)

        if next_pos[0] != piece.pos[0] - 1 and prev_pos[0] != piece.pos[0] - 1:
            draw_border(piece, "l", border_color)

        if next_pos[0] != piece.pos[0] + 1 and prev_pos[0] != piece.pos[0] + 1:
            draw_border(piece, "r", border_color)

        if next_pos[1] != piece.pos[1] - 1 and prev_pos[1] != piece.pos[1] - 1:
            draw_border(piece, "u", border_color)

        if next_pos[1] != piece.pos[1] + 1 and prev_pos[1] != piece.pos[1] + 1:
            draw_border(piece, "d", border_color)


def draw_border(piece, dir, border_color):
    if dir == "l":
        pos = (piece.pos[0] * piece_size, piece.pos[1] * piece_size)
        size = (1, piece_size)
    elif dir == "u":
        pos = (piece.pos[0] * piece_size, piece.pos[1] * piece_size)
        size = (piece_size, 1)
    elif dir == "r":
        pos = (piece.pos[0] * piece_size + piece_size - 1, piece.pos[1] * piece_size)
        size = (1, piece_size)
    elif dir == "d":
        pos = (piece.pos[0] * piece_size, piece.pos[1] * piece_size + piece_size - 1)
        size = (piece_size, 1)
    pygame.draw.rect(screen, border_color, pygame.Rect(pos, size))


def draw_apple(a: apple):
    pygame.draw.rect(
        screen,
        (226, 64, 50),
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


def draw_background():
    for y in range(0, h // piece_size):
        for x in range(0, w // piece_size):
            col = (31, 41, 54) if (x + y) % 2 == 0 else (38, 52, 69)
            pygame.draw.rect(
                screen,
                col,
                pygame.Rect((x * piece_size, y * piece_size), (piece_size, piece_size)),
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

