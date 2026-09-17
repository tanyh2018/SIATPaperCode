import tensorflow as tf
import numpy as np
from config import *

input_img = tf.placeholder(tf.float32, [rotate_num, detector_num], name="input_CT")
out = ATX.atx(input_img, BATCH_SIZE, SO, OD, scale, img_size,
               img_size, detector_num, det_size, y_os, nt,
               tmp_size, rotate_num, nv_pi, 0)

if __name__ == "__main__":
    # input = np.fromfile('./H.raw', dtype=np.float32)
    input = np.fromfile('/media/newHD1/JTZ/Workspace/DECT/idoine_cacl2_water_2/v11/新光谱数据/I2/仿真/0_sino_low.raw', dtype=np.float32)
    input = input.reshape([rotate_num, detector_num])
    sess = tf.Session()
    result = sess.run(out, feed_dict={input_img:input})
    print(result)
    result.astype(np.float32).tofile('/media/newHD1/JTZ/Workspace/DECT/idoine_cacl2_water_2/v11/新光谱数据/I2/仿真/low_FBP.raw')
