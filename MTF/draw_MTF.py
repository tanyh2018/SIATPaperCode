import sys

import matplotlib.pyplot as plt 
import matplotlib.colors as mcolors
import numpy as np
import os 
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
colors = ['#1A68FA','#F43C3C','#8BE1FF','#F38929','purple','#fabed4','gold','#fabed4','green', '#911eb4', '#000000','#f58231','#42d4f4','#f032e6','#ffe119', '#911eb4','#f58231', '#46f0f0', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff', '#3cb44b']  
marsi1 = ['+','.','<','d','|']    
marsi2 = ['x','*','^','s','.']
nn=16
#----------------------------------------
# Main Calculation defined here
#----------------------------------------
def main():
    ### paper result
    draw_TIS_MTF()
    # test_split_gauss_effect_MTFs()
    # draw_MTFs_likeref()
    # draw_material_MTF()
    # draw_pixel_size()
    # draw_act_sample_size()
    #draw_TIS_MTFs_choose()
    plt.show()

def draw_TIS_MTF():
    ## poly
    file_path_poly = './data/delta_s_graphite_poly/CTresult/MTF_result_txt/'  #res 20um
    fig1 = plt.figure(figsize=(9,6))
    TIS_MTF_poly(file_path_poly)
    plt.xlim(xmax=12, xmin=0.0)
    plt.ylim(ymax=1.0, ymin=0.0)
    yticks = np.linspace(0,1.0,11)
    xticks = np.linspace(0,12.0,13)
    plt.xticks(xticks)
    plt.yticks(yticks)
    fig_setting()
    plt.text(6.0, 0.2, '(D=300$\mu m$$, \Delta$del=48$\mu m$ \n Graphite, Poly)', fontsize=20, color='Black')
    plt.savefig('./figure/deltas_MTF_poly.svg',bbox_inches='tight',pad_inches=0)
    
    # fig1 = plt.figure(figsize=(9,1))
    # TIS_MTF_poly(file_path_poly)
    # plt.xlim(xmax=6, xmin=3)
    # plt.ylim(ymax=0.31, ymin=0.29)
    # plt.xticks([])
    # plt.yticks([])
    # plt.savefig('./figure/deltas_MTF_poly_larger.svg',bbox_inches='tight',pad_inches=0)

    ## mono
    file_path_mono = './data/delta_s_graphite_mono_30/CTresult/MTF_result_txt/'  #res 20um
    fig1 = plt.figure(figsize=(9,6))
    TIS_MTF_mono(file_path_mono)
    plt.xlim(xmax=12, xmin=0.0)
    plt.ylim(ymax=1.0, ymin=0.0)
    yticks = np.linspace(0,1.0,11)
    xticks = np.linspace(0,12.0,13)
    plt.xticks(xticks)
    plt.yticks(yticks)
    fig_setting()
    plt.text(6.0, 0.2, '(D=300$\mu m$$, \Delta$del=48$\mu m$ \n Graphite, Mono)', fontsize=20, color='Black')
    plt.savefig('./figure/deltas_MTF_mono.svg',bbox_inches='tight',pad_inches=0)

    # fig1 = plt.figure(figsize=(9,1))
    # TIS_MTF_mono(file_path_mono)
    # plt.xlim(xmax=6, xmin=3)
    # plt.ylim(ymax=0.31, ymin=0.29)
    # plt.xticks([])
    # plt.yticks([])
    # plt.savefig('./figure/deltas_MTF_mono_larger.svg',bbox_inches='tight',pad_inches=0)

def TIS_MTF_poly(file_path):
    file_names,list_phi = read_datas(file_path)

    DSS = ['d_8.0000','d_2.1124','d_0.5600']
    DSS2 = ['d_8.0000','d_2.000','d_0.5600']
    k=0

    nn=6
    for j in range (len(DSS)):
        for i in range(len(list_phi)):    
            if 'notfit'  not in file_names[i] and 'ACT' in file_names[i] and 'sigma' in file_names[i] and 'mono'  not in file_names[i] and DSS[j] in file_names[i]:
                nm=sep_dis2(file_names[i])
                print(file_names[i])
                list_v = []
                list_v = load_data(list_phi[i])
                labels = 'ACT: $\Delta s$=' + str(int(float(nm[3])))+'$\mu m$'
                draw_scatter(list_v,k,labels,'ACT')
                # plt.plot(list_v[0],list_v[1],'-', label=  'ACT: $\Delta s$=' + str(int(float(nm[3])))+'$\mu m$',lw=3,color=colors[k]) 
                k=k+1
    k=0
    marsi2 = ['s','d','+']
    for j in range (len(DSS2)):
        for i in range(len(list_phi)):    
            if 'notfit'  not in file_names[i] and 'DPC' in file_names[i] and 'sigma' in file_names[i] and 'mono'  not in file_names[i] and DSS2[j] in file_names[i]:
                nm=sep_dis2(file_names[i])
                list_v = []
                list_v = load_data(list_phi[i])
                labels = 'DPCT: $\Delta s$=' + str(int(float(nm[3])))+'$\mu m$'
                draw_scatter(list_v,k,labels,'DPCT')
                k=k+1
    
def TIS_MTF_mono(file_path):
    file_names,list_phi = read_datas(file_path)

    DSS = ['sep_2.50','sep_7.50','sep_34.5']
    DSS2 = ['sep_2.50','sep_8.50','sep_34.5']
    k=0
    for j in range (len(DSS)):
        for i in range(len(list_phi)):    
            if 'notfit'  not in file_names[i] and 'ACT' in file_names[i] and 'sigma' in file_names[i] and 'mono'  in file_names[i] and DSS[j] in file_names[i]:
                nm=sep_dis2(file_names[i])
                list_v = []
                list_v = load_data(list_phi[i])
                if DSS[j] == 'sep_2.50':
                    ns = '2'
                elif DSS[j] == 'sep_7.50':
                    ns = '8'
                elif DSS[j] == 'sep_34.5':
                    ns = '32'
                labels = 'ACT: $\Delta s$=' + ns +'$\mu m$'
                draw_scatter(list_v,k,labels,'ACT')
                k=k+1
    k=0
    for j in range (len(DSS2)):
        for i in range(len(list_phi)):    
            if 'notfit'  not in file_names[i] and 'DPC' in file_names[i] and 'sigma' in file_names[i] and 'mono'  in file_names[i] and DSS2[j] in file_names[i]:
                nm=sep_dis2(file_names[i])
                list_v = []
                list_v = load_data(list_phi[i])
                if DSS2[j] == 'sep_2.50':
                    ns = '2'
                elif DSS2[j] == 'sep_8.50':
                    ns = '8'
                elif DSS2[j] == 'sep_34.5':
                    ns = '32'
                labels = 'DPCT: $\Delta s$=' +  ns +'$\mu m$'
                print(ns)
                draw_scatter(list_v,k,labels,'DPCT')
                k=k+1    
    
def fig_setting():
    plt.xlabel( "lp/mm ",fontdict={'size': 20} )
    plt.ylabel("MTF",fontdict={'size': 20} )
    plt.legend(loc='best',fontsize=20,frameon=True)
    plt.tick_params(labelsize=18)
    plt.grid()
    
def draw_pixel_size():
    file_path = './data/detector_pixel_size_line/CTresult/MTF_result_txt/'
    ps=['size_8_','size_24_','size_48_']

    fig1 = plt.figure(figsize=(9,6))
    draw_act_pixel_size(file_path,ps,model='line_source')
    plt.xlim(xmax=16, xmin=0.0)
    plt.ylim(ymax=1.0, ymin=0.0)
    yticks = np.linspace(0,1.0,11)
    plt.yticks(yticks)
    xticks = np.linspace(0,16.0,17)
    plt.xticks(xticks)
    plt.text(3.0, 0.9, 'ACT', fontsize=30, color='Black')
    fig_setting()
    #plt.text(9.0, 0.15, '(D=300$\mu m$, $\Delta s$=2$\mu m$ \n Graphite)', fontsize=20, color='Black')       
    plt.savefig('./figure/Pixel_Size_ACT_MTF.svg',bbox_inches='tight',pad_inches=0)
    
    fig1 = plt.figure(figsize=(9,6))
    draw_dpc_pixel_size_MTF(file_path,ps,model='line_source')
    yticks = np.linspace(0,1.0,11)
    plt.yticks(yticks)
    xticks = np.linspace(0,13.0,14)
    plt.xticks(xticks)
    plt.text(3.0, 0.9, 'DPCT', fontsize=30, color='Black')
    plt.xlim(xmax=13, xmin=0.0)
    plt.ylim(ymax=1.0, ymin=0.0)
    fig_setting()
    #plt.text(7.0, 0.15, '(D=300$\mu m$, $\Delta s$=2$\mu m$\n Graphite)', fontsize=20, color='Black')    
    plt.savefig('./figure/Pixel_Size_DPC_MTF.svg',bbox_inches='tight',pad_inches=0)
    
    file_path = './data/detector_pixel_size_point/CTresult/MTF_result_txt/'
    fig1 = plt.figure(figsize=(9,6))
    draw_act_pixel_size(file_path,ps,model='line_source')
    plt.xlim(xmax=16, xmin=0.0)
    plt.ylim(ymax=1.0, ymin=0.0)
    yticks = np.linspace(0,1.0,11)
    plt.yticks(yticks)
    xticks = np.linspace(0,16.0,17)
    plt.xticks(xticks)
    plt.text(3.0, 0.9, 'ACT', fontsize=30, color='Black')
    fig_setting()
    #plt.text(9.0, 0.15, '(D=300$\mu m$, $\Delta s$=2$\mu m$ \n Graphite)', fontsize=20, color='Black')       
    plt.savefig('./figure/Pixel_Size_ACT_MTF_point.svg',bbox_inches='tight',pad_inches=0)
    
    fig1 = plt.figure(figsize=(9,6))
    draw_dpc_pixel_size_MTF(file_path,ps,model='line_source')
    yticks = np.linspace(0,1.0,11)
    plt.yticks(yticks)
    xticks = np.linspace(0,13.0,14)
    plt.xticks(xticks)
    plt.text(3.0, 0.9, 'DPCT', fontsize=30, color='Black')
    plt.xlim(xmax=13, xmin=0.0)
    plt.ylim(ymax=1.0, ymin=0.0)
    fig_setting()
    #plt.text(7.0, 0.15, '(D=300$\mu m$, $\Delta s$=2$\mu m$\n Graphite)', fontsize=20, color='Black')    
    plt.savefig('./figure/Pixel_Size_DPC_MTF_point.svg',bbox_inches='tight',pad_inches=0)
        
def draw_act_pixel_size(file_path,ps,model):
    file_names,list_phi = read_datas(file_path)
    k=0
    for j in range(len(ps)):
        for i in range(len(list_phi)):    
            if 'notfit'  not in file_names[i] and 'ACT' in file_names[i] and 'poly' in file_names[i] and ps[j] in  file_names[i]:
                if (model=='line_source' and 'line' in file_names[i]) or (model=='point_source' and 'point' in file_names[i]):
                    nm=sep_dis2(file_names[i])
                    list_v = []
                    list_v = load_data(list_phi[i])
                    labels = '$\Delta del$=' + (nm[9]) +'$\mu m$  (Poly)'
                    draw_scatter(list_v,k,labels,'ACT','c')
                    k=k+1
    k=0
    for j in range(len(ps)):
        for i in range(len(list_phi)):    
            if 'notfit'  not in file_names[i] and 'ACT' in file_names[i] and 'mono' in file_names[i] and ps[j] in  file_names[i]:
                if (model=='line_source' and 'line' in file_names[i]) or (model=='point_source' and 'point' in file_names[i]):
                    nm=sep_dis2(file_names[i])
                    list_v = []
                    list_v = load_data(list_phi[i])
                    labels = '$\Delta del$=' + (nm[9]) +'$\mu m$  (Mono)'
                    draw_scatter(list_v,k,labels,'DPCT','c')
                    k=k+1

def draw_dpc_pixel_size_MTF(file_path,ps,model):
    file_names,list_phi = read_datas(file_path)
    k=0
    for j in range(len(ps)):
        for i in range(len(list_phi)):    
            if 'notfit'  not in file_names[i] and 'DPC' in file_names[i] and 'poly' in file_names[i] and ps[j] in  file_names[i]:
                if (model=='line_source' and 'line' in file_names[i]) or (model=='point_source' and 'point' in file_names[i]):
                    nm=sep_dis2(file_names[i])
                    list_v = []
                    list_v = load_data(list_phi[i])
                    labels ='$\Delta del$=' + (nm[9]) +'$\mu m$  (Poly)'
                    draw_scatter(list_v,k,labels,'ACT','c') 
                    k=k+1
    k=0
    for j in range(len(ps)):
        for i in range(len(list_phi)):    
            if 'notfit'  not in file_names[i] and 'DPC' in file_names[i] and 'mono' in file_names[i] and ps[j] in  file_names[i]:
                if (model=='line_source' and 'line' in file_names[i]) or (model=='point_source' and 'point' in file_names[i]):
                    nm=sep_dis2(file_names[i])
                    list_v = []
                    list_v = load_data(list_phi[i])
                    labels ='$\Delta del$=' + (nm[9])+'$\mu m$  (Mono)'
                    draw_scatter(list_v,k,labels,'DPCT','c') 
                    k=k+1

def draw_act_sample_size():
    file_path = './data/dpc_sample_size/CTresult/MTF_result_txt/'
    fig1,ax = plt.subplots(figsize=(9,6)) 
    model = 'poly' 
    nmn=8
    sample_size_e(file_path,model,nmn)
    plt.xlim(xmax=12, xmin=0.0)
    plt.ylim(ymax=1.0, ymin=0.0)
    yticks = np.linspace(0,1.0,11)
    plt.yticks(yticks)
    xticks = np.linspace(0,12.0,13)
    plt.xticks(xticks)
    fig_setting()
    plt.text(6.5, 0.15, '($\Delta del$=48$\mu m$, $\Delta s$=2$\mu m$ \n Graphite, poly)', fontsize=20, color='Black')        
    plt.savefig('./figure/Sample_Size_ACT_DPC_MTF_'+model+'.svg', bbox_inches='tight',pad_inches=0)
    
    nmn=-4
    file_path = './data/dpc_sample_size_mono/CTresult/MTF_result_txt/'
    fig1,ax = plt.subplots(figsize=(9,6)) 
    model = 'mono' 
    sample_size_e(file_path,model,nmn)
    plt.xlim(xmax=12, xmin=0.0)
    plt.ylim(ymax=1.0, ymin=0.0)
    yticks = np.linspace(0,1.0,11)
    plt.yticks(yticks)
    xticks = np.linspace(0,12.0,13)
    plt.xticks(xticks)
    fig_setting()
    plt.text(6.5, 0.15, '($\Delta del$=48$\mu m$, $\Delta s$=2$\mu m$ \n Graphite, mono)', fontsize=20, color='Black')        
    plt.savefig('./figure/Sample_Size_ACT_DPC_MTF_'+model+'.svg', bbox_inches='tight',pad_inches=0)
    
        
def sample_size_e(file_path,model,nmn):
    file_names,list_phi = read_datas(file_path)
    k=0
    for i in range(len(list_phi)):    
        if 'notfit'  not in file_names[i] and 'ACT' in file_names[i] and model in file_names[i] and '900' not in file_names[i] and '600' not in file_names[i] : 
            nm=sep_dis2(file_names[i])
            list_v = []
            list_v = load_data(list_phi[i])
            labels ="ACT: D=" + nm[nmn] +'$\mu m$'
            draw_scatter(list_v,k,labels,'ACT','g') 
            k=k+1
    k=0
    for i in range(len(list_phi)):    
        if 'notfit'  not in file_names[i] and 'DPC-CT' in file_names[i] and model in file_names[i] and '900' not in file_names[i] and '600' not in file_names[i]: 
            nm=sep_dis2(file_names[i])
            list_v = []
            list_v = load_data(list_phi[i])

            labels ="DPCT: D=" + nm[nmn] +'$\mu m$'
            draw_scatter(list_v,k,labels,'DPCT','g') 
            k=k+1


def draw_material_MTF():
    file_path = './data/material_20221212/CTresult/MTF_result_txt/'  #res 20um
    fig1 = plt.figure(figsize=(9,6))
    material_poly(file_path)
    plt.xlim(xmax=15, xmin=0.0)
    plt.ylim(ymax=1.0, ymin=0.0)
    fig_setting()
    yticks = np.linspace(0,1.0,11)
    plt.yticks(yticks)
    xticks = np.linspace(0,15.0,16)
    plt.xticks(xticks)
    plt.text(8.5, 0.05, '(D=300$\mu m$, $\Delta s$=2$\mu m$\n $\Delta del$=48$\mu m$, Mono)', fontsize=20, color='Black')
    plt.savefig('./figure/Material_MTF_mono.svg', bbox_inches='tight',pad_inches=0)
    
    
    file_path = './data/material_20240523_poly/CTresult/MTF_result_txt/'  #res 20um
    fig1 = plt.figure(figsize=(9,6))
    material_poly(file_path)
    plt.xlim(xmax=15, xmin=0.0)
    plt.ylim(ymax=1.0, ymin=0.0)
    fig_setting()
    yticks = np.linspace(0,1.0,11)
    plt.yticks(yticks)
    xticks = np.linspace(0,15.0,16)
    plt.xticks(xticks)
    plt.text(8.5, 0.05, '(D=300$\mu m$, $\Delta s$=2$\mu m$\n $\Delta del$=48$\mu m$, Poly)', fontsize=20, color='Black')
    plt.savefig('./figure/Material_MTF_poly.svg', bbox_inches='tight',pad_inches=0)    
    
    
def material_poly(file_path):
    file_names,list_phi = read_datas(file_path)
    period = ['0.62','0.67','6.1','5.1','7.1','0.52','0.72','0.87','0.92','4.1','1.1','0.57','3.1']
    Material = ['water','graphite','mylar','PMMA']
    k=0
    percent=0.1
    print(file_names)
    for j in range(len(Material)):
        for i in range(len(list_phi)):    
            if 'notfit'  not in file_names[i] and 'ACT' in file_names[i] and Material[j] in file_names[i]:
                nm=sep_dis2(file_names[i])
                list_v = []
                list_v = load_data(list_phi[i])
                MTF = get_MTF_value(list_v,percent)
                labels = "ACT: " + Material[j]
                draw_scatter(list_v,k,labels,'ACT')
                k=k+1
                print(file_names[i])
                print('MTF=',MTF)
    k=0
    for j in range(len(Material)):
        for i in range(len(list_phi)):    
            if 'notfit'  not in file_names[i] and 'DPC' in file_names[i] and Material[j] in file_names[i]:
                nm=sep_dis2(file_names[i])
                list_v = []
                list_v = load_data(list_phi[i])
                labels = "DPCT: " + Material[j]
                draw_scatter(list_v,k,labels,'DPCT')
                k=k+1
                MTF = get_MTF_value(list_v,percent)
                print(file_names[i])
                print('MTF=',MTF)

        
def get_MTF_value(list_v,percent):
    x = list_v[0] 
    y = list_v[1]
    for i in range(len(x)):
        if y[i]==percent:
            MTF = x[i]
            break
        elif y[i]<percent:
            x_tmp = x[i] - (percent-y[i])/(y[i-1]-y[i])*(x[i]-x[i-1])
            MTF = x_tmp
            break
    return MTF

def read_datas(file_path):
    file_names = []
    list_phi = []
    for file_name in os.listdir(file_path):        
        file_names.append(file_name)
        list_phi.append(read_data(file_path + file_name))
    return file_names,list_phi

def test_split_gauss_effect_MTFs():
    file_path = './data/deltas_s_calculate_20240531/CTresult/MTF_result_txt/' 
    sigmas=['_sigma_1.55','_sigma_0.0']
    for j in range(0,2):
        sigma = sigmas[j]
        fig1 = plt.figure(figsize=(9,6))
        test_split_gauss_effect_MTF_repeat(file_path,sigma)
        fig_setting()
        if sigma=='1.55':
            plt.xlim(xmax=12.0, xmin=0.0)
            plt.ylim(ymax=1.0, ymin=0.0)
            plt.yticks(np.linspace(0,1.0,11))
            plt.xticks(np.linspace(0,12.0,13))
            plt.text(6, 0.15, '(D=300$\mu m$, $\Delta del$=48$\mu m$ \n Graphite)', fontsize=20, color='Black')
            plt.legend(loc='best',fontsize=20,frameon=True)   
        else:
            plt.xlim(xmax=12.0, xmin=0.0)
            plt.ylim(ymax=1.0, ymin=0.0)
            plt.yticks(np.linspace(0,1.0,11))
            plt.xticks(np.linspace(0,12.0,13))
            plt.text(6, 0.15, '(D=300$\mu m$, $\Delta del$=48$\mu m$ \n Graphite)', fontsize=20, color='Black')  
            plt.legend(loc='best',fontsize=20,frameon=True)         
        plt.savefig('./figure/delta_s_value_sim_sigma'+sigma+'_.svg',bbox_inches='tight',pad_inches=0)
        
        # fig1 = plt.figure(figsize=(9,1))
        # test_split_gauss_effect_MTF_repeat(file_path,colors,sigma)
        # if sigma=='1.55':
        #     plt.xlim(xmax=3.1, xmin=2.5)
        #     plt.ylim(ymax=0.31, ymin=0.29)
        # else:
        #     plt.xlim(xmax=4.2, xmin=3)
        #     plt.ylim(ymax=0.31, ymin=0.29)
        # plt.yticks([])
        # plt.xticks([])
        # plt.savefig('./figure/delta_s_value_sim_sigma_'+sigma+'_larger.svg',bbox_inches='tight',pad_inches=0)    
def test_split_gauss_effect_MTF_repeat(file_path,sigma):    
    file_names,list_phi = read_datas(file_path)
    name_list = ['_sd_0.0_','_sd_2_','_sd_8_','_sd_32_']
    k=0
    nn=6
    for j in range (len(name_list)):
        for i in range(len(list_phi)):  
            if 'notfit'  not in file_names[i] and sigma in file_names[i] and 'ACT' in file_names[i] and name_list[j] in file_names[i]:
                print(file_names[i])
                nm=sep_dis2(file_names[i])
                list_v = []
                list_v = load_data(list_phi[i])
                if '_sd_0.0_' in file_names[i]:
                    labels = 'No grating'
                else:
                    labels = 'ACT: $\Delta s$='+str(nm[12]) + '$\mu m$'
                draw_scatter(list_v,k,labels,'ACT')
                k=k+1
    k=0
    for j in range (len(name_list)):
        for i in range(len(list_phi)):  
            if 'notfit'  not in file_names[i] and sigma in file_names[i] and 'DPC-CT' in file_names[i] and name_list[j] in file_names[i]:
                nm=sep_dis2(file_names[i])
                list_v = []
                list_v = load_data(list_phi[i])
                if '_sd_0.0_' in file_names[i]:
                    labels = 'No grating'
                else:
                    labels = 'DPCT: $\Delta s$='+str(nm[12]) + '$\mu m$'
                draw_scatter(list_v,k,labels,'DPCT')
                k=k+1
                
def arrange_name(list_phi,file_names,listnm):
    nat = []
    for i in range(len(list_phi)):
        nm=sep_dis2(file_names[i])
        if nm[12] != '0.0':
            if (float(nm[12])<=60.0 and float(nm[12])<=60.0) or float(nm[12])<1.0:
                nat.append(float(nm[12]))
    nat = list(set(nat))
    nat = sorted(nat)
    nat = ['_'+listnm+'_'+str(nat[i])+'_' for i in range(len(nat))]
    nat.insert(0,'_'+listnm+'_0.0_')
    return nat


def draw_MTFs(file_path):
    fig1 = plt.figure(figsize=(12,8))
    file_names,list_phi = read_datas(file_path)
    
    k=0
    for i in range(len(list_phi)):  
        if 'notfit'  not in file_names[i] and 'ACT' in file_names[i]:
            nm=sep_dis2(file_names[i])
            list_v = []
            list_v = load_data(list_phi[i])
            labels = nm[1]
            plt.plot(list_v[0],list_v[1],'-', label= labels,lw=3) 
            k=k+1
    k=0
    for i in range(len(list_phi)):  
        if 'notfit'  not in file_names[i] and 'DPC' in file_names[i]:
            nm=sep_dis2(file_names[i])
            list_v = []
            list_v = load_data(list_phi[i])
            labels = nm[1]
            plt.plot(list_v[0],list_v[1],'--', label= labels,lw=3) 
            k=k+1
    plt.xlim(xmax=12, xmin=0.0)
    plt.ylim(ymax=1.0, ymin=0.0)
    plt.xlabel( "lp/mm ",fontdict={'size': 20} )
    plt.ylabel("MTF",fontdict={'size': 20} )
    fig_setting()
    xticks = np.linspace(0,12.0,13)
    plt.xticks(xticks)
    plt.grid()

def draw_MTFs_gejijin():
    file_path = "D:/xianjinyuan/工作内容/Jiecheng/NanoCT/Simulation/NanoCT_Sim/SimCode/withoutZP/data/split_test3/CTresult/MTF_result_txt/"
    fig1 = plt.figure(figsize=(12,8))
    file_names,list_phi = read_datas(file_path)
    # k=0
    # for i in range(len(list_phi)):  
    #     if 'notfit'  not in file_names[i] and 'ACT' in file_names[i] and 'restore' in file_names[i] and '24.0' in file_names[i] :
    #         nm=sep_dis2(file_names[i])
    #         list_v = []
    #         list_v = load_data(list_phi[i])
    #         labels = "Absor"
    #         plt.plot(list_v[0],list_v[1],'-', label= labels,lw=3,color='#44AFC6') 
    #         k=k+1
    k=0
    for i in range(len(list_phi)):  
        if 'notfit'  not in file_names[i] and 'DPC' in file_names[i]  and '24.0' in file_names[i] :
            nm=sep_dis2(file_names[i])
            list_v = []
            list_v = load_data(list_phi[i])
            labels = "Phase"
            if k==1:
                plt.plot(list_v[0],list_v[1],'-', label= labels,lw=5,color='#FFC000') 
            if k==0:
                plt.plot(list_v[0],list_v[1],'-', label= labels,lw=5,color='#44AFC6') 
                k=k+1

    plt.xlim(xmax=12, xmin=0.0)
    plt.ylim(ymax=1.0, ymin=0.0)
    plt.xlabel( "lp/mm ",fontdict={'size': 20} )
    plt.ylabel("MTF",fontdict={'size': 20} )
    # plt.legend(loc='best',fontsize=25,frameon=True)
    plt.tick_params(labelsize=18)
    xticks = np.linspace(0,12.0,13)
    plt.xticks(xticks)
    # plt.grid()
    plt.savefig('../test1.svg',bbox_inches='tight')
    #plt.show()


def draw_TIS_MTFs_choose():
    file_path = 'D:/xianjinyuan/工作内容/Jiecheng/NanoCT/Simulation/ReconCT/add/yuhang/talbot_result/paper_version_2022_12_19/delta_s_graphite_poly_2022_12_19/CTresult/MTF_result_txt/'
    #file_path = 'D:/xianjinyuan/工作内容/Jiecheng/NanoCT/Simulation/ReconCT/add/yuhang/talbot_result/paper_version_2022_12_19/delta_s_graphite_poly_2022_12_19_mono/CTresult/MTF_result_txt/'
    #file_path = 'D:/xianjinyuan/工作内容/Jiecheng/NanoCT/Simulation/ReconCT/add/yuhang/talbot_result/paper_version_2022_12_19/mono_30/CTresult/MTF_result_txt/'
    fig1 = plt.figure(figsize=(9,8))
    file_names,list_phi = read_datas(file_path)
    name_list_act = []
    name_list_dpc = []
    value_list_act = []
    value_list_dpc = []
    rn=120
    for i in range(len(list_phi)):  
        nm=sep_dis2(file_names[i])
        if 'notfit' not in file_names[i]:
            list_v = []
            list_v = load_data(list_phi[i])
            if 'ACT' in file_names[i]:
                ref_ACT = list_v[1][rn]
                value_list_act.append(ref_ACT)
                name_list_act.append(file_names[i])
                if 'd_11.9701' in file_names[i]:
                    ref_ACT2 = list_v[1][rn]
            if 'DPC' in file_names[i]:
                ref_DPC = list_v[1][rn]
                value_list_dpc.append(ref_DPC)
                name_list_dpc.append(file_names[i])
                if 'd_11.9701' in file_names[i]:
                    ref_DPC2 = list_v[1][rn]
    list1, list_names_act = (list(t) for t in zip(*sorted(zip(value_list_act, name_list_act),reverse=True)))
    list2, list_names_dpc = (list(t) for t in zip(*sorted(zip(value_list_dpc, name_list_dpc),reverse=True)))
    # for j in range(len(list_names_act)):       
    #     for i in range(len(list_phi)):  
    #         # if 'notfit' not in file_names[i] and 'ACT' in file_names[i] and list_names_act[j] in file_names[i] and ('8.000' in file_names[i] or '0.5600' in file_names[i] or '2.1124' in file_names[i]) :
    #         if 'notfit' not in file_names[i] and 'ACT' in file_names[i] and list_names_act[j] in file_names[i]  :
    #             nm=sep_dis2(file_names[i])
    #             list_v = []
    #             list_v = load_data(list_phi[i])
    #             if list_v[1][120] <= ref_ACT2:
    #                 labels = nm[1]+'_'+nm[3]
    #                 plt.plot(list_v[0],list_v[1],'-', label= labels,lw=3) 
    print(list_names_dpc)
    list_dpc=[]
    for j in range(len(list_names_dpc)):       
        for i in range(len(list_phi)):  
            # if 'notfit'  not in file_names[i] and 'DPC' in file_names[i] and list_names_dpc[j] in file_names[i] and ('8.000' in file_names[i] or '0.5600' in file_names[i] or '2.0000' in file_names[i]):
            if 'notfit'  not in file_names[i] and 'DPC' in file_names[i] and list_names_dpc[j] in file_names[i] :
                nm=sep_dis2(file_names[i]) 
                list_v = []
                list_v = load_data(list_phi[i])
                if list_v[1][rn] >= ref_DPC2:
                    labels = nm[1]+'_'+nm[3]
                    plt.plot(list_v[0],list_v[1],'--', label= labels,lw=3) 
    list_names_dpc =[ (list_names_dpc[i]).split('_')[3] for i in range(len(list_names_dpc)) ]
    list_names_act =[ (list_names_act[i]).split('_')[3] for i in range(len(list_names_act)) ]
    print('DPC:',list_names_dpc)
    print('ACT:',list_names_act)
    plt.xlim(xmax=12, xmin=0.0)
    plt.ylim(ymax=1.0, ymin=0.0)
    plt.xlabel( "lp/mm ",fontdict={'size': 20} )
    plt.ylabel("MTF",fontdict={'size': 20} )
    plt.legend(loc='best',fontsize=15,frameon=True)
    plt.tick_params(labelsize=15)
    xticks = np.linspace(0,12.0,13)
    plt.xticks(xticks)
    yticks = np.linspace(0,1.0,11)
    plt.yticks(yticks)
    plt.grid()


def draw_MTFs_likeref():
    ''' repeat LiKe paper result and comparision. Ref: Spatial resolution characterization of differential phase contrast CT systems via modulation transfer function (MTF) measurements '''
    
    file_path = './data/likerepeat/CTresult/MTF_result_txt/'
    fig1 = plt.figure(figsize=(9,6))
    file_names,list_phi = read_datas(file_path)
    
    #period = ['1.1','4.1','0.22','0.32','0.82']
    period = ['8.0']
    k=0
    for i in range(len(list_phi)):    
        if 'notfit'  not in file_names[i] and 'ACT' in file_names[i]  and 'like' not in file_names[i] and ('1.55_' in file_names[i]) and 'graphite' not in file_names[i]:
            nm=sep_dis2(file_names[i])
            sim_act = []
            sim_act = load_data(list_phi[i])
            test = [True for j in range(len(period)) if period[j] in file_names[i]]
            if True:
                plt.plot(sim_act[0],sim_act[1],'-', label='ACT simulated',lw=3,color='#44AFC6') 
                #plt.plot(sim_act[0],sim_act[1],'-', label='ACT sim'+nm[-3],lw=3,color=colors[k]) 
                k=k+1
    k=0
    for i in range(len(list_phi)):    
        if 'notfit'  not in file_names[i] and 'DPC-CT' in file_names[i] and 'like' not in file_names[i] and ('1.55_' in file_names[i] ) and 'graphite' not in file_names[i]:
            nm=sep_dis2(file_names[i])
            sim_dpcct = []
            sim_dpcct = load_data(list_phi[i])
            test = [True for j in range(len(period)) if period[j] in file_names[i]]
            if True:
                plt.plot(sim_dpcct[0],sim_dpcct[1],'-', label='DPCT simulated',lw=3,color='#F38929') 
                #plt.plot(sim_dpcct[0],sim_dpcct[1],'-', label='DPCT sim'+nm[-3],lw=3,color=colors[k]) 
                k=k+1
    for i in range(len(list_phi)):    
        if 'like'  in file_names[i]  and  'ACT' in file_names[i]:
            data_act = []
            data_act = load_data(list_phi[i])
            plt.plot(data_act[0],data_act[1],'--',label='ACT measured',lw=3,color='#44AFC6') 
            # plt.scatter(data_act[0],data_act[1])
    for i in range(len(list_phi)):    
        if 'like'  in file_names[i]  and  'DPC-CT' in file_names[i]:
            data_dpcct = []
            data_dpcct = load_data(list_phi[i])
            plt.plot(data_dpcct[0],data_dpcct[1],'--', label='DPCT measured',lw=3,color='#F38929') 
    plt.xlim(xmax=12, xmin=0.0)
    plt.ylim(ymax=1.0, ymin=0.0)
    yticks = np.linspace(0,1.0,11)
    plt.yticks(yticks)
    xticks = np.linspace(0,12.0,13)
    plt.xticks(xticks)
    fig_setting()
    plt.savefig('./figure/sim_data_MTF.pdf')
    plt.savefig('./figure/sim_data_MTF.svg', bbox_inches='tight',pad_inches=0)

def read_data(file_name):
    data_x = []
    data_y = []
    file_handler = open(file_name, 'r')
    with file_handler as file_in:
        for line in file_in:
            data_x.append(float(line.split(',')[0]))
            data_y.append(float(line.split(',')[1]))
    return [data_x,data_y]

def load_data(list_v):
    plot_valuex = []
    plot_value_y = []
    for i in range(len(list_v[0])):
        if list_v[0][i] >= 0:
            plot_valuex.append(list_v[0][i])
            plot_value_y.append(list_v[1][i])
    return [plot_valuex,plot_value_y] 

def sep_dis(file_names):
    sep_dis_list = []
    for i in range(len(file_names)):
        fst= file_names[i].split('_')[:]
        sep_dis_list.append(fst[0]+'_'+fst[2]+'_'+fst[3]+'_'+fst[4]+'_'+fst[5]+'$\mu m$')    
    return sep_dis_list

def sep_dis2(file_name):
    fst= file_name.split('_')[:]
    return fst

def draw_scatter(list_v,k,labels,mtype,ntype='g'):
      
    ap = 1.0
    masize = 10
    marsi1 = ['s','x','d','*','|']      
    if mtype == 'ACT':
        st=3*k
        line_style = '-'
        marker = marsi1[k]
        markerfacecolor = 'none' 
    else:
        st=2*k
        line_style = ':'
        marker = marsi1[k]
        markerfacecolor = 'none'
    if k>1:
        markerfacecolor = None
        ap=0.85
        masize=8
    if k==2:
        ap=1.0
    if ntype=='c' and  mtype == 'ACT':
        marker=None
    plt.plot(list_v[0][st::nn], list_v[1][st::nn], line_style, color=colors[k], marker=marker, markersize=masize,
             markerfacecolor=markerfacecolor, label=labels, lw=2, markeredgewidth=1.5,alpha=ap-k*0.03)

if __name__ == '__main__':
    main()