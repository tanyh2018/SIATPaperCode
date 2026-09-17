#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/7/5 上午11:10
# @Author  : Sesame CT
# @describe :Test
# @File    : config.py
import os
import numpy as np
import tensorflow as tf
from tensorflow.python.framework import ops


img_size = 512
I2_density = 0.03
water_density = 1.00
bone_density = 1.40

threshold1 = 0.1
threshold2 = 0.3
threshold3 = 0.5
threshold4 = 0.85
zero_range = [200,230]

total_circular = 6
tube_min_distance = 10
tube_radius = [10, 28]  # 试管半径
boundary_distance = [10, 25]  # 试管到基圆边界的距离范围
I2_density_range = [0.0098, 0.0143]


BATCH_SIZE = 1
detector_num = 600
rotate_num = 720
factor_ray = 1
SO = 0.11563
OD = 0.04043
scale = 0.15e-4
det_size = 0.15e-4
nt = 1
nv_pi = 360
y_os = 0
tmp_size = rotate_num



N_shift = 10
BATCH_THREAD_NUMBER = 14
MIN_AFTER_DEQUEUE = 32
BATCH_CAPACITY = BATCH_THREAD_NUMBER * BATCH_SIZE + MIN_AFTER_DEQUEUE


# def create_file_path(folder_path):
#     if not os.path.exists(folder_path):
#         os.makedirs(folder_path) 
        
         
# date = "20230731" 
# corn = "/check/"     ### "/check/" or "/"
# path_home =  "../PPT" + corn + date + "/"
# #path_home = '../PPT/' 
# save_ct_path = path_home +'Basis/'  # 图片存储路径
# save_sino_path = path_home +'Sino/'
# save_LH_path = path_home +'SinoLH/'
# save_fbp_path = path_home +'FBP/'
# create_file_path(save_ct_path)
# create_file_path(save_sino_path)
# create_file_path(save_LH_path)
# create_file_path(save_fbp_path)

# # Create split Sino
# sino_out_rawfile = path_home + "wrap/raw_" + date + "_test/"
# sino_out_wrapfile = path_home + "wrap/wrap_" + date + "_test/"
# sino_out_itenfile = path_home + "wrap/iten_" + date + "_test/"
# # 创建文件夹
# create_file_path(sino_out_rawfile)
# create_file_path(sino_out_wrapfile)
# create_file_path(sino_out_itenfile)



# 
# # I2_density_range = [0.0015, 0.03]

# # I2_density_range = [0.0025, 0.005, 0.01, 0.02]
# ######高低能sino生成参数.
# gaussian_operator = [0.0005, 0.1196, 0.7599, 0.1196, 0.0005]  # 调用matlab, fspecial('gaussian',[5,1],sigma)函数得出. sigma=0.52
# gaussian_kernel = np.zeros([5, 5])  # kernel为向量时，将值放置于中心位置
# for i in range(len(gaussian_operator)):
#     gaussian_kernel[2][i] = gaussian_operator[i]

# NumDettmp = 360
# NumDet = 600
# Views = 720
# Pixels = 512
# I0_base = 1e7
# I0 = I0_base
# sigma = 0.52
# energy_weighted = 100

# spectrum_xlsx_path = '../xlsx/spectrum_75-125kvp.xlsx'
# sensitometry_xlsx_path = '../xlsx/sensitometrydata_2013Ver.xlsx'

# #######sino图参数


# SO = 0.11563
# OD = 0.04043
# scale = 0.15e-4
# det_size = 0.15e-4
# nt = 1
# nv_pi = 360
# y_os = 0
# tmp_size = rotate_num


# #仿真生成参数
# # muscle_density = 1.05
# # adipose_density = 0.95


# N_shift = 107
# image_size = 512


# #out file name list

# wrap_path = '/data/tanyh/V1/code_zhu/PPT' + corn + date +'/wrap/'
# pre_path = wrap_path + 'predict_' + date +'_test/'
# out_fig_path = wrap_path + 'figure_' + date +'_test/'
# create_file_path(out_fig_path)

# input_path_test =  '/data/tanyh/V1/code_zhu/PPT' + corn + date +'/wrap/wrap_'+ date +'_test/'
# output_path_test =  '/data/tanyh/V1/code_zhu/PPT' + corn + date +'/wrap/predict_'+ date +'_test/'
# create_file_path(output_path_test)

# inv_sino_path = '/data/tanyh/V1/code_zhu/PPT' + corn + date +'/wrap/predict_'+ date +'_test/'
# inv_out_pre_path = '/data/tanyh/V1/code_zhu/PPT' + corn + date +'/wrap/predict_'+ date +'_FBP/'

# fig_wrap_path = '/data/tanyh/V1/code_zhu/PPT' + corn + date +'/wrap/'
# fig_pre_path = fig_wrap_path + 'predict_'+ date +'_test/'
# fig_out_fig_path = fig_wrap_path + 'figure_'+ date +'_test/'
# create_file_path(fig_out_fig_path)

# pixels = 512

