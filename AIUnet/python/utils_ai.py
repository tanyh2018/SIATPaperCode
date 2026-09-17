#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/26 下午2:39
# @Author  : Sesame CT
# @describe :工具函数
# @File    : utils.py
import tensorflow as tf
import numpy as np

from config import BATCH_SIZE, rotate_num, detector_num


def leaky_relu(x, alpha=0.2):
    return tf.maximum(tf.minimum(0.0, alpha * x), x)


def relu(x):
    return tf.nn.relu(x)


def concat(input):
    concat = tf.concat(input, axis=3, name='concat')
    return concat


def getsplit(x, dim, channel=3):
    x_tmp = tf.split(x, channel, axis=3)[dim]
    return x_tmp


def getloss(tensor1, tensor2, name):
    return tf.reduce_mean(tf.squared_difference(tensor1, tensor2), name=name)


def getmassloss(label_BM, output):
    """
    计算mass约束
    :param label_BM:
    :param output:
    :return:
    """
    label_tensor = getsplit(label_BM, 0) / 5.0 + getsplit(label_BM, 1) / 4.94 + getsplit(label_BM, 2)
    out_tensor = getsplit(output, 0) / 5.0 + getsplit(output, 1) / 4.94 + getsplit(output, 2)
    bool_mask = label_tensor > 0.9999
    label = tf.boolean_mask(label_tensor, bool_mask)
    output = tf.boolean_mask(out_tensor, bool_mask)

    return tf.reduce_mean(tf.squared_difference(label, output), name="loss_mass")


def concat_sino(x, num):
    x = tf.split(x, num, axis=3)
    out = []
    for i in x:
        out.append(tf.reshape(i, [BATCH_SIZE, rotate_num, detector_num, 1]))
    return tf.concat(out, axis=1)
