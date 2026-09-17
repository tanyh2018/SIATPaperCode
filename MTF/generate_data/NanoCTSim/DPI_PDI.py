import numpy as np
import matplotlib.pyplot as plt 



# Function 1 Exp[-x^2/2], Function 1 Exp[-x^2/8]
x1 = []
y1 = []
y2 = []
y1_l = []
y2_l = []
A = pow(10,-6)
lamda = 1.242/8.*A
d4 = 559
M= 10.1687
p = []
epsi = []
for i in range(11000):
    p1  = 0.0024 + i*0.00001
    epsi.append(lamda*d4/p1/M*1000)
    p.append(p1*1000)



# print(A)
# Fout = scipy.signal.convolve2d(grids,grids)

fig1 = plt.figure(figsize=(9,6))
# # plt.plot(x1,Fout[0])
# # plt.plot(x1,Fout[0],color = "blue")
plt.plot(epsi,p,color = "blue")
# plt.plot(x1[0],gridsy2[0],color = "red")
# plt.plot(x1[0],A[0],color = "black")
# plt.grid()
plt.xlabel( "Spatial resolution[$\mu$m]" )
plt.ylabel( "Phase grating period [$\mu$m]" )
plt.xlim(0,0.5)
# # plt.ylabel("$F^{-1}[g_{1}(x)*g_{2}(x)]$")
# # plt.title("$F^{-1}[g_{1}(x)*g_{2}(x)]$")
# # plt.ylabel("Integrate")
# # plt.title("Integrate")

p =0.010

x_v = []
epsi = []
for i in range(11000):
    x_v_t   = 0 + i*0.006
    epsi.append(lamda*x_v_t/p*1000)
    x_v.append(x_v_t)

fig1 = plt.figure(figsize=(9,6))
# # plt.plot(x1,Fout[0])
# # plt.plot(x1,Fout[0],color = "blue")
plt.plot(epsi,x_v,color = "blue")
# plt.plot(x1[0],gridsy2[0],color = "red")
# plt.plot(x1[0],A[0],color = "black")
# plt.grid()
plt.xlabel( "Spatial resolution[$\mu$m]" )
plt.ylabel( "$d_4$/M [mm]" )
plt.xlim(0,0.6)
plt.show()