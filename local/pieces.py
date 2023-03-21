import numpy as np

t_piece_a = np.array([
    [0, 1, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 0]
])

t_piece_b = np.array([
    [0, 0, 0, 0],
    [1, 1, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 0]
])

t_piece_c = np.array([
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 0]
])

bar_piece_a = np.array([
    [0, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 0, 0]
])

bar_piece_b = np.array([
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [1, 1, 1, 1],
    [0, 0, 0, 0]
])


l_piece_a = np.array([
    [0, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 0, 0]
])

l_piece_b = np.array([
    [0, 0, 0, 0],
    [0, 0, 1, 0],
    [1, 1, 1, 0],
    [0, 0, 0, 0]
])

l_piece_c = np.array([
    [0, 0, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 0]
])

l_piece_d = np.array([
    [0, 0, 0, 0],
    [0, 1, 1, 1],
    [0, 1, 0, 0],
    [0, 0, 0, 0]
])


z_piece_a = np.array([
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 0]
])

z_piece_b = np.array([
    [0, 0, 0, 0],
    [0, 1, 1, 0],
    [1, 1, 0, 0],
    [0, 0, 0, 0]
])


z_piece_m_a = np.array([
    [0, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 0]
])

z_piece_m_b = np.array([
    [0, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 0, 0]
])

block_piece_a = np.array([
    [0, 0, 0, 0],
    [0, 1, 1, 0],
    [0, 1, 1, 0],
    [0, 0, 0, 0]
])

t_piece = [t_piece_a, t_piece_b, t_piece_c, t_piece_a]
bar_piece = [bar_piece_a, bar_piece_b, bar_piece_a, bar_piece_b]
l_piece = [l_piece_a, l_piece_b, l_piece_c, l_piece_d]
z_piece = [z_piece_a, z_piece_b, z_piece_a, z_piece_b]
z_piece_m = [z_piece_m_a, z_piece_m_b, z_piece_m_a, z_piece_m_b]
block_piece = [block_piece_a, block_piece_a, block_piece_a, block_piece_a]

base_pieces = [t_piece, bar_piece, l_piece, z_piece, z_piece_m, block_piece]