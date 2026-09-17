#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/26 下午4:29
# @Author  : Sesame CT
# @describe :
# @File    : config.py
import tensorflow as tf
from tensorflow.python.framework import ops
import os

def create_file_path(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


BATCH_SIZE = 1
NUM_EPOCHS = 20
BATCH_THREAD_NUMBER = 14
MIN_AFTER_DEQUEUE = 32
BATCH_CAPACITY = BATCH_THREAD_NUMBER * BATCH_SIZE + MIN_AFTER_DEQUEUE

FBP_NUM = 32  # 需要进行FBP的次数
NumDet = 600
Views = 720
pixels = 512

detector_num = NumDet
img_size = pixels
rotate_num = Views

SO = 0.11563
OD = 0.04043
scale = 0.15e-4
det_size = 0.25e-4

nt = 1
nv_pi = 360
y_os = 0
tmp_size = rotate_num


sourceDir = '/data/tanyh/V1/train_data/TFrecord/'
tfFile = 'Fanbeam_nature_data_sim_2023_6_20_noise.tfrecords'


#out file name list
date = "20230731"

input_path_test =  '/data/tanyh/V1/code_zhu/PPT/check/'+ date +'/wrap/wrap_'+ date +'_test/'
output_path_test =  '/data/tanyh/V1/code_zhu/PPT/check/'+ date +'/wrap/predict_'+ date +'_test/'
create_file_path(output_path_test)