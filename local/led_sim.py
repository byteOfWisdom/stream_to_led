import curses
import socket

BLOCK = 'U/2588'

def main():
    stdscr = curses.initscr()
    curses.noecho()
    stdscr.keypad(True)
    stdscr.nodelay(True)

    sock = make_socket()

    while True:
        try:
            k = stdscr.getkey()
            print("got key", k)
            if k == "q":
                curses.endwin()
                return True
        except: pass

        #get data
#        data, _ = sock.recvfrom()

        #draw data
        stdscr.clear()
        for line in range(8):
            line = ''.join([BLOCK for _ in range(16)]) + "\n"
            stdscr.addstr(line)
            stdscr.addstr(line)
        stdscr.refresh()


def make_socket():
    port = 4242
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0.2)
    return s



if __name__ == '__main__':
    main()