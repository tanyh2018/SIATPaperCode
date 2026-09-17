import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve1d, gaussian_filter1d
from scipy.ndimage import gaussian_filter

def read_raw_file(file_path,shape):
    with open(file_path, 'rb') as file:
        data = np.fromfile(file, dtype=np.float32)
    return data.reshape(shape)

def fig_config(xname,yname):
    pass
    
file_path = '../data/phase_MTF_image.raw'
shape =(2048,2048)
signal = read_raw_file(file_path,shape)
signal = gaussian_filter(signal,5)
convolved_signal = np.zeros_like(signal)
diff_signals = np.zeros_like(signal)
# 计算离散信号的差分（近似微分）
for i in range(signal.shape[0]):
    data = signal[i,:]
    diff_signal = np.diff(data)
    diff_signal = np.insert(diff_signal, 0, 0)

    # 定义一个卷积核来强调中间凹陷部分
    kernel = np.array([-1.0, 0, 1.0])  # 这是一个简单的拉普拉斯核

    # 对微分信号进行卷积处理
    convolved_signal[i,:] = convolve1d(diff_signal, kernel, mode='constant')
    diff_signals[i,:] = diff_signal
plt.gca().get_xaxis().set_visible(False)
plt.gca().get_yaxis().set_visible(False)
zernike = signal + convolved_signal*60
zernike.tofile("zernike.raw")
r1 = 300
r2 = 550
plt.figure(figsize=(9, 9))
plt.plot(signal[1200,r1:r2],lw=3)
plt.xticks([])
plt.yticks([])
fig_config(' ',' ')
plt.savefig("phase_line.svg", bbox_inches='tight',pad_inches=0)

plt.figure(figsize=(9,9))
plt.plot(diff_signals[1200,r1:r2],lw=3)

plt.figure(figsize=(10, 6))
plt.plot(convolved_signal[1200,r1:r2])

plt.figure(figsize=(9, 9))
plt.plot(zernike[1200,r1:r2],lw=3)    
plt.xticks([])
plt.yticks([])
fig_config(' ',' ')
plt.savefig("zernike_line.svg", bbox_inches='tight',pad_inches=0)
    
# plt.figure(figsize=(10, 6))
# plt.imshow(signal,'gray')
# plt.axis("off")
# plt.savefig("phase.svg", bbox_inches='tight',pad_inches=0)

# plt.figure(figsize=(10, 6))
# plt.imshow(diff_signals,'gray')

# plt.figure(figsize=(10, 6))
# plt.imshow(convolved_signal,'gray')

plt.figure(figsize=(10, 6))
plt.imshow(zernike,'gray')
plt.axis("off")
plt.savefig("zernike.svg", bbox_inches='tight',pad_inches=0)
plt.show()

