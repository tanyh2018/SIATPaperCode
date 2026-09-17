#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/13 下午2:19
# @Author  : Sesame CT
# @describe :工具函数
# @File    : utils.py
import matplotlib.pyplot as plt 
import numpy as np

def draw_twoD_figure(input_data):
    input_data = np.array(input_data)
    fig, axs = plt.subplots(1,1,figsize=(9, 6))
    axs.imshow(input_data,cmap='gray')
    sdex = int(len(input_data)/2)
    fig, axs = plt.subplots(1,1,figsize=(9, 6))
    plt.plot(input_data[sdex][:],'#F38624')
    plt.xlabel('Pixels')
    plt.ylabel('Phase')
    plt.legend(fontsize=15,frameon=False)

