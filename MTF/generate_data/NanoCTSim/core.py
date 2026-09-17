import numpy as np
from material import mat_delta_beta
from material import read_para
import scipy
import matplotlib.pyplot as plt 
import propagator
import sympy
#----------------------------------------
# Several useful function defined here
#----------------------------------------

def AbsRing(total_count, pos, outlength, ilength, size, fs):
    absring = np.ones([int(total_count),int(total_count)])
    for i in range(int(size*fs)):
        for j in range(int(size*fs)):
            if (outlength*fs/2.-i)**2 + (outlength*fs/2.-j)**2 < (outlength*fs/2.)**2. and (outlength*fs/2.-i)**2 + (outlength*fs/2.-j)**2 > (ilength*fs/2.)**2.:
                absring[int(total_count/2 + i + pos*fs - outlength/2.*fs)][int(total_count/2 + j + pos*fs - outlength/2.*fs)] = 0.
    return absring

def Fourier_grating(period, step, fs, total_count):
    gridg = np.zeros([int(total_count),int(total_count)],dtype=complex)
    for i in range(int(total_count)):
        for j in range(int(total_count)):
            gridg[i][j] = 1./fs * (j-total_count/2.)  + step
    # grating = np.sqrt(abs(1./2. + (-1j/np.pi)* np.exp(2*1j*np.pi*(gridg) /period)+(1j/np.pi)* np.exp(2*1j*np.pi*(-1)*(gridg) /period))**2.)
    grating = 1./2. + (-1j/np.pi)* np.exp(2*1j*np.pi*(gridg) /period)+(1j/np.pi)* np.exp(2*1j*np.pi*(-1)*(gridg) /period)
    # grating = 1./4. + 20./9/np.pi/np.pi - 2*np.cos(4*np.pi*gridg/period)/3/np.pi/np.pi  \
    # - 4.*np.cos(8*np.pi*gridg/period)/3/np.pi/np.pi - 2*np.cos(12.*np.pi*gridg/period)/9./np.pi/np.pi \
    # + 2.*np.sin(2.*np.pi*gridg/period)/np.pi + 2.*np.sin(6.*np.pi*gridg/period)/np.pi
    return grating

def Fourier_grating1(period, step, fs, total_count):
    gridg = np.zeros([int(total_count),int(total_count)],dtype=complex)
    for i in range(int(total_count)):
        for j in range(int(total_count)):
            gridg[i][j] = 1./fs * (i-total_count/2.)+1./fs * (j-total_count/2.)+ step
    grating = 1./2. + (-1j/np.pi)* np.exp(2*1j*np.pi*(gridg) /period)+(1j/np.pi)* np.exp(2*1j*np.pi*(-1)*(gridg) /period)
    return grating

def Fourier_grating2(period, step, fs, total_count):
    gridg = np.zeros([int(total_count),int(total_count)],dtype=complex)
    for i in range(int(total_count)):
        for j in range(int(total_count)):
            gridg[i][j] = 1./fs * (i-total_count/2.)+ step
    grating = 1./2. + (-1j/np.pi)* np.exp(2*1j*np.pi*(gridg) /period)+(1j/np.pi)* np.exp(2*1j*np.pi*(-1)*(gridg) /period)
    return grating

def GaussianAperture(total_count, diameter, width, area_length, x_shift, y_shift, fs):
    gaussaperture = np.ones([int(total_count),int(total_count)],dtype=complex)
    for i in range(int(diameter*fs)):
        for j in range(int(diameter*fs)):
            if (diameter*fs/2.-i)**2 + (diameter*fs/2.-j)**2 < (diameter*fs/2.)**2.:
                gaussaperture[int(area_length*fs/2.)+int(x_shift*fs)+i-int(diameter*fs/2.)][int(area_length*fs/2.)+int(y_shift*fs)+j-int(diameter*fs/2.)] = \
                1 - np.exp((-1)*((diameter/2.-i/fs)**2.+(diameter/2.-j/fs)**2.)/2/width/width)
                #-0.9*np.sqrt(0.01*((olength/2.)**2.-(olength/2.-i/fs)**2.-(olength/2.-j/fs)**2.)) + 0.05*1j*2*np.sqrt(0.01*((olength/2.)**2.-(olength/2.-i/fs)**2.-(olength/2.-j/fs)**2.))
    return gaussaperture

def Lens2d(f, wave_length, grids):
    lens = np.exp((-1j) * np.pi * grids / f / wave_length)
    return lens

def Objecto(total_count, olength, area_length, oposx, oposy, fs):
    object = np.ones([int(total_count),int(total_count)],dtype=complex)
    for i in range(int(olength*fs)):
        for j in range(int(olength*fs)):
            if (olength*fs/2.-i)**2 + (olength*fs/2.-j)**2 < (olength*fs/2.)**2.:
                object[int(area_length*fs/2.)+int(oposy*fs)+i][int(area_length*fs/2.)+int(oposx*fs)+j]=np.exp(-1.485*1j*2*np.sqrt(0.01*((olength/2.)**2.-(olength/2.-i/fs)**2.-(olength/2.-j/fs)**2.))) #-0.9*np.sqrt(0.01*((olength/2.)**2.-(olength/2.-i/fs)**2.-(olength/2.-j/fs)**2.)) + 0.05*1j*2*np.sqrt(0.01*((olength/2.)**2.-(olength/2.-i/fs)**2.-(olength/2.-j/fs)**2.))
    return object

def Object(total_count, wave_number, olength, area_length, fs):
    object = np.ones([int(total_count),int(total_count)],dtype=complex)
    for i in range(int(total_count)):
        for j in range(int(olength*fs)):
            object[i][int(area_length*fs/2.)+int(0*fs)+j]=1-np.exp(wave_number * (-0.000001)*((j-2.*fs)/fs)**2.)/5. + 0.0003*1j*(np.exp(wave_number * (-0.0000001)*((j-2.*fs)/fs)**2.))
    return object

def Object_sphere_ref(total_count, wave_number, sphere, area_length, fs,material,xenergy,amp):
    delta,beta = mat_delta_beta(material,xenergy)

    object = np.ones([int(total_count),int(total_count)],dtype=complex)
    olength = sphere[0]
    for i in range(int(olength*fs)):
        for j in range(int(olength*fs)):
            if (olength/2.-i/fs)**2 + (olength/2.-j/fs)**2 < (olength/2.)**2.:
                object[int(area_length*fs/2.)+int(sphere[1]*fs)+i][int(area_length*fs/2.)+int(sphere[2]*fs)+j]=-1j*wave_number*delta*2/amp*np.sqrt((olength/2.)**2.-(olength/2.-i/fs)**2.-(olength/2.-j/fs)**2) 
    return object
    
def Object_sphere(total_count, wave_number, sphere, area_length, fs,material,xenergy):
    delta,beta = mat_delta_beta(material,xenergy)

    object = np.ones([int(total_count[0]),int(total_count[1])],dtype=complex)
    olength = sphere[0]
    # for i in range(int(olength*fs[0])):
    for j in range(int(olength*fs[1])):
        if (olength/2.-j/fs[1])**2 < (olength/2.)**2.:
                # object[int(area_length[0]*fs[0]/2.)+int(sphere[1]*fs[0])+i][int(area_length[1]*fs[1]/2.)+int(sphere[2]*fs[1])+j]=np.exp(-1j*wave_number*delta*2*np.sqrt((olength/2.)**2.-(olength/2.-i/fs[0])**2.-(olength/2.-j/fs[1])**2) - wave_number*beta*2.*np.sqrt((olength/2.)**2.-(olength/2.-i/fs[0])**2.-(olength/2.-j/fs[1])**2))
            object[0][int(area_length[1]*fs[1]/2.)+int(sphere[2]*fs[1])+j]=np.exp(-1j*wave_number*delta*2*np.sqrt((olength/2.)**2.-(olength/2.-j/fs[1])**2) - wave_number*beta*2.*np.sqrt((olength/2.)**2.-(olength/2.-j/fs[1])**2))
                #object[int(area_length[0]*fs[0]/2.)+int(sphere[1]*fs[0])+i][int(area_length[1]*fs[1]/2.)+int(sphere[2]*fs[1])+j]=-1j*wave_number*delta*2*np.sqrt((olength/2.)**2.-(olength/2.-i/fs[0])**2.-(olength/2.-j/fs[1])**2) - wave_number*beta*2.*np.sqrt((olength/2.)**2.-(olength/2.-i/fs[0])**2.-(olength/2.-j/fs[1])**2)           
    return object

def ObjRef(total_count, wave_number, cylinder, area_length,fs,material,xenergy,amp,sep):
    delta,beta = mat_delta_beta(material,xenergy)

    objrefabs = Obj_Abs_Ref(total_count, wave_number, cylinder, area_length,fs,beta,amp,sep) \
                  + Obj_Abs_Ref(total_count, wave_number, cylinder, area_length,fs,beta,amp,-sep)

    objrefdpc = Obj_DPC_Ref(total_count, wave_number, cylinder, area_length,fs,delta,amp,-sep)\
                 - Obj_DPC_Ref(total_count, wave_number, cylinder, area_length,fs,delta,amp,sep)        
    return objrefabs,np.imag(objrefdpc)

def Obj_Abs_Ref(total_count, wave_number, cylinder, area_length,fs,beta,amp,sep):
    olengthd = cylinder[0]*amp
    pos_x = cylinder[3]*amp + sep
    object = np.ones([int(total_count[0]),int(total_count[1])])
    for j in range(int(olengthd*fs[1])):
        object[0][int(area_length[1]*fs[1]/2.)+int(pos_x*fs[1])+j]=np.exp(- wave_number*beta*2./amp*np.sqrt((olengthd/2.)**2 - (olengthd/2.-j/fs[1])**2)) 
    return object

def Obj_DPC_Ref(total_count, wave_number, cylinder, area_length,fs,delta,amp,sep):
    olengthd = cylinder[0]*amp
    pos_x = cylinder[3]*amp + sep
    object = np.ones([int(total_count[0]),int(total_count[1])], dtype=complex) 
    for j in range(int(olengthd*fs[1])):
        object[0][int(area_length[1]*fs[1]/2.)+int(pos_x*fs[1])+j]=-wave_number*delta*2./amp*np.sqrt((olengthd/2.)**2 - (olengthd/2.-j/fs[1])**2)*1j
    return object

def Object_cylinder_side(total_count, wave_number, cylinder, area_length,fs,material,xenergy):
    # Side of a cylinder
    # Circular surface of a cylinder
    delta,beta = mat_delta_beta(material,xenergy)
    olengthd = cylinder[0]
    object = np.ones([int(total_count[0]),int(total_count[1])],dtype=complex)
    for j in range(int(olengthd*fs[1])):
        object[0][int(area_length[1]*fs[1]/2.)+int(cylinder[3]*fs[1])+j]=np.exp(- 1j*wave_number*delta*2*np.sqrt((olengthd/2.)**2 - (olengthd/2.-j/fs[1])**2) - wave_number*beta*2.*np.sqrt((olengthd/2.)**2 - (olengthd/2.-j/fs[1])**2))
    return object


def Object_cylinder_circular(total_count, wave_number, olength, area_length, oposx, oposy, fs,material,xenergy):
    # Circular surface of a cylinder
    delta,beta = mat_delta_beta(material,xenergy)
    # p_phi = 0
    object = np.ones([int(total_count),int(total_count)],dtype=complex)
    for i in range(int(olength*fs)):
        for j in range(int(olength*fs)):
            if (olength*fs/2.-i)**2 + (olength*fs/2.-j)**2 < (olength*fs/2.)**2.:
                # object[int(area_length*fs/2.)+int(oposy*fs)+i][int(area_length*fs/2.)+int(oposx*fs)+j]=np.exp(-2*wave_number*beta*20 - 1j*wave_number*delta*20)
                object[int(area_length*fs/2.)+int(oposy*fs)+i][int(area_length*fs/2.)+int(oposx*fs)+j]=np.exp(- 1j*wave_number*delta*1.78 -  wave_number*beta*1.78)
    return object

def Phase_grating(period,fs, total_count,xenergy):
    #phase grating An function
    # print('test')
    # gridg = np.zeros([int(total_count[0]),int(total_count[1])],dtype=complex)
    # for i in range(int(total_count[0])):
    #     for j in range(int(total_count[1])):
    #         gridg[i][j] =  1./fs[1] * (j-total_count[1]/2.)
    # phi = np.pi*get_xenergy_phi(xenergy)
    # for n in range(2):
    #     if n  == 0:
    #         gridg2 = 1./2.*(np.exp(1j*phi) + 1)
    #     else:
    #         gridg2 += 1./(np.pi*n)*np.sin(np.pi*n/2.)*(np.exp(1j*phi)-1)*(np.exp(1j*2.*np.pi*n*(gridg)/period) + np.exp(1j*2.*np.pi*-n*(gridg)/period))

    #phase grating Square wave function
    phi = np.pi*get_xenergy_phi(xenergy)
    t = np.linspace(0, int(total_count[1]), int(total_count[1]), endpoint=False) 
    grating_prex = (scipy.signal.square(2. * np.pi/(period*fs[1]) * (t-2./8.*period*fs[1]))+1)*0.5
    gridg2 = np.zeros([int(total_count[0]),int(total_count[1])],dtype=complex)
    for i in range(int(total_count[0])):
        for j in range(int(total_count[1])):
            gridg2[i][j] =  abs(grating_prex[j] - 1)*1.j + grating_prex[j]
    #gridg2 = (gridg2-(1.j+1)/2.) * ( np.cos(phi) + 1.j*np.sin(phi)-1)/( np.cos(np.pi/2.) + 1.j*np.sin(np.pi/2.)-1) + (np.cos(phi) + 1.j*np.sin(phi)+1)/2.
    return gridg2

def Fourier_grating_y(period, step, fs, total_count):
    #Absorption grating from spatial direction
    t = np.linspace(0, int(total_count[1]), int(total_count[1]), endpoint=False)
    grating = (scipy.signal.square(2. * np.pi/(period*fs[1]) * (t+1/8.*period*fs[1]+step*fs[1]))+1)*0.5
    gridging = np.zeros([int(total_count[0]),int(total_count[1])],dtype=complex)
    for i in range(int(total_count[0])):
        for j in range(int(total_count[1])):
            gridging[i][j] =  grating[j]

    # #absorption gratingAn function
    # gridg = np.zeros([int(total_count[0]),int(total_count[1])],dtype=complex)
    # for i in range(int(total_count[0])):
    #     for j in range(int(total_count[1])):
    #         gridg[i][j] =  1./fs[1] * (j-total_count[1]/2.)+step
    # # xenergy = 25
    # for n in range(2):
    #     if n  == 0:
    #         grating = 1./2
    #     elif (n%2) == 0:
    #         grating += 0
    #     else:
    #         grating += - 1j/n/np.pi*np.exp(1j*2*np.pi*n*(gridg)/period)
    #         grating +=  1j/n/np.pi*np.exp(1j*2*np.pi*(-n)*(gridg)/period)  
    # gridg = np.zeros([int(total_count[0]),int(total_count[1])],dtype=complex)
    # for i in range(int(total_count[0])):
    #     for j in range(int(total_count[1])):
    #         gridg[i][j] =  1./fs[1] * (j-total_count[1]/2.) + step
    # theta = 0.00001
    # F_absor_x3 = 1 + np.cos(2*np.pi/period*gridg*np.cos(theta))

    # fig, axs = plt.subplots(1,3,figsize=(9, 6))
    # axs[0].plot(np.real(F_absor_x3[0]),'r')
    # axs[0].plot(np.real(gridging[0])*2,'b')
    # plt.show()
    return grating

def Fourier_grating_y2(period, step, fs, total_count):
    #Absorption grating 1 + cos(2 PI/p2 x3)

    gridg = np.zeros([int(total_count[0]),int(total_count[1])],dtype=complex)
    for i in range(int(total_count[0])):
        for j in range(int(total_count[1])):
            gridg[i][j] =  1./fs[1] * (j-total_count[1]/2.) + step
    theta = 0.00001
    F_absor_x3 = 1 + np.cos(2*np.pi/period*gridg*np.cos(theta))

    # fig, axs = plt.subplots(1,3,figsize=(9, 6))
    # axs[0].plot(np.real(F_absor_x3[0]))
    # axs[1].plot(np.imag(F_absor_x3[0]))
    # axs[2].plot(abs(F_absor_x3[0])**2)
    # plt.show()
    return F_absor_x3


def get_xenergy_phi(xenergy):
    beta_list,delta_list = read_para('Si')
    for i in range(len(beta_list)):
        if(float_def(beta_list[i][0]) and float_def(delta_list[i][1])):
            if abs(float(beta_list[i][0])/1000. - xenergy) < 1e-6:    #kev
                xenergy_phi_delta =  float(delta_list[i][1])
            if abs(float(beta_list[i][0])/1000. - 25) < 1e-6:    #kev
                ref_phi_delta =  float(delta_list[i][1])    
    return xenergy_phi_delta/ref_phi_delta


def PhaseStepping(Fin, numStep, total_count, fs, xenergy_ratio,G2Period):
    sourceT = []
    period_test = 0
    for i in range(1,numStep+1):
        step = i*G2Period/numStep
        # period_test += step
        FD2 = Fin*Fourier_grating_y(G2Period, step, fs, total_count)
        sourceT.append(abs(FD2)**2*xenergy_ratio)
    print("period_test=",period_test)
    return sourceT

def PhaseStepping_nograting(Fin, numStep, total_count, fs, xenergy_ratio,G2Period):
    sourceT = []
    sourceT.append(abs(Fin)**2*xenergy_ratio)
    return sourceT

def Signal_extract(data,total_count, pixel_number):
    FDetT1 = np.zeros([int(total_count[0]),int(pixel_number)])
    FDetS1 = np.zeros([int(total_count[0]),int(pixel_number)])
    FDetC1 = np.zeros([int(total_count[0]),int(pixel_number)])
    I_stpt_obj = xspec_total(data)
    sourceT = []
    FDetT1s = []
    FDetS1s = []
    FDetC1s = []
    number_step = len(I_stpt_obj)
    for i in range(len(I_stpt_obj)):
        sourceT = gauss_filter_reshape(I_stpt_obj[i],pixel_number)
        sourceS = sourceT * np.sin(2*np.pi*(i+1)/number_step)
        sourceC = sourceT * np.cos(2*np.pi*(i+1)/number_step) 
        FDetT1s.append(sourceT)
        FDetS1s.append(sourceS)
        FDetC1s.append(sourceC)
        FDetT1 = FDetT1 + sourceT
        FDetS1 = FDetS1 + sourceS
        FDetC1 = FDetC1 + sourceC
    dark_field = 2./number_step*(FDetS1**2 + FDetC1**2)
    return -np.arctan(FDetS1/FDetC1),FDetT1/number_step,dark_field

def Signal_extract_fft(data,pixel_number,numStep):
    I_stpt_obj = xspec_total(data)
    sourceT = []
    FDetT1s = []
    for i in range(len(I_stpt_obj)):
        sourceT = gauss_filter_reshape(I_stpt_obj[i],pixel_number)
        FDetT1s.append(sourceT)
    FTout = get_phi_with_fft(FDetT1s,pixel_number,numStep)
    return FTout,FDetT1s

def get_phi_with_fft(input_datas,pixel_number,numStep):
    input_datas = np.array(input_datas)
    input_datas = input_datas.reshape(numStep,pixel_number)
    # import scipy.fftpack
    input_datas = np.array(input_datas)
    FTout = np.fft.fft(input_datas,int(len(input_datas)),-2)
    return FTout

def xspec_total(input_data):
    data_out = []
    data_in = input_data.copy()
    print('phase step = ',len(data_in[0]))
              
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
def gauss_filter_reshape(data,pixel_number):
    data = data.reshape(pixel_number,int(len(data[0])/pixel_number)).mean(1)
    # data= scipy.ndimage.gaussian_filter(data,sigma=0)
    return data

def ZonePlate2d(f, wave_length, grids):
    zoneplate =  np.exp((-1j) * np.pi * grids / f / wave_length) / np.sqrt(np.pi)
    return zoneplate

def ZonePlate2d1(f, wave_length, radius, total_count, fs, grids):
    zoneplate = np.zeros([int(total_count), int(total_count)], dtype=complex)
    for i in range(int(2.*radius*fs)):
        for j in range(int(2.*radius*fs)):
            if (radius*fs-i)**2. + (radius*fs-j)**2. < (radius*fs)**2.:
                zoneplate[int(total_count/2. + i - radius*fs)][int(total_count/2. + j - radius*fs)] = np.exp((-1j) * np.pi * (((-1.)*radius+i/fs)**2.+((-1.)*radius+j/fs)**2.) / f / wave_length) / np.pi
    return zoneplate

def float_def(input):
    try:
        float(input)
        return True
    except Exception as exc:
        return False