import matplotlib.pyplot as plt 
import numpy as np
import sys
import io

def main():
      #dt2,pt2=two_rec()
      dt1,pt1=two_circle()

      # dif = max(pt2)-max(pt1)
      # pt2 = [x - dif for x in pt2]
      minpt1 = max(pt1)
      #minpt2 = max(pt2)
      #pt1 = [x/minpt1 for x in pt1]
      pt1 = [1- x/minpt1 for x in pt1]
      #pt2 = [x/minpt2-1 for x in pt2]
      fig, axs = plt.subplots(1,1,figsize=(9, 6))
      plt.plot(dt1,pt1,'#44AFC6',lw=2,label="Absorption Ring")
      # plt.plot(dt2,pt2,'#FFC000',lw=2,label="Absorption Grating")
      plt.xlabel( "Ring Shift Distance",fontdict={'size': 20} )
      plt.ylabel("Intensity",fontdict={'size': 20} )
      plt.tick_params(labelsize=15)
      plt.legend(loc='best',fontsize=20,frameon=False)
      plt.ylim([-0.2, 1.3])
      plt.savefig('Ring_grating.svg', bbox_inches='tight')
      plt.show()

def two_rec():
      amp = 1
      Nx = 500*amp
      Ny = 500*amp
      percent = []
      dt = []
      for j in range(200):
            print(j)
            data2 = np.zeros((Ny,Nx))
            #rec1
            for i in range(3):
                  p=60
                  rec_size= [100*amp, p/2]
                  data1 = np.zeros((Ny,Nx))
                  center = [150,200+p*i]
                  data2 = data2 + fill_rectangle(center,rec_size,data1)
            #rec2
            for i in range(7):
                  rec_size= [100*amp, 30]
                  data1 = np.zeros((Ny,Nx))
                  center = [150,200+j+p*i-p/2*7]
                  data2 = data2 + fill_rectangle2(center,rec_size,data1)
            mask = (data2 == 2)
            # 统计等于2的元素的数量
            count = np.count_nonzero(mask)
            percent.append(count/float(Nx)/float(Ny)*100)
            dt.append(j)
            # fig, axs = plt.subplots(1,1,figsize=(9, 6))
            # axs.imshow(data2,cmap='gray')
            # plt.show()
      return dt,percent
      fig, axs = plt.subplots(1,1,figsize=(9, 6))
      plt.plot(dt,percent)
      plt.xlabel( "Distance",fontdict={'size': 20} )
      plt.ylabel("Signal",fontdict={'size': 20} )
      plt.tick_params(labelsize=15)
      plt.show()


def two_circle():
      percent = []
      dt = []
      for i in range(60):
            print(i)
            amp = 1
            Nx = 500*amp
            Ny = 500*amp
            data2 = np.zeros((Ny,Nx))
            ## Ring1
            rr = [10*amp,20*amp]
            data1 = np.zeros((Ny,Nx))
            center = [250*amp,250*amp]
            data2 = data2 + fill_ring(center,rr,data1)
            ## Ring2
            cx2 = 250
            c2 = 250
            p = 20

            data1 = np.zeros((Ny,Nx))
            center = [cx2*amp,(c2+i)*amp]
            data2 = data2 + fill_ring2(center,rr,data1)
            # ## Ring3

            data1 = np.zeros((Ny,Nx))
            center = [cx2*amp,(c2+p+i)*amp]
            data2 = data2 + fill_ring2(center,rr,data1)

            data1 = np.zeros((Ny,Nx))
            center = [cx2*amp,(c2+2*p+i)*amp]
            data2 = data2 + fill_ring2(center,rr,data1)

            data1 = np.zeros((Ny,Nx))
            center = [cx2*amp,(c2+3*p+i)*amp]
            data2 = data2 + fill_ring2(center,rr,data1)

            data1 = np.zeros((Ny,Nx))
            center = [cx2*amp,(c2+4*p+i)*amp]
            data2 = data2 + fill_ring2(center,rr,data1)
            # data1 = np.zeros((Ny,Nx))
            # center = [500*amp,(c2+4*p+i)*amp]
            # data2 = data2 + fill_ring2(center,rr,data1)
            # ## Ring5

            data1 = np.zeros((Ny,Nx))
            center = [cx2*amp,(c2-p+i)*amp]
            data2 = data2 + fill_ring2(center,rr,data1)

            data1 = np.zeros((Ny,Nx))
            center = [cx2*amp,(c2-2*p+i)*amp]
            data2 = data2 + fill_ring2(center,rr,data1)

            data1 = np.zeros((Ny,Nx))
            center = [cx2*amp,(c2-3*p+i)*amp]
            data2 = data2 + fill_ring2(center,rr,data1)

            data1 = np.zeros((Ny,Nx))
            center = [cx2*amp,(c2-4*p+i)*amp]
            data2 = data2 + fill_ring2(center,rr,data1)

            # data1 = np.zeros((Ny,Nx))
            # center = [500*amp,(c2-4*p+i)*amp]
            # data2 = data2 + fill_ring2(center,rr,data1)

            # fig, axs = plt.subplots(1,1,figsize=(9, 6))
            # axs.imshow(data2,cmap='gray')
            # plt.show()
            mask = (data2 > 10)
            # 统计等于2的元素的数量
            count = np.count_nonzero(mask)
            percent.append(count/float(Nx)/float(Ny)*100)
            dt.append(i)
      return dt,percent
      fig, axs = plt.subplots(1,1,figsize=(9, 6))
      plt.plot(dt,percent)
      plt.xlabel( "Distance",fontdict={'size': 20} )
      plt.ylabel("Signal",fontdict={'size': 20} )
      plt.tick_params(labelsize=15)
      plt.show()


      # outpath = "D:/xianjinyuan/reconstruction/tyh/DPC_rec/generate_tan/python/"
      # with io.open(outpath + model + "_image.raw",'wb') as f:
      #       data2.astype(np.float32).tofile(f)  

def fill_ring(center,rr,data):
      Ny,Nx = data.shape
      rin = rr[0]
      rout = rr[1]
      for j in range(Ny):
            for i in range(Nx):
                  if rout*rout>=(center[1]-i)**2 + (center[0]-j)**2 and rin*rin<=(center[1]-i)**2 + (center[0]-j)**2:
                        data[j,i] = 10
      return data

def fill_ring2(center,rr,data):
      Ny,Nx = data.shape
      rin = rr[0]
      rout = rr[1]
      for j in range(Ny):
            for i in range(Nx):
                  if rout*rout>=(center[1]-i)**2 + (center[0]-j)**2 and rin*rin<=(center[1]-i)**2 + (center[0]-j)**2:
                        data[j,i] += 1
      return data

def fill_rectangle(center,rec_size,data):
      Ny,Nx = data.shape
      r = rec_size
      for j in range(Ny):
            for i in range(Nx):
                  if j - center[0] >= 0 and j - center[0] <= r[0]:
                        if i - center[1] >= 0 and i - center[1] <= r[1]: 
                              data[j,i] = 1           
      return data

def fill_rectangle2(center,rec_size,data):
      Ny,Nx = data.shape
      r = rec_size
      for j in range(Ny):
            for i in range(Nx):
                  if j - center[0] >= 0 and j - center[0] <= r[0]:
                        if i - center[1] >= 0 and i - center[1] <= r[1]: 
                              data[j,i] += 1           
      return data

if __name__ == '__main__':
      main()