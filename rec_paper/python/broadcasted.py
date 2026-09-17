import numpy as np

A = np.random.rand(920, 920)
I = np.random.rand(361, 1000, 920)
phase_T = np.random.rand(920, 920, 361)

result = np.matmul(A, I.reshape(361, -1)).reshape(920, 1000, 361).transpose(1, 2, 0)

print(result.shape)
