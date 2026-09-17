from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
t = np.linspace(0, 1000000, 1000000, endpoint=False)
y = (signal.square(2 * np.pi/(4.48721399730821*1000) * t)+1)*0.5
print((signal.square(2 * np.pi/(4.48721399730821*1000) * t)+1)*0.5)
plt.plot(t[0:10000], y[0:10000],'b')
plt.ylim(-2, 2)
plt.grid()
plt.show()