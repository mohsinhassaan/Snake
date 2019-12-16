from collections import deque


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

        for piece in self.pieces:
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
