#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/26 下午4:41
# @Author  : Sesame CT
# @describe :
# @File    : train.py
from utils_ai import getloss
from nets import *
from config import *
import numpy as np
import datetime
import os
import sys

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

if not os.path.exists(sys.argv[2]+'/checkpoints'):
    os.mkdir(sys.argv[2]+'checkpoints')

if not os.path.exists(sys.argv[2]+'logs'):
    os.mkdir(sys.argv[2]+'logs')

if not os.path.exists(sys.argv[2]+'outputs'):
    os.mkdir(sys.argv[2]+'outputs')


class Train(object):
    def __init__(self, XX_Net, gen_batch, BATCH_SIZE, Views, NumDet):
        self.XX_Net = XX_Net
        self.gen_batch = gen_batch
        self.BATCH_SIZE = BATCH_SIZE
        self.Views = Views
        self.NumDet = NumDet
        self.bowtie_img_batch, self.single_energy_img_batch = self.gen_batch()
        self.label_single_energy = tf.placeholder(tf.float32, [self.Views * BATCH_SIZE, 1, NumDet, 1],
                                                  name='label_single_energy')
        self.input_bowtie_energy = tf.placeholder(tf.float32, [self.Views * BATCH_SIZE, 1, NumDet, 1],
                                                  name='input_bowtie_energy')

        # nets
        self.single_energy_output = self.XX_Net(self.input_bowtie_energy)

        # loss
        self.loss = getloss(self.label_single_energy, self.single_energy_output, name='loss')

        # optmizer
        self.start_learning_rate = 1e-4
        self.decay_rate = 0.98
        self.decay_step = 1000
        self.global_steps = tf.Variable(tf.constant(0))
        self.Learining_rate = tf.train.exponential_decay(self.start_learning_rate, self.global_steps, self.decay_step,
                                                         self.decay_rate, staircase=True)

        self.Optmizer = tf.train.AdamOptimizer(learning_rate=self.Learining_rate).minimize(self.loss,
                                                                                           var_list=[var for var in
                                                                                                     tf.global_variables()])

        self.tensorboardshow()
        self.merged = tf.summary.merge_all()
        self.train_writer = tf.summary.FileWriter(sys.argv[2]+'/logs/', tf.get_default_graph())

        self.saver = tf.train.Saver()

    def tensorboardshow(self):
        # with tf.name_scope('SinogramShow'):
        #     tf.summary.image("input_bowtie_energy", self.input_bowtie_energy, 1)
        #     tf.summary.image("single_energy_output", self.single_energy_output, 1)
        #     tf.summary.image("label_single_energy", self.label_single_energy, 1)

        with tf.name_scope('Loss'):
            tf.summary.scalar('loss', self.loss)

    def train(self, train_steps=1000000):
        self.tf_config = tf.ConfigProto()
        self.tf_config.gpu_options.allow_growth = True
        self.sess = tf.Session(config=self.tf_config)

        self.sess.run([tf.global_variables_initializer(), tf.local_variables_initializer()])
        #self.saver.restore(self.sess, save_path=sys.argv[2] + 'checkpoints/check_CT_taining_')
        #self.saver.restore(self.sess, save_path='/data/tanyh/twin_img_AL/AIresult/twin_train/20240108_train/checkpoints/twin20240108_result_13000')
        self.start_time = datetime.datetime.now()
        self.start_timeALL = datetime.datetime.now()
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=self.sess, coord=coord)

        try:
            for steps in range(1, train_steps):
                bowtie_input, single_label  = self.sess.run(
                    [self.bowtie_img_batch, self.single_energy_img_batch])
                # single_label = np.delete(single_label, [0, 1, 2, 3, 4, 5, 699, 698, 697, 696, 695, 694], 2)
                # bowtie_input = np.delete(bowtie_input, [0, 1, 2, 3, 4, 5, 699, 698, 697, 696, 695, 694], 2)
                # for angle in range(Views):
                if BATCH_SIZE == 1:
                    single_label = np.transpose(single_label, (1, 0, 2, 3))
                    bowtie_input = np.transpose(bowtie_input, (1, 0, 2, 3))
                else:
                    single_label = np.reshape(single_label, [-1, 700, 1])
                    bowtie_input = np.reshape(bowtie_input, [-1, 700, 1])
                    single_label = np.expand_dims(single_label, axis=1)
                    bowtie_input = np.expand_dims(bowtie_input, axis=1)

                feed_dict = {
                    self.input_bowtie_energy: bowtie_input,
                    self.label_single_energy: single_label
                }

                summary, _, self.train_step_loss = self.sess.run([self.merged, self.Optmizer, self.loss],
                                                                 feed_dict=feed_dict)

                if steps % 1 == 0:
                    self.train_writer.add_summary(summary, steps)
                    duration = datetime.datetime.now() - self.start_time
                    self.start_time = datetime.datetime.now()
                    print("Duration %ss, CT_Loss at step %s: %s" % (duration.seconds, steps, self.train_step_loss))

                if steps % 200 == 0:
                    save_path = self.saver.save(self.sess, sys.argv[2]+"/checkpoints/"+sys.argv[3]+"_{}".format(str(steps)))
                    print("Model saved in file: %s loss=%s" % (save_path, self.train_step_loss))

        except tf.errors.OutOfRangeError:
            print('Done training -- epoch limit reached')
            durationAll = datetime.datetime.now() - self.start_timeALL
            print("Duration ALL %ss" % (durationAll.seconds))
        finally:
            coord.request_stop()

        coord.join(threads)
        self.sess.close()


if __name__ == '__main__':
    XX_Net = XX_Net()

    gen_batch = Gen_Batch(inputfile=sys.argv[1], BATCH_SIZE=BATCH_SIZE,
                          BATCH_THREAD_NUMBER=BATCH_THREAD_NUMBER, BATCH_CAPACITY=BATCH_CAPACITY,
                          MIN_AFTER_DEQUEUE=MIN_AFTER_DEQUEUE, pixels=img_size, Views=rotate_num, NumDet=detector_num)

    train_root = Train(XX_Net, gen_batch, BATCH_SIZE, rotate_num, detector_num)
    train_root.train()
