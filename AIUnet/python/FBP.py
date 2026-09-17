#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/13 下午6:33
# @Author  : Sesame CT
# @describe :CT重建
# @File    : FBP.py
from config import *
import os
import tensorflow as tf
import numpy as np
import tools
import matplotlib.pyplot as plt 

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
sess = tf.Session()

MODULE_ATX = tf.load_op_library('../CBCT/fanbeam/Atx/Atx.so')
# sino_path = save_sino_path
mgData_Sino = np.fromfile('./test_phase_2.raw', dtype=np.float32)
imgData_Sino = np.reshape(imgData_Sino, [512,512,361])
sino_path = '/data/tanyh/V1/code_zhu/Code/'
# sino_path = './Train_data/512_512/FBP/'
Sino_image_files = sorted(os.listdir(sino_path))

input_img = tf.placeholder(tf.float32, [rotate_num, detector_num], name="input_CT")
out = MODULE_ATX.atx(input_img, BATCH_SIZE, SO, OD, scale, img_size, img_size,
                     detector_num, det_size / factor_ray, y_os, nt, tmp_size, rotate_num, nv_pi, 0)

if __name__ == '__main__':
    for i in range(len(Sino_image_files)):
        Sino_image_file_name = Sino_image_files[i]
        Sino_img = np.fromfile(os.path.join(sino_path, Sino_image_file_name), dtype='float32', sep="")
        Sino_img = np.reshape(Sino_img, [rotate_num, detector_num])
        result = sess.run(out, feed_dict={input_img: Sino_img})
        result.astype(np.float32).tofile(save_fbp_path + Sino_image_file_name.replace('sino', 'CT'))
        
    # Sino_image_file_name = '/data/tanyh/V1/code_zhu/Code/test_sino.raw'
    # print(Sino_image_file_name)
    # Sino_img = np.fromfile(os.path.join(sino_path, Sino_image_file_name), dtype=np.float32, sep="")
    # Sino_img = np.reshape(Sino_img, [rotate_num, detector_num])
    # result = sess.run(out, feed_dict={input_img: Sino_img})

    # result = np.reshape(result,[img_size, img_size])
    # tools.draw_twoD_figure(result)

    
    # result.astype(np.float32).tofile('test.raw')
    # plt.show()
    #result.astype(np.float32).tofile(save_fbp_path + Sino_image_file_name.replace('sino', 'CT'))
