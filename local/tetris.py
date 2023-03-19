import frame_sender
import curses
import rangetools
import random
import time
import numpy as np

width = 12
height = 16
OUTLINE = (255, 0, 0)
DIMX = 16
DIMY = 16

rot = 0

def main():
    global rot
    frame_sender.ready_conn("PicoW")
    stdscr = curses.initscr()
    curses.noecho()
    stdscr.keypad(True)
    stdscr.nodelay(True)

    pos = 7

    while True:
        try:
            k = stdscr.getkey()
            if k == "a": pos -= 1
            if k == "d": pos += 1

            if k == "z": rot += 1
            if k == "x": rot -= 1

            if k == "q": 
                curses.endwin()
                break
        except:
            pass

        game_tick()


def xy_to_index(x, y):
    if x >= DIMX or y >= DIMY: return
    if x < 0 or y < 0: return
    index = ((y * 16) + (16 - x) - 1)
    if y % 2:
        index = (y * 16) + x
    return index


bar_piece = np.array([
    [0, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 0, 0]
])

l_piece = np.array([
    [0, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 0, 0]
])

z_piece = np.array([
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 0]
])

z_piece_m = np.array([
    [0, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 0]
])

block_piece = np.array([
    [0, 0, 0, 0],
    [0, 1, 1, 0],
    [0, 1, 1, 0],
    [0, 0, 0, 0]
])


base_pieces = [bar_piece, l_piece, z_piece, z_piece_m, block_piece]


class Piece:
    def __init__(self, kind):
        self.rotation = 0
        self.parts = base_pieces[kind]


    def rotate(self, rotation):
        while rotation < 0: rotation += 4

        for _ in range(rotation):
            self.parts = np.swapaxes(self.parts, 0, 1)


    def get_origin(self):
        average_x = 0
        average_y = 0
        for x in range(4):
            for y in range(4):
                if self.parts[x][y]:
                    average_x += x
                    average_y += y
        return round(average_x / 4), round(average_y / 4)


    def get_parts(self):
        ox, oy = self.get_origin()
        res = []
        for x, y in rangetools.xy_range(4, 4):
            if self.parts[x][y]:
                res.append((x - ox, y - oy))
        return res


class Tetris:
    def __init__(self):
        self.blocks = rangetools.xy_list(width, height, 0)
        self.active_piece = None
        self.piece_pos_x = 6
        self.piece_pos_y = 2


    def spawn_piece(self):
        piece_num = random.randint(0, 4)
        self.active_piece = Piece(piece_num)        


    def draw_board(self):
        board = [0 for _ in rangetools.xy_range(16, 16)]
        for x, y in rangetools.xy_range(3, 16):
            board[xy_to_index(x, y)] = frame_sender.rgb_to_value(*OUTLINE)
            board[xy_to_index(x + 13, y)] = frame_sender.rgb_to_value(*OUTLINE)

        if self.active_piece:
            piece_color = frame_sender.rgb_to_value(0, 0, 255)
            for x, y in self.active_piece.get_parts():
                index = xy_to_index(x + self.piece_pos_x, y + self.piece_pos_y)
                board[index] = piece_color

        return board


game = Tetris()

def game_tick():
    global rot
    if not game.active_piece:
        game.spawn_piece()

    game.active_piece.rotate(rot)
    rot = 0

    state = game.draw_board()
    frame_sender.send_frame(state)
    time.sleep(1 / 30)


if __name__ == '__main__':
    main()