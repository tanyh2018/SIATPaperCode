import numpy as np
import matplotlib.pyplot as plt


def main():
    col=1000
    R=150
    Nshift = 150
    x=np.zeros(col)
    pro = cylinder_twoD_define(x,R)*0.001
    pro_l = np.roll(pro,Nshift,axis=0)
    pro_R = np.roll(pro,-Nshift,axis=0)
    pro = pro_l - pro_R
    xdf = np.linspace(0,1000,1000)
    pro_d1 = np.gradient(pro,xdf)
    pro_d2 = np.gradient(pro,xdf)
    draw_plot(pro)
    draw_plot(pro_d1)
    draw_plot(pro_d2)
    plt.show()



def cylinder_twoD_define(x,R):
    pro = np.zeros_like(x)
    for i in range(x.shape[0]):
            ds =  (i-x.shape[0]/2.0)**2
            if ds<= R**2:
                pro[i] = 2.0*np.sqrt(R**2-ds)
            else:
                pro[i] = 00.0
    return pro

def draw_plot(data):
    fig, axs = plt.subplots(1,1,figsize=(9, 6))
    plt.plot(data)


if __name__ == '__main__':
    main()