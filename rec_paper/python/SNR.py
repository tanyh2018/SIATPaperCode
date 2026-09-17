import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit
from scipy import optimize
import numpy as np
import os
def main():
      data_path = './SNRdata/'
      SNR = []
      input_names = []
      for file_name in os.listdir(data_path):
            input_name = data_path + file_name
            input_names.append(input_name)
            SNR.append(get_SNR(input_name))
      draw_SNR_pixel(input_names,SNR)
      plt.show()

def get_SNR(input_name):
      #data read
      data = read_data_spc(input_name)
      data = data.reshape(512,512)

      #Signal mean
      fig, axs = plt.subplots(1,1,figsize=(9, 6))
      plt.plot(data[427])
      signal_mean = 0
      for i in range(5):
            signal_mean += np.mean(data[425+i][50:180])
      signal_mean = signal_mean/5/1000 #m->mm
      print("signal_mean=",signal_mean)

      noise = []
      for i in range(5):
            for j in range(len(data[425])):
                  if (j>200 and j<290) or (j>335):
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
      x_list = np.linspace(min(noise), max(noise), 2*nbin)
      out_put_LSF = func_gauss(x_list, *popt)
      plt.plot(x_list, out_put_LSF ,'r-',lw=3)

      #Get SNR
      noise_sigma = abs(popt[2]/1000)
      print('noise_sigma=',popt[2]/1000)
      SNR = signal_mean/noise_sigma
      print("SNR=",SNR)
      return SNR 
      # plt.show()
def draw_SNR_pixel(input_names,SNR):
      Nshift = []
      for i in range(len(input_names)):
            Nshift.append(int((input_names[i]).split('_')[4]))
      zipped = list(zip(Nshift, SNR))
      zipped_sorted = sorted(zipped, key=lambda x: x[0])
      list1, list2 = zip(*zipped_sorted)
      fig, axs = plt.subplots(1,1,figsize=(9, 6))
      plt.plot(list1,list2,'black',lw=2)
      plt.xlabel( "$\Delta s$ pixel",fontdict={'size': 20} )
      plt.ylabel("SNR",fontdict={'size': 20} )
      plt.show()
def read_data_spc(input_path):
      data_type = 'float32'
      raw_image = np.fromfile(input_path,data_type)
      return raw_image

def func_gauss(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))

if __name__ == '__main__':
      main()