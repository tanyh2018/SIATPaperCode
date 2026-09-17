import matplotlib.pyplot as plt 
import numpy as np
import sys
import io

def main():
      amp = 10
      Nx = 512*amp
      Ny = 512*amp

      # absor attenuation coefficient and phase coefficient
      model = "absor"   # "phase or absor"    unit  mm-1
      k = 2*np.pi*8.0/1.24*1e6     # mm-1
      print(k)
      if model == "absor":
            mat1 = 0.4178     # polystyrene    
            mat2 = 13.4       # Aluminum
            mat3 = 14.9       # SiC
      if model == "phase":
            mat1 = 3.71e-6*k    # polystyrene
            mat2 = 8.58e-6*k    # Aluminum
            mat3 = 1.06e-5*k    # SiC

      ## Circular

      data2 = np.zeros((Ny,Nx))
      for i in range(6):
            data1 = np.zeros((Ny,Nx))
            center = [80*amp+15*amp*i,250*amp-15*amp*i]
            data2 = data2 + fill_circular(center,10*amp,mat1,data1)
      for i in range(6):
            data1 = np.zeros((Ny,Nx))
            center = [100*amp+15*amp*i,260*amp-15*amp*i]
            data2 = data2 + fill_circular(center,10*amp,mat1,data1)
      for i in range(4):
            data1 = np.zeros((Ny,Nx))
            center = [200*amp+35*amp*i,210*amp-35*amp*i]
            data2 = data2 + fill_circular(center,20*amp,mat1,data1)
      for i in range(4):
            data1 = np.zeros((Ny,Nx))
            center = [290*amp+35*amp*i,185*amp]
            data2 = data2 + fill_circular(center,15*amp,mat1,data1)

      # Rectangle

      for i in range(6):
            rec_size= [10*amp,150*amp-i*10*amp]
            data1 = np.zeros((Ny,Nx))
            center = [80*amp+35*amp*i,320*amp]
            data2 = data2 + fill_rectangle(center,rec_size,mat2,data1)

      for i in range(6):
            rec_size= [80*amp,15*amp]
            data1 = np.zeros((Ny,Nx))
            center = [320*amp,300*amp+i*30*amp]
            data2 = data2 + fill_rectangle(center,rec_size,mat2,data1)

      ## Ring
      for i in range(6):
            rr = [15*amp-i*amp,20*amp]
            data1 = np.zeros((Ny,Nx))
            center = [460*amp,100*amp+i*60*amp]
            data2 = data2 + fill_ring(center,rr,mat3,data1)

      # MTF shape
      # data2 = np.zeros((Ny,Nx))
      # data1 = np.zeros((Ny,Nx))
      # center = [256*amp,256*amp]
      # data2 = data2 + fill_circular(center,150*amp,mat2,data1)

      data2 = data2.reshape(int(Nx/amp),amp,int(Ny/amp),amp)
      data2 = (data2.mean(1)).mean(2)
      # fig, axs = plt.subplots(1,1,figsize=(9, 6))
      # axs.imshow(data2,cmap='gray')
      # plt.show()

      outpath = "D:/xianjinyuan/reconstruction/tyh/DPC_rec/likelihood_tv/data/"
      with io.open(outpath + model + "_MTF_image.raw",'wb') as f:
            data2.astype(np.float32).tofile(f)  

def fill_circular(center,radius,mat,data):
      Ny,Nx = data.shape
      R=radius
      for j in range(Ny):
            for i in range(Nx):
                  if R*R>=(center[1]-i)**2 + (center[0]-j)**2:
                        data[j,i] = mat
      return data

def fill_rectangle(center,rec_size,mat,data):
      Ny,Nx = data.shape
      r = rec_size
      for j in range(Ny):
            for i in range(Nx):
                  if j - center[0] >= 0 and j - center[0] <= r[0]:
                        if i - center[1] >= 0 and i - center[1] <= r[1]: 
                              data[j,i] = mat           
      return data

def fill_ring(center,rr,mat,data):
      Ny,Nx = data.shape
      rin = rr[0]
      rout = rr[1]
      for j in range(Ny):
            for i in range(Nx):
                  if rout*rout>=(center[1]-i)**2 + (center[0]-j)**2 and rin*rin<=(center[1]-i)**2 + (center[0]-j)**2:
                        data[j,i] = mat
      return data

if __name__ == '__main__':
      main()