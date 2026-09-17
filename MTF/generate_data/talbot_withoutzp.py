import sys

# from matplotlib.image import composite_images
sys.path.insert(1, './NanoCTSim')
from NanoCTSim import *
import gc
from time import * 
import datetime
import matplotlib.pyplot as plt 
import os
import core
import savedata 
import numpy as np
import misc
import propagator
import material as matl
#----------------------------------------
# Main Calculation defined here
#----------------------------------------
def main():
    args = sys.argv[1:]
    gc.set_threshold(500,5,5)
    begin_time = time()
    # material = "bonecortical"
    #material = 'mgo'
    #material = "aluminum"
    #material = "graphite"
    #material = "PMMA"
    #material = "water"
    # material = "LiF"
    material = "mylar"
    #material = "polyimide"
    #material = "teflon"
    #material = material + 'pure_absor'
    out_path = 'data2/talbot_result/20240522_'+material
    # ------------- Field init. -------------
    fs = [0.01,1000]                    # Sampling frequency [y,x] now only 1D can wolk
    total_length = [100*um,4800.*um]          # Size of the 2D square view [y,x]
    detector_res = 48.*um
    pixel_number = int(total_length[1]/detector_res)

    #-------------- Geometry --------------

    grating_type = 'Pi phase'   # Grating type
    distance1 = 1382*mm         # Source to Sample distance
    distance2 = 104*mm         # Sample to Zone plate distance
    distance3 = 181*mm         # Zone plate to grating distance

        #------------ Optics param. ------------
    numStep = 10               # Number of Stepping

    # sphere 1
    olength1 = 100*um           # Size of spherical sample
    opos_x1 = -1.*olength1/2.      # Position of the object
    opos_y1 = -1.*olength1/2.
    sphere_1 = [olength1,opos_x1,opos_y1]

    # sphere 2
    olength2 = 1.80*um            # Size of spherical sample
    opos_x2 = 1.*olength1/2.       # Position of the object
    opos_y2 = 1.*olength1/2.
    sphere_2 = [olength2,opos_x2,opos_y2]

    #cylinder_side
    cylinder_diameter = 300*um            # Size of spherical sample
    cylinder_length = 100.*um 
    opos_y3 =   -cylinder_length/2.  # Position of the object
    opos_x3 = -cylinder_diameter/2.
    cylinder_1 = [cylinder_diameter,cylinder_length,opos_y3,opos_x3]

    #source position
    width = 20*um
    pos_y = 0.*um
    G0SampNum = 1 # number of point
    #pos_x=np.linspace( (-1.) * width / 2., (width) / 2. ,int(G0SampNum))
    pos_x = [0]
    #material = "boneplastic_pure_phase"

    #material = "boneplastic_pure_absor"
    #material = alminum bone gold graphite PMMA bone_cortical

    #------------ Initialize Calc. ------------
    total_count = [int(fs[0]*total_length[0]),int(fs[1]*total_length[1])]
    grids  = Initialize(total_length, total_count)
    xenergy_ref = 25 #KeV
    wave_length = 1.24/xenergy_ref*nm
    sep  = float(args[2])*um
    period = (2*wave_length*distance3)/sep


    delta_r,beta_r=matl.mat_delta_beta(material,xenergy_ref)
    amp = (distance3+distance2+distance1)/distance1                 # sample before grating
    #sep = 2*wave_length*distance3/period                           # sample before grating
    # amp = (distance3+distance2+distance1)/(distance1 + distance2)   # sample after grating
    # sep = 2*wave_length*distance1*distance3/period/(distance1 + distance2)          # sample after grating
    para = []
    para.extend((distance1,distance2,distance3,xenergy_ref,period,sep,cylinder_diameter,material,cylinder_diameter,detector_res,pixel_number,delta_r,beta_r))
    G2Period     = (distance3+distance2+distance1)/2/(distance2+distance1) * period
    fringe_period = (distance3+distance2+distance1)/((1.0/G2Period - 1.0/period)*(distance2+distance1) + 1.0/G2Period*distance3)
    print(fringe_period)
    # G2Period = 4.48 
    # G2Period = 8.0
    print("sep=",sep,"amp=",amp,"G2_period=",G2Period,"Fringe_period=",fringe_period)
    sourceT_objs = []
    sourceT_bkgs = []
    xenergy_ratio =  float(args[1])
    xenergy =  float(args[0])               # X-ray energy in keV
    for j in range(G0SampNum):        
        wave_length = 1.24/xenergy_ref*nm
        wave_number = 2.*np.pi/wave_length
        absor_ref_obj,objrefdpc = core.ObjRef(total_count, wave_number,cylinder_1,total_length,fs,material,xenergy,amp,sep/2.0)
        print('xenergy = ',xenergy,'xenergy_ratio=',xenergy_ratio)
        print('position_x = ',pos_x[j])
        #------------ Calc. starts ------------
        source2obj = propagator.Propagation_point_source(pos_x[j],distance1,total_count,total_length,wave_length)
        #sample beforer grating
        #Sample and grating
        Object_cylinder_1 = core.Object_cylinder_side(total_count, wave_number, cylinder_1, total_length, fs,material,xenergy)
        grating = core.Phase_grating(period, fs, total_count,xenergy)
        # #------------ with sample -------------

        source2gobj = propagator.Propagation_dfft(source2obj*Object_cylinder_1, distance2, distance1, wave_length, 1.0/fs[1])
        source2zp=propagator.Propagation_dfft(source2gobj*grating, distance3,distance1,wave_length, 1.0/fs[1])
        sourceT_obj = core.PhaseStepping(source2zp, numStep, total_count, fs,xenergy_ratio,G2Period)   # with a PI/2 phase grating
        sourceT_objs.append(sourceT_obj)
        # #------------ without sample -------------
        source2gbkg = propagator.Propagation_dfft(source2obj, distance2,distance1,wave_length, 1.0/fs[1])
        source2zpb = propagator.Propagation_dfft(source2gbkg*grating, distance3,distance1,wave_length, 1.0/fs[1])
        sourceT_bkg = core.PhaseStepping(source2zpb, numStep, total_count, fs,xenergy_ratio,G2Period)
        sourceT_bkgs.append(sourceT_bkg)


        #sample after grating
        # #------------ with sample -------------
        # Object_cylinder_1 = core.Object_cylinder_side(total_count, wave_number, cylinder_1, total_length, fs,material,xenergy)
        # grating = core.Phase_grating(period, fs, total_count,xenergy)
        # source2gobj = propagator.Propagation_dfft(source2obj*grating, distance2, distance1, wave_length, 1.0/fs[1])
        # source2zp=propagator.Propagation_dfft(source2gobj*Object_cylinder_1, distance3,distance1,wave_length, 1.0/fs[1])
        # sourceT_obj = core.PhaseStepping(source2zp, numStep, total_count, fs,xenergy_ratio,G2Period)   # with a PI/2 phase grating
        # sourceT_objs.append(sourceT_obj)
        # # #------------ without sample -------------
        # source2zpb = propagator.Propagation_dfft(source2gobj, distance3,distance1,wave_length, 1.0/fs[1])
        # sourceT_bkg = core.PhaseStepping(source2zpb, numStep, total_count, fs,xenergy_ratio,G2Period)
        # sourceT_bkgs.append(sourceT_bkg)
        #plot_compare_figures(source2zp[0],source2zpb[0])
        del source2obj
        del Object_cylinder_1
        del grating
        del source2gobj
        del source2gbkg
        del sourceT_bkg
        del source2zpb
        del sourceT_obj
        del source2zp
        #save_figure_split([sourceT_obj],[sourceT_bkg],'obj_bkg_split_figure',begin_time,fs,total_length,para,xenergy,pos_x[j])

    FTout_obj, FDetT1s_obj = core.Signal_extract_fft(sourceT_objs,pixel_number,numStep)      
    FTout_bkg, FDetT1s_bkg = core.Signal_extract_fft(sourceT_bkgs,pixel_number,numStep)  
    phi_final,absor_final = misc.result_info(FTout_obj, FTout_bkg)

    phi_prj,abs_img,df_img = core.Signal_extract(sourceT_objs,total_count, pixel_number)
    phi_bkg,abs_img_bkg,df_img_bkg = core.Signal_extract(sourceT_bkgs,total_count, pixel_number) 
    phi_final_2 = misc.Phi_info(phi_prj, phi_bkg,pixel_number)
    absor_final_2 = -np.log(abs_img/abs_img_bkg)
    absor_final_dark_field =  -np.log(df_img/df_img_bkg)
    savedata.save_intensity_data(FDetT1s_obj,FDetT1s_bkg,'intensity',begin_time,fs,total_length,para,xenergy,out_path)
    savedata.save_data_split(sourceT_objs,'obj_split',begin_time,fs,total_length,para,xenergy,out_path)
    savedata.save_data_split(sourceT_bkgs,'bkg_split',begin_time,fs,total_length,para,xenergy,out_path)
    savedata.save_data_1D([phi_final],"phi_final_fft",begin_time,fs,total_length,para,pixel_number,xenergy,out_path)
    savedata.save_data_1D([absor_final],"absor_final_fft",begin_time,fs,total_length,para,pixel_number,xenergy,out_path)
    savedata.save_data_1D(phi_final_2,"phi_final_atan",begin_time,fs,total_length,para,pixel_number,xenergy,out_path)
    savedata.save_data_1D(absor_final_2,"absor_final_atan",begin_time,fs,total_length,para,pixel_number,xenergy,out_path)
    savedata.save_data_1D(absor_final_dark_field,"absor_final_atan_dark_fild",begin_time,fs,total_length,para,pixel_number,xenergy,out_path)
    savedata.save_imshow(phi_final,absor_final,begin_time,fs,total_length,para,xenergy,'fft',out_path)
    savedata.save_imshow(phi_final_2[0],absor_final_2[0],begin_time,fs,total_length,para,xenergy,'arctan',out_path)
    savedata.save_imshow(phi_final_2[0],absor_final_dark_field[0],begin_time,fs,total_length,para,xenergy,'arctandf',out_path)

    #draw_ref_final(absor_final,phi_final,absor_ref_obj,objrefdpc,pixel_number)
    end_time = time()
    run_time = end_time-begin_time
    print ('time',run_time)

def plot_compare_figures(data_A,data_B):
    ''' Compare the intensity and phase of data_A and data_B'''
    # print(int(len((data_A)/50)))
    data_A_c = data_A.copy()
    data_B_c = data_B.copy()
    # data_A_c = data_A_c.reshape(10000,int(len(data_A_c)/10000)).mean(1)
    # data_B_c = data_B_c.reshape(10000,int(len(data_B_c)/10000)).mean(1)
    test_phi_complex(data_A_c,data_B_c)
    # data_A = data_A.reshape(10000,int(len(data_A)/10000)).mean(1)
    # data_B = data_B.reshape(10000,int(len(data_B)/10000)).mean(1)
    fig, axs = plt.subplots(2,2,figsize=(9, 6))
    axs[0,0].plot(abs((data_A)**2),'r--',label='With sample')
    axs[0,1].plot(abs((data_B)**2),'b--',label='Without sample')
    axs[1,1].plot(abs((data_B)**2) - abs((data_A)**2),'b',label='Without sample - With sample')
    axs[1,0].plot(abs((data_A)**2),'r--',label='With sample')
    axs[1,0].plot(abs((data_B)**2),'b--',label='Without sample')
    axs[0,0].legend(loc='best',fontsize=10,frameon=False)
    axs[0,1].legend(loc='best',fontsize=10,frameon=False)
    axs[1,0].legend(loc='best',fontsize=10,frameon=False)
    axs[1,1].legend(loc='best',fontsize=10,frameon=False)
    plt.show()

def test_phi_complex(data_A,data_B):
    ''' Compare phase of data_A and data_B'''
    phi = []
    data_A = [ [np.real(data_A[i]),np.imag(data_A[i])]   for i in range(len(data_A))]
    data_B = [ [np.real(data_B[i]),np.imag(data_B[i])]   for i in range(len(data_B))]
    for i in range(len(data_A)):
        a = data_A[i]
        b = data_B[i]
        cos_ab = np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))
        sin_ab = np.cross(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))
        angle_ab = np.arctan2(sin_ab, cos_ab)
        phi.append(angle_ab)
    fig, axs = plt.subplots(1,1,figsize=(9, 6))
    x_data = np.arange(len(phi))
    plt.plot(phi,'r')
    plt.title('difference phase of without obj and with obj')
    # plt.scatter(x_data,phi)
    # plt.show()

def draw_ref_final(absor_final,phi_final,absor_ref_obj,objrefdpc,pixel_number):
    ''' Compare simulation and ref'''
    refobj = (gauss_filter_reshape(absor_ref_obj,int(pixel_number)))[0]
    refobj = abs(refobj-max(refobj))
    #refobj = refobj/(max(refobj))
    #absor_final = absor_final/(max(absor_final))
    #phi_final = phi_final/(max(phi_final))
    objrefdpc = (gauss_filter_reshape(objrefdpc,int(pixel_number)))[0]
    #objrefdpc = objrefdpc/(max(objrefdpc))
    fig, axs = plt.subplots(1,2,figsize=(9, 6))
    axs[0].plot(absor_final,'r--',lw=2,label='sim_obj_absor')
    axs[0].plot(refobj,'b',lw=2,label='ref_obj_absor')
    axs[1].plot(phi_final,'r--',lw=2,label='sim_obj_phi')
    axs[1].plot(np.real(objrefdpc),'b',lw=2,label='ref_obj_phi')
    axs[0].grid()
    axs[1].grid()    
    axs[0].legend(loc='best',fontsize=15,frameon=False)
    axs[1].legend(loc='best',fontsize=15,frameon=False)
    plt.show()     

def smooth_curve(data,obj_legth,fs):
    ''' sim curve smooth '''
    number_data= int(len(data[0]))
    number_obj = int(obj_legth*fs[1])
    min_obj = int(number_data/2-number_obj/2)
    max_obj =int(number_data/2+number_obj/2)
    for i in range(80):
        data[0][min_obj-i] = ( data[0][min_obj-i] +  data[0][min_obj+1-i])/2.
    for i in range(80):
        data[0][max_obj+i] = ( data[0][max_obj+i] +  data[0][max_obj-1+i])/2.
    return data

def gauss_filter_reshape(data,pixel_number):
    '''  Bin data '''
    data = [(data[0]).reshape(pixel_number,int(len(data[0])/pixel_number)).mean(1)]
    data = np.array(data)
    #data= gaussian_filter(data,sigma=1)
    return data

def read_xenergy(dir_path_name):
    ''' Get infor of x energy and ratio for sprectrum'''
    file_v = open(dir_path_name,'r')
    v_info = file_v.readlines()
    xenergy_list = [float(v_info[i].split('  ')[0]) for  i in range(len(v_info))]
    v_list_y = [float(v_info[i].split('  ')[1]) for  i in range(len(v_info))]
    xenergy_ratio = [v_list_y[i]/sum(v_list_y) for i in range(len(v_list_y))]
    return [xenergy_list,xenergy_ratio]

def xspec_total1(input_data):
    ''' Add all intensities together for each steps'''
    data_out = []
    data_in = input_data.copy()          
    for i in range(len(data_in)):
        if i == 0:
            for j in range(len(data_in[0])):
                exec('s_%s = data_in[%d][%d]'%(j,i,j))
        else:
            for j in range(len(input_data[0])):          
                exec('s_%s = s_%s + data_in[%d][%d]'%(j,j,i,j))
    for j in range(len(data_in[0])):   
        exec('data_out = data_out.append(s_%s)'%(j))
    return data_out   

if __name__ == '__main__':
    main()