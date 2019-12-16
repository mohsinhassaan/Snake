from collections import deque
from typing import Deque, Tuple


class apple(object):
    def __init__(self, pos):
        self.pos: Tuple[int, int] = pos


class snake(object):
    def __init__(self, w: int, h: int):
        self.width: int = w
        self.height: int = h
        self.pieces: Deque[snake.__snake_bit] = deque([snake.__snake_bit((0, 0))])
        self.alive: bool = True

    def move(self, dir: str, ap: apple):
        head: snake.__snake_bit = self.pieces[-1]

        if dir == "r":
            pos: Tuple[int, int] = (head.pos[0] + 1, head.pos[1])
        elif dir == "l":
            pos: Tuple[int, int] = (head.pos[0] - 1, head.pos[1])
        elif dir == "u":
            pos: Tuple[int, int] = (head.pos[0], head.pos[1] - 1)
        elif dir == "d":
            pos: Tuple[int, int] = (head.pos[0], head.pos[1] + 1)

        pos: Tuple[int, int] = self.__wall_collision(pos)

        eating: bool = True if pos == ap.pos else False

        if self.__valid_pos(pos, eating):
            if eating:
                self.pieces.append(snake.__snake_bit(pos))
                return True
            else:
                self.pieces.popleft()
                self.pieces.append(snake.__snake_bit(pos))
                return False
        else:
            self.alive: bool = False

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

    def __valid_pos(self, pos: Tuple[int, int], eating: bool):
        for piece in self.pieces:
            if piece.pos == pos:
                return False
        return True

    class __snake_bit(object):
        def __init__(self, pos: Tuple[int, int]):
            self.pos: Tuple[int, int] = pos

        def __str__(self):
            return str(self.pos)
