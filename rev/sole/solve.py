#!/usr/bin/env python3

from z3 import *

flag = [BitVec(f'idx{i}', 8) for i in range(26)]

solver = Solver()

solver.add(flag[11] * flag[19] * flag[4] == 391020)
solver.add(flag[8] * flag[13] * flag[22] == 567720)
solver.add(flag[0] * flag[22] + flag[15] == 4872)
solver.add(flag[8] + flag[0] + flag[11] == 199)
solver.add(flag[13] - flag[12] * flag[22] == -3721)
solver.add(flag[4] * flag[9] - flag[1] == 8037)
solver.add(flag[16] * flag[9] * flag[11] == 272832)
solver.add(flag[3] * flag[23] + flag[15] == 9792)
solver.add(flag[9] - flag[23] - flag[4] == -70)
solver.add(flag[5] - flag[21] - flag[8] == -63)
solver.add(flag[3] * flag[24] + flag[0] == 5359)
solver.add(flag[1] * flag[25] + flag[17] == 10483)
solver.add(flag[19] * flag[7] * flag[2] == 893646)
solver.add(flag[11] - flag[4] + flag[19] == 93)
solver.add(flag[6] + flag[7] - flag[10] == 136)
solver.add(flag[25] + flag[0] + flag[10] == 287)
solver.add(flag[5] + flag[12] - flag[22] == 104)
solver.add(flag[12] + flag[7] * flag[4] == 8243)
solver.add(flag[1] - flag[22] + flag[4] == 81)
solver.add(flag[8] - flag[11] * flag[19] == -5503)
solver.add(flag[8] - flag[10] - flag[7] == -129)
solver.add(flag[22] + flag[20] + flag[21] == 224)
solver.add(flag[23] + flag[24] + flag[12] == 232)
solver.add(flag[15] - flag[9] + flag[4] == 2)
solver.add(flag[15] * flag[9] + flag[2] == 5635)
solver.add(flag[14] + flag[24] + flag[16] == 210)
solver.add(flag[10] + flag[1] - flag[12] == 125)
solver.add(flag[18] - flag[1] - flag[5] == -111)
solver.add(flag[12] - flag[14] - flag[7] == -163)
solver.add(flag[5] + flag[1] - flag[16] == 158)


solver.check()

model = solver.model()
flag = ''.join([chr(int(str(model[flag[i]]))) for i in range(len(model))])
print(flag)