import matplotlib.pyplot as plt 
import numpy as np
import sys
import io
from scipy.ndimage import gaussian_filter
import os
import gc

def main():
      detector_effect()
      # material_effect()
      # sample_size_effect()
      # dir_path = '/data2/tanyuhang/data/talbot_result/material/20221212_'
      # dir_pre = ['graphite']
      #dir_pre = ['bonecortical','aluminum','graphite','mgo','PMMA']
      # dir_pre = ['water','graphite','mylar','PMMA']

def sample_size_effect():
      names = ['20221025_sample_size_400/','20221025_sample_size_500/']
      dir_path = '/data2/tanyuhang/data/talbot_result/sample_size/'
      args = sys.argv[1:]
      gc.set_threshold(500,5,5)
      for j in range(len(names)):
            dir_paths = dir_path + names[j]
            dir_path_prexs = os.listdir(dir_paths)
            for i in range(len(dir_path_prexs)):
                  dir_path_prex = dir_paths + dir_path_prexs[i]+'/'
                  period = float((dir_path_prexs[i]).split('_')[1])
                  if args[0] in dir_path_prex:
                        print(dir_path_prex)
                        draw_linesource_figure(dir_path_prex) 


def material_effect():
      names = ['20240522_mylar/','20240522_graphite/','20240522_PMMA/','20240522_water/']
      dir_path = '/data4/tanyuhang/data/talbot_result/'
      args = sys.argv[1:]
      gc.set_threshold(500,5,5)
      for j in range(len(names)):
            dir_paths = dir_path + names[j]
            dir_path_prexs = os.listdir(dir_paths)
            for i in range(len(dir_path_prexs)):
                  dir_path_prex = dir_paths + dir_path_prexs[i]+'/'
                  period = float((dir_path_prexs[i]).split('_')[1])
                  if args[0] in dir_path_prex:
                        print(dir_path_prex)
                        draw_linesource_figure(dir_path_prex) 


def detector_effect():
      dir_path = '/data2/tanyuhang/data/talbot_result/20221212_graphite/'
      args = sys.argv[1:]
      gc.set_threshold(500,5,5)
      for j in range(1):
            dir_paths = dir_path
            dir_path_prexs = os.listdir(dir_paths)
            for i in range(len(dir_path_prexs)):
                  dir_path_prex = dir_paths + dir_path_prexs[i]+'/'
                  period = float((dir_path_prexs[i]).split('_')[1])
                  if args[0] in dir_path_prex:
                        print(dir_path_prex)
                        draw_linesource_figure(dir_path_prex) 

def delta_s_effect():
      args = sys.argv[1:]
      gc.set_threshold(500,5,5)
      dir_path = '/data4/tanyuhang/data/talbot_result/graphite_sd/20221212_'
      dir_pre = ['graphite']
      for j in range(1):
            dir_paths = dir_path + dir_pre[j]+'/'
            dir_path_prexs = os.listdir(dir_paths)
            for i in range(len(dir_path_prexs)):
                  dir_path_prex = dir_paths + dir_path_prexs[i]+'/'
                  # run batch jobs
                  if args[0] in dir_path_prex:
                        print(dir_path_prex)
                        draw_linesource_figure(dir_path_prex) 
                        
def draw_linesource_figure(dir_path_prex):
      '''  Get the intensity and phase result'''
      file_path_list = os.listdir(dir_path_prex)
      j=0
      for i in range (len(file_path_list)):
            if 'xenergy_25' in file_path_list[i]:
                  print(file_path_list[i])
                  obj_data, bkg_data = linesource_data_file(dir_path_prex+file_path_list[i])
                  if j==0:
                        obj_datas=obj_data
                        bkg_datas=bkg_data
                        j=1
                  else:
                        obj_datas+=obj_data
                        bkg_datas+=bkg_data
                        j=j+1    
                  del obj_data
                  del bkg_data                    
      if j > 1:
            colormodel = 'poly'
      else: 
            colormodel = 'mono'
      model = "line_source"
      #model = "point_source"
      i=5

      for j in range(1):
            total_number = 4800000
            step_n = 10
            pixel_size = 30 + 18*j
            pixel_number = int(total_number/pixel_size/1000)
            sigma = (1.55)*48/pixel_size

            # get_intensity_line_source(obj_datas,i,total_number,dir_path_prex + 'obj_intensity.png',step_n)
            # get_intensity_line_source(bkg_datas,i,total_number,dir_path_prex + 'bkg_intensity.png',step_n)
            I_stpt_obj =  get_line_signal_total_fft(obj_datas,i,total_number,step_n,model)
            del obj_datas
            I_stpt_bkg =  get_line_signal_total_fft(bkg_datas,i,total_number,step_n,model)
            del bkg_datas
            save_reshape_result(I_stpt_obj,dir_path_prex,'signal',colormodel,model)
            del I_stpt_obj
            save_reshape_result(I_stpt_bkg,dir_path_prex,'bkg',colormodel,model)
            del I_stpt_bkg

            # FTout_obj=get_gauss_filter(I_stpt_obj,pixel_number,sigma)
            # FTout_bkg=get_gauss_filter(I_stpt_bkg,pixel_number,sigma)
            # phi_final,absor_final = result_info(FTout_obj, FTout_bkg)
            # # phi_prj,abs_img  = get_line_signal_total(obj_datas,pixel_number,i,total_number,step_n,model,sigma)
            # # phi_bkg,abs_img_bkg = get_line_signal_total(bkg_datas,pixel_number,i,total_number,step_n,model,sigma)
            # # phi_final_2 = Phi_info(phi_prj, phi_bkg,pixel_number)
            # # absor_final_2 = -np.log(abs_img/abs_img_bkg)

            # materiral = (dir_path_prex.split('/')[6]).split('_')[1]
            # plot_data_sim(phi_final,i,dir_path_prex + 'phi_fft.png')
            # plot_data_sim(absor_final,i,dir_path_prex + 'absor_fft.png')
            # # plot_data_sim(phi_final_2,i,dir_path_prex + 'phi_artan.png')
            # # plot_data_sim(absor_final_2,i,dir_path_prex + 'absor_artan.png')
            # save_raw_data(phi_final,dir_path_prex + dir_path_prex.split('/')[-2] + '_sigma_' + str(round(sigma,2)) + '_phi_'+'pixel_size_'+str(pixel_size)+'_'+materiral+'_'+colormodel+'.raw') #single_energy sprectrum
            # save_raw_data(absor_final,dir_path_prex + dir_path_prex.split('/')[-2] + '_sigma_' + str(round(sigma,2)) + '_absor_'+'pixel_size_'+str(pixel_size)+'_'+materiral+'_'+colormodel+'.raw')
            # save_imshow(phi_final,absor_final,dir_path_prex +'sigma_'+str(sigma) +'_pixel_'+str(pixel_size) + '_imshowfft.png')      
      for x in list(locals().keys()):
            del locals()[x]
      gc.collect()
def save_imshow(phi_final,absor_final,name):
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
      plt.savefig(name) 

def save_different_gauss_filter_factor(dir_path_prex):
      ''' Use different gausss simga to blur the signal '''
      obj_datas = []
      bkg_datas = []

      file_path_list = os.listdir(dir_path_prex)
      for i in range (len(file_path_list)):
            if 'xenergy_' in file_path_list[i]:
                  print(file_path_list[i])
                  obj_data, bkg_data = linesource_data_file(dir_path_prex+file_path_list[i])
                  obj_datas.append(obj_data)
                  bkg_datas.append(bkg_data)
      model = "line_source"
      #model = "point_source"
      i=5
      total_number = 4800000
      step_n = 10
      pixel_number = 100
      I_stpt_obj =  get_line_signal_total_fft(obj_datas,i,total_number,step_n,model)
      I_stpt_bkg =  get_line_signal_total_fft(bkg_datas,i,total_number,step_n,model)
      for j in range(19):
            print('j=',j)
            sigma = round(1.4+0.01*(j+1),2)
            FTout_obj=get_gauss_filter(I_stpt_obj,pixel_number,sigma)
            FTout_bkg=get_gauss_filter(I_stpt_bkg,pixel_number,sigma)
            phi_final,absor_final = result_info(FTout_obj, FTout_bkg)
            plot_data_sim(phi_final,i,dir_path_prex  + '_sigma_'+str(sigma)+ 'phi_fft.png')
            plot_data_sim(absor_final,i,dir_path_prex  + '_sigma_'+str(sigma)+ 'absor_fft.png')
            save_raw_data(phi_final,dir_path_prex + dir_path_prex.split('/')[-2] + '_sigma_'+str(sigma)+'_phi.raw') #single_energy sprectrum
            save_raw_data(absor_final,dir_path_prex + dir_path_prex.split('/')[-2]  + '_sigma_'+str(sigma)+ '_absor.raw')
      # plt.show()
def save_reshape_result(input_list,dir_path_prex,model,colormodel,modeln):
      #second save
      FDetT1s = []
      pixel_number = 1000
      for i in range(len(input_list)):
            FDetT1s.append(gauss_filter_reshape(input_list[i],int(len(input_list[i])/pixel_number),0))
      data = np.array(FDetT1s)
      if model == 'signal':
            file_name_real = dir_path_prex +colormodel +'_' + modeln + '_obj_split.raw'
      elif model == 'bkg':
            file_name_real = dir_path_prex +colormodel +'_' + modeln + '_bkg_split.raw'
      with io.open(file_name_real,'wb') as f:
            data.astype(np.float32).tofile(f)
      print(file_name_real)
      return FDetT1s

def get_gauss_filter(input_list,pixel_number,sigma=1):
      FDetT1s = []
      for i in range(len(input_list)):
            FDetT1s.append(gauss_filter_reshape(input_list[i],pixel_number,sigma))
      output_list = get_phi_with_fft(FDetT1s)
      return output_list

def get_gauss_filter_nograting(input_list,pixel_number,sigma=1):
      FDetT1s = []
      for i in range(len(input_list)):
            FDetT1s.append(gauss_filter_reshape(input_list[i],pixel_number,sigma))
      return FDetT1s

def linesource_data_file(input_path):
      ''' Read datas '''
      file_name_list = os.listdir(input_path)
      dir_path_obj_real = [ "".join([input_path,'/',file_name_list[j]]) for j in range(len(file_name_list)) if ('obj_split' in file_name_list[j] and 'raw' in file_name_list[j])]
      dir_path_bkg_real = (dir_path_obj_real[0]).replace('obj','bkg')
      obj_data =  read_data_spc(dir_path_obj_real[0])
      bkg_data =  read_data_spc(dir_path_bkg_real)
      return obj_data, bkg_data
def read_data_spc(input_path):
      data_type = 'float32'
      raw_image = np.fromfile(input_path,data_type)
      return raw_image

def get_line_signal_total_fft(obj_datas,sig_number,total_number,step_n,model='None'):
      ''' fft method to acquire phase and intensity '''
      obj_datas = obj_datas.reshape(sig_number,1,step_n,total_number) 
      I_stpt_obj = xspec_total(obj_datas,model)

      return I_stpt_obj
      
def get_phi_with_fft(input_datas):
    ''' fft method to acquire phase and intensity '''
    input_datas = np.array(input_datas)
    FTout = np.fft.fft(input_datas,int(len(input_datas)),-2)
    return FTout

def get_line_signal_total(obj_datas,pixel_number,sig_number,total_number,step_n,model,sigma=1):
      ''' arctan method to acquire phase and intensity '''
      FDetT1 = np.zeros([int(pixel_number)])
      FDetS1 = np.zeros([int(pixel_number)])
      FDetC1 = np.zeros([int(pixel_number)])
      obj_data = (obj_datas[0]).copy()
      for j in range(1,len(obj_datas)):
            obj_data = obj_data + obj_datas[j]
      obj_data = obj_data.reshape(sig_number,1,step_n,total_number)
      I_stpt_obj = xspec_total(obj_data,model)
      number_step = len(I_stpt_obj)
      print("number_step=",number_step)
      for i in range(len(I_stpt_obj)):
            sourceT = gauss_filter_reshape(I_stpt_obj[i],pixel_number,sigma)
            sourceS = sourceT * np.sin(2*np.pi*(i+1)/number_step)
            sourceC = sourceT * np.cos(2*np.pi*(i+1)/number_step) 
            FDetT1 = FDetT1 + sourceT
            FDetS1 = FDetS1 + sourceS
            FDetC1 = FDetC1 + sourceC
      return -np.arctan(FDetS1/FDetC1),FDetT1/number_step

def get_line_signal_total_no_grating(obj_datas,pixel_number,sig_number,total_number,step_n,sigma=1):
      ''' arctan method to acquire phase and intensity '''
      obj_data = (obj_datas[0]).copy()
      for j in range(1,len(obj_datas)):
            obj_data = obj_data + obj_datas[j]
      obj_data = obj_data.reshape(sig_number,1,step_n,total_number)
      I_stpt_obj = xspec_total(obj_data[0])
      number_step = len(I_stpt_obj)
      print("number_step=",number_step)
      sourceT = gauss_filter_reshape(I_stpt_obj[0],pixel_number,sigma)
      return sourceT

def save_raw_data(data,name):
    with io.open(name,'wb') as f:
        for i in range(360):
            data.astype(np.float32).tofile(f)

def xspec_total(input_data,model):
    ''' batch jobs add together'''
    data_out = []
    data_in = input_data.copy() 
    print('phase step = ',len(data_in[0][0]))
    print('point number = ', len(data_in))
    for i in range(len(data_in)):
      data_in2 = data_in[i] 
      if i == 0:
            for j in range(len(data_in2[0])):
                exec('s_%s = data_in2[%d][%d]'%(j,0,j))
      elif model != 'point_source':
            for j in range(len(data_in2[0])):          
                exec('s_%s = s_%s + data_in2[%d][%d]'%(j,j,0,j))
      elif model == 'point_source':
            if i==3:
                  for j in range(len(data_in2[0])):
                        exec('s_%s = data_in2[%d][%d]'%(j,0,j))            
    for j in range(len(data_in2[0])):   
        exec('data_out = data_out.append(s_%s)'%(j))
    return data_out  

def get_intensity_line_source(obj_datas,i,total_number,name,step_n,sigma=0):
      for k in range(len(obj_datas)):
            obj_data = (obj_datas[k]).reshape(i,1,step_n,total_number)
            inten_t = obj_data[0][0]
            for j in range(1,i):
                  # if j==5: 
                  obj_data1 = obj_data[j][0]
                  inten_t =  inten_t + obj_data1
      fig, axs = plt.subplots(1,3,figsize=(9, 6))
      # new_data = raw_image[0,200:1800].reshape(100,16).mean(1)
      out_data = gauss_filter_reshape(inten_t[1],50,0)
      axs[0].plot(gauss_filter_reshape(inten_t[0],50,0))
      axs[1].plot(gauss_filter_reshape(inten_t[1],50,0))
      axs[2].plot(gauss_filter_reshape(inten_t[2],50,0))
      axs[0].grid()
      axs[1].grid()
      axs[2].grid()
      plt.suptitle(name,fontsize=15)
      plt.savefig(name)   

def gauss_filter_reshape(data,pixel_number,gsigma):
    ''' Simulate Ch of detector'''
#     print(len(data))
    data = data.reshape(pixel_number,int(len(data)/pixel_number)).mean(1)
    data= gaussian_filter(data,sigma=gsigma)
    return data

def Phi_info(phi_prj, phi_bkg, total_count):
      ''' Arctan result '''
      phi_final = phi_prj-phi_bkg
      for jk in range(total_count):
            if phi_final[jk] > np.pi/2.:
                phi_final[jk] = phi_final[jk]-np.pi
            elif phi_final[jk] < -np.pi/2.:
                phi_final[jk] = phi_final[jk]+np.pi
      return phi_final

def result_info(fin_obj, fin_bkg):
      ''' fft result'''
      obj_phi = np.angle(fin_obj[1,:])
      bkg_phi = np.angle(fin_bkg[1,:])
      phi_final = obj_phi - bkg_phi
      phi_final = (phi_final + np.pi)%(2.*np.pi) - np.pi
      eps = 1e-10
      obj_absor = fin_obj[0,:]    
      bkg_absor = fin_bkg[0,:]
      absor_final = -np.log(obj_absor/(bkg_absor+eps)+eps)
      return phi_final,np.real(absor_final)



def plot_data_sim(data,i,name):
      fig, axs = plt.subplots(1,2,figsize=(9, 6))
      xticks = np.linspace(0,len(data),int(len(data)/5)+1)
      axs[0].plot(data)
      axs[0].grid()
      # axs[0].set_xticks(xticks)
      data_t = []
      for i in range(len(data)):
            data_t.append(data)
      axs[1].imshow(data_t,cmap='gray')
      plt.savefig(name)

def save_data(dir_path):
      fig, axs = plt.subplots(1,1,figsize=(9, 6))
      data_type = 'float32'
      raw_image = np.fromfile(dir_path,data_type)
      raw_image=raw_image.reshape(360,400,400)
      # new_data = raw_image[0,200:1800].reshape(100,16).mean(1) 
      plt.plot(raw_image[0][200])
      # file_name_raw = dir_path.split('.raw')[0] + "1.raw"
      # with io.open(file_name_raw,'wb') as f:
      #       for i in range(360):
      #             new_data.astype(np.float32).tofile(f)

def draw_sample(file_name,dir_path,y_range,total_length,fs,x_range):
      fig, axs = plt.subplots(2,2,figsize=(9, 6))
      x_ax = Initialize_1D(total_length,fs)
      h_array_total = []
      for i in range(len(file_name)):
            file_path = dir_path + file_name[i]
            data = np.loadtxt(file_path,delimiter=',')
            # range_index = [int(len(data)*(y_range[0])),int(len(data)*(y_range[1]))]     
            # h_array_c = data[int(len(data)/2.),range_index[0]:range_index[1]]
            # x_list_data = x_ax[range_index[0]:range_index[1]]
            # phi_pixel = data.reshape(int(len(data)/4),4,int(len(data)/4),4).mean(-1).sum(1)
            phi_pixel = data
            phi_pixel = phi_pixel[int(len(phi_pixel)/2.),200:int(len(phi_pixel))-200]
            if i == 0:
                  axs[0,1].plot(phi_pixel)
            elif i == 1:
                  axs[1,1].plot(phi_pixel)

      # for i in range(len(file_name)):
      #       file_path = dir_path + file_name[i]
      #       data = np.loadtxt(file_path,delimiter=',')
      #       range_index_y = [int(len(data)*(y_range[0])),int(len(data)*(y_range[1]))]     
      #       range_index_x = [int(len(data)*x_range[0]),int(len(data)*x_range[1])]  
      #       h_array_c = data[range_index_y[0]:range_index_y[1],range_index_x[0]:range_index_x[1]]
      #       # h_array_total.append(h_array_c)
      #       x_data_min = x_ax[range_index_x[0]]
      #       x_data_max = x_ax[range_index_x[1]]
      #       y_data_min = x_ax[range_index_y[0]]
      #       y_data_max = x_ax[range_index_y[1]]
      #       if i == 0:
      #             axs[0,0].imshow(h_array_c,origin = 'upper',cmap=  "gray",extent = [x_data_min, x_data_max, y_data_min, y_data_max])
      #       elif i == 1:
      #             axs[1,0].imshow(h_array_c,origin = 'upper',cmap=  "gray",extent = [x_data_min, x_data_max, y_data_min, y_data_max])
      axs[0,0].set_xlabel("x direction [$\mu$m]")
      axs[0,1].set_xlabel("x direction [$\mu$m]")
      axs[1,0].set_xlabel("x direction [$\mu$m]")
      axs[1,1].set_xlabel("x direction [$\mu$m]")

      axs[0,0].set_ylabel("y direction [$\mu$m]")
      axs[0,1].set_ylabel("Phase [Arb.]")
      axs[1,0].set_ylabel("Phase [Arb.]")
      axs[1,1].set_ylabel("Phase [Arb.]")


      # axs[0,0].grid(which='major', axis='both', linestyle='-')
      # axs[0,1].grid(which='major', axis='both', linestyle='-')
      axs[0,1].grid(which='major', axis='both', linestyle='-')
      axs[1,1].grid(which='major', axis='both', linestyle='-')
      fig.suptitle('Different results of step phase')
      file_number = dir_path.split("/")[1] 
      plt.savefig("figure/phase_amp_"+ file_number + ".png")


def DetBin(Fin, pixels, other_count):
    return Fin.reshape(pixels, other_count, 1, 1).sum(1).mean(1)
def AveBin(Fin, pixels, total_count):
    return Fin.reshape(pixels, int(total_count)//pixels, 1, 1).mean(-1).mean(1)

def draw_total(x_list_data,h_array_total,dir_path):
      h_total_value = h_array_total[0]
      for i in range(1,len(h_array_total)):
            print(i)
            h_total_value +=  h_array_total[i]
      fig1 = plt.figure(figsize=(9,6))
      plt.plot(x_list_data,h_total_value)
      # plt.xticks([- total_length/2., + total_length/2.])
      plt.grid()
      plt.xlabel( "x direction [$\mu$m] " )
      plt.ylabel("Intensity [Arb.]")
      plt.title("All phase step sum")
      file_number = dir_path.split("/")[1] 
      plt.savefig("figure/total_intensity"+ file_number + ".png")

def plt_2ddraw(file_name,dir_path,y_range,x_range,total_length,fs):
      fig, axs = plt.subplots(1,1,figsize=(10, 10))
      x_ax = Initialize_1D(total_length,fs)
      h_array_total = []
      # for i in range(len(file_name)):
      file_path = dir_path + file_name[0]
      data = np.loadtxt(file_path,delimiter=',')
      range_index_y = [int(len(data)*(y_range[0])),int(len(data)*(y_range[1]))]     
      range_index_x = [int(len(data)*x_range[0]),int(len(data)*x_range[1])]  
      h_array_c = data[range_index_y[0]:range_index_y[1],range_index_x[0]:range_index_x[1]]
      # h_array_total.append(h_array_c)
      x_data_min = x_ax[range_index_x[0]]
      x_data_max = x_ax[range_index_x[1]]
      y_data_min = x_ax[range_index_y[0]]
      y_data_max = x_ax[range_index_y[1]]
      axs.imshow(h_array_c,origin = 'upper',  extent = [x_data_min, x_data_max, y_data_min, y_data_max])
      # axs.imshow(h_array_c,cmap=plt.cm.gray)
      plt.xlabel('x direction [$\mu$m]')
      plt.ylabel('y direction [$\mu$m]')
      file_number = dir_path.split("/")[1] 
      plt.savefig("figure/twoD_intensity"+ file_number + ".png")
      # plt.show()

def plt_draw(file_name,dir_path,y_range,total_length,fs):
      fig, axs = plt.subplots(2,2,figsize=(9, 6))
      x_ax = Initialize_1D(total_length,fs)
      h_array_total = []
      for i in range(len(file_name)):
            file_path = dir_path + file_name[i]
            data = np.loadtxt(file_path,delimiter=',')
            range_index = [int(len(data)*(y_range[0])),int(len(data)*(y_range[1]))]     
            h_array_c = data[int(len(data)/2.),range_index[0]:range_index[1]]
            h_array_total.append(h_array_c)
            x_list_data = x_ax[range_index[0]:range_index[1]]
            cal_period(h_array_c,fs)
            if i == 0:
                  axs[0,0].plot(x_list_data,h_array_c)
            elif i == 1:
                  axs[0,1].plot(x_list_data,h_array_c)
            elif i == 2:
                  axs[1,0].plot(x_list_data,h_array_c)
            elif i == 3:
                  axs[1,1].plot(x_list_data,h_array_c)
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
      file_number = dir_path.split("/")[1] 
      plt.savefig("figure/four_intensity"+ file_number + ".png")
      return x_list_data,h_array_total
      # plt.show()

def plt_x_position_draw(file_name,dir_path,y_range,total_length,fs):
      fig, axs = plt.subplots(2,2,figsize=(10, 10))
      x_ax = Initialize_1D(total_length,fs)
      h_array_total = []
      file_path = dir_path + file_name[0]
      data = np.loadtxt(file_path,delimiter=',')
      range_index = [int(len(data)*(y_range[0])),int(len(data)*(y_range[1]))]
      for i in range(4):
            h_array_c = data[int(len(data)*i/4.),range_index[0]:range_index[1]]
            h_array_total.append(h_array_c)
            x_list_data = x_ax[range_index[0]:range_index[1]]
            if i == 0:
                  axs[0,0].plot(x_list_data,h_array_c)
            elif i == 1:
                  axs[0,1].plot(x_list_data,h_array_c)
            elif i == 2:
                  axs[1,0].plot(x_list_data,h_array_c)
            elif i == 3:
                  axs[1,1].plot(x_list_data,h_array_c)
      axs[0,0].set_xlabel("x direction [$\mu$m]")
      axs[0,1].set_xlabel("x direction [$\mu$m]")
      axs[1,0].set_xlabel("x direction [$\mu$m]")
      axs[1,1].set_xlabel("x direction [$\mu$m]")

      axs[0,0].set_ylabel("Intensity [Arb.]")
      axs[0,1].set_ylabel("Intensity [Arb.]")
      axs[1,0].set_ylabel("Intensity [Arb.]")
      axs[1,1].set_ylabel("Intensity [Arb.]")

      axs[0,0].set_title("y = -20 [$\mu$m]")
      axs[0,1].set_title("y = -10 [$\mu$m]")
      axs[1,0].set_title("y = 0 [$\mu$m]")
      axs[1,1].set_title("y = 10 [$\mu$m]")

      axs[0,0].grid(which='major', axis='both', linestyle='-')
      axs[0,1].grid(which='major', axis='both', linestyle='-')
      axs[1,0].grid(which='major', axis='both', linestyle='-')
      axs[1,1].grid(which='major', axis='both', linestyle='-')
      # fig.suptitle('Different results of step phase')
      file_number = dir_path.split("/")[1] 
      plt.savefig("figure/four_y_intensity"+ file_number + ".png")
      # plt.show() 

      return x_list_data,h_array_total

def cal_period(h_array_c,fs):
      ar_value = []
      arb_value = []
      averge = sum(h_array_c)/len(h_array_c)
      j = 0
      for i in range(int(len(h_array_c)-2)):
            a = h_array_c[i]
            b = h_array_c[i+1]
            if averge >= a and averge <=b and b>a and (i-j)>20:
                  ar_value.append(i)
                  j = i
      for i in range(len(ar_value)-1):
            arb_value.append(ar_value[i+1]-ar_value[i])
      print("averge period = %f"%(sum(arb_value)/len(arb_value)/fs))

def Initialize_1D(total_length,fs):
    rightmost_area = (total_length - 1.) / 2.
    leftmost_area = -1. * total_length / 2.
    return np.linspace(leftmost_area,rightmost_area,int(total_length*fs))

def float_def(input):
    try:
        float(input)
        return True
    except Exception as exc:
        return False
        
if __name__ == '__main__':
      main()
