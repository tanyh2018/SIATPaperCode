import sys
import matplotlib.pyplot as plt 
import numpy as np
from scipy.optimize import curve_fit
from astropy import modeling
import os 
import io
import math
from scipy import optimize
#----------------------------------------
# Main Calculation defined here
#----------------------------------------
def main():
    file_path = 'D:/xianjinyuan/工作内容/Jiecheng/NanoCT/Simulation/NanoCT_Sim/SimCode/withoutZP/data/split_test4/CTresult/MTF_result_LSF_txt/'  #res 20um

    file_names,list_LSF = read_datas(file_path)
    fit_LSF(list_LSF,file_names,file_path)
    #plt.show()
def read_datas(file_path):
    file_names = []
    list_phi = []
    for file_name in os.listdir(file_path):
        if '.raw' not in file_name:
            file_names.append(file_name)
            list_phi.append(read_data(file_path + file_name))
    return file_names,list_phi

def fit_LSF(list_LSF,file_names,file_path):
    for i in range(len(file_names)):
        model = 'gauss'
        if ('p' in file_names[i]):
            fig1 = plt.figure(figsize=(9,6))
        
            ydata_raw = (list_LSF[i])
            xdata_raw = np.arange(len(ydata_raw)) + 1
            ydata  = (ydata_raw.copy())

            y_max = max(ydata)
 
            xdata = [x+1 for x in range(len(ydata)) if ydata[x] > y_max*0.05*-100 ]
            ydata = [ydata[x] for x in range(len(ydata)) if ydata[x] > y_max*0.05*-100 ]
            # sys.exit()
            if model  == 'gauss':
                max_index_min = 0
            else:
                max_index_min = ydata.index(max(ydata)) - 3
            ydata_cal = np.array(ydata[max_index_min:])
            xdata_cal = np.array(xdata[max_index_min:])
            mean,sigma = cal_gauss_sigma_mean(xdata_cal,ydata_cal)
            xdata_list = np.linspace(xdata_raw[0]-10,xdata_raw[-1],len(xdata_raw)*4)
            if model == 'gauss':
                popt, covariance = optimize.curve_fit(func_gauss, xdata, ydata,p0=[y_max,mean,sigma])
                out_put_LSF = func_gauss(xdata_list, *popt)
                out_put_LSF_fit = func_gauss(xdata_raw, *popt)
                r_squared(ydata_raw,out_put_LSF_fit)
            elif model == 'sep_func':
                popt, covariance = optimize.curve_fit(func, xdata, ydata,p0=[1,mean,sigma,13-10,0.2,max_index_min])
                out_put_LSF = func(xdata_list, *popt)
                # z1 = np.polyfit(xdata, ydata,2)
                # p1 = np.poly1d(z1)
                # out_put_LSF = p1(xdata_list)
            save_data(xdata_list,out_put_LSF,file_names[i],file_path)
            plt.plot(xdata_list, out_put_LSF ,'r-')
            plt.title(file_names[i])
            plt.scatter(xdata_raw,ydata_raw)

def small_range_fit(xdata_raw,ydata_raw,out_put_LSF_fit,range_t,xdata_list):
    xdata = xdata_raw[range_t[0]:range_t[1]]
    ydata = ydata_raw[range_t[0]:range_t[1]] - out_put_LSF_fit[range_t[0]:range_t[1]]
    xdata_list_copy=[]
    mean,sigma = cal_gauss_sigma_mean(xdata,ydata)
    popt, covariance = optimize.curve_fit(func_gauss, xdata, ydata,p0=[1,mean,sigma])
    # for i in range(len(xdata_list)):
    #     if xdata_list[i]>=range_t[0] and xdata_list[i]<=range_t[1]:
    #         xdata_list_copy.append(xdata_list[i])
    xdata_list_copy = [ xdata_list[i] for i in range(len(xdata_list)) if xdata_list[i]>=range_t[0] and xdata_list[i]<=range_t[1] ]
    fit_data = func_gauss(xdata_list_copy, *popt)
    return xdata_list_copy,fit_data

def cal_gauss_sigma_mean(xdata_cal,ydata_cal):
    n = len(ydata_cal)
    mean = sum(xdata_cal*ydata_cal)/sum(ydata_cal)
    sigma = np.sqrt(abs(sum(ydata_cal*(xdata_cal-mean)**2))/sum(ydata_cal))
    if math.isnan(float(sigma)):
        sigma=0.5
    return mean,sigma

def save_data(xdata_list,out_put_LSF,file_name,file_path):
    file_name_raw = file_path + ((file_name).split('notfit.txt'))[0] + '.raw'
    output = [xdata_list,out_put_LSF]
    out_put = np.array(output)
    with io.open(file_name_raw,'wb') as f:
        out_put.astype(np.float32).tofile(f)

def func(x, a, x0, sigma,c,b,g):
    return np.piecewise(x, [x <= g, x > g], [lambda x : c*np.exp(b*x),
lambda x: a*np.exp(-(x-x0)**2/(2*sigma**2))])

# def func(x, a, x0, sigma,c,b,g):
#     return np.piecewise(x, [x <= g, x > g], [lambda x : c*np.exp(b*x)+a*np.exp(-(x-x0)**2/(2*sigma**2)),
# lambda x: a*np.exp(-(x-x0)**2/(2*sigma**2))])
def r_squared(y_true, y_pred):
    """计算决定系数"""
    y_mean = np.mean(y_true)  # 实际观测值的均值
    ss_total = np.sum((y_true - y_mean) ** 2)  # 总平方和
    ss_residual = np.sum((y_true - y_pred) ** 2)  # 残差平方和
    r2 = 1 - (ss_residual / ss_total)  # 决定系数
    print('R2:', r2)

def func_gauss(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))

# def func_gauss(x, a, x0, sigma):
#     return np.piecewise(x, [x <= 8, x > 8], [lambda x : x*0,
# lambda x: a*np.exp(-(x-x0)**2/(2*sigma**2))])

def color_matlab(number):
    d = number+1
    a = [i for i in range(d)]
    rgb_mask = [0, 0, 1]
    color_set = []
    c=1
    for i in range(d):   
        color_set.append((a[i]/d*rgb_mask[c%3], a[i]/d*rgb_mask[(c+1)%3], a[i]/d*rgb_mask[(c+2)%3]))
    return color_set

def read_data(file_name):
    data_x = []
    file_handler = open(file_name, 'r')
    with file_handler as file_in:
        for line in file_in:
            data_x.append(float(line.split(',')[0]))
    return data_x

def load_data(list_v):
    plot_valuex = []
    plot_value_y = []
    for i in range(len(list_v[0])):
        if list_v[0][i] >= 0:
            plot_valuex.append(list_v[0][i])
            plot_value_y.append(list_v[1][i])
    return [plot_valuex,plot_value_y] 

def sep_dis(file_names):
    sep_dis_list = []
    for i in range(len(file_names)):
        fst= file_names[i].split('_')[:]
        fst[1] = str(round(float(fst[1]),1))
        sep_dis_list.append('p:'+fst[1]+'_'+fst[2]+':'+fst[3]+' '+'$\mu$m')
        #sep_dis_list.append(float(file_names[i].split('_')[-4]))
    return sep_dis_list

if __name__ == '__main__':
    main()