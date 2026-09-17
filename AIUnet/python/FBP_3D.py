import tensorflow as tf
import numpy as np
from ctypes import *
import numpy as np
import math as math
import os
import time
from config import *
import matplotlib.pyplot as plt 
import tools

os.environ["CUDA_VISIBLE_DEVICES"] = "1"

cuda_op_module = tf.load_op_library('/data/tanyh/V1/code_zhu/CBCT/conebeam/Atx/Atx.so')

# dir(cuda_op_module)
# cuda_op_module.OP_LIST

imgData_Sino = np.fromfile('./test_phase_2.raw', dtype=np.float32)
imgData_Sino = np.reshape(imgData_Sino, [512,512,361])

# imgData_Sino = np.reshape(imgData_Sino, [361,1024,1024])
# imgData_Sino = np.transpose(imgData_Sino, (1, 2, 0))
# imgData_Sino = imgData_Sino.reshape(512, 2, 512, 2, 361).mean(axis=(1, 3))
# imgData_Sino.astype(np.float32).tofile('test_phase_2.raw')
imgData_Sino = imgData_Sino.reshape(512, 1, 512, 1, 361).mean(axis=(1, 3))
# imgData_Sino = np.reshape(imgData_Sino, [256,256,361])
tools.draw_twoD_figure(imgData_Sino[:,:,90])
plt.show()
# # int Batch_size;	
# # float SO;
# # float OD;
# # float scale;
# # float dy_det;
# # float y_os;
# # float dz;
# # int nx;
# # int ny;
# # int nz;
# # int nt;
# # int na;
# # int nb;
# # int nv;
# # float nv_pi;
# # int tmp_size;
# # int nv_block;
# # int filter;
# if __name__ == "__main__":
# out = cuda_op_module.atx(imgData_Sino,BATCH_SIZE,SO,OD,scale,det_size,y_os,dz,256,256,20,nt,128,128,Views,nv_pi,nv_pi,4,0)
out = cuda_op_module.atx(imgData_Sino,1,1000,500,1,0.75,0,1,256,256,33,1,512,128,361,180,180,4,0)
sess = tf.Session()
p1 = time.time()
result = sess.run(out)
p2 = time.time()
print(p2-p1)
# print(result)
result.astype(np.float32).tofile('./CT_recon_3D.raw')
