import matplotlib.pyplot as plt 
import numpy as np
import sys
import io

def main():

      Nx = 512
      Ny = 512
      
      # absor attenuation coefficient and phase coefficient
      model = "absor-tmp"   # "phase or absor"    unit  mm-1
      k = 2*np.pi*8.0/1.24*1e6     # mm-1
      print(k)
      if model == "absor-tmp":
            mat1 = 0.4178     # polystyrene    
            mat2 = 13.4       # Aluminum
            mat3 = 14.9       # SiC
      if model == "phase-tmp":
            mat1 = 3.71e-6*k    # polystyrene
            mat2 = 8.58e-6*k    # Aluminum
            mat3 = 1.06e-5*k    # SiC

      ## Circular
      data2 = np.zeros((Ny,Nx))
      for i in range(1):
            data1 = np.zeros((Ny,Nx))
            center = [130,256]
            data2 = data2 + fill_oval(center,50,35,mat1,data1)
      ## Rectangle
      for i in range(1):
            rec_size= [60,210]
            data1 = np.zeros((Ny,Nx))
            center = [220,151]
            data2 = data2 + fill_rectangle(center,rec_size,mat2,data1)

      for i in range(1):
            rec_size= [40,312]
            data1 = np.zeros((Ny,Nx))
            center = [334,100]
            data2 = data2 + fill_rectangle(center,rec_size,mat2,data1)

      plt.show()

      outpath = "D:/xianjinyuan/reconstruction/tyh/DPC_rec/likelihood_tv/python/"
      with io.open(outpath + model + "_image.raw",'wb') as f:
            data2.astype(np.float32).tofile(f)  

def fill_circular(center,radius,mat,data):
      Ny,Nx = data.shape
      R=radius
      for j in range(Ny):
            for i in range(Nx):
                  if R*R>=(center[1]-i)**2 + (center[0]-j)**2:
                        data[j,i] = mat
      return data

def fill_oval(center,r1,r2,mat,data):
      Ny,Nx = data.shape
      # R=radius
      for j in range(Ny):
            for i in range(Nx):
                  if 1>=(center[1]-i)**2/r1/r1 + (center[0]-j)**2/r2/r2:
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