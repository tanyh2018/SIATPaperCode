# `ctrl+alt+L`??????
# ???????????RAW??
import matplotlib.pyplot as plt 
import tensorflow as tf
from config import *
import numpy as np
import sys
import os

Data_path = sys.argv[1]
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

writer_test = tf.python_io.TFRecordWriter(sys.argv[2] + sys.argv[3]+'.tfrecords')

data_image_files = os.listdir(Data_path)
data_image_files = [(img.split('phase_')[-1]).split('.raw')[0] for img in data_image_files if "phaseref" not in img]
data_image_files = set(data_image_files)

count = 1
# Views = 720
# NumDet = 600
i=0
for index in data_image_files:
    if i <=20000:
        tf.reset_default_graph()
        data_img = np.fromfile(Data_path + 'phase_{}.raw'.format(index), dtype='float32',
                                    sep="")
        if data_img.size == rotate_num*detector_num:
            data_img =data_img.reshape([rotate_num, detector_num])
        else:
            continue

        ref_img = np.fromfile(Data_path + 'phaseref_{}.raw'.format(index), dtype='float32',
                                    sep="")
        if ref_img.size == rotate_num*detector_num:
                ref_img = ref_img.reshape([rotate_num, detector_num])
        else:
            continue

        img_raw_0 = data_img.tobytes()
        img_raw_1 = ref_img.tobytes()

        example = tf.train.Example(features=tf.train.Features(feature={
            'data_img': tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw_0])),
            'ref_img': tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw_1])),
        }))
        count += 1
        if count % 100 == 0:
            print(count)
        writer_test.write(example.SerializeToString())
        i=i+1
writer_test.close()

with tf.Session() as sess:
    init_op = tf.global_variables_initializer()
    sess.run(init_op)
