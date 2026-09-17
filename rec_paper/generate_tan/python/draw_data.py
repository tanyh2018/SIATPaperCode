import matplotlib.pyplot as plt 
import numpy as np
import sys
import io

def main():

      Nx = 5120
      Ny = 5120
      
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
            center = [800+150*i,2000-150*i]
            data2 = data2 + fill_circular(center,100,mat1,data1)
      for i in range(6):
            data1 = np.zeros((Ny,Nx))
            center = [1000+150*i,2100-150*i]
            data2 = data2 + fill_circular(center,100,mat1,data1)
      for i in range(4):
            data1 = np.zeros((Ny,Nx))
            center = [2000+350*i,2100-350*i]
            data2 = data2 + fill_circular(center,200,mat3,data1)
      for i in range(4):
            data1 = np.zeros((Ny,Nx))
            center = [2900+350*i,1850]
            data2 = data2 + fill_circular(center,150,mat3,data1)

      ## Rectangle
      for i in range(6):
            rec_size= [100,1500-i*100]
            data1 = np.zeros((Ny,Nx))
            center = [800+350*i,3200]
            data2 = data2 + fill_rectangle(center,rec_size,mat2,data1)

      for i in range(6):
            rec_size= [800,150]
            data1 = np.zeros((Ny,Nx))
            center = [3200,3000+i*300]
            data2 = data2 + fill_rectangle(center,rec_size,mat2,data1)

      ## Ring
      for i in range(6):
            rr = [150-i*10,200]
            data1 = np.zeros((Ny,Nx))
            center = [4600,1000+i*600]
            data2 = data2 + fill_ring(center,rr,mat2,data1)

      data2 = data2.reshape(int(Nx/10),10,int(Ny/10),10)
      data2 = (data2.mean(1)).mean(2)
      # fig, axs = plt.subplots(1,1,figsize=(9, 6))
      # axs.imshow(data2,cmap='gray')
      # plt.show()

      outpath = "D:/xianjinyuan/reconstruction/tyh/DPC_rec/generate_tan/python/"
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