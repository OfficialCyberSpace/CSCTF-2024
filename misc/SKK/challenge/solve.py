import numpy as np
import cv2


enc = cv2.imread('enc.png')
size_x, size_y = enc.shape[:2]


dec = np.zeros_like(enc)
dec[0, 0] = [141, 195, 241]  #initially decrypted pixel

for j in range(1, size_y):
    compare = dec[0, j - 1].astype(int)
    perm = np.zeros((6, 8, 3), dtype=int)
    for row in range(6):
        for bitflip in range(8):
            bit3 = bitflip % 2
            bit2 = (bitflip // 2) % 2
            bit1 = (bitflip // 4) % 2
            for rgb in range(3):
                if [bit1, bit2, bit3][rgb] == 0:
                    perm[row, bitflip, rgb] = enc[0, j, rgb]
                else:
                    perm[row, bitflip, rgb] = enc[0, j, rgb] ^ 255
    diff = np.sum(np.abs(compare - perm), axis=2)
    min_diff = np.min(diff)
    for row in range(6):
        for col in range(8):
            if diff[row, col] == min_diff:
                dec[0, j] = perm[row, col]
                break

for i in range(1, size_x):
    for j in range(size_y):
        compare = dec[i - 1, j].astype(int)
        perm = np.zeros((6, 8, 3), dtype=int)
        for row in range(6):
            for bitflip in range(8):
                bit3 = bitflip % 2
                bit2 = (bitflip // 2) % 2
                bit1 = (bitflip // 4) % 2
                for rgb in range(3):
                    if [bit1, bit2, bit3][rgb] == 0:
                        perm[row, bitflip, rgb] = enc[i, j, rgb]
                    else:
                        perm[row, bitflip, rgb] = enc[i, j, rgb] ^ 255
        diff = np.sum(np.abs(compare - perm), axis=2)
        min_diff = np.min(diff)
        for row in range(6):
            for col in range(8):
                if diff[row, col] == min_diff:
                    dec[i, j] = perm[row, col]
                    break


cv2.imwrite('flag_rec.png', dec)