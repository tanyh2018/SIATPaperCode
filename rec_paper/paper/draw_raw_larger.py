import matplotlib.pyplot as plt 
import numpy as np
import os
import matplotlib.ticker as ticker
from scipy.optimize import curve_fit
from scipy import optimize
def main():

      #data_path = './deltas/'
      data_path = './belta=0.05/'
      #data_path = './fig4/'
      SNR = []
      input_names = []
      vr = [0,1.2e-5]
      vrd = [0,4.5e-6]

      # vr = [0,95]
      # vrd = [0,95]

      for file_name in os.listdir(data_path):
            if "sub"  not in file_name and "phase" not in file_name and ".raw" in file_name:
                  
                  input_name = data_path + file_name
                  input_names.append(input_name)
                  get_total_fig(input_name,vr)
                  print(file_name)
                  print("SNR=",get_SNR(input_name))
            # if "sub.raw" in file_name:
            #       print(file_name)
            #       input_name = data_path + file_name
            #       input_names.append(input_name)
            #       get_total_fig2(input_name,vr,vrd)
            # if "sub"  not in file_name and "phase" not in file_name and ".raw" in file_name:
            #       print(file_name)
            #       input_name = data_path + file_name
            #       input_names.append(input_name)
            #       figure4_plot(input_name,vr)
      plt.show()

def get_SNR(input_name):
      #data read
      data = read_data_spc(input_name)
      data = data.reshape(512,512)

      #Signal mean
      fig, axs = plt.subplots(1,1,figsize=(9, 6))
      plt.plot(data[430])

      signal_mean = 0
      for i in range(3):
            signal_mean += np.mean(data[425+i][44:180])
      signal_mean = signal_mean/5/1000 #m->mm
      print("signal_mean=",signal_mean)

      noise = []
      for i in range(3):
            for j in range(len(data[425])):
                  if (j>330):
                        if data[425+i][j] !=0:
                              noise.append(data[425+i][j])

      #Noise fit to get sigma
      nbin = 40
      fig, axs = plt.subplots(1,1,figsize=(9, 6))
      hist =  plt.hist(noise, bins=nbin)
      y = hist[0]
      x_l = np.linspace(min(noise), max(noise), nbin)
      mean = np.mean(noise)
      variance = np.var(noise)
      sigma = np.sqrt(variance)
      popt, covariance = optimize.curve_fit(func_gauss, x_l, y,p0=[1,mean,sigma])
      
      #Fit data
      print(popt)
      x_list = np.linspace(min(noise), max(noise), 2*nbin)
      out_put_LSF = func_gauss(x_list, *popt)
      plt.plot(x_list, out_put_LSF ,'r-',lw=3)

      #Get SNR
      noise_sigma = abs(popt[2]/1000)
      print('noise_sigma=',noise_sigma)
      SNR = signal_mean/noise_sigma
      print("SNR=",SNR)
      return SNR 


def get_total_fig(input_name,vr):
      xmi = 360
      xma = 445
      ymi = 237
      yma = 310
      data = read_data_spc(input_name)
      outp = input_name.split(".raw")[0]
      data = data.reshape(512,512)
      # draw_line(data,outp)
      fig, axs = plt.subplots(1,1,figsize=(9, 6))
      h=plt.imshow(data[xmi:xma,ymi:yma], cmap='gray',vmin=0,vmax=4.5e-6)
      clim = plt.gci().get_clim()
      plt.axis('off')
      plt.savefig(outp+'_d.svg', bbox_inches='tight')
      fig, axs = plt.subplots(1,1,figsize=(9, 6))
      plt.imshow(data, cmap='gray',vmin=vr[0],vmax=vr[1])
      print("Contrast=",clim)
      #plt.imshow(data, cmap='gray',vmin=0,vmax=360000)
      #plt.imshow(data, cmap='gray')
      plt.plot([ymi, yma, yma, ymi, ymi],[xmi, xmi, xma, xma, xmi], color='#7FC8D7',lw=1.5)

      # plt.plot([0,999],[342,342], color='#7FC8D7',lw=4)

      # plt.plot([50, 100],[500,500], color='white',lw=4.0)
      # plt.text(20, 480, '1 $\mathrm{\mu}$m', color='white', fontsize=30)


      # plt.plot([800, 900],[950,950], color='white',lw=4.0)
      # plt.text(740, 900, '1 $\mathrm{\mu}$m', color='white', fontsize=35)
      plt.axis('off')
      plt.savefig(outp+'_h.svg', bbox_inches='tight')


def get_total_fig2(input_name,vr,vrd):
      #data read
      xmi = 360
      xma = 445
      ymi = 237
      yma = 310
      data = read_data_spc(input_name)
      outp = input_name.split(".raw")[0]
      data = data.reshape(512,512)
      # fig, axs = plt.subplots(1,1,figsize=(9, 6))
      # h=plt.imshow(data[xmi:xma,ymi:yma], cmap='gray',vmin=vrd[0],vmax=vrd[1])
      # clim = plt.gci().get_clim()
      # plt.axis('off')
      # plt.savefig(outp+'_h.svg', bbox_inches='tight')
      fig, axs = plt.subplots(1,1,figsize=(9, 6))
      #plt.imshow(data, cmap='gray',vmin=clim[0],vmax=clim[1])
      plt.imshow(data, cmap='gray',vmin=vrd[0],vmax=vrd[1])
      #plt.imshow(data, cmap='gray')
      #plt.plot([ymi, yma, yma, ymi, ymi],[xmi, xmi, xma, xma, xmi], color='#7FC8D7',lw=1.5)
      plt.axis('off')
      if "PWLS-TV-sub" in input_name:
            plt.plot([400, 450],[480,480], color='white',lw=4.0)
            plt.text(365, 450, '1 $\mathrm{\mu}$m', color='white', fontsize=30)
      plt.savefig(outp+'_d.svg', bbox_inches='tight')

def draw_line(data,outp):
      fig, axs = plt.subplots(1,1,figsize=(9, 4))
      my_list = [i*10 for i in range(1,513)]
      plt.plot(my_list,np.mean(data[140:160,:],0), color='#7FC8D7',lw=2)
      plt.ylabel( "$\delta$",fontdict={'size': 30} )
      plt.xlabel("x (nm)",fontdict={'size': 30} )
      plt.tick_params(labelsize=25)
      axs.tick_params(axis='y', labelsize=25)
      #axs.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.0e'))
      axs.yaxis.set_major_locator(ticker.MultipleLocator(1e-5))
      axs.yaxis.set_major_formatter(ticker.FuncFormatter(my_formatter))
      plt.ylim(0,1.2e-5)
      plt.savefig(outp+'_line.svg', bbox_inches='tight')
      # axs.xaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
      # axs.ticklabel_format(axis='x', style='sci', scilimits=(-2, 3))

def figure4_plot(input_name,vr):
      xmi = 360
      xma = 445
      ymi = 237
      yma = 310
      data = read_data_spc(input_name)
      outp = input_name.split(".raw")[0]
      data = data.reshape(512,512)
      draw_line(data,outp)

      fig, axs = plt.subplots(1,1,figsize=(9, 6))
      plt.imshow(data, cmap='gray',vmin=vr[0],vmax=vr[1])
      plt.plot([0,511],[150,150], color='#7FC8D7',lw=4)
      plt.plot([ymi, yma, yma, ymi, ymi],[xmi, xmi, xma, xma, xmi], color='#7FC8D7',lw=1.5)
      # plt.plot([80, 130],[500,500], color='white',lw=4.0)
      # plt.text(45, 480, '1 $\mathrm{\mu}$m', color='white', fontsize=30)
      plt.axis('off')
      plt.savefig(outp+'_h.svg', bbox_inches='tight')

def my_formatter(x, pos):
    if x == 0:
        return '0'
    else:
        return '%.0e' % x
def read_data_spc(input_path):
      data_type = 'float32'
      raw_image = np.fromfile(input_path,data_type)
      return raw_image

def func_gauss(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))

if __name__ == '__main__':
      main()