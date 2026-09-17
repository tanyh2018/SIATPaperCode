import sys

import matplotlib.pyplot as plt 

import numpy as np
from scipy.ndimage import gaussian_filter
import os 
#----------------------------------------
# Main Calculation defined here
#----------------------------------------
def main():
    dir_path_name = '..//para/x_ray_spe_1mm_al.txt'
    xenergy_i = read_xenergy(dir_path_name)
    fig1 = plt.figure(figsize=(9,6))
    # print(xenergy_i[0])
    plt.scatter(xenergy_i[0],xenergy_i[1])
    plt.xlabel("x-ray energy [keV]")
    plt.ylabel("Ratio")
    plt.show()


def read_xenergy(dir_path_name):
    file_v = open(dir_path_name,'r')
    v_info = file_v.readlines()
    xenergy_list = [float(v_info[i].split('  ')[0]) for  i in range(len(v_info))]
    v_list_y = [float(v_info[i].split('  ')[1]) for  i in range(len(v_info))]
    xenergy_ratio = [v_list_y[i]/sum(v_list_y) for i in range(len(v_list_y))]
#     print(sum(xenergy_ratio))
#     sys.exit()
    return [xenergy_list,xenergy_ratio]

def float_def(input):
    try:
        float(input)
        return True
    except Exception as exc:
        return False

if __name__ == '__main__':
    main()