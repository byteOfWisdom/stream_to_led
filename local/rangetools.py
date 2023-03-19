def xy_range(x, y):
    for n in range(x):
        for m in range(y):
            yield n, m


def xy_list(x, y, value):
    return [[value for _ in range(x)] for _ in range(y)]