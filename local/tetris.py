import curses
import random
import time
import numpy as np

import rangetools
import frame_sender
import pieces


width = 12
height = 16
OUTLINE = (255, 0, 0)
DIMX = 16
DIMY = 16
SPEED = 10
SPAWN_X = 6
SPAWN_Y = 2
BOARD_BOUND_UPPER = 13
BOARD_BOUND_LOWER = 3

rot = 0
delta_pos = 0
drop_count = SPEED


def main():
    global rot
    global pos
    #frame_sender.ready_conn("PicoW")
    frame_sender.ready_conn("localhost")
    stdscr = curses.initscr()
    curses.noecho()
    stdscr.keypad(True)
    stdscr.nodelay(True)


    while True:
        try:
            k = stdscr.getkey()
            if k == "n": delta_pos -= 1
            if k == "m": delta_pos += 1

            if k == "z": rot -= 1
            if k == "x": rot += 1

            if k == "q": 
                curses.endwin()
                break
        except:
            pass

        game_tick()


def xy_to_index(x, y):
    if x >= DIMX or y >= DIMY: return 0
    if x < 0 or y < 0: return 0
    index = ((y * 16) + (16 - x) - 1)
    if y % 2:
        index = (y * 16) + x
    return index


class Piece:
    def __init__(self, kind):
        self.rotation = 0
        self.color = frame_sender.rgb_to_value(255, 0, 0) # todo make this be different
        self.parts = pieces.base_pieces[kind]


    def rotate(self, rotation):
        while rotation < 0: rotation += 4
        self.rotation += rotation
        self.rotation = self.rotation % 4

    def get_origin(self):
        average_x = 0
        average_y = 0
        for x in range(4):
            for y in range(4):
                if self.parts[self.rotation][x][y]:
                    average_x += x
                    average_y += y
        return round(average_x / 4), round(average_y / 4)


    def get_parts(self):
        ox, oy = self.get_origin()
        res = []
        for x, y in rangetools.xy_range(4, 4):
            if self.parts[self.rotation][x][y]:
                res.append((x - ox, y - oy))
        return res


class Tetris:
    def __init__(self):
        self.blocks = rangetools.xy_list(width, height, 0)
        self.active_piece = None
        self.piece_pos_x = SPAWN_X
        self.piece_pos_y = SPAWN_Y


    def spawn_piece(self):
        piece_num = random.randint(0, 4)
        self.active_piece = Piece(piece_num)        


    def draw_board(self):
        board = [0 for _ in rangetools.xy_range(16, 16)]
        for x, y in rangetools.xy_range(BOARD_BOUND_LOWER, 16):
            board[xy_to_index(x, y)] = frame_sender.rgb_to_value(*OUTLINE)
            board[xy_to_index(x + BOARD_BOUND_UPPER, y)] = frame_sender.rgb_to_value(*OUTLINE)

        if self.active_piece:
            piece_color = frame_sender.rgb_to_value(0, 0, 255)
            for x, y in self.active_piece.get_parts():
                index = xy_to_index(x + self.piece_pos_x, y + self.piece_pos_y)
                board[index] = piece_color

        return board


    def try_move_x(self, delta_x):
        new_pos = self.piece_pos_x + delta_x

        # return False if some part of the block is out of the boards bounds
        for part_x, part_y in self.active_piece.get_parts():
            if (new_pos + part_x) > BOARD_BOUND_UPPER or (new_pos + part_x) < BOARD_BOUND_LOWER:
                return False

        #check if some part of the block would be put where there
        #already is a block
            if self.blocks[new_pos + part_x][part_y]:
                return False

        self.piece_pos_x = new_pos
        return True


    def try_move_y(self, delta_y):
        new_pos = self.piece_pos_y + delta_y

        # return False if some part of the block is out of the boards bounds
        for part_x, part_y in self.active_piece.get_parts():
            if (new_pos + part_y) >= DIMY or (new_pos + part_y) < 0:
                return False

        #check if some part of the block would be put where there
        #already is a block
            if self.blocks[part_x][new_pos + part_y]:
                return False

        self.piece_pos_y = new_pos
        return True


    def try_rotate(self, rotation):
        self.active_piece.rotate(rotation)
        for part_x, part_y in self.active_piece.get_parts():
            if self.blocks[self.piece_pos_x + part_x][self.piece_pos_y + part_y]:
                #undo the rotation again
                self.active_piece.rotate(-rotation)
                return False
        return True


    def place_active_piece(self):
        for part_x, part_y in self.active_piece.get_parts():
            x = self.piece_pos_x + part_x
            y = self.piece_pos_y + part_y
            self.blocks[y][x] = piece_color
        self.active_piece = None
        self.piece_pos_y = SPAWN_Y
        self.piece_pos_x = SPAWN_X


    def check_full_lines(self):
        lines_to_clear = []

        #mark full lines
        for line in range(DIMY):
            this_line = True
            for x in range(BOARD_BOUND_LOWER, BOARD_BOUND_UPPER):
                if not self.blocks[x][line]: this_line = False
            if this_line: lines_to_clear.appen(line)

        for full_line in lines_to_clear:
            # make lines disappear
            # slide everything above down
            # points?
            pass



game = Tetris()

def game_tick():
    global rot
    global delta_pos
    global drop_count

    if not game.active_piece:
        game.spawn_piece()

    game.try_rotate(rot)
    rot = 0

    game.try_move_x(delta_pos)
    delta_pos = 0

    if drop_count == 0:
        drop_count = SPEED
        if not game.try_move_y(1):
            game.place_active_piece()
    else:
        drop_count -= 1

    state = game.draw_board()
    frame_sender.send_frame(state)
    time.sleep(1 / 30)





if __name__ == '__main__':
    main()