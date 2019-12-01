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
