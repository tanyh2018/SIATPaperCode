import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.optimize import curve_fit
import math
import csv
import sys
# 从 CSV 文件读取数据
#df = pd.read_csv('../data.csv', header=None)
def main():
    df = pd.read_csv('output1.csv', header=None)
    # # 将数据转换为 numpy 数组
    data = np.array(df)


    mean_sigma(data)
    #save_onepixel_data()


def mean_sigma(data):
    xv = []
    yv = []
    # 绘制直方图
    means = get_mean(data)
    for i in range(600):
        data_tmp = data[:,i]
        nonzero_indices = np.nonzero(data_tmp)
        # print(len(nonzero_indices[0]))
        if len(nonzero_indices[0])>100:
            nonzero_elements = data_tmp[nonzero_indices]
            data1 = nonzero_elements*100
            # fig1 = plt.figure(figsize=(9,6))
            plt.hist(data1, bins=20, density=True, alpha=0.6)
            
            # # 计算高斯分布的参数
            mu, std = norm.fit(data1)

            # # 生成一组用于绘制高斯分布曲线的 x 值
            x = np.linspace(data1.min(), data1.max(), 100)

            # # 计算高斯分布曲线的 y 值
            y = norm.pdf(x, mu, std)

            # # 绘制高斯分布曲线
            plt.plot(x, y, 'r--', linewidth=2)

            # # 设置图表标题和轴标签
            plt.xlabel('$\phi$', fontdict={'size':20})
            plt.ylabel('Density', fontdict={'size':20})
            plt.tick_params(labelsize=10)
            print(mu,std*std)
            xv.append(mu)
            yv.append(math.log(std*std))    
            mean=1/(math.log(std*std*8000))*mu
            diffs = 1/8000*(math.e)**(mu)
            # xv.append(diffs)
            # yv.append(std*std)
            print(diffs)
            # if mu > 0.01:
            #     plt.show()
            # else:
            #     plt.close()
            # print(math.sqrt((math.e)**(mu)/500))
            # # 显示图表
    # print(sum(means)/len(means))
    fig1 = plt.figure(figsize=(9,6))
    plt.plot(xv, yv, 'k*', linewidth=2)
    print(len(yv))
    # phi
    # plt.xlabel('$e^{\phi/\eta}/I_0$', fontdict={'size':20} )
    # plt.ylabel('$\sigma_{\phi}^2$', fontdict={'size':20} )
    # absor
    plt.xlabel('$e^{q_i/\eta}/I_0$', fontdict={'size':20} )
    plt.ylabel('$\sigma_{q_i}^2$', fontdict={'size':20} )
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    # plt.xlim(1.5e-6,2.3e-6)
    # plt.ylim(0,3e-4)
    plt.tick_params(labelsize=10)
    plt.show()

def get_mean(data):
    means = []
    for i in range(600):
        data_tmp = data[:,i]
        nonzero_indices = np.nonzero(data_tmp)
        mean=0
        # print(len(nonzero_indices[0]))
        if len(nonzero_indices[0])>100:
            nonzero_elements = data_tmp[nonzero_indices]
            data1 = nonzero_elements
            # fig1 = plt.figure(figsize=(9,6))
            plt.hist(data1, bins=20, density=True, alpha=0.6)
            
            # # 计算高斯分布的参数
            mu, std = norm.fit(data1)

            # # 生成一组用于绘制高斯分布曲线的 x 值
            x = np.linspace(data1.min(), data1.max(), 100)

            # # 计算高斯分布曲线的 y 值
            y = norm.pdf(x, mu, std)
            mean=1/(math.log(std*std*500))*mu
        means.append(mean)
    return means

def save_multi_pro_data(): 
    import csv
    import numpy as np
    data = []
    with open('../data_absor.csv', 'r') as file:
        csv_reader = csv.reader(file)
        i = 1
        for row in csv_reader:
            # if i < 10:
            row1 = np.array(row)
            new_list = row1.reshape(600,720)
            new_list = np.array(new_list).astype(np.float)
            new_list = new_list.mean(1)
            print(len(new_list))
            data.append(new_list)
            i = i+1
            print(i)
    with open('output_absor.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

def save_onepixel_data(): 
    import csv
    import numpy as np
    data = []
    with open('../data_absor.csv', 'r') as file:
        csv_reader = csv.reader(file)
        i = 1
        for row in csv_reader:
            # if i < 10:
            new_list = row[::720]
            # new_list = row1.reshape(600,720)
            # new_list = np.array(new_list).astype(np.float)
            # new_list = new_list.mean(1)
            # print(len(new_list))
            data.append(new_list)
            i = i+1
            print(i)
    with open('output_absor2.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

if __name__ == '__main__':
      main()


# import csv
# data = []
# with open('../data.csv', 'r') as file:
#     csv_reader = csv.reader(file)
#     i = 1
#     for row in csv_reader:
#         # if i < 10:
#         new_list = row[4::600]
#         data.append(new_list)
#         i = i+1
#         print(i)
#         # else:
#         #     break

# with open('output2.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerows(data)


