#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/13 下午5:17
# @Author  : Sesame CT
# @describe :生成Sino图
# @File    : GenSino.py
from config import *
import os
import tensorflow as tf
import numpy as np 
import sys

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
sess = tf.Session()

MODULE_AX = tf.load_op_library('/data/tanyh/V1/code_zhu/CBCT/fanbeam/Ax/Ax.so')
MODULE_ATX = tf.load_op_library('/data/tanyh/V1/code_zhu/CBCT/fanbeam/Atx/Atx.so')

# MODULE_AX = tf.load_op_library('/home/amax/Workspace/OP/20190813/CBCT/fanbeam/Ax/Ax.so')
# MODULE_ATX = tf.load_op_library('/home/amax/Workspace/OP/20190813/CBCT/fanbeam/Atx/Atx.so')

CT_image_files = sorted(os.listdir(sys.argv[1]))

# Sino_image_files = sorted(os.listdir(save_sino_path))
# CT_image_files = [name for name in CT_image_files if name not in Sino_image_files]  #避免重复生成

input_img = tf.placeholder(tf.float32, [BATCH_SIZE, img_size, img_size, 1], name="input_CT")
sino_img = MODULE_AX.ax(input_img, BATCH_SIZE, SO, OD, scale, img_size, img_size, rotate_num, nv_pi, detector_num, nt,
                        det_size / factor_ray, y_os)
sino_img = tf.reshape(sino_img, [rotate_num, detector_num])



for i in range(len(CT_image_files)):
    if i%100==0:
        print(i)
    CT_image_file_name = CT_image_files[i]
    CT_img = np.fromfile(os.path.join(sys.argv[1], CT_image_file_name), dtype=np.float32)
    CT_img = CT_img.reshape([BATCH_SIZE, img_size, img_size, 1])

    sino = sess.run(sino_img, feed_dict={input_img: CT_img})


    # 假设原始矩阵名为matrix，形状为 (720, 490)
    # num_zeros = int((NumDet - NumDettmp)/2)    #需要添加的零值列数量

    # zero_columns = np.zeros((sino.shape[0], num_zeros))  # 创建零值列矩阵

    # # 将零值列与原始矩阵列连接在一起
    # result_matrix = np.concatenate((zero_columns, sino), axis=1)
    # result_matrix = np.concatenate((result_matrix, zero_columns), axis=1)

    sino .astype(np.float32).tofile(sys.argv[2] + CT_image_file_name)
