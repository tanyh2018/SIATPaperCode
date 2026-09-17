#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/7/5 上午11:19
# @Author  : Sesame CT
# @describe :
# @File    : Genimg.py
import os
import cv2
import random
from config import *
from utils import DrawImage, GenCircularCoordAndRadius
import numpy as np
from multiprocessing.pool import Pool
import time
import copy


def imadjust(img, low_in, high_in, low_out, high_out, gamma=1):
    """
    matlab imadjust仿写
    :param img:
    :param low_in:
    :param high_in:
    :param low_out:
    :param high_out:
    :param gamma:
    :return:
    """
    img_adj = ((img - low_in) / (high_in - low_in)) ** gamma
    img_adj = img_adj * (high_out - low_out) + low_out
    img_adj[img <= low_in] = low_out
    img_adj[img >= high_in] = high_out

    return img_adj


def blood_vessel(a, b, O_i, O_j):
    """
    生成血管
    :param a:  椭圆的轴
    :param b: 椭圆的轴
    :param O_i: 椭圆中心坐标
    :param O_j: 椭圆中心坐标
    :return:
    """
    bv_mask = np.zeros([img_size, img_size])

    num = random.randint(4, 6)  # 生成血管个数
    a = a - 10  # 防止生成的血管过于靠近图像边缘
    b = b - 10
    for index in range(num):

        x = random.randint(O_i - b, O_i + b)

        y = random.randint(O_j - a, O_j + a)

        bv_a = random.uniform(20.0, 60.0) / 2

        bv_b = bv_a * random.uniform(0.98, 1.02)

        value = random.uniform(0.002, 0.03)  # 实验碘的浓度范围
        for i in range(O_i - b, O_i + b):
            for j in range(O_j - a, O_j + a):
                if (j - x) ** 2 / (bv_a ** 2) + (i - y) ** 2 / bv_b ** 2 <= 1:
                    # bv_mask[i, j] = value + (value * random.uniform(-0.045, 0.045)) #添加随机噪声
                    bv_mask[i, j] = value
    return bv_mask


def circ_mask():
    """
    随机生成mask 椭圆
    :param img_size:
    :return:
    """

    a = img_size / (2.5 + random.random())
    # b = img_size / (2.5 + random.random())
    b = a
    circ_mask = np.zeros([img_size, img_size])

    O_i = img_size // 2 + random.randint(-4, 4) * 4

    O_j = img_size // 2 + random.randint(-4, 4) * 4
    for i in range(img_size):
        for j in range(img_size):
            if (j - O_j) ** 2 / (a ** 2) + (i - O_i) ** 2 / b ** 2 <= 1:
                circ_mask[i, j] = 1
    return circ_mask[:, :], a, b, O_i, O_j


def blur_img(img_mask, img_input, is_bone=False):
    """
    羽化边缘
    Canny边缘提取
    用dilate做膨化，用一个粗颗粒，再用一个细颗粒
    粗颗粒的膨化结果用于提取原图像，之后，再做高斯模糊
    细颗粒的膨化结果用于定位覆盖掉原图像的结果，将边缘部分贴回去
    :param img:
    :return:
    """
    img_mask[img_mask != 0] = 255
    img = np.asarray(img_mask, dtype=np.uint8)  # 计算边缘用
    g = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 细颗粒
    g2 = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))  # 粗颗粒
    imgCanny = cv2.Canny(img, threshold1=50, threshold2=220)
    water_density = np.zeros([img_size, img_size], dtype=np.float32)  # 骨头中水的密度
    # 膨化处理
    # 更细腻
    img_dilate = cv2.dilate(imgCanny, g)
    # 更粗大
    img_dilate2 = cv2.dilate(imgCanny, g2)

    # shape = img_dilate.shape
    img_temp = copy.deepcopy(img_input)
    img_output = copy.deepcopy(img_input)
    # 提取
    img_temp[img_dilate2 == 0] = 0

    dst = cv2.GaussianBlur(img_temp, (3, 3), 0, 0, cv2.BORDER_DEFAULT)

    if is_bone:
        choice_index = random.choice([1, 2, 3])
        if choice_index == 1:  # 返回带有骨髓的骨头
            img_output[img_dilate != 0] = 0  # 将骨头边界置为0,用于生成水
            Bone_img = dst  # 骨头边缘图像
            Bone_mean = Bone_img[np.nonzero(Bone_img)].mean()  # 找出骨头图像中的最小值
            if Bone_mean > 1.4:
                Bone_mean = 1.4

            water_img = img_output  # 水图像
            water_max = np.max(water_img[np.nonzero(water_img)])
            water_min = np.min(water_img[np.nonzero(water_img)])

            if Bone_mean > water_max:  # 如果骨头中的最小值大于水中的最大值，不做处理
                water_density[water_img != 0] = 1.0 - (water_img[water_img != 0] / 1.4)
                img_output[img_dilate != 0] = Bone_img[img_dilate != 0]
            else:  # 若相反，需要将水中的值进行缩放处理。
                # ratio = Bone_mean / water_max
                water_img = imadjust(water_img, low_in=water_min, high_in=water_max, low_out=0, high_out=Bone_mean,
                                     gamma=1)
                water_density[water_img != 0] = 1.0 - (water_img[water_img != 0] / 1.4)
                img_output[img_dilate != 0] = dst[img_dilate != 0]
                img_output[water_img != 0] = water_img[water_img != 0]

        elif choice_index ==2: #返回只有边界的骨头
            Bone_img = dst  # 骨头边缘图像
            img_output = Bone_img

        elif choice_index == 3: #返回纯骨头
            img_output[img_dilate != 0] = dst[img_dilate != 0]
    else:
        img_output[img_dilate != 0] = dst[img_dilate != 0]
    return img_output, water_density


def genbasis_imgs(img_path):
    """
    :param img: 输入通道BGR
    :return:
    """
    name = img_path.split('_')[-1]
    name = name.split('.')[0]
    name = str(int(name))
    im_bgr = cv2.imread(img_path)
    im_rgb = im_bgr[:, :, ::-1]

    # 直方图均衡
    for i in range(3):
        im_rgb[:, :, i] = cv2.equalizeHist(im_rgb[:, :, i])

    shape = im_rgb.shape
    if shape[2] < 3:
        return
    img = cv2.resize(im_rgb, (img_size, img_size))
    img = img.astype(np.float32) / 255.0

    R_img = img[:, :, 0]

    img = cv2.resize(img, (64, 64))  # 模糊图像
    img = cv2.resize(img, (img_size, img_size))  # 模糊图像

    img[img < 0] = 0

    R_channel = img[:, :, 0]
    G_channel = img[:, :, 1]
    B_channel = img[:, :, 2]

    sum_RGB = R_channel + G_channel + B_channel

    Circ_mask, a, b, O_i, O_j = circ_mask()  # 生成圆形
    I2_tubes = GenCircularCoordAndRadius(int(a), int(O_i), int(O_j))  # 试管的坐标与半径
    I2_mask = DrawImage(I2_tubes)
    # I2_mask = blood_vessel(math.ceil(a), math.ceil(b), O_i, O_j)  # 生成血管造影图
    I2_mask_bool = np.array(I2_mask, dtype=bool)
    # I2_mask_contrary_bool = np.array(1 - I2_mask_bool, dtype=bool)

    bone_mask = R_channel >= threshold4
    bone_mask = bone_mask * Circ_mask
    if (np.sum(bone_mask == 1) / np.sum(Circ_mask == 1)) <= 0.4 and (
            np.sum(bone_mask == 1) / np.sum(Circ_mask == 1)) >= 0.2:  # 划定骨头面积范围到10%-30%之间
        Bone_adj = imadjust(R_img, low_in=threshold3, high_in=1, low_out=0.6, high_out=1, gamma=1)
        Bone_img = Bone_adj * bone_mask * (0.8 + random.randint(0, 2) * 0.2)
        # I2_mask = R_channel <= (threshold3 - 0.1)
        # I2_adj = imadjust(R_img, low_in=0, high_in=threshold3 - 0.1, low_out=threshold4, high_out=1, gamma=1)
        # I2_img = I2_adj * I2_mask
        I2_img = I2_mask

        water_mask = (R_channel < threshold4) & (R_channel >= threshold1)
        water_adj = imadjust(R_img, low_in=threshold1, high_in=threshold4, low_out=threshold4, high_out=1.15,
                             gamma=1)  # 肌肉1.15
        water_img = water_adj * water_mask

        Basis_bone = Bone_img * bone_density * Circ_mask
        Basis_bone, Bone_water_density = blur_img(bone_mask, Basis_bone, is_bone=True)
        Basis_bone[I2_mask_bool] = 0  # 有碘的地方不能有骨头

        # Basis_water = (water_img * (1 - I2_mask) * water_density + Bone_img * bone_density * 0.1)
        Basis_water = water_img * (1 - I2_mask) * water_density
        Basis_water, _ = blur_img(water_mask, Basis_water, is_bone=False)
        Basis_water = Basis_water + Bone_water_density
        Basis_water[I2_mask_bool] = (1 - I2_img[I2_mask_bool] / 4.94)
        Basis_water = (Basis_water) * Circ_mask

        Basis_I2 = I2_img * Circ_mask
        Basis_I2, _ = blur_img(I2_mask, Basis_I2, is_bone=False)

        Basis_water.astype(np.float32).tofile(save_ct_path + '{}_label_water.raw'.format(name))
        # Basis_I2.astype(np.float32).tofile(save_ct_path + '{}_label_I2.raw'.format(name))
        Basis_bone.astype(np.float32).tofile(save_ct_path + '{}_label_bone.raw'.format(name))


if __name__ == '__main__':
    path = '/media/nic89/ZJT 4.0T/实验数据/ILSVRC2012_img_test/'
    # path = './Pic_ImgNet/'
    images = os.listdir(path)
    images = [os.path.join(path, img) for img in images]
    images = images[10000:10200]
    # images = ['/media/newHD1/JTZ/Workspace/实验数据/ILSVRC2012_img_test/ILSVRC2012_test_00075991.JPEG']

    p1 = time.time()  # temp
    cores = 6
    pool = Pool(processes=cores)
    pool.map(genbasis_imgs, images)
    p2 = time.time()
    print(p2 - p1)

    # cnt = 0
    # for img in images:
    #     im_bgr = cv2.imread(os.path.join('./Pic_ImgNet', img))
    #     im_rgb = im_bgr[:, :, ::-1]
    #
    #     name = img.split('.')[0]
    #     genbasis_imgs(im_rgb, name)
