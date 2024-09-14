FLAG = "CSCTF{you_should_learn_how_to_binary_search_before_segment_tree}"

import random, bisect


def gen(mn, mx):
    n = random.randint(mn, mx)
    global p
    p = [0] * n
    for i in range(n):
        p[i] = (random.randint(1, n - 1), random.randint(1, n - 1))

    # Preprocess ask
    global sort_x, sort_y, px, py
    sort_x = [0] * n
    px = [0] * n
    sort_y = [0] * n
    py = [0] * n

    for i in range(n):
        sort_x[i] = p[i][0]
        sort_y[i] = p[i][1]

    sort_x.sort()
    sort_y.sort()
    for i in range(n):
        px[i] = px[i - 1] + sort_x[i]
    for i in range(n):
        py[i] = py[i - 1] + sort_y[i]

    # Preprocess query
    global Sx, Sy, S0, pSx, pSy
    Sx = [0] * n
    pSx = [0] * n
    Sy = [0] * n
    pSy = [0] * n

    def S(x0, y0):
        i = bisect.bisect_left(sort_x, x0)
        j = bisect.bisect_left(sort_y, y0)
        sum_x = (x0 * i - (px[i - 1] if i else 0)) + (
            px[n - 1] - (px[i - 1] if i else 0) - x0 * (n - i)
        )
        sum_y = (y0 * j - (py[j - 1] if j else 0)) + (
            py[n - 1] - (py[j - 1] if j else 0) - y0 * (n - j)
        )
        return sum_x + sum_y

    for i in range(n):
        Sx[i] = S(i, 0)
        pSx[i] = pSx[i - 1] + Sx[i]
        Sy[i] = S(0, i)
        pSy[i] = pSy[i - 1] + Sy[i]

    S0 = S(0, 0)

    return p


def ask(x0, y0):
    return Sx[x0] + Sy[y0] - S0


def query(x0, y0, x1, y1):
    return (
        (pSx[x1] - pSx[x0 - 1]) * (y1 - y0 + 1)
        + (x1 - x0 + 1) * (pSy[y1] - pSy[y0 - 1])
        - (x1 - x0 + 1) * (y1 - y0 + 1) * S0
    )


# S(x0, y0) = Σ_(x, y) ∈ P {|x - x0| + |y - y0|}
# S(x0, y0) = sum_x += |x - x0|; sum_y += |y - y0|
# S(x0, 0): sum += |x - x0| + |y|
# S(0, y0): sum += |x| + |y - y0|
# S(0, 0): sum += |x| + |y|
# -> S(x, y) = S(x, 0) + S(0, y) - S(0, 0)
