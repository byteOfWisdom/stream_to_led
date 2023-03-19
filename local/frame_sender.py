import socket

transmitter = None
addr = None

R_SHIFT = 16
G_SHIFT = 24
B_SHIFT = 8

# 0xff = 8bits all 1
R_MASK = 0xff << R_SHIFT
G_MASK = 0xff << G_SHIFT
B_MASK = 0xff << B_SHIFT

LED_NUM = 256


def ready_conn(board):
    global transmitter
    global addr
    transmitter = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = (board, 4242)
    return transmitter, addr


def rgb_to_value(r, g, b):
    return (r << R_SHIFT) | (g << G_SHIFT) | (b << B_SHIFT)


def value_to_rgb(value):
    r = (R_MASK & value) >> R_SHIFT
    g = (G_MASK & value) >> G_SHIFT
    b = (B_MASK & value) >> B_SHIFT
    return (r, g, b)


def encode_scalar_frame(frame):
    res = []
    for i in range(LED_NUM):
        r, g, b = value_to_rgb(frame[i])
        r = r.to_bytes(1, 'little')
        g = g.to_bytes(1, 'little')
        b = b.to_bytes(1, 'little')
        res.append(r)
        res.append(g)
        res.append(b)
    return b''.join(res)[:3 * LED_NUM]


def send_frame(frame):
    global transmitter
    msg = encode_scalar_frame(frame)
    transmitter.sendto(msg, addr)
    reply, _ = transmitter.recvfrom(2)
    if reply: return True
    else: return False