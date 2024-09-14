from pwn import *
import subprocess


def handle_pow(r):
    r.recvuntil(b"python3 ")
    r.recvuntil(b" solve ")
    challenge = r.recvline().decode("ascii").strip()
    log.info(f"POW: {challenge}")
    result = subprocess.run(
        [
            "bash",
            "-c",
            f"python3 <(curl -sSL https://goo.gle/kctf-pow) solve {challenge}",
        ],
        capture_output=True,
        text=True,
    )
    solution = result.stdout.strip().encode()
    r.sendline(solution)
    r.recvuntil(b"Correct\n")


def main():
    r = remote("quantum.challs.csc.tf", 1337)
    r.recvuntil(b"== proof-of-work: ")
    if r.recvline().startswith(b"enabled"):
        handle_pow(r)


    n = int(r.recvline().decode().strip())
    print(n)

    r.recvuntil(b"Ask me anything?\n")

    global q
    q = 0

    def ask(xs, ys):
        m = len(xs)
        assert len(ys) == m

        r.sendline(str(m).encode())
        r.sendline(" ".join([str(x) for x in xs]).encode())
        r.sendline(" ".join([str(y) for y in ys]).encode())

        global q
        q += m
        print(q)

        return list(map(int, r.recvline().decode().strip().split()))

    value_x = [-1] * n
    value_y = [-1] * n
    v00 = ask([0], [0])[0]
    value_x[0], value_y[0] = v00, v00

    def colinear(p, q, r):
        return (q[1] - p[1]) * (r[0] - q[0]) == (r[1] - q[1]) * (q[0] - p[0])

    for bit in range(len(bin(n)[2:]) - 1, -1, -1):
        jump = 1 << bit
        xs, ys = [], []
        for i in range(0, n, jump):
            if value_x[i] == -1:
                xs.append(i)
                ys.append(0)
        resp = ask(xs, ys)
        index = 0
        for i in range(0, n, jump):
            if value_x[i] == -1:
                value_x[i] = resp[index]
                index += 1
        if bit == 0:
            break
        for i in range(jump, n - jump, jump):
            if colinear(
                (i - jump, value_x[i - jump]),
                (i, value_x[i]),
                (i + jump, value_x[i + jump]),
            ):
                for j in range(i - jump + 1, i + jump):
                    value_x[j] = value_x[i - jump] * ((i + jump) - j) + value_x[
                        i + jump
                    ] * (j - (i - jump))
                    assert value_x[j] % (2 * jump) == 0
                    value_x[j] //= 2 * jump

    for bit in range(len(bin(n)[2:]) - 1, -1, -1):
        jump = 1 << bit
        xs, ys = [], []
        for i in range(0, n, jump):
            if value_y[i] == -1:
                xs.append(0)
                ys.append(i)
        resp = ask(xs, ys)
        index = 0
        for i in range(0, n, jump):
            if value_y[i] == -1:
                value_y[i] = resp[index]
                index += 1
        if bit == 0:
            break
        for i in range(jump, n - jump, jump):
            if colinear(
                (i - jump, value_y[i - jump]),
                (i, value_y[i]),
                (i + jump, value_y[i + jump]),
            ):
                for j in range(i - jump + 1, i + jump):
                    value_y[j] = value_y[i - jump] * ((i + jump) - j) + value_y[
                        i + jump
                    ] * (j - (i - jump))
                    assert value_y[j] % (2 * jump) == 0
                    value_y[j] //= 2 * jump

    r.sendline(b"-1")

    q_used = q

    print(f"Used query: {q_used}, n: {n}, ratio: {q_used / n}, dif: {2 * n - q_used}")

    pref_x = [0] * (n + 1)
    pref_y = [0] * (n + 1)
    for i in range(0, n):
        assert min(value_x[i], value_y[i]) >= 0
        pref_x[i + 1] = pref_x[i] + value_x[i]
        pref_y[i + 1] = pref_y[i] + value_y[i]

    print(r.recvline())

    qn = int(r.recvline().decode().strip())
    res = [-1] * qn
    for qi in range(qn):
        x0, y0, x1, y1 = map(int, r.recvline().decode().strip().split())
        x1, y1 = x1 + 1, y1 + 1
        res[qi] = (
            (pref_x[x1] - pref_x[x0]) * (y1 - y0)
            + (x1 - x0) * (pref_y[y1] - pref_y[y0])
            - (x1 - x0) * (y1 - y0) * v00
        )

    print(r.recvuntil(b"Your answer? "))
    r.sendline(" ".join([str(x) for x in res]).encode())

    print(r.recvline())

    print(r.recvline())


if __name__ == "__main__":
    while True:
        try:
            main()
            break
        except:
            continue
