import numpy as np
import matplotlib.pyplot as plt 
from scipy.ndimage import gaussian_filter
from scipy.integrate import quad
from scipy.integrate import cumtrapz
from scipy.optimize import curve_fit
from scipy.interpolate import UnivariateSpline,interp1d
from scipy.ndimage import rotate
import math
# from skimage.measure import block_reduce
c1 = '#ADC0E5'
c2 = '#F38624'
c3 = '#990000'
c4 = '#8EC182'
c5 = '#1C5D64'
c6 = '#404040'
c7 = '#7030A0'
r1=200
r2=950

r3=1000
r6=2400

r4=230
r5=360

def mian():
    gold_line_4000s()

def gold_line_4000s():
    size=[2950,2950]
    absor_path = "D:/xianjinyuan/工作内容/NanoCT/experiment/result/Gs/result/"
    A1 = "absor0.raw"
    A2 = "absor1.raw"
    A3 = "absor2.raw"
    A4 = "absor3.raw"
    A1d = read_data2(absor_path + A1,size)
    A2d = read_data2(absor_path + A2,size)
    A3d = read_data2(absor_path + A3,size)
    A4d = read_data2(absor_path + A4,size)

    phi1 = "phi0.raw"
    phi2 = "phi1.raw"
    phi3 = "phi2.raw"
    phi4 = "phi3.raw"

    phi1d = read_data2(absor_path + phi1,size)
    phi2d = read_data2(absor_path + phi2,size)
    phi3d = read_data2(absor_path + phi3,size)
    phi4d = read_data2(absor_path + phi4,size)

    absorngG0_path ="D:/xianjinyuan/工作内容/NanoCT/experiment/result/G0/absor_rotaten0.4.raw"
    absornoG_path = "D:/xianjinyuan/工作内容/NanoCT/experiment/result/noG/absor_rotaten0.4.raw"
    absorngG0G1_path = "D:/xianjinyuan/工作内容/NanoCT/experiment/result/G0G1/absor_rotaten0.4.raw"

    G0d = read_data2(absorngG0_path,size)
    noGd = read_data2(absornoG_path,size)
    G01d = read_data2(absorngG0G1_path,size)
    [A1d,A2d,A3d,A4d,phi1d,phi2d,phi3d,phi4d,G0d,noGd,G01d] = isnan_solve([A1d,A2d,A3d,A4d,phi1d,phi2d,phi3d,phi4d,G0d,noGd,G01d])
    [A1dy,A2dy,A3dy,A4dy,phi1dy,phi2dy,phi3dy,phi4dy,G0dy,noGdy,G01dy] = data_part([A1d,A2d,A3d,A4d,phi1d,phi2d,phi3d,phi4d,G0d,noGd,G01d])

    AA,AB = remove_streaks([A1dy,A2dy,A3dy,A4dy])
    [A1dy,A2dy,A3dy,A4dy] = AA
    [Ab1dy,Ab2dy,Ab3dy,Ab4dy] = AB
    pA,pB = remove_streaks2([phi1dy,phi2dy,phi3dy,phi4dy])
    [phi1dy,phi2dy,phi3dy,phi4dy] = pA
    [s_phi1dy,s_phi2dy,s_phi3dy,s_phi4dy] = pB

    Ab4dy = np.roll(Ab4dy,-1,axis=1)
    Ab3dy = np.roll(Ab3dy,-1,axis=1)
    s_phi4dy = np.roll(s_phi4dy,-1,axis=1)
    s_phi3dy = np.roll(s_phi3dy,-1,axis=1)

    G0dys = np.roll(G0dy,-28,axis=1)
    noGdys = np.roll(noGdy,6,axis=1)
    G01dys = np.roll(G01dy,-20,axis=1)

    s_data((s_phi1dy+s_phi2dy+s_phi3dy+s_phi4dy)/4.0,'phi_img','phi')
    s_data((Ab1dy+Ab2dy+Ab3dy+Ab4dy)/4.0,'A_Gs_img','A')
    s_data(noGdys,'A_noGs_img','A')
    s_data(G01dys,'A_G0G1_img','A')
    s_data(G0dys,'A_G0_img','A')

    # A1dy = np.mean(A1dy,axis=0)
    # A2dy = np.mean(A2dy,axis=0)
    # A3dy = np.mean(A3dy,axis=0)
    # A4dy = np.mean(A4dy,axis=0)
    G0dy = np.mean(G0dy,axis=0)
    noGdy = np.mean(noGdy,axis=0)
    G01dy = np.mean(G01dy,axis=0)



    [A1dy,A2dy,A3dy,A4dy,phi1dy,phi2dy,phi3dy,phi4dy,G0dy,noGdy,G01dy] = data_part2([A1dy,A2dy,A3dy,A4dy,phi1dy,phi2dy,phi3dy,phi4dy,G0dy,noGdy,G01dy])
    
    A4dy = np.roll(A4dy,-1,axis=0)
    A3dy = np.roll(A3dy,-1,axis=0)
    phi4dy = np.roll(phi4dy,-1,axis=0)
    phi3dy = np.roll(phi3dy,-1,axis=0)

    G0dy = np.roll(G0dy,-28,axis=0)
    noGdy = np.roll(noGdy,6,axis=0)
    G01dy = np.roll(G01dy,-19,axis=0)

    xd = np.arange(0,r5-r4,1)
    print("fit_result")
    xfit,A1dyf = curve_spline(xd,norm(A1dy))
    xfit,A2dyf = curve_spline(xd,norm(A2dy))
    xfit,A3dyf = curve_spline(xd,norm(A3dy))
    xfit,A4dyf = curve_spline(xd,norm(A4dy))
    xfit,G0dyf = curve_spline(xd,norm(G0dy))
    xfit,noGdyf = curve_spline(xd,norm(noGdy))
    xfit,G01dyf = curve_spline(xd,norm(G01dy))


    A1dyf =norm(normz(A1dyf))
    A2dyf =norm(normz(A2dyf))
    A3dyf =norm(normz(A3dyf))
    A4dyf =norm(normz(A4dyf))
    G0dyf =norm(normz(G0dyf))
    noGdyf = norm(normz(noGdyf))
    G01dyf = norm(normz(G01dyf))
    mean_Af = (A1dyf + A2dyf + A3dyf + A4dyf)/4.0

    A1dy = norm(normz(A1dy))
    A2dy = norm(normz(A2dy))
    A3dy = norm(normz(A3dy))
    A4dy = norm(normz(A4dy))
    G0dy = norm(normz(G0dy))
    noGdy = norm(normz(noGdy))
    G01dy = norm(normz(G01dy))
    mean_A = (A1dy + A2dy + A3dy + A4dy)/4.0

    Nshift = 5
    noGdy = noGdy*0.001
    theoryA = -0.5*np.log(0.5*(np.exp(-2.0*np.roll(noGdy,Nshift,axis=0)) + np.exp(-2.0*np.roll(noGdy,-Nshift,axis=0))))
    theoryB = -0.5*np.log(0.5*(np.exp(-2.0*np.roll(noGdy,Nshift-1,axis=0)) + np.exp(-2.0*np.roll(noGdy,-Nshift+1,axis=0))))
    fig, axs = plt.subplots(1,1,figsize=(9, 6))
    plt.plot(theoryA)
    plt.plot(noGdy)

    #### absor
    fig, axs = plt.subplots(1,1,figsize=(9, 6))

    # plt.plot(phiy ,label='phi',color=c1,lw=3)
    plt.plot(norm((norm(mean_A))),label=r'$A (G_0+G_1+G_2)$',color=c2,lw=3)
    plt.plot(norm(norm(G01dy)),label=r'$A (G_0+G_1)$',linestyle='--',color=c3,lw=3)
    plt.plot(norm(G0dy),label=r'$A (G_0)$',color=c4,lw=3)
    plt.plot(norm(noGdy),label=r'$A (-)$',linestyle='--',color=c5,lw=3)
    #plt.plot(norm(theoryAf),label=r'$T_A (\Delta s=50.6\mu m)$',linestyle='-',color=c1,lw=3)
    plt.ylim(0.0,1.3)
    fig_config('Pixels','Profile (Norm.)','test')
    save_fig('./figure/A.png')

    fig, axs = plt.subplots(1,1,figsize=(9, 6))
    noGdyf = noGdyf*0.0001
    theoryAf = -0.5*np.log(0.5*(np.exp(-2.0*np.roll(noGdyf,Nshift+1,axis=0)) + np.exp(-2.0*np.roll(noGdyf,-Nshift,axis=0))))
    # plt.plot(phiy ,label='phi',color=c1,lw=3)
    plt.plot(norm(noGdyf),label=r'$A (-)$',linestyle='--',color=c5,lw=3)
    plt.plot(norm(G0dyf),label=r'$A (G_0)$',color=c4,lw=3)
    plt.plot(norm(norm(G01dyf)),label=r'$A (G_0+G_1)$',linestyle='--',color=c3,lw=3)
    plt.plot(norm((norm(mean_Af))),label=r'$A (G_0+G_1+G_2)$',color=c2,lw=3)
    #plt.plot(norm(theoryAf),label=r'$T_A (\Delta s=50.6\mu m)$',linestyle='-',color=c1,lw=3)
    plt.ylim(0,1.8)
    # plt.xlim(150,240)
    fig_config('Pixels','Profile (Norm.)','test')
    save_fig('./figure/A_fit.png')
    A = np.zeros([4,r5-r4])
    A[0] = A1dy 
    A[1] = A2dy 
    A[2] = A3dy
    A[3] = A4dy 

    fig, axs = plt.subplots(1,1,figsize=(9, 6))
    mean_values = np.mean(A, axis=0)
    std_errors = np.std(A, axis=0, ddof=1) / np.sqrt(4)
    # 绘制平均值和误差条
    plt.errorbar(range(len(mean_values)), mean_values, yerr=std_errors, fmt='--', capsize=2, label=r'$A\,(G_0+G_1+G_2)$ with error',lw=3,color=c1)
    plt.plot(norm(theoryB),label=r'$A(G_0)$ with $\Delta s=36.8\mu m$',lw=3,color=c4)
    plt.plot(norm(theoryA),label=r'$A(G_0)$ with $\Delta s=46\mu m$',lw=3,color=c2)
    plt.ylim(0,1.5)
    fig_config('Pixels','Profile (Norm.)','test')
    save_fig('./figure/error.png')
    ### phase
    pdata = [mean_Af,G01dyf,G0dyf,noGdyf]
    [pmean_A,pG01dy,pG0dy,pnoGdy] = grad(pdata,xfit)

    phi = np.zeros([4,r5-r4])
    phi[0] = norm(normz(phi1dy))
    phi[1] = norm(normz(phi2dy)) 
    phi[2] = norm(normz(phi3dy))
    phi[3] = norm(normz(phi4dy))
    phi = np.roll(phi,-1,axis=1)
    mean_valuesp = np.mean(phi, axis=0)
    std_errorsp = np.std(phi, axis=0, ddof=1) / np.sqrt(4)

    fig, axs = plt.subplots(1,1,figsize=(9, 6))
    plt.errorbar(range(len(mean_valuesp)), norm(mean_valuesp), yerr=std_errorsp, fmt='--', color=c1, capsize=2, label=r'$\Delta \Phi$ with error',lw=3)
    # plt.plot(mean_valuesp,label=r'$\Delta \phi$',color=c1,lw=3)
    plt.plot(pmean_A,label=r'$\Delta A (G_0+G_1+G_2)$',color=c2,lw=3)
    plt.ylim(-1.2,1.8)
    fig_config('Pixels','Profile (Norm.)','test')
    save_fig('./figure/diffA.png')
    # plt.show()


def s_data(data,title,dtype):
    tdata = data[0:1400,200:400]
    window_size=70
    # 指定旋转角度（例如45度）
    # angle = 0.2
    # # 以矩阵中心为旋转中心，逆时针旋转矩阵
    # tdata = rotate(tdata, angle, reshape=False)
    new_data = tdata.reshape(tdata.shape[0] // window_size, window_size, tdata.shape[1]).sum(axis=1)
    fig, axs = plt.subplots(1,1,figsize=(9, 6))
    if dtype == "phi":
        plt.imshow(new_data/np.max(new_data),cmap='gray',vmin=-0.7,vmax=0.7)    
    else:
        plt.imshow(new_data/np.max(new_data),cmap='gray',vmin=np.min(new_data/np.max(new_data)),vmax=np.max(new_data/np.max(new_data)))
    plt.axis("off")
    plt.savefig(title+".svg", bbox_inches='tight',pad_inches=0)
    new_data.astype(np.float32).tofile("test1.raw")

def grad(data,xdf):
    datal = np.zeros_like(data)
    for i in range(len(data)):
        B_prime_values = np.gradient(data[i],xdf)
        B_prime_values = B_prime_values/np.max(B_prime_values)
        datal[i] =norm(B_prime_values*(-1.0))
    return datal

def remove_streaks(data):
    mdatas = []
    fig, axs = plt.subplots(1,1,figsize=(9, 6))
    for i in range(len(data)):
        mdata = np.mean(data[i],axis=0)
        tmp = np.copy(mdata)
        tmp[250:335] = 0
        tmp[250:335]= np.max(tmp)*0.97
        xd=np.arange(1,len(tmp)+1,1)
        xf,df = pfit(xd,tmp)
        mdata= mdata - df
        plt.plot(mdata)
        mdatas.append(mdata)
        for j in range(len(data[i])):
            data[i][j][:] = data[i][j][:] - df
    return np.array(mdatas),data

def remove_streaks2(data):
    mdatas = []
    fig, axs = plt.subplots(1,1,figsize=(9, 6))    
    for i in range(len(data)):
        mdata = np.mean(data[i],axis=0)
        tmp = np.copy(mdata[0:430])
        tmp[250:340] = np.mean(tmp[250:340])
        xd=np.arange(1,len(tmp)+1,1)
        xf,df = pfit(xd,tmp)
        mdata[0:430]= mdata[0:430] - df
        plt.plot(mdata)
        mdatas.append(mdata)
        for j in range(len(data[i])):
            data[i][j][0:430] = data[i][j][0:430] - df
    return np.array(mdatas),data

def data_part(data):
    datas = []
    angle=0.2
    for i in range(len(data)):
        tmp = data[i]
        tmp = rotate(tmp, angle, reshape=False)
        datas.append(tmp[r3:r6,r1:r2])
    return np.array(datas)       

def data_part2(data):
    datas = []
    for i in range(len(data)):
        tmp = data[i]
        datas.append(tmp[r4:r5])
    return np.array(datas)      

def isnan_solve(data):
    for i in range(len(data)):
        tmp = data[i]
        tmp[np.isnan(tmp) | np.isinf(tmp)] = 0
        data[i] = tmp
    return data

def normz(data):
    data = data - np.min(np.abs(data))
    return data

def norm(data):
    return data/np.max(data)


def save_fig(outp):
    plt.savefig(outp, bbox_inches='tight',pad_inches=0)
    if "png" in outp:
        plt.savefig(outp.replace('png','svg'), bbox_inches='tight',pad_inches=0)

def fig_config(xname,yname,title_name,sci=None):

    plt.legend(fontsize=20, frameon=False,loc='upper left')
    plt.xlabel(xname,fontdict={'size': 20})
    plt.ylabel(yname,fontdict={'size': 20})
    plt.xticks(fontsize=20) 
    plt.yticks(fontsize=20)
    # plt.title(title_name,fontdict={'size': 12},y=1.1)
    if sci == True:
        plt.yscale('log')
        #plt.ticklabel_format(axis='y', style='sci')

def curve_spline(xdata,ydata):
    # 创建 UnivariateSpline 对象
    # spline = UnivariateSpline(xdata, ydata,k=4,s=0.01)  # s 控制平滑度，可以调整
    # #spline = interp1d(xdata, ydata, kind='previous') 
    # # 生成拟合后的曲线
    # x_fit = np.linspace(np.min(xdata),np.max(xdata), int(len(xdata))*10)
    # y_pre = spline(x_fit)
    # r_squared(ydata,y_pre)

    x_fit = np.linspace(np.min(xdata),np.max(xdata), int(len(xdata)))
    mean,sigma=cal_gauss_sigma_mean(xdata,ydata)

    p0=[-7.545,63.29,14.81,8.203,63.32,15.23,0.116,-2159,9647,1.0,1.0,1.0]
    
    popt, pcov = curve_fit(gaussian_mixture, xdata, ydata, p0, maxfev = 100000000)
    y_pre = gaussian_mixture(x_fit,*popt)

    r_squared(ydata,y_pre)
    print(np.argmax(y_pre))
    fig, axs = plt.subplots(1,1,figsize=(9, 6))
    plt.plot(xdata,ydata,color=c2,linestyle='--',lw=3)
    plt.plot(x_fit,y_pre,color=c1,lw=3)

    return x_fit,y_pre

def pfit(xdata,ydata):
    ### 多项式
    degree = 20  # 多项式的次数
    # coefficients = np.polyfit(xdata, ydata, deg=degree)
    # poly_fit = np.poly1d(coefficients)
    # x_fit = np.linspace(np.min(xdata),np.max(xdata), int(len(xdata)))
    # y_fit = poly_fit(x_fit)

    ### 高斯
    x_fit = np.linspace(np.min(xdata),np.max(xdata), int(len(xdata)))
    mean,sigma=cal_gauss_sigma_mean(xdata,ydata)
    p0=[1.0,mean,sigma,1.0]
    
    popt, pcov = curve_fit(func_gauss, xdata, ydata, p0, maxfev = 100000000)
    print("mean=",popt[1])
    y_pre = func_gauss(x_fit,*popt)

    r_squared(ydata,y_pre)

    fig, axs = plt.subplots(1,1,figsize=(9, 6))
    plt.plot(xdata,ydata,color=c2,linestyle='--',lw=3)
    plt.plot(x_fit,y_pre,color=c1,lw=3)

    return x_fit,y_pre

def gaussian_mixture(x, amp1, mu1, sigma1, amp2, mu2, sigma2,amp3, mu3, sigma3,amp4, mu4, sigma4):
    return func_gauss2(x, amp1, mu1, sigma1) + func_gauss2(x, amp2, mu2, sigma2) + func_gauss2(x, amp3, mu3, sigma3)  +  + func_gauss2(x, amp4, mu4, sigma4)  

def func_gauss2(x, a, x0, sigma):
    return a*np.exp(-((x-x0)/sigma)**2)

def func_gauss(x, a, x0, sigma,baseline):
    return a*np.exp(-(x-x0)**2/(2*sigma**2)) + baseline

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

def needle():
    sig_path = "./data/com/absor_final_needle_912_1200_FFT2.raw"
    bkg_path = "./data/com/without_grating.raw"

    sig_data = read_data2(sig_path)
    bkg_data = read_data2(bkg_path)

    fig, axs = plt.subplots(1,1,figsize=(9, 6))
    sig_data = np.roll(sig_data,27,axis=0)
    sig_data = np.roll(sig_data,200,axis=1)
    diff = sig_data-bkg_data/1.98
    
    plt.imshow(diff,cmap='gray')
    diff.astype(np.float32).tofile("./data/com/diff.raw")
    plt.show()

def read_data2(sino_path_name,size):
    with open(sino_path_name, 'rb') as fid_3:
        sino_2 = np.fromfile(fid_3, dtype=np.float32).reshape([size[0],size[1]])
    return sino_2
if __name__ == '__main__':
    mian()