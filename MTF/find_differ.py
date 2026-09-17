import sys
import matplotlib.pyplot as plt 
import numpy as np
import os 
import math
#----------------------------------------
# Main Calculation defined here
#----------------------------------------

fs_sep_2_absor = 'period_7.1821_sep_2.50_sigma_1.55_absor_pixel_size_48_graphite_mono.raw'
fs_sep_2_phi = 'period_7.1821_sep_2.50_sigma_1.55_phi_pixel_size_48_graphite_mono.raw'
fs_sep_8_absor = 'period_2.3940_sep_7.50_sigma_1.55_absor_pixel_size_48_graphite_mono.raw'
fs_sep_8_phi = 'period_2.1124_sep_8.50_sigma_1.55_phi_pixel_size_48_graphite_mono.raw'
fs_sep_32_absor = 'period_0.5204_sep_34.50_sigma_1.55_absor_pixel_size_48_graphite_mono.raw'
fs_sep_32_phi = 'period_0.5204_sep_34.50_sigma_1.55_phi_pixel_size_48_graphite_mono.raw'

fp_sep_2_absor = 'period_8.0000_sep_2.24_sigma_1.55_absor_pixel_size_48_8.0000_poly.raw'
fp_sep_2_phi = 'period_8.0000_sep_2.24_sigma_1.55_phi_pixel_size_48_8.0000_poly.raw'
fp_sep_8_absor = 'period_2.1124_sep_8.50_sigma_1.55_absor_pixel_size_48_graphite_poly.raw'
fp_sep_8_phi = 'period_2.0000_sep_8.98_sigma_1.55_phi_pixel_size_48_graphite_poly.raw'
fp_sep_32_absor = 'period_0.5600_sep_32.06_sigma_1.55_absor_pixel_size_48_graphite_poly.raw'
fp_sep_32_phi = 'period_0.5600_sep_32.06_sigma_1.55_phi_pixel_size_48_graphite_poly.raw'


fc_sep_2_absor = 'period_8_sep_2.24_sigma_0.0_absor_pixel_size_48.0_m1_sd_2.raw'
fc_sep_2s_absor = 'period_8_sep_2.24_sigma_1.55_absor_pixel_size_48.0_m1_sd_2.raw'
fc_sep_2_phi = 'period_8_sep_2.24_sigma_0.0_phi_pixel_size_48.0_m1_sd_2.raw'
fc_sep_2s_phi = 'period_8_sep_2.24_sigma_1.55_phi_pixel_size_48.0_m1_sd_2.raw'

fc_sep_8_absor = 'period_8_sep_2.24_sigma_0.0_absor_pixel_size_48.0_m1_sd_8.raw'
fc_sep_8s_absor = 'period_8_sep_2.24_sigma_1.55_absor_pixel_size_48.0_m1_sd_8.raw'
fc_sep_8_phi = 'period_8_sep_2.24_sigma_0.0_phi_pixel_size_48.0_m1_sd_8.raw'
fc_sep_8s_phi = 'period_8_sep_2.24_sigma_1.55_phi_pixel_size_48.0_m1_sd_8.raw'

fc_sep_32_absor = 'period_8_sep_2.24_sigma_0.0_absor_pixel_size_48.0_m1_sd_32.raw'
fc_sep_32s_absor = 'period_8_sep_2.24_sigma_1.55_absor_pixel_size_48.0_m1_sd_32.raw'
fc_sep_32_phi = 'period_8_sep_2.24_sigma_0.0_phi_pixel_size_48.0_m1_sd_32.raw'
fc_sep_32s_phi = 'period_8_sep_2.24_sigma_1.55_phi_pixel_size_48.0_m1_sd_32.raw'

def main():

    # a1 = fs_sep_2_absor
    # a2 = fp_sep_2_absor
    # a3 = fc_sep_2_absor
    # a4 = fc_sep_2s_absor
    
    # p1 = fs_sep_2_phi
    # p2 = fp_sep_2_phi
    # p3 = fc_sep_2_phi
    # p4 = fc_sep_2s_phi
    # draw_diff([a1,a2,a3,a4,p1,p2,p3,p4])

    # a1 = fs_sep_8_absor
    # a2 = fp_sep_8_absor
    # a3 = fc_sep_8_absor
    # a4 = fc_sep_8s_absor
    # p1 = fs_sep_8_phi
    # p2 = fp_sep_8_phi
    # p3 = fc_sep_8_phi
    # p4 = fc_sep_8s_phi
    # draw_diff([a1,a2,a3,a4,p1,p2,p3,p4])
    
    # a1 = fs_sep_32_absor
    # a2 = fp_sep_32_absor
    # a3 = fc_sep_32_absor
    # a4 = fc_sep_32s_absor
    # p1 = fs_sep_32_phi
    # p2 = fp_sep_32_phi
    # p3 = fc_sep_32_phi
    # p4 = fc_sep_32s_phi
    # draw_diff([a1,a2,a3,a4,p1,p2,p3,p4])
    
    #absor
    mono = [fs_sep_2_absor,fs_sep_8_absor,fs_sep_32_absor]
    poly = [fp_sep_2_absor,fp_sep_8_absor,fp_sep_32_absor]
    s0 = [fc_sep_2_absor,fc_sep_8_absor,fc_sep_32_absor]
    s0s = [fc_sep_2s_absor,fc_sep_8s_absor,fc_sep_32s_absor]
    
    diff_deltas(mono,s0,'mono')
    plt.show()        
    
def draw_diff(dnames):
    shape = (360,100)
    fs = './data/delta_s_graphite_mono_30/'
    fsp = './data/delta_s_graphite_poly/'
    fc = './data/deltas_s_calculate_20240531/'    
    
    fs_2_act = fs + dnames[0]
    fs_2p_act = fsp + dnames[1]
    fc_2_act = fc + dnames[2]
    fc_2s_act = fc + dnames[3]
    
    fs_2_actd = read_raw_file(fs_2_act,shape)
    fs_2p_actd = read_raw_file(fs_2p_act,shape)
    fc_2_actd = read_raw_file(fc_2_act,shape)
    fc_2s_actd = read_raw_file(fc_2s_act,shape)
    
    lb1='sim_mono'
    lb2='sim_poly'
    lb3='cal_0'
    lb4='cal_1.55'
    fig1 = plt.figure(figsize=(9,6))
    plt.plot(normd(fs_2_actd[1,:]),label=lb1,lw=3,color='#44AFC6')
    plt.plot(normd(fs_2p_actd[1,:]),label=lb2,lw=3,color='#1A68FA')
    plt.plot(normd(fc_2_actd[1,:]),label=lb3,lw=3,color='#F38929')
    plt.plot(normd(fc_2s_actd[1,:]),label=lb4,lw=3,color='#fabed4')
    fig_setting()
    
    
    fs_2_phi = fs + dnames[4]
    fs_2p_phi = fsp + dnames[5]
    fc_2_phi = fc + dnames[6]
    fc_2s_phi = fc + dnames[7]
    
    fs_2_phid = read_raw_file(fs_2_phi,shape)
    fs_2p_phid = read_raw_file(fs_2p_phi,shape)
    fc_2_phid = read_raw_file(fc_2_phi,shape)
    fc_2s_phid = read_raw_file(fc_2s_phi,shape)
    
    fig1 = plt.figure(figsize=(9,6))
    plt.plot(normd(fs_2_phid[1,:]),label=lb1,lw=3,color='#44AFC6')
    plt.plot(normd(fs_2p_phid[1,:]),label=lb2,lw=3,color='#1A68FA')
    plt.plot(normd(fc_2_phid[1,:]),label=lb3,lw=3,color='#F38929')
    plt.plot(normd(fc_2s_phid[1,:]),label=lb4,lw=3,color='#fabed4')
    fig_setting()
    
def diff_deltas(data1,data2,stype):
    shape1 = (360,100)
    shape2 = (360,480)
    fs = './data/delta_s_graphite_mono_30/'
    fsp = './data/delta_s_graphite_poly/'
    fc = './data/deltas_s_calculate_20240601/'    
    if stype == 'mono':
        fs_2_act = fs + data1[0]
        fs_8_act = fs + data1[1]
        fs_32_act = fs + data1[2]
    else:
        fs_2_act = fsp + data1[0]
        fs_8_act = fsp + data1[1]
        fs_32_act = fsp + data1[2]
    fc_2_act = fc + data2[0]
    fc_8_act = fc + data2[1]
    fc_32_act = fc + data2[2]
            
    fs_2_actd = read_raw_file(fs_2_act,shape1)
    fs_8_actd = read_raw_file(fs_8_act,shape1)
    fs_32_actd = read_raw_file(fs_32_act,shape1)
    
    fc_2_actd = read_raw_file(fc_2_act,shape2)
    fc_8_actd = read_raw_file(fc_8_act,shape2)
    fc_32_actd = read_raw_file(fc_32_act,shape2)
    lb1='sim_2'
    lb2='sim_8'
    lb3='sim_32'
    lb4='cal_2'
    lb5='cal_8'
    lb6='cal_32'
    fig1 = plt.figure(figsize=(9,6))
    x = np.linspace(0,len(fc_32_actd[1,:]),len(fc_32_actd[1,:]))
    # plt.plot(x,normd(fs_2_actd[1,:]),label=lb1,lw=3,color='#1A68FA')
    # plt.plot(x,normd(fs_8_actd[1,:]),label=lb2,lw=3,color='#F38929')
    # plt.plot(x,normd(fs_32_actd[1,:]),label=lb3,lw=3,color='#fabed4')
    
    plt.plot(x,normd(fc_2_actd[1,:]),label=lb4,lw=3,color='#1A68FA')
    plt.plot(x,normd(fc_8_actd[1,:]),label=lb5,lw=3,color='#F38929')
    plt.plot(x,normd(fc_32_actd[1,:]),label=lb6,lw=3,color='#fabed4')
    fig_setting()
        
def normd(data):
    return data/np.max(data)

def read_raw_file(file_path,shape):
    with open(file_path, 'rb') as file:
        data = np.fromfile(file, dtype=np.float32)
    return data.reshape(shape)

def fig_setting():
    plt.xlabel( " ",fontdict={'size': 20} )
    plt.ylabel(" ",fontdict={'size': 20} )
    plt.legend(loc='best',fontsize=20,frameon=True)
    plt.tick_params(labelsize=18)
    plt.grid()
    
if __name__ == '__main__':
    main()