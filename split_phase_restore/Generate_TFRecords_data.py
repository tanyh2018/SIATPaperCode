# `ctrl+alt+L`??????
# ???????????RAW??
import matplotlib.pyplot as plt 
import tensorflow as tf
from config import *
import numpy as np
import sys
import os

Data_path = './code_zhu/PPT/wrap'
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

wrap_imgs = Data_path + '/wrap_20230621_more/'  # can be both absolute path and relative path
nowrap_imgs = Data_path + '/raw_20230621_more/'  # can be both absolute path and relative path
if not os.path.exists('./train_data/TFrecord/'):
    os.mkdir('./train_data/TFrecord/')

writer_test = tf.python_io.TFRecordWriter(sourceDir + tfFile)

wrap_image_files = os.listdir(wrap_imgs)
wrap_image_files = [(img.split('phase_')[-1]).split('.raw')[0] for img in wrap_image_files]
wrap_image_files = set(wrap_image_files)

count = 1
# Views = 720
# NumDet = 600
for index in wrap_image_files:
    tf.reset_default_graph()
    wrap_img = np.fromfile(wrap_imgs + 'phase_{}.raw'.format(index), dtype='float32',
                                sep="")
    if wrap_img.size == Views*NumDet:
        wrap_img =wrap_img.reshape([Views, NumDet])
    else:
        continue

    nowrap_img = np.fromfile(nowrap_imgs + 'phase_{}.raw'.format(index), dtype='float32',
                                sep="")
    if wrap_img.size == Views*NumDet:
            nowrap_img = nowrap_img.reshape([Views, NumDet])
    else:
        continue

    img_raw_0 = wrap_img.tobytes()
    img_raw_1 = nowrap_img.tobytes()

    example = tf.train.Example(features=tf.train.Features(feature={
        'wrap_img': tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw_0])),
        'ref_img': tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw_1])),
    }))
    count += 1
    if count % 100 == 0:
        print(count)
    writer_test.write(example.SerializeToString())
writer_test.close()

with tf.Session() as sess:
    init_op = tf.global_variables_initializer()
    sess.run(init_op)
