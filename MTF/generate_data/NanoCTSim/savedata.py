# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt 

from matplotlib.gridspec import GridSpec

import pandas as pd

import numpy as np

from scipy.ndimage import gaussian_filter

import os

import core

import io 

import misc
'''

Considering the case of nano CT,

save the fig in the simulation process

'''

def save_intensity_data(data_obj,data_bkg,name,begin_time,fs,total_length,para,xenergy,out_path):
    
    dir_path = out_path+'/period_'+ str('{:.4f}'.format(para[4])) + '_sep_' +   str('{:.2f}'.format(para[5]))+'/' + str(begin_time) + '_fsy'+str(fs[0])+'_fsx'+str(fs[1])+'_total_lengthy'+str(total_length[0])+'_total_lengthx'+str(total_length[1])+'_xenergy_'+ str('{:.2f}'.format(xenergy)) + '/' 
    print("1D=%s"%dir_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    save_fig(data_obj,dir_path,name,'obj')
    save_fig(data_bkg,dir_path,name,'bkg')

def draw_contrast_ratio(data,dir_path):
    fig, axs = plt.subplots(1,2,figsize=(10, 10))
    #h_array_c = data[int(len(data)/2.)]
    h_array_c = data[0]
    h_array_2 = data[0,2500000:2500000+20000]
    axs[0].plot(h_array_c)
    axs[1].plot(h_array_2)
    plt.xlabel("[$\mu$m]")
    plt.ylabel("Intensity [Arb.]")
    plt.grid()
    plt.savefig(dir_path+"_intensity_contrast_ratio.png")
    plt.close()


def save_data_1D(data,name,begin_time,fs,total_length,para,pixel_number,xenergy,out_path):

    dir_path = out_path+'/period_'+ str('{:.4f}'.format(para[4])) + '_sep_' +   str('{:.2f}'.format(para[5]))+'/' + str(begin_time) + '_fsy'+str(fs[0])+'_fsx'+str(fs[1])+'_total_lengthy'+str(total_length[0])+'_total_lengthx'+str(total_length[1])+'_xenergy_' + str('{:.2f}'.format(xenergy)) + '/' 
    print("1D=%s"%dir_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    file_name_prefix = dir_path + name + "_d1_" + str('{:.0f}'.format(para[0]/1000.)) + "_d2_" + str('{:.0f}'.format(para[1]/1000.)) + "_d3_" +  str('{:.0f}'.format(para[2]/1000.)) +"_xenergy_"+str(para[3])+"_period_"+ str('{:.2f}'.format(para[4]))
    #file_name = file_name_prefix + '.csv'
    fig_name =file_name_prefix + '.png'
    if "final" in name or 'Objectdata' in name:
        phi_content = np.array(data)
        file_name_raw = dir_path + name +'index'+str(int(pixel_number))+para[7] + str('{:.3f}'.format(para[8])) + '.raw'
        with io.open(file_name_raw,'wb') as f:
            for i in range(360):
                phi_content.astype(np.float32).tofile(f)
        save_final_result(file_name_raw,dir_path,name,para,pixel_number,phi_content)
    save_fig_1D(data,file_name_prefix,name)

def save_final_result(file_name_raw,dir_path,name,para,pixel_number,phi_content):
    data_type = 'float32'
    raw_image = np.fromfile(file_name_raw,data_type)
    raw_image=raw_image.reshape(360,pixel_number)
    fig, axs = plt.subplots(1,2,figsize=(9, 6))
    axs[0].imshow(raw_image,cmap='gray')
    axs[1].plot(raw_image[int(len(raw_image)/2.)])
    axs[0].set_xlabel("x direction ")
    axs[1].set_xlabel("x direction ")

    axs[0].set_ylabel("y direction ")
    if 'absor' in name:
        axs[1].set_ylabel("Intensity [Arb.]")
    elif 'phi' in name:
        axs[1].set_ylabel("Phase [Arb.]")

    dir_path = 'data/figure/' 
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    fig_name_prefix = dir_path + name + "_period_"+ str('{:.4f}'.format(para[4])) + "_sep_"+str('{:.3f}'.format(para[5])) + '+' + para[7] + str('{:.0f}'.format(para[8]))  +'_index'+str(int(pixel_number))+'_res_'+str('{:.1f}'.format(para[9]))
    fig_name = fig_name_prefix + '.png'
    file_name_raw = fig_name_prefix + '.raw'
    with io.open(file_name_raw,'wb') as f:
        for i in range(360):
            phi_content.astype(np.float32).tofile(f)
    plt.savefig(fig_name)

def save_fig_1D(data,file_name_prefix,name):
    fig, axs = plt.subplots(1,1,figsize=(10, 10))
    #h_array_c = data[int(len(data)/2.)]
    h_array_c = data[0]
    plt.plot(h_array_c)
    plt.xlabel("x direction [$\mu$m]")
    plt.ylabel("[Arb.]")
    plt.title(name)
    plt.grid()
    print(file_name_prefix+name+".png")
    plt.savefig(file_name_prefix+name+".png")
    plt.close()

def save_fig(data,dir_path,name,name2):
    fig, axs = plt.subplots(2,2,figsize=(10, 10))

    for i in range(len(data)):
        h_array_c = data[i]
        if i == 0:
            axs[0,0].plot(h_array_c)
            axs[0,0].grid()
        elif i == 1:
            axs[0,1].plot(h_array_c)
            axs[0,1].grid()
        elif i == 2:
            axs[1,0].plot(h_array_c)
            axs[1,0].grid()
        elif i == 3:
            axs[1,1].plot(h_array_c)
            axs[1,1].grid()

    axs[0,0].set_xlabel("x direction [$\mu$m]")
    axs[0,1].set_xlabel("x direction [$\mu$m]")
    axs[1,0].set_xlabel("x direction [$\mu$m]")
    axs[1,1].set_xlabel("x direction [$\mu$m]")

    axs[0,0].set_ylabel("Intensity [Arb.]")
    axs[0,1].set_ylabel("Intensity [Arb.]")
    axs[1,0].set_ylabel("Intensity [Arb.]")
    axs[1,1].set_ylabel("Intensity [Arb.]")

    axs[0,0].set_title("step = 1")
    axs[0,1].set_title("step = 2")
    axs[1,0].set_title("step = 3")
    axs[1,1].set_title("step = 4")

    axs[0,0].grid(which='major', axis='both', linestyle='-')
    axs[0,1].grid(which='major', axis='both', linestyle='-')
    axs[1,0].grid(which='major', axis='both', linestyle='-')
    axs[1,1].grid(which='major', axis='both', linestyle='-')
    fig.suptitle('Different results of step phase') 
    plt.savefig(dir_path+name+name2+".png")


def save_imshow(phi_final,absor_final,begin_time,fs,total_length,para,xenergy,name,out_path):
    dir_path = out_path+'/period_'+ str('{:.4f}'.format(para[4])) + '_sep_' +   str('{:.2f}'.format(para[5]))+'/' + str(begin_time) + '_fsy'+str(fs[0])+'_fsx'+str(fs[1])+'_total_lengthy'+str(total_length[0])+'_total_lengthx'+str(total_length[1])+'_xenergy_' + str('{:.2f}'.format(xenergy)) + '/' 
    fig, axs = plt.subplots(2,2,figsize=(9, 6))
    phi_final_t = []
    absor_final_t = []
    for i in range(len(phi_final)):
        phi_final_t.append(phi_final)
        absor_final_t.append(absor_final)
    xticks = np.linspace(0,len(phi_final),int(len(phi_final)/5)+1)
    axs[0,0].plot(phi_final)
    axs[0,1].imshow(phi_final_t,cmap='gray')
    axs[1,0].plot(absor_final)
    axs[1,1].imshow(absor_final_t,cmap='gray')
    axs[0,0].grid(True)
    # axs[0,0].set_xticks(xticks)
    axs[1,0].grid(True)
    # axs[1,0].set_xticks(xticks)
    delta = float(para[11])*1e8
    beta=  float(para[12])*1e11
    plt.savefig(dir_path+name+"delta1e8:"+ str(delta) +"beta1e11:"+str(beta)+"imshow.png")


def save_data_split(data,name,begin_time,fs,total_length,para,xenergy,out_path):

    dir_path = out_path+'/period_'+ str('{:.4f}'.format(para[4])) + '_sep_' +   str('{:.2f}'.format(para[5]))+'/' + str(begin_time) + '_fsy'+str(fs[0])+'_fsx'+str(fs[1])+'_total_lengthy'+str(total_length[0])+'_total_lengthx'+str(total_length[1])+'_xenergy_' + str('{:.2f}'.format(xenergy)) + '/' 
    if not os.path.exists(dir_path): 
        os.makedirs(dir_path)
    data = np.array(data)
    data_real = np.real(data)
    file_name_prefix = dir_path + name + "_d1_" + str('{:.0f}'.format(para[0]/1000.)) + "_d2_" + str('{:.0f}'.format(para[1]/1000.)) + "_d3_" +  str('{:.0f}'.format(para[2]/1000.)) +"_xenergy_"+str(para[3])+"_period_"+ str('{:.2f}'.format(para[4]))
    file_name_real = file_name_prefix  + '.raw' 

    #np.save(file_name_real,data_real.reshape((1,np.size(data_real))))
    with io.open(file_name_real,'wb') as f:
        data_real.astype(np.float32).tofile(f)

def save_figure_split(data,databkg,name,begin_time,fs,total_length,para,xenergy,pos_x):

    dir_path = 'data/period_'+ str('{:.4f}'.format(para[4])) + '_sep_' +   str('{:.2f}'.format(para[5]))+'/' + str(begin_time) + '_fsy'+str(fs[0])+'_fsx'+str(fs[1])+'_total_lengthy'+str(total_length[0])+'_total_lengthx'+str(total_length[1])+'/' 
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    # data = np.array(data)
    file_name = dir_path + "_xe_"+str(xenergy)+'_position_x_'+  str('{:.2f}'.format(pos_x))+ name +'.png'
    phi_prj,abs_img = core.Signal_extract(data,[1,0], fs, para[10],para,begin_time,total_length,False,name)  
    phi_bkg,abs_img_bkg = core.Signal_extract(databkg,[1,0], fs, para[10],para,begin_time,total_length,False,name)
    phi_final = misc.Phi_info(phi_prj, phi_bkg,para[10])
    absor_final = -np.log(abs_img/abs_img_bkg)
    fig, axs = plt.subplots(1,2,figsize=(9, 6))
    axs[0].plot(phi_final[0])
    axs[1].plot(absor_final[0])
    plt.savefig(file_name)
    plt.close()