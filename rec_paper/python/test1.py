import numpy as np

A = np.zeros((720,600, 600))
B = np.zeros((500,600, 600))

C = np.matmul(A, B)
print(C.shape)  # 输出结果为 (600, 600)
print((A.T).shape)  # 输出结果为 (600, 600)