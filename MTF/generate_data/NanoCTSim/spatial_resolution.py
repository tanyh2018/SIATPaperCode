import numpy as np
import matplotlib.pyplot as plt 
import scipy.signal


# Function 1 Exp[-x^2/2], Function 1 Exp[-x^2/8]
x1 = []
y1 = []
y2 = []
y1_l = []
y2_l = []

n = 1000
grids = np.zeros([1,n])
gridsy = np.zeros([1,n])
gridsy2 = np.zeros([1,n])
x1 = np.zeros([1,n])
sigma_1 = 2
sigma_2 = 2
b2 = 5
sigma_3 = sigma_1*sigma_1 + sigma_2*sigma_2
for i in range(1): 
    for j in range(n):
        x = (j-n/2)*10 / n * 2
        x1[i][j] = x
        grids[i][j]= np.exp(-(x+b2)**2/(2.0*sigma_1**2))   #sigma_1 = 1
        gridsy[i][j] = np.exp(-x**2/(2.0*sigma_2**2)) #sigma_1 = 1
        gridsy2[i][j] = np.sqrt(2*np.pi/sigma_3)*sigma_1*sigma_2*np.exp(-x**2/(2.0*sigma_3)) #sigma_1 = 1


fig1 = plt.figure(figsize=(9,6))
# plt.plot(x1,Fout[0])
# plt.plot(x1,Fout[0],color = "blue")
plt.plot(x1[0],grids[0]+gridsy[0],color = "black",linewidth=2)
plt.plot(x1[0],grids[0],color = "blue",linewidth=2)
plt.plot(x1[0],gridsy[0],color = "red",linewidth=2)

plt.grid()
plt.xlabel( "x direction " )
# plt.ylabel("$F^{-1}[g_{1}(x)*g_{2}(x)]$")
# plt.title("$F^{-1}[g_{1}(x)*g_{2}(x)]$")
# plt.ylabel("Integrate")
# plt.title("Integrate")
plt.show()