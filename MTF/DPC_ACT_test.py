import numpy as np
from scipy.ndimage import gaussian_filter
import scipy.signal
import matplotlib.pyplot as plt 
import sys
import io
import os
# figure 5

def main():
    paper_result()
    #split_CT_test()
    
def paper_result():
    N=960000
    Pixel=100
    size = [-2.4,2.4]    #Units:mm
    Pixel_size = (size[1]-size[0])/Pixel*1000
    sigma = 1.55*48/Pixel_size 
    R=0.15    #mm
    print('sigma=',sigma,'\nPixel size=',Pixel_size,'um')
    #pro_com_act()
    outfile = './data/deltas_s_calculate_20240531/'
    if not os.path.exists(outfile):
        os.mkdir(outfile)
    sd=[0.0,0.01,2,8,32]
    # sd=[8]
    sdpc=[]
    sact=[]
    for i in range(len(sd)):
        splitdis = sd[i]     #um
        print('splitdis=',splitdis)
        dpc_raw = pro_com_dpc(size,N,outfile,splitdis,sigma,Pixel,R)
        act_raw = pro_com_act(size,N,outfile,splitdis,sigma,Pixel,R)
        draw_raw_dpc_act(dpc_raw,act_raw,size,N,outfile,splitdis,sigma,Pixel)
        # plt.show()
def split_CT_test():
    N=2000
    Pixel=400
    size = [-2.4,2.4]    #Units:mm
    gx = np.linspace(size[0],size[1],N)
    splitdis = 100.0
    deltax=splitdis/1000.0
    sigma = 1.55
    f1 = np.ones(N)
    f2 = np.ones(N)
    f3 = np.ones(N)
    beta = 9.38901e-011  
    k = 2*np.pi/(1.24/25.)/1e-3
    R=1.0
    for j in range(N):
        f1[j]=func_circle_phase(gx[j],R,0.0)*beta*k*1e3
        f2[j]=func_circle_phase(gx[j],R,-deltax)*beta*k*1e3
        f3[j]=func_circle_phase(gx[j],R,deltax)*beta*k*1e3
    projection = f2+ f3
    fig1 = plt.figure(figsize=(9,6))
    plt.plot(projection)
    fig1 = plt.figure(figsize=(9,6))

    projection = np.fft.fftshift(np.fft.fft(np.fft.ifftshift(projection)))
    for i in range(N):
        if projection[i] > 3:
            projection[i] = 3
    plt.plot(projection)

    fig1 = plt.figure(figsize=(9,6))
    projection = np.fft.fftshift(np.fft.ifft(np.fft.ifftshift(projection*0.1)))
    plt.plot(projection)
    plt.show()


def draw_circle_with_color(n,R,size):
    gridg = np.zeros([n,n])
    gx = np.linspace(size[0],size[1],n)
    gy = np.linspace(0,5,n)
    x_array=[]
    y_array=[]
    fig1 = plt.figure(figsize=(6,6))
    data = []
    for i in range(n):
        for j in range(n):
            re=func_circle_phase2(gx[i],gy[j],R,0.0)
            if re>0:
                gridg[i,j] = re
    plt.imshow(gridg,cmap='gray')
    fig1 = plt.figure(figsize=(6,6))
    plt.plot(gridg[int(n/2)])
    plt.show()
    sys.exit()
def func_circle_phase2(x,y,R,deltax):
    re = R**2-(x-deltax)**2-(y-deltax)**2
    if re>=0:
        return  np.sqrt(re)
    else:
        return 0

def draw_raw_dpc_act(dpc_raw,act_raw,size,N,outfile,splitdis,sigmad,Pixel):
    gx = np.linspace(size[0],size[1],N)
    gx = rpn(gx,Pixel,N)
    fig1 = plt.figure(figsize=(9,6))
    plt.plot(gx,dpc_raw/np.max(dpc_raw),'red',label='DPC_Raw')
    plt.plot(gx,act_raw/np.max(act_raw),'blue',label='ACT_Raw')
    plt.xlabel( "Direction x [mm]",fontdict={'size': 20} )
    plt.ylabel("Normalization",fontdict={'size': 20} )
    plt.tick_params(labelsize=18)
    plt.grid()
    # plt.plot(gx,p2/np.max(p2),'b',label='$\Delta$x=0.001')
    # plt.plot(gx,p3/np.max(p3),'black',label='$\Delta$x=0.01')
    #plt.legend(loc='best',fontsize=15,frameon=False)
    act_rawn=gauss_filter_reshape(act_raw,Pixel,sigmad*0.8)   #ref 0.8
    dpc_rawn=gauss_filter_reshape(dpc_raw,Pixel,sigmad*0.8)
    act_rawg=gauss_filter_reshape(act_raw,Pixel,sigmad*0.95)  #ref 0.95
    dpc_rawg=gauss_filter_reshape(dpc_raw,Pixel,sigmad*0.95)
    sigma=1.55            
    outfile_name_a = outfile + 'period_8_sep_2.24_sigma_'+str(0.0)+'_absor_pixel_size_'+str(4800/Pixel)+'_m1'+'_sd_'+str(splitdis)+'.raw'
    with io.open(outfile_name_a,'wb') as f:
        for i in range(360):
            act_rawn.astype(np.float32).tofile(f)
    outfile_name_a = outfile + 'period_8_sep_2.24_sigma_'+str(sigma)+'_absor_pixel_size_'+str(4800/Pixel)+'_m1'+'_sd_'+str(splitdis)+'.raw'
    with io.open(outfile_name_a,'wb') as f:
        for i in range(360):
            act_rawg.astype(np.float32).tofile(f)
    if splitdis > 0:
        outfile_name_a = outfile + 'period_8_sep_2.24_sigma_'+str(0.0)+'_phi_pixel_size_'+str(4800/Pixel)+'_m1'+'_sd_'+str(splitdis)+'.raw'
        with io.open(outfile_name_a,'wb') as f:
            for i in range(360):
                dpc_rawn.astype(np.float32).tofile(f)
        outfile_name_a = outfile + 'period_8_sep_2.24_sigma_'+str(sigma)+'_phi_pixel_size_'+str(4800/Pixel)+'_m1'+'_sd_'+str(splitdis)+'.raw'
        with io.open(outfile_name_a,'wb') as f:
            for i in range(360):
                dpc_rawg.astype(np.float32).tofile(f)                     




            
            
def pro_com_dpc(size,N,outfile,splitdis,sigma,Pixel,R):
    # sim twin distance effect on projection for phase Units:mm
    gx = np.linspace(size[0],size[1],N)
    deltax=splitdis/1000
    p1,f1,p1res,df_1=phi1phi2_phase(gx,N,deltax,Pixel,R)
    # p1=gauss_filter_reshape(p1,Pixel,sigma)
    # df_1=gauss_filter_reshape(df_1,Pixel,sigma)
    # p1res=gauss_filter_reshape(p1res,Pixel,sigma)
    # f1,p2=phi1phi2_phase(n,deltax=0.001)
    # f1,p3=phi1phi2_phase(n,deltax=0.01)
    # fig1 = plt.figure(figsize=(9,6))
    # plt.plot(gx,p1,'red',label='$\Delta$x=2.2 $\mu$m')
    # plt.title('DPC signal')
    # plt.xlabel( "Direction x [mm]",fontdict={'size': 20} )
    # plt.ylabel("DPC",fontdict={'size': 20} )
    # plt.tick_params(labelsize=18)
    # # plt.plot(gx,p2/np.max(p2),'b',label='$\Delta$x=0.001')
    # # plt.plot(gx,p3/np.max(p3),'black',label='$\Delta$x=0.01')
    # #plt.legend(loc='best',fontsize=10,frameon=False)

    # outfile_name_d = outfile + 'period_8_sep_2.24_sigma_0.0_phi_pixel_size_'+str(4800/Pixel)+'_m2'+'_sd_'+str(splitdis)+'_restore.raw'
    # with io.open(outfile_name_d,'wb') as f:
    #     for i in range(360):
    #        p1res.astype(np.float32).tofile(f)    

    # outfile_name_d = outfile + 'period_8_sep_2.24_sigma_0.0_phi_pixel_size_'+str(4800/Pixel)+'_m2'+'_sd_'+str(splitdis)+'.raw'
    # with io.open(outfile_name_d,'wb') as f:
    #     for i in range(360):
    #        p1.astype(np.float32).tofile(f)    

    # outfile_name_d = outfile + 'period_8_sep_2.24_sigma_0.0_absor_pixel_size_'+str(4800/Pixel)+'_m2'+'_df_'+str(splitdis)+'.raw'
    # with io.open(outfile_name_d,'wb') as f:
    #     for i in range(360):
    #        df_1.astype(np.float32).tofile(f)   
    return p1

def phi1phi2_phase(gx,n,deltax,Pixel,R):
    # Function1 e^(-A1), Function2 e^(-A2) mm
    # Material is graphite, X-ray energy is 25keV
    delta = 7.50045e-007
    k = 2*np.pi/(1.24/25.)/1e-3
    sn = (R*2.0)/(gx[-1] - gx[0])*n
    f1 = func_circle_2(sn,gx,n,R)*delta*k*1e3
    N_s = int(deltax/(gx[1]-gx[0]))
    f2 = np.roll(f1,-N_s,axis=0)
    f3 = np.roll(f1,N_s,axis=0)
    # DF_plot(f1,f2,f3,n,gx)
    # fig1 = plt.figure(figsize=(9,6))
    # gridg = np.zeros([n,n])
    # g2 = np.zeros([n,n])
    # g3 = np.zeros([n,n])
    # for i in range(n):
    #     for j in range(n):
    #         g2[j][i] = -f2[i]
    #         g3[j][i] = f3[i]
    #         gridg[j][i] = f3[i] - f2[i]
    # extent = [0,4.8,0,4.8]
    # plt.imshow(gridg,cmap='gray',extent =extent)
    # # plt.xlabel( "x [mm]",fontdict={'size': 20} )
    # # plt.ylabel( "y [mm]",fontdict={'size': 20} )
    # plt.xticks([])
    # plt.yticks([])
    # plt.ylim(ymax=2.4)
    # plt.xlim(xmax=4.5,xmin=0.3)
    # plt.tick_params(labelsize=18)
    # plt.axhline(1.2,color='#FCFC97',linestyle="-",lw=6)
    # plt.savefig('D:/xianjinyuan/工作内容/Jiecheng/NanoCT/Simulation/NanoCT_Sim/SimCode/withoutZP/p1/DPC_pro.svg',bbox_inches='tight')

    # fig1 = plt.figure(figsize=(9,6))
    # lines = g2[1000,:]
    # lines = lines.tolist()
    # #plt.axvline(lines.index(min(lines))/n*4.8,color='#9DC3E6',linestyle="-",lw=6)
    # plt.imshow(g2,cmap='gray',extent =extent)
    # # plt.xlabel( "x [mm]",fontdict={'size': 20} )
    # # plt.ylabel( "y [mm]",fontdict={'size': 20} )
    # plt.xticks([])
    # plt.yticks([])
    # plt.ylim(ymax=2.4)
    # plt.xlim(xmax=3.8,xmin=1)
    # plt.axis('off')
    # plt.savefig('D:/xianjinyuan/工作内容/Jiecheng/NanoCT/Simulation/NanoCT_Sim/SimCode/withoutZP/p1/DPC_pro_L.svg',bbox_inches='tight')
    # # plt.plot(g2[:,1000])

    # fig1 = plt.figure(figsize=(9,6))
    # lines = g3[1000,:]
    # lines = lines.tolist()
    # #plt.axvline(lines.index(max(lines))/n*4.8,color='#9DC3E6',linestyle="-",lw=6)
    # plt.imshow(g3,cmap='gray',extent =extent)
    # # plt.xlabel( "x [mm]",fontdict={'size': 20} )
    # # plt.ylabel( "y [mm]",fontdict={'size': 20} )
    # plt.xticks([])
    # plt.yticks([])
    # plt.ylim(ymax=2.4)
    # plt.xlim(xmax=3.8,xmin=1)
    # plt.axis('off')
    # plt.savefig('D:/xianjinyuan/工作内容/Jiecheng/NanoCT/Simulation/NanoCT_Sim/SimCode/withoutZP/p1/DPC_pro_R.svg',bbox_inches='tight')
    # # plt.show()

    fig1 = plt.figure(figsize=(9,6))
    pro_phase = rpn(f3-f2,Pixel,n)
    pro_df_norm = (2*f1-f3-f2)**2
    pro_df_norm = pro_df_norm/np.max(pro_df_norm+1e-6)
    pro_df = rpn(pro_df_norm,Pixel,n)

    f3res = split_restore_1D(f3,n,deltax,gx)
    f2res = split_restore_1D(f2,n,deltax,gx)
    pro_phase_res = rpn(f3res-f2res,Pixel,n)
    f1 = rpn(f1,Pixel,n)
    f2 = rpn(f2,Pixel,n)
    f3 = rpn(f3,Pixel,n)
    gx = rpn(gx,Pixel,n)
    # plt.plot(gx,-f2/(max(f2)),'red',linestyle="--",label='$\Phi_1$',lw=1)
    # plt.plot(gx,f3/(max(f3)),'blue',linestyle="--",label='$\Phi_2$',lw=1)
    # plt.plot(gx,pro_phase/(max(pro_phase)),'black',label='L $\Phi_2$ -  $\Phi_1$',lw=2)
    # plt.plot(gx,pro_phase2/(max(pro_phase2)),'c',label='S $\Phi_2$ -  $\Phi_1$',lw=2)
    # plt.plot(gx,f1/(max(f1)),'m',label='Raw Signal',lw=2)
    # f22 = f2.tolist()
    # f33 = f3.tolist()
    # plt.axvline(gx[f33.index(max(f33))],color='b',linestyle="--",lw=1)
    # plt.axvline(gx[f22.index(max(f22))],color='r',linestyle="--",lw=1)
    # plt.xlabel( "Direction",fontdict={'size': 20} )
    # plt.ylabel("DPC Projection",fontdict={'size': 20} )
    # plt.savefig('DPC process.svg',bbox_inches='tight')
    #plt.legend(loc='best',fontsize=15,frameon=False)
    fig1 = plt.figure(figsize=(9,6))
    plt.plot(gx+2.4,f1/(max(f1)),'#44AFC6',label='w/o diffraction',lw=3)
    plt.plot(gx+2.4,pro_phase/(max(pro_phase)),'#FFC000',label='$\Phi_2$ -  $\Phi_1$',lw=3)
    plt.xlabel( "x [mm]",fontdict={'size': 20} )
    plt.ylabel("Norm. Projection",fontdict={'size': 20} )
    plt.legend(loc='best',fontsize=28,frameon=False)
    plt.xlim(xmax=4.5,xmin=0.3)
    plt.ylim(ymax=2.0)
    plt.tick_params(labelsize=18)
    plt.savefig('D:/xianjinyuan/工作内容/Jiecheng/NanoCT/Simulation/NanoCT_Sim/SimCode/withoutZP/p1/DPC_signal.svg',bbox_inches='tight')
    
    
    f1g= gaussian_filter(f1,sigma=1.55)
    pro_phaseg= gaussian_filter(pro_phase,sigma=1.55)
    print("len(f1g)",len(f1g))
    fig1 = plt.figure(figsize=(9,6))
    plt.plot(gx+2.4,f1g/(max(f1g)),'#44AFC6',label='w/o diffraction',lw=3)
    plt.plot(gx+2.4,pro_phaseg/(max(pro_phaseg)),'#FFC000',label='$\Phi_2$ -  $\Phi_1$',lw=3)
    plt.xlabel( "x [mm]",fontdict={'size': 20} )
    plt.ylabel("Norm. Projection",fontdict={'size': 20} )
    plt.legend(loc='best',fontsize=28,frameon=False)
    plt.xlim(xmax=4.5,xmin=0.3)
    plt.ylim(ymax=2.0)
    plt.tick_params(labelsize=18)
    plt.savefig('D:/xianjinyuan/工作内容/Jiecheng/NanoCT/Simulation/NanoCT_Sim/SimCode/withoutZP/p1/DPC_signal_sigma_1.55.svg',bbox_inches='tight')
    
    fig1 = plt.figure(figsize=(9,8))
    plt.plot(gx,pro_df/(max(pro_df)),'red',linestyle="--",label='$DF_1$',lw=1)
    plt.savefig('D:/xianjinyuan/工作内容/Jiecheng/NanoCT/Simulation/NanoCT_Sim/SimCode/withoutZP/p1/DF_signal.svg',bbox_inches='tight')
    pro_df=pro_df/max(pro_df)
    return pro_phase, f1,pro_phase_res,pro_df


def DF_plot(f1,f2,f3,n,gx):
    extent = [0,4.8,0,4.8]
    g1 = np.zeros([n,n])
    g2 = np.zeros([n,n])
    g3 = np.zeros([n,n])
    for i in range(n):
        for j in range(n):
            g1[j][i] = f1[i]
            g2[j][i] = f2[i]
            g3[j][i] = f3[i]
    fig1 = plt.figure(figsize=(9,6))
    # lines = g2[1000,:]
    # lines = lines.tolist()
    #plt.axvline(lines.index(min(lines))/n*4.8,color='#9DC3E6',linestyle="-",lw=6)
    plt.imshow(g2,cmap='gray',extent =extent)
    # plt.xlabel( "x [mm]",fontdict={'size': 20} )
    # plt.ylabel( "y [mm]",fontdict={'size': 20} )
    plt.xticks([])
    plt.yticks([])
    plt.ylim(ymax=2.4)
    plt.xlim(xmax=3.8,xmin=1)
    plt.axis('off')
    plt.savefig('D:/xianjinyuan/工作内容/Jiecheng/NanoCT/Simulation/NanoCT_Sim/SimCode/withoutZP/p1/DF_pro_L.svg',bbox_inches='tight')
    # plt.plot(g2[:,1000])

    fig1 = plt.figure(figsize=(9,6))
    lines = g3[1000,:]
    lines = lines.tolist()
    #plt.axvline(lines.index(max(lines))/n*4.8,color='#9DC3E6',linestyle="-",lw=6)
    plt.imshow(g3,cmap='gray',extent =extent)
    # plt.xlabel( "x [mm]",fontdict={'size': 20} )
    # plt.ylabel( "y [mm]",fontdict={'size': 20} )
    plt.xticks([])
    plt.yticks([])
    plt.ylim(ymax=2.4)
    plt.xlim(xmax=3.8,xmin=1)
    plt.axis('off')
    plt.savefig('D:/xianjinyuan/工作内容/Jiecheng/NanoCT/Simulation/NanoCT_Sim/SimCode/withoutZP/p1/DF_pro_R.svg',bbox_inches='tight')

    fig1 = plt.figure(figsize=(9,6))
    lines = g3[1000,:]
    lines = lines.tolist()
    #plt.axvline(lines.index(max(lines))/n*4.8,color='#9DC3E6',linestyle="-",lw=6)
    plt.imshow(g1,cmap='gray',extent =extent)
    # plt.xlabel( "x [mm]",fontdict={'size': 20} )
    # plt.ylabel( "y [mm]",fontdict={'size': 20} )
    plt.xticks([])
    plt.yticks([])
    plt.ylim(ymax=2.4)
    plt.xlim(xmax=3.8,xmin=1)
    plt.axis('off')
    plt.savefig('D:/xianjinyuan/工作内容/Jiecheng/NanoCT/Simulation/NanoCT_Sim/SimCode/withoutZP/p1/DF_pro_m.svg',bbox_inches='tight')

    pro_df_norm = (2*g1-g3-g2)**2
    pro_df_norm_1D = (2*f1-f3-f2)**2
    #pro_df_norm = pro_df_norm/np.max(pro_df_norm)
    #pro_df = rpn(pro_df_norm,Pixel,n)

    fig1 = plt.figure(figsize=(9,6))
    lines = g3[1000,:]
    lines = lines.tolist()
    #plt.axvline(lines.index(max(lines))/n*4.8,color='#9DC3E6',linestyle="-",lw=6)
    plt.imshow(pro_df_norm,cmap='gray',extent =extent)
    # plt.xlabel( "x [mm]",fontdict={'size': 20} )
    # plt.ylabel( "y [mm]",fontdict={'size': 20} )
    plt.xticks([])
    plt.yticks([])
    plt.ylim(ymax=2.4)
    plt.xlim(xmax=3.8,xmin=1)
    plt.axis('off')
    plt.savefig('D:/xianjinyuan/工作内容/Jiecheng/NanoCT/Simulation/NanoCT_Sim/SimCode/withoutZP/p1/DF_pro_total.svg',bbox_inches='tight')

    fig1 = plt.figure(figsize=(9,6))
    plt.plot(gx+2.4,f1/(max(f1)),'#44AFC6',label='w/o diffraction',lw=3)
    plt.plot(gx+2.4,pro_df_norm_1D/(max(pro_df_norm_1D)),'#FFC000',label='$\Phi_2$ -  $\Phi_1$',lw=3)
    plt.xlabel( "x [mm]",fontdict={'size': 20} )
    plt.ylabel("Norm. Projection",fontdict={'size': 20} )
    #plt.legend(loc='best',fontsize=33,frameon=False)
    plt.xlim(xmax=4.5,xmin=0.3)
    plt.ylim(ymax=2.2)
    plt.tick_params(labelsize=18)
    plt.savefig('D:/xianjinyuan/工作内容/Jiecheng/NanoCT/Simulation/NanoCT_Sim/SimCode/withoutZP/p1/DF_signal.svg',bbox_inches='tight')

def split_restore_1D(data,n,deltax,gx):
    N_s = int(deltax/(gx[1]-gx[0]))
    print("Nshift=",N_s)
    phase = data
    prior = np.zeros_like(phase)
    for j in range(N_s):
        prior[j] = 0

    for j in range(N_s, 2*N_s):
        prior[j] = -phase[j-N_s]

    for j in range(2*N_s, n):
        prior[j] = prior[j-2*N_s] - phase[j-N_s]
    return prior

def split_restore_1D_absor(data,n,deltax,gx):
    N_s = int(deltax/(gx[1]-gx[0]))
    print("Nshift=",N_s)
    phase = data
    prior = np.zeros_like(phase)
    error=0
    for j in range(N_s):
        prior[j] = 0

    for j in range(N_s, 2*N_s):
        prior[j] = np.log(2.0*np.exp(-2.0*phase[j-N_s])-1+error)/(-2.0)

    for j in range(2*N_s, n):
        prior[j] = np.log(np.abs(-np.exp(-2.0*prior[j-2*N_s]) +2.0*np.exp(-2.0*phase[j-N_s]))+error)/(-2.0)
    return prior

def rpn(data,Pixel,n):
    data = (data.reshape(Pixel,int(n/Pixel))).mean(1)
    return data

def pro_com_act(size,N,outfile,splitdis,sigma,Pixel,R):
    # sim twin distance effect on projection for absorption
    gx = np.linspace(size[0],size[1],N)
    deltax=splitdis/1000.0
    p1,f1,p1res=A1A2_absorption(gx,N,deltax,Pixel,R)
    # p1=gauss_filter_reshape(p1,Pixel,sigma)
    # p1res=gauss_filter_reshape(p1res,Pixel,sigma)
    #p2=A1A2_absorption(deltax=0.2)
    # fig1 = plt.figure(figsize=(9,6))
    # plt.plot(gx,p1,'red',label='$\Delta$x=2.2 $\mu$m')
    # plt.plot(gx,f1,'blue',label='$\Delta$x=2.2 $\mu$m')
    # plt.title('Absorption signal')
    # plt.xlabel( "Direction x [mm]",fontdict={'size': 20} )
    # plt.ylabel("Absorption projection process",fontdict={'size': 20} )
    # plt.tick_params(labelsize=18)
    # #plt.legend(loc='best',fontsize=10,frameon=False)

    # outfile_name_d = outfile + 'period_8_sep_2.24_sigma_0.0_absor_pixel_size_'+str(4800/Pixel)+'_m3'+'_sd_'+str(splitdis)+'_restore.raw'
    
    # with io.open(outfile_name_d,'wb') as f:
    #     for i in range(360):
    #        p1res.astype(np.float32).tofile(f)    

    # outfile_name_d = outfile + 'period_8_sep_2.24_sigma_0.0_absor_pixel_size_'+str(4800/Pixel)+'_m2_sd_0.0.raw'
    # f1g=gaussian_filter(f1,sigma=1.55)
    # with io.open(outfile_name_d,'wb') as f:
    #     for i in range(360):
    #        f1.astype(np.float32).tofile(f)    

    # outfile_name_d = outfile + 'period_8_sep_2.24_sigma_1.55_absor_pixel_size_'+str(4800/Pixel)+'_m2_sd_0.0.raw'
    # with io.open(outfile_name_d,'wb') as f:
    #     for i in range(360):
    #        f1g.astype(np.float32).tofile(f)    
           
    return p1

def A1A2_absorption(gx,n,deltax,Pixel,R):
    # Function1 e^(-A1), Function2 e^(-A2)
    # Material is graphite, X-ray energy is 25keV
    beta = 9.38901e-011
    k = 2*np.pi/(1.24/25.)/1e-3
    sn = (R*2.0)/(gx[-1] - gx[0])*n
    f1 = func_circle_2(sn,gx,n,R)*beta*k*1e3
    N_s = int(deltax/(gx[1]-gx[0]))
    f2 = np.roll(f1,-N_s,axis=0)
    f3 = np.roll(f1,N_s,axis=0)
    projection = -np.log((np.exp(-2*f2)+np.exp(-2*f3))/2.)/2.0
    projection_res = split_restore_1D_absor(projection,n,deltax,gx)
    # gridg = np.zeros([n,n])
    # g2 = np.zeros([n,n])
    # g3 = np.zeros([n,n])
    # for i in range(n):
    #     for j in range(n):
    #         gridg[j][i] = projection[i]
    #         g2[j][i] = 2*f2[i]
    #         g3[j][i] = 2*f3[i]
    # extent = [0,4.8,0,2.4]
    # plt.imshow(gridg,cmap='gray',extent = extent)
    # # plt.xlabel( "x [mm]",fontdict={'size': 20} )
    # # plt.ylabel( "y [mm]",fontdict={'size': 20} )
    # plt.xticks([])
    # plt.yticks([])
    # plt.ylim(ymax=2.4)
    # plt.xlim(xmax=4.5,xmin=0.3)
    # plt.tick_params(labelsize=18)
    # plt.axhline(1.2,color='#FCFC97',linestyle="-",lw=6)
    # plt.savefig('D:/xianjinyuan/工作内容/Jiecheng/NanoCT/Simulation/NanoCT_Sim/SimCode/withoutZP/p1/ACT_pro.svg',bbox_inches='tight')
    # lines = g2[0,:]
    # fig1 = plt.figure(figsize=(9,6))
    # lines = lines.tolist()
    # #plt.axvline(lines.index(max(lines))/n*4.8,color='#9DC3E6',linestyle="-",lw=6)
    # plt.imshow(g2,cmap='gray',extent =extent)
    # # plt.xlabel( "x [mm]",fontdict={'size': 20} )
    # # plt.ylabel( "y [mm]",fontdict={'size': 20} )
    # plt.xticks([])
    # plt.yticks([])
    # plt.axis('off')
    # plt.ylim(ymax=2.4)
    # plt.xlim(xmax=3.8,xmin=1)
    # plt.savefig('D:/xianjinyuan/工作内容/Jiecheng/NanoCT/Simulation/NanoCT_Sim/SimCode/withoutZP/p1/ACT_pro_L.svg',bbox_inches='tight')
    # # plt.plot(g2[:,1000])

    # fig1 = plt.figure(figsize=(9,6))
    # lines = g3[0,:]
    # lines = lines.tolist()
    # #plt.axvline(lines.index(max(lines))/n*4.8,color='#9DC3E6',linestyle="-",lw=6)
    # plt.imshow(g3,cmap='gray',extent =extent)
    # # plt.xlabel( "x [mm]",fontdict={'size': 20} )
    # # plt.ylabel( "y [mm]",fontdict={'size': 20} )
    # plt.xticks([])
    # plt.yticks([])
    # plt.ylim(ymax=2.4)
    # plt.xlim(xmax=3.8,xmin=1)
    # plt.axis('off')
    # plt.savefig('D:/xianjinyuan/工作内容/Jiecheng/NanoCT/Simulation/NanoCT_Sim/SimCode/withoutZP/p1/ACT_pro_R.svg',bbox_inches='tight')



    # fig1 = plt.figure(figsize=(9,6))
    # gridg = np.zeros([n,n])
    # for i in range(n):
    #     # for j in range(100):
    #     gridg[i] = f1[i]
    # plt.imshow(gridg,cmap='gray')
    # plt.xticks([])
    # plt.yticks([])
    # plt.savefig('raw_pro.svg',bbox_inches='tight')
    #plt.show()
    fig1 = plt.figure(figsize=(9,6))
    projection = rpn(projection,Pixel,n)
    projection_res = rpn(projection_res,Pixel,n)
    gx = rpn(gx,Pixel,n)
    f1 = rpn(f1,Pixel,n)
    f2 = rpn(f2,Pixel,n)
    f3 = rpn(f3,Pixel,n)
    plt.plot(gx,2*f2,'red',label='$2A_1$',linestyle="--",lw=1)
    plt.plot(gx,2*f3,'blue',label='$2A_2$',linestyle="--",lw=1)
    plt.plot(gx,projection,'black',label='Projection',lw=2)
    plt.plot(gx,2*f1,'m',label='Raw Signal',linestyle="-",lw=2)
    plt.xlabel( "Direction",fontdict={'size': 20} )
    plt.ylabel("Absorption Projection",fontdict={'size': 20} )
    f22 = f2.tolist()
    f33 = f3.tolist()

    #plt.legend(loc='best',fontsize=15,frameon=False)

    fig1 = plt.figure(figsize=(9,6))
    plt.plot(gx+2.4,f1/np.max(f1),'#44AFC6',label='w/o diffraction',lw=3)
    plt.plot(gx+2.4,projection/np.max(projection),'#FFC000',label='-ln($\\frac{e^{-2A_1}+e^{-2A_2}}{2}$)',lw=3)
    plt.xlabel( "x [mm]",fontdict={'size': 20} )
    plt.ylabel("Norm. Projection",fontdict={'size': 20} )
    plt.xlim(xmax=4.5,xmin=0.3)
    plt.ylim(ymax=1.6)
    plt.tick_params(labelsize=18)
    plt.legend(loc='best',fontsize=28,frameon=False)
    # ax = plt.gca()
    # ax.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
    # ax.get_yaxis().get_offset_text().set(va='bottom', ha='left')
    # ax.yaxis.get_offset_text().set_fontsize(18)#设置1e6的大小与位置
    plt.savefig('D:/xianjinyuan/工作内容/Jiecheng/NanoCT/Simulation/NanoCT_Sim/SimCode/withoutZP/p1/ACT_signal.svg',bbox_inches='tight')

    f1g= gaussian_filter(f1,sigma=1.55)
    projectiong= gaussian_filter(projection,sigma=1.55)
    
    fig1 = plt.figure(figsize=(9,6))
    plt.plot(gx+2.4,f1g/np.max(f1g),'#44AFC6',label='w/o diffraction',lw=3)
    plt.plot(gx+2.4,projectiong/np.max(projectiong),'#FFC000',label='-ln($\\frac{e^{-2A_1}+e^{-2A_2}}{2}$)',lw=3)
    plt.xlabel( "x [mm]",fontdict={'size': 20} )
    plt.ylabel("Norm. Projection",fontdict={'size': 20} )
    plt.xlim(xmax=4.5,xmin=0.3)
    plt.ylim(ymax=1.6)
    plt.tick_params(labelsize=18)
    plt.legend(loc='best',fontsize=28,frameon=False)
    # ax = plt.gca()
    # ax.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
    # ax.get_yaxis().get_offset_text().set(va='bottom', ha='left')
    # ax.yaxis.get_offset_text().set_fontsize(18)#设置1e6的大小与位置
    plt.savefig('D:/xianjinyuan/工作内容/Jiecheng/NanoCT/Simulation/NanoCT_Sim/SimCode/withoutZP/p1/ACT_signal_sigma_1.55.svg',bbox_inches='tight')
    
    return projection,2*f1,projection_res
    #plt.show()
def func_gauss(x, x0, sigma):
    return np.exp(-(x-x0)**2/(2*sigma**2))

def func_circle_phase(x, R,deltax):
    re = R**2-(x-deltax)**2
    if re>=0:
        return  np.sqrt(re)*2.0
    else:
        return 0

def func_circle_2(sn,gx,n,R):
    f11 = np.zeros(n)
    dnv = (gx[-1] - gx[0])/n
    for i in range(int(sn)):
        f11[int((n-sn)//2+i)] = np.sqrt(R**2-(R-i*dnv)**2)*2.0
    return f11    
    
def dark_field():
    # sim twin distance effect on projection for absorption
    p1= df1df2_phase(deltax=0.0)
    p2= df1df2_phase(deltax=0.2)

    n = 1000000
    gx = np.linspace(-1.5,1.5,n)
    fig1 = plt.figure(figsize=(9,6))
    plt.plot(gx,p1,'red',label='$\Delta$x=0')
    plt.plot(gx,p2,'b',label='$\Delta$x=0.2')
    #plt.legend(loc='best',fontsize=10,frameon=False)
    plt.show()

def df1df2_phase(deltax):
    # Function1 e^(-A1), Function2 e^(-A2)
    n = 1000000
    gx = np.linspace(-1.5,1.5,n)
    f2 = np.ones(n)
    f3=np.ones(n)
    sigma = 0.2
    for j in range(n):
        f2[j]=func_gauss(gx[j],-deltax,sigma)
        f3[j]=func_gauss(gx[j],deltax,sigma)
    fig1 = plt.figure(figsize=(9,6))
    plt.plot(gx,f2,'red',label='A1')
    plt.plot(gx,f3,'b',label='A2')
    projection = -np.log((np.exp(-f2 - f3)))
    plt.plot(gx,projection,'black',label='Projection')
    return projection

def gauss_filter_reshape(data,pixel_number,gsigma):
    ''' Simulate Ch of detector'''
#     print(len(data))
    # data = data.reshape(pixel_number,int(len(data)/pixel_number)).mean(1)
    data= gaussian_filter(data,sigma=gsigma)
    return data


if __name__ == '__main__':
    main()