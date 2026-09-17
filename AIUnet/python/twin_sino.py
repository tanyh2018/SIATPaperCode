
from multiprocessing.pool import Pool
import numpy as np
import time
import os
import tools
import matplotlib.pyplot as plt 
from config import *
import sys

def main():
    path_name = sys.argv[1]
    images = os.listdir(path_name)
    images = [os.path.join(path_name, img) for img in images]
    images = images[:]
    p1 = time.time()  # temp
    cores = 30
    pool = Pool(processes=cores)
    pool.map(twin_img, images)
    p2 = time.time()
    print(p2 - p1)

def twin_img(img_path):
    # 设置参数
    M=8
    # I0 = 1000
    Nimg2 = (720,600)
    #phase_range = np.linspace(1,6.54,30)
    # phase_range = np.linspace(1.0,np.pi,10)
    # I0s = np.linspace(100,np.pi,10)
    # N_shift = N_shift
    # 读取吸收信息
    file_path = os.path.join(img_path)
    with open(file_path, 'rb') as fid_3:
        sino_2 = np.fromfile(fid_3, dtype=np.float32).reshape(Nimg2)
    # 读取相位信息
    sino_1 = sino_2*358.8
 
    # 循环计算
    for ss in range(20):
        I0 = np.random.uniform(500, 10000)
        prp = np.random.uniform(0.5,2.8)
        sino_1,sino_2 = get_scale_phase_factor(sino_1,sino_2,prp)
        exp_sino = np.exp(-sino_2)
        # 进行计算
        raw_phase = shift_left(sino_1,N_shift,'phase') - shift_right(sino_1,N_shift,'phase')
        raw_absor = (shift_left(exp_sino,N_shift,'absor') + shift_right(exp_sino,N_shift,'absor'))/2.0       
        Isig = np.ones((M,Nimg2[0],Nimg2[1]))
        phi_final,Isig,noise= phase_step(Isig,raw_phase,raw_absor,I0,M)
        input_name = img_path.split('/')[-1]
        raw_phase = raw_phase + noise
        phi_final.astype(np.float32).tofile(sys.argv[2] + 'phase_' + str(ss) + '_' + str(round(prp,2)) + '_' + input_name)
        print(sys.argv[2] + 'phase_' + str(ss) + '_' + str(round(prp,2)) + '_' + input_name)
        if sys.argv[3] == 'train':
            sino_1.astype(np.float32).tofile(sys.argv[2]  + 'phaseref_' +  str(ss) + '_' + str(round(prp,2)) + '_' + input_name)
        #raw_phase.astype(np.float32).tofile(sino_out_itenfile + 'phase_' + str(round(prp,2)) + '_' + input_name)

def get_scale_phase_factor(sino_1,sino_2,prp):
    smax = np.max(sino_1)
    smin = np.min(sino_1)
    if abs(smax) >= abs(smin):
        max = abs(smax)
    else:
        max = abs(smin)
    percent = prp / max
    sino_1 = sino_1*percent
    sino_2 = sino_2*percent
    return sino_1, sino_2

def phase_step(Isig,raw_phase,raw_absor,I0,M):
    Nx, Ny, Nz = Isig.shape
    eps = 0.7
    Ibkg = np.ones_like(Isig)
    ab_bkg = np.ones_like(raw_absor)
    phase_bkg = np.zeros_like(raw_phase)
    Isig = I0 * raw_absor * (1 + eps * np.cos(2 * np.pi * np.arange(Nx)[:, None, None] / M + raw_phase))
    Ibkg = I0 * ab_bkg * (1 + eps * np.cos(2 * np.pi * np.arange(Nx)[:, None, None] / M + phase_bkg))
    Isig = np.random.poisson(Isig)
    Ibkg = np.random.poisson(Ibkg)
    Isig = Isig/I0
    Ibkg = Ibkg/I0
    phi_final = fft_result(Isig,Ibkg)
    raw_phase2 = (raw_phase + np.pi)%(2.*np.pi) - np.pi
    # tools.draw_twoD_figure(phi_final)
    # tools.draw_twoD_figure(raw_phase2-phi_final)
    noise = phi_final - raw_phase2
    noise[noise > np.pi]  -= 2*np.pi
    noise[noise < -np.pi]  += 2*np.pi
    return phi_final,Isig,noise

def fft_result(sdata,bgdata):
    FTout_obj =  get_phi_with_fft(sdata)
    FTout_bkg =  get_phi_with_fft(bgdata)
    phi_final = result_info(FTout_obj,FTout_bkg)
    return phi_final
    #return phi_final,absor_final

def get_phi_with_fft(input_datas):
    input_datas = np.array(input_datas)
    FTout = np.fft.fft(input_datas,int(len(input_datas)),0)
    return FTout

def result_info(fin_obj, fin_bkg):
    obj_phi = np.angle(fin_obj[1,:])
    bkg_phi = np.angle(fin_bkg[1,:])
    phi_final = obj_phi - bkg_phi
    phi_final = (phi_final + np.pi)%(2.*np.pi) - np.pi
    # obj_absor = fin_obj[0,:]    
    # bkg_absor = fin_bkg[0,:]
    # absor_final = -np.log(obj_absor/bkg_absor)
    return phi_final
    #return phi_final,np.real(absor_final)


def shift_left(data,Nshift,model):
    # n = -1
    if model == 'phase':
        new_arr = np.zeros_like(data)
    elif model == 'absor':
        new_arr = np.ones_like(data)
    new_arr[:,Nshift:] = data[:,:-Nshift]
    return new_arr

def shift_right(data,Nshift,model):
    # n = 1
    if model == 'phase':
        new_arr = np.zeros_like(data)
    elif model == 'absor':
        new_arr = np.ones_like(data)
    new_arr[:,:-Nshift] = data[:,Nshift:]
    return new_arr

if __name__ == '__main__':
    main()