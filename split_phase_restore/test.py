#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/26 下午4:41
# @Author  : Sesame CT
# @describe :
# @File    : train.py
from utils import getloss, getsplit
from nets import *
# from config import *
import numpy as np
import datetime
import os


os.environ["CUDA_VISIBLE_DEVICES"] = "0"

if not os.path.exists('./checkpoints'):
    os.mkdir('./checkpoints')

if not os.path.exists('./logs'):
    os.mkdir('./logs')

if not os.path.exists('./outputs'):
    os.mkdir('./outputs')


class Test(object):
    def __init__(self, XX_Net, gen_batch, BATCH_SIZE, Views, NumDet):
        self.XX_Net = XX_Net
        self.gen_batch = gen_batch
        self.BATCH_SIZE = BATCH_SIZE
        self.Views = Views
        self.NumDet = NumDet
        self.bowtie_img_batch, self.single_energy_img_batch = self.gen_batch()
        self.label_single_energy = tf.placeholder(tf.float32, [self.Views*BATCH_SIZE, 1, NumDet, 1], name='label_single_energy')
        self.input_bowtie_energy = tf.placeholder(tf.float32, [self.Views*BATCH_SIZE, 1, NumDet, 1], name='input_bowtie_energy')

        # nets
        self.single_energy_output = self.XX_Net(self.input_bowtie_energy)
        self.saver = tf.train.Saver()

    def load_data(self, L_path):
        L_img = np.fromfile(L_path, dtype=np.float32)
        L_img = np.reshape(L_img, [rotate_num, detector_num])
        return L_img

    def test(self, Img_path,output_path):
        self.Img_path = Img_path
        self.tf_config = tf.ConfigProto()
        self.tf_config.gpu_options.allow_growth = True
        self.sess = tf.Session(config=self.tf_config)
        self.sess.run([tf.global_variables_initializer(), tf.local_variables_initializer()])
        self.saver.restore(self.sess, save_path='./checkpoints/check_CT_taining_2023_6_21_118800')
        self.start_time = datetime.datetime.now()
        self.start_timeALL = datetime.datetime.now()
        coord = tf.train.Coordinator()
        # threads = tf.train.start_queue_runners(sess=self.sess, coord=coord)

        try:
            for steps in range(1):
                input_single_label = self.load_data(Img_path)
                # L_img = np.transpose(L_img, [])
                input_single_label = np.expand_dims(input_single_label, axis=1)
                input_single_label = np.expand_dims(input_single_label, axis=-1)
                feed_dict = {self.input_bowtie_energy: input_single_label}

                save_single_energy_output = self.sess.run(self.single_energy_output, feed_dict=feed_dict)
                save_single_energy_output = np.transpose(save_single_energy_output, [1, 0, 2, 3])
                save_single_energy_output[0, :, :, :].astype(np.float32).tofile(output_path)

        except tf.errors.OutOfRangeError:
            print('Done training -- epoch limit reached')
            durationAll = datetime.datetime.now() - self.start_timeALL
            print("Duration ALL %ss" % (durationAll.seconds))
        finally:
            # coord.request_stop()
            pass
def create_file_path(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)  

if __name__ == '__main__':
    XX_Net = XX_Net()
    # BATCH_SIZE = 1
    gen_batch = Gen_Batch(sourceDir=sourceDir, tfFile=tfFile, BATCH_SIZE=BATCH_SIZE,
                        BATCH_THREAD_NUMBER=BATCH_THREAD_NUMBER, BATCH_CAPACITY=BATCH_CAPACITY,
                        MIN_AFTER_DEQUEUE=MIN_AFTER_DEQUEUE, pixels=pixels, Views=Views, NumDet=NumDet)

    test_root = Test(XX_Net, gen_batch, BATCH_SIZE, Views, NumDet)

    for file_name in os.listdir(input_path_test):
        img_path = input_path_test + file_name
        output_path1 = output_path_test + file_name
        test_root.test(img_path,output_path1)
