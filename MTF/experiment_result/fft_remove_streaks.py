import numpy as np
import matplotlib.pyplot as plt 
from scipy.ndimage import gaussian_filter
from PIL import Image
import math 
from scipy.optimize import curve_fit
import os
c1 = '#ADC0E5'
c2 = '#F38624'
c3 = '#990000'
c4 = '#8EC182'
c5 = '#1C5D64'
c6 = '#404040'
c7 = '#7030A0'

def mian():
    path = "D:/xianjinyuan/工作内容/NanoCT/experiment/result/Gs/"
    A1 = "absor0.raw"
    size=[2950,2950]
    A1d = read_data2(path + A1,size)
    mA1d = np.mean(A1d,axis=0)

    tmp = np.copy(mA1d[230:950])
    for i in range(len(tmp)):
        if i>170 and i<350:
            if tmp[i]>0.14:
                tmp[i]=0.14

    
    # tmp[mask] = gaussian_filter(tmp, 10.0)[mask]
    xd = np.arange(230,950,1)
    cdfit,tmpf = pfit(xd,tmp)
    mA1d[230:950] = mA1d[230:950] - tmpf
    #ifft_result.astype(np.float32).tofile("test.raw")
    fig, axs = plt.subplots(1,1,figsize=(9, 8))
    plt.plot(tmpf)
    plt.plot(mA1d[230:950])
    plt.show()
    #plt.imshow(np.real(fft_result))
    #plt.show()


def pfit(xdata,ydata):
    ### 多项式

    ### 高斯
    x_fit = np.linspace(np.min(xdata),np.max(xdata), int(len(xdata)))
    mean,sigma=cal_gauss_sigma_mean(xdata,ydata)
    p0=[1.0,mean,sigma,1.0]
    
    popt, pcov = curve_fit(func_gauss, xdata, ydata, p0)
    print("mean=",popt[1])
    y_pre = func_gauss(x_fit,*popt)

    r_squared(ydata,y_pre)

    fig, axs = plt.subplots(1,1,figsize=(9, 8))
    plt.plot(xdata,ydata,color=c2,linestyle='--',lw=3)
    plt.plot(x_fit,y_pre,color=c1,lw=3)


    return x_fit,y_pre

def func_gauss(x, a, x0, sigma,b):
    return a*np.exp(-(x-x0)**2/(2*sigma**2)) + b

def cal_gauss_sigma_mean(xdata_cal,ydata_cal):
    n = len(ydata_cal)
    mean = sum(xdata_cal*ydata_cal)/sum(ydata_cal)
    sigma = np.sqrt(abs(sum(ydata_cal*(xdata_cal-mean)**2))/sum(ydata_cal))
    if math.isnan(float(sigma)):
        sigma=0.5
    return mean,sigma



def r_squared(y_true, y_pred):
    """计算决定系数"""
    y_mean = np.mean(y_true)  # 实际观测值的均值
    ss_total = np.sum((y_true - y_mean) ** 2)  # 总平方和
    ss_residual = np.sum((y_true - y_pred) ** 2)  # 残差平方和
    r2 = 1 - (ss_residual / ss_total)  # 决定系数
    print('R2:', r2)

def read_data2(sino_path_name,size):
    with open(sino_path_name, 'rb') as fid_3:
        sino_2 = np.fromfile(fid_3, dtype=np.float32).reshape([size[0],size[1]])
    sino_2 = sino_2.astype(float)
    return sino_2
if __name__ == '__main__':
    mian()