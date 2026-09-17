#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/26 下午2:39
# @Author  : Sesame CT
# @describe :网络代码
# @File    : nets.py
import tensorflow.contrib.layers as tcl
import tensorflow as tf
from tensorflow.python.framework import ops
from utils import leaky_relu, relu, concat
from config import *


class XX_Net(object):
    def __init__(self):
        self.name = 'XX_net'

    def __call__(self, x):
        with tf.variable_scope(self.name):
            conv1 = tcl.conv2d(x, num_outputs=32, kernel_size=[1, 5], stride=1, activation_fn=leaky_relu)
            conv2 = tcl.conv2d(conv1, num_outputs=64, kernel_size=[1, 5], stride=1, activation_fn=leaky_relu)
            conv3 = tcl.conv2d(conv2, num_outputs=96, kernel_size=[1, 5], stride=1, activation_fn=leaky_relu)
            conv4 = tcl.conv2d(conv3, num_outputs=128, kernel_size=[1, 5], stride=1, activation_fn=leaky_relu)
            conv5 = tcl.conv2d(conv4, num_outputs=160, kernel_size=[1, 5], stride=1, activation_fn=leaky_relu)
            conv6 = tcl.conv2d(conv5, num_outputs=192, kernel_size=[1, 5], stride=1, activation_fn=leaky_relu)
            conv7 = tcl.conv2d(conv6, num_outputs=224, kernel_size=[1, 5], stride=1, activation_fn=leaky_relu)
            conv8 = tcl.conv2d(conv7, num_outputs=256, kernel_size=[1, 5], stride=1, activation_fn=leaky_relu)
            conv9 = tcl.conv2d(conv8, num_outputs=224, kernel_size=[1, 5], stride=1, activation_fn=leaky_relu)
            conv10 = tcl.conv2d(conv9, num_outputs=192, kernel_size=[1, 5], stride=1, activation_fn=leaky_relu)
            conv11 = tcl.conv2d(conv10, num_outputs=160, kernel_size=[1, 5], stride=1, activation_fn=leaky_relu)
            conv12 = tcl.conv2d(conv11, num_outputs=128, kernel_size=[1, 5], stride=1, activation_fn=leaky_relu)
            conv13 = tcl.conv2d(conv12, num_outputs=96, kernel_size=[1, 5], stride=1, activation_fn=leaky_relu)
            conv14 = tcl.conv2d(conv13, num_outputs=64, kernel_size=[1, 5], stride=1, activation_fn=leaky_relu)
            conv15 = tcl.conv2d(conv14, num_outputs=32, kernel_size=[1, 5], stride=1, activation_fn=leaky_relu)

            flatten_x = tcl.flatten(conv15)
            flatten_1 = tcl.fully_connected(flatten_x, NumDet, activation_fn=tf.nn.leaky_relu)
            output = tf.reshape(flatten_1, [Views * BATCH_SIZE, 1, NumDet, 1])
            return output

    @property
    def vars(self):
        return [var for var in tf.global_variables() if self.name in var.name]


class Gen_Batch(object):
    def __init__(self, **kwargs):
        self.sourceDir = kwargs["sourceDir"]
        self.tfFile = kwargs["tfFile"]
        self.BATCH_SIZE = kwargs["BATCH_SIZE"]
        self.BATCH_THREAD_NUMBER = kwargs["BATCH_THREAD_NUMBER"]
        self.BATCH_CAPACITY = kwargs["BATCH_CAPACITY"]
        self.MIN_AFTER_DEQUEUE = kwargs["MIN_AFTER_DEQUEUE"]
        self.pixels = kwargs["pixels"]
        self.Views = kwargs["Views"]
        self.NumDet = kwargs["NumDet"]

    def __call__(self):
        with tf.name_scope('Gen_Batches'):
            bowtie_img, single_energy_img = self.read_and_decode_single_example()
            bowtie_img_batch, single_energy_img_batch = tf.train.shuffle_batch(
                [bowtie_img, single_energy_img],
                batch_size=self.BATCH_SIZE,
                num_threads=self.BATCH_THREAD_NUMBER,
                capacity=self.BATCH_CAPACITY,
                min_after_dequeue=self.MIN_AFTER_DEQUEUE)
            bowtie_img_batch = tf.reshape(bowtie_img_batch, [self.BATCH_SIZE, self.Views, self.NumDet, 1])
            single_energy_img_batch = tf.reshape(single_energy_img_batch, [self.BATCH_SIZE, self.Views, self.NumDet, 1])
        return bowtie_img_batch, single_energy_img_batch

    def read_and_decode_single_example(self):
        filename_queue = tf.train.string_input_producer([self.sourceDir + self.tfFile], num_epochs=10000, shuffle=False)
        reader = tf.TFRecordReader()
        _, serialized_example = reader.read(filename_queue)
        features = tf.parse_single_example(
            serialized_example,
            features={
                'wrap_img': tf.FixedLenFeature([], tf.string),
                'ref_img': tf.FixedLenFeature([], tf.string),
            })
        bowtie_img = tf.decode_raw(features['wrap_img'], tf.float32)
        bowtie_img = tf.reshape(bowtie_img, [self.Views, self.NumDet])

        single_energy_img = tf.decode_raw(features['ref_img'], tf.float32)
        single_energy_img = tf.reshape(single_energy_img, [self.Views, self.NumDet])

        return bowtie_img, single_energy_img


if __name__ == '__main__':
    XX_Net = XX_Net()
    tensor1 = tf.placeholder(tf.float32, [BATCH_SIZE, 1, NumDet, 1])
    XX_Net(tensor1)
