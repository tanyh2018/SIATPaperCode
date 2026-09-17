import numpy as np
import matplotlib.pyplot as plt 
import scipy.signal
import sys
import copy
import math

def main():    
    print("test")
    #simulation_condition_judge()
    #Propagation_with_sample_pure_absor()
    Propagation_with_sample_pure_phase()
    #complex_angle_test()
    # #xray_propag_process()
    # # fourier_change()
    # #simulation_condition_judge()
    #progation_p = xray_propag_process()
    #xray_propag_process_fft()
    #xray_propag_process_fft_delta()
    # print("test")
    # progation_t = xray_propag_theory()
    
    plt.show()
    pass


def complex_angle_test():
    a = [2 + 2j,2 + 1j,2 + 3j]
    b = [2+0j,1+0j,2+0j]
    c = np.array(a)*(b)
    print(np.angle(a))    
    print(np.angle(c))  


def simulation_condition_judge():
    dx = 1e-6 #m
    det_l = 0.005 #m
    N_sim = det_l/dx
    lambda_min = 1.239842/40*1e-9
    lambda_max = 1.239842/4*1e-9
    # print(lambda_max)
    d_max = det_l**2/N_sim/lambda_max
    print("distance max = ",d_max)
    print("condition factor=",det_l**2 /(lambda_min**2*N_sim**2/2.))
    pass

def xray_propag_process_fft():
    """ Compare simulation and theory result for x ray propagation"""
    det_l = 0.005*1e6
    dx=1e-9*1e6
    Detector = [-det_l/2.,det_l/2.]   #um
    number = int(det_l/dx) + 1
    sigma = 1e-6*1e6
    
    d1 = 1.382 *1e6  #um
    d2 = 0.104  *1e6  #um
    d3 = 1.04  *1e6  #um
    wavelength = 4.96*10**(-11)*1e6
    x = np.linspace(Detector[0],Detector[1],number)
    wave_number = 2.*np.pi/wavelength
    # simulation
    source  = gauss_source(Detector,number,sigma,dx)
    progation1_s = Propagation2d_zhangran(source, d2, wavelength, dx)
    progation2_s = Propagation2d_zhangran(progation1_s, d2, wavelength, dx)
    progation3_s = Propagation2d_zhangran(progation2_s, d3,wavelength, dx)

    # #theory
    wave_number = 2.*np.pi/wavelength
    #gausss theory
    progation1_t =  2.50663*np.exp(1j*d1*wave_number - wave_number*x**2/(2.j*d1 + 2.*wave_number*sigma**2))/np.sqrt(1.j * d1 *wavelength)/np.sqrt(-1.j*wave_number/d1 + 1./sigma**2)
    progation2_t = 2.50663*np.exp(1j*(d1+d2)*wave_number - wave_number*x**2/(2.j*(d1+d2) + 2.*wave_number*sigma**2))/np.sqrt(1.j * (d1+d2) *wavelength)/np.sqrt(-1.j*wave_number/(d1+d2) + 1./sigma**2)
    progation3_t = 2.50663*np.exp(1j*(d1+d2+d3)*wave_number - wave_number*x**2/(2.j*(d1+d2+d3) + 2.*wave_number*sigma**2))/np.sqrt(1.j * (d1+d2+d3) *wavelength)/np.sqrt(-1.j*wave_number/(d1+d2+d3) + 1./sigma**2)
    plot_together_show(x,progation3_s,progation3_t)

def xray_propag_process_fft_delta():
    """ Compare simulation and theory result for x ray propagation"""
    det_l = 0.005*1e6
    dx=1e-9*1e6
    Detector = [-det_l/2.,det_l/2.]   #um
    number = int(det_l/dx) + 1
    sigma = 1e-6*1e6
    
    d1 = 1.382 *1e6  #um
    d2 = 0.104  *1e6  #um
    d3 = 1.04  *1e6  #um
    wavelength = 4.96*10**(-11)*1e6
    x = np.linspace(Detector[0],Detector[1],number)
    wave_number = 2.*np.pi/wavelength
    progation1_t  = 1.0*np.exp(1.j*wave_number*(d1 + x**2/2./d1))/(np.sqrt(1.j*d1*wavelength))

    fig, axs = plt.subplots(1,1,figsize=(9, 6))
    plt.plot(np.real(progation1_t))
    plt.show()
    # simulation
    source = delta_source(Detector,number)
    # source  = gauss_source(Detector,number,sigma,dx)
    progation2_s = Propagation2d_zhangran(progation1_t, d2, wavelength, dx)
    #progation2_s = Propagation2d_scipy_convolve(progation1_t, d2, wavelength, x)
    # progation2_s = Propagation2d_zhangran(progation1_s, d2,wavelength, dx)
    # progation3_s = Propagation2d_zhangran(progation2_s, d3,wavelength, dx)
    # progation2_s = Propagation2d_zhangran(progation1_s, d2,wavelength, dx)
    # #progation3 = Propagation2d_zhangran(progation2, d2,wavelength, dx)

    # #theory
    wave_number = 2.*np.pi/wavelength
    
    #diracDelta theory
    progation2_t  = 1.0*np.exp(1.j*wave_number*(d1+d2 + x**2/2./(d1+d2)))/(np.sqrt(1.j*(d1+d2)*wavelength))
    # print(progation1_t)

    #gausss theory
    #progation1_t =  2.50663*np.exp(1j*d1*wave_number - wave_number*x**2/(2.j*d1 + 2.*wave_number*sigma**2))/np.sqrt(1.j * d1 *wavelength)/np.sqrt(-1.j*wave_number/d1 + 1./sigma**2)
    # progation2_t = 2.50663*np.exp(1j*(d1+d2)*wave_number - wave_number*x**2/(2.j*(d1+d2) + 2.*wave_number*sigma**2))/np.sqrt(1.j * (d1+d2) *wavelength)/np.sqrt(-1.j*wave_number/(d1+d2) + 1./sigma**2)
    # progation3_t = 2.50663*np.exp(1j*(d1+d2+d3)*wave_number - wave_number*x**2/(2.j*(d1+d2+d3) + 2.*wave_number*sigma**2))/np.sqrt(1.j * (d1+d2+d3) *wavelength)/np.sqrt(-1.j*wave_number/(d1+d2+d3) + 1./sigma**2)
    plot_together_show(x,progation2_s,progation1_t)

def Propagation_with_sample_pure_absor():
    det_l = 6e-4
    dx=1e-8
    Detector = [-det_l/2.,det_l/2.]   #um
    number = int(det_l/dx) + 1
    sigma = 1e-6
    
    d1 = 1.382   #um
    d2 = 0.104    #um
    d3 = 1.04    #um
    wavelength = 4.96*10**(-11)
    x = np.linspace(Detector[0],Detector[1],number)
    wave_number = 2.*np.pi/wavelength
    sigma = 5e-5
    b=0.5

    progation1_t  = 1.0*np.exp(1.j*wave_number*(d1 + x**2/2./d1))/(np.sqrt(1.j*d1*wavelength))
    #cylinder_1 = np.exp(-1*x**2/(2.0*sigma**2))*(-b)+1
    cylinder_1 = np.exp(1j*wave_number*150*x*1e-8)
    fig, axs = plt.subplots(1,1,figsize=(9, 6))
    plt.plot(abs(cylinder_1)**2)

    progation_withobj = cylinder_1*progation1_t

    propogation_garting = Propagation2d_zhangran(progation_withobj, d2, wavelength, dx)

    propogation_witgoutobj = Propagation2d_zhangran(progation1_t, d2, wavelength, dx)

    fig, axs = plt.subplots(1,1,figsize=(9, 6))
    plt.plot(abs(propogation_garting)**2)

    #Theory with sample
    propogation_garting_theory_1obj =  np.exp(1j*wave_number*(d1+x**2/2/d1))*(1-b*np.exp(-x**2/2/sigma**2))/np.sqrt(1j*d1*wavelength)
    propogation_garting_theory_2obj = np.sqrt(2*np.pi)*(-b*np.exp(0.5*1j*wave_number*(2.*d2+x**2/d2+d1*(2.-wave_number*x**2*sigma**2/(d2*(1j*d1*d2+d1*wave_number*sigma**2+d2*wave_number*sigma**2)))))/np.sqrt((d1*d2*wavelength*wavelength)*(1j*(wave_number/d1+wave_number/d2)-1/sigma**2)) + np.exp(1j*wave_number*(2.*(d1+d2)**2+x**2)/2/(d1+d2))/(np.sqrt(1j*(d1+d2)*wave_number*wavelength*wavelength)))

   
    progation2_t  = 1.0*np.exp(1.j*wave_number*(d1+d2 + x**2/2./(d1+d2)))/(np.sqrt(1.j*(d1+d2)*wavelength))
    # test_phi_complex(propogation_garting_theory_2obj,progation2_t)
    # plot_together_show(x,propogation_garting_theory_2obj,progation2_t)

    test_phi_complex(propogation_garting,propogation_witgoutobj)
    #plot_together_show(x,propogation_garting,propogation_witgoutobj)

def Propagation_with_sample_pure_phase():
    det_l = 6e-4
    dx=1e-8
    Detector = [-det_l/2.,det_l/2.]   #um
    number = int(det_l/dx) + 1
    sigma = 1e-6
    
    d1 = 1.382   #um
    d2 = 0.104    #um
    d3 = 1.04    #um
    wavelength = 4.96*10**(-11)
    x = np.linspace(Detector[0],Detector[1],number)
    wave_number = 2.*np.pi/wavelength
    sigma = 5e-5*2
    b=0.5
    delta=1e-8
    const_pa = (2.0*wave_number*delta*2)*0.0001

    progation1_t  = 1.0*np.exp(1.j*wave_number*(d1 + x**2/2./d1))/(np.sqrt(1.j*d1*wavelength))
    #cylinder_1 = np.exp(-1j*(np.exp(-1*x**2/(2.0*sigma**2))+1)*const_pa)
    guas_y = np.exp(-1*x**2/(2.0*sigma**2))*1e-6


    cylinder_1 = np.ones(len(x),dtype=complex)
    for i in range(len(x)):
        if x[i] > -5e-5 and x[i] < 5e-5:
            cylinder_1[i] = np.exp(-1j*wave_number*150*1e-8*0.001*guas_y[i])
        else:
            cylinder_1[i] = np.exp(-1j*wave_number*150*1e-8*0.001*guas_y[i])
    # fig, axs = plt.subplots(1,1,figsize=(9, 6))
    # plt.plot(abs(cylinder_1)**2)
    # plt.plot(np.real(cylinder_1))
    # plt.plot(np.imag(cylinder_1))
    # plt.show()
    progation_withobj = cylinder_1*progation1_t
    test_phi_complex(progation_withobj,progation1_t)
    #propogation_garting = Propagation2d_zhangran(progation_withobj, d2, wavelength, dx)

    #propogation_witgoutobj = Propagation2d_zhangran(progation1_t, d2, wavelength, dx)
    propogation_garting =  Propagation2d_scipy_convolve(progation_withobj, d2, wavelength, x)
    propogation_witgoutobj = Propagation2d_scipy_convolve(progation1_t, d2, wavelength, x)
    fig, axs = plt.subplots(1,1,figsize=(9, 6))
    plt.plot(abs(progation_withobj)**2,label = 'Obj effect')
    plt.title('Sample Intensity')
    #Theory with sample
    # propogation_garting_theory_1obj =  np.exp(1j*wave_number*(d1+x**2/2/d1))*(1-b*np.exp(-x**2/2/sigma**2))/np.sqrt(1j*d1*wavelength)
    # propogation_garting_theory_2obj = np.sqrt(2*np.pi)*(-b*np.exp(0.5*1j*wave_number*(2.*d2+x**2/d2+d1*(2.-wave_number*x**2*sigma**2/(d2*(1j*d1*d2+d1*wave_number*sigma**2+d2*wave_number*sigma**2)))))/np.sqrt((d1*d2*wavelength*wavelength)*(1j*(wave_number/d1+wave_number/d2)-1/sigma**2)) + np.exp(1j*wave_number*(2.*(d1+d2)**2+x**2)/2/(d1+d2))/(np.sqrt(1j*(d1+d2)*wave_number*wavelength*wavelength)))
    # progation2_t  = 1.0*np.exp(1.j*wave_number*(d1+d2 + x**2/2./(d1+d2)))/(np.sqrt(1.j*(d1+d2)*wavelength))
    test_phi_complex(propogation_garting,propogation_witgoutobj)
    fig, axs = plt.subplots(1,1,figsize=(9, 6))
    plt.plot(abs(propogation_garting)**2,label = 'Obj effect')
    plt.title('Sample Intensity')    
    # plot_together_show(x,propogation_garting_theory_2obj,progation2_t)
    plt.show()
    # test_phi_complex(propogation_garting,propogation_witgoutobj)
    # plot_together_show(x,propogation_garting,propogation_witgoutobj)


def test_phi_complex(data_A,data_B):
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
    plt.title('Sample Phase')

def Propagation2d_zhangran(Fin, distance, wave_length, dx):
    wave_number = 2.*np.pi/wave_length
    N0 = len(Fin)
    # Wf_zpad = np.zeros(N0)
    # Wf_zpad[:] = Fin
    # print('N0=',N0)
    # print('dx=',dx)
    x = np.linspace(-1/2.,1/2,N0)/dx
    #print(Fin)
    F_index = np.exp(1j*wave_number*distance*np.sqrt(1 - (wave_length*x)**2))
    # print(Fin[0])
    F_origi = np.fft.fft(np.fft.fftshift(Fin))
    #fig1 = plt.figure(figsize=(9,6))
    # plt.plot(np.real(F_origi))
    #plt.scatter(np.real(F_origi),np.imag(F_origi))
    # fig1 = plt.figure(figsize=(9,6))
    # plt.plot(np.imag(F_origi))
    # plt.show()
    # sys.exit()
    F_index = np.fft.fftshift(F_index)
    Fout =  np.fft.fftshift(np.fft.ifft((F_origi*F_index)))
    # for i in range(len(Fout)):
    #     print("real",np.round(np.real(Fout[i]),4))
    # for i in range(len(Fout)):
    #     print("imag",np.round(np.imag(Fout[i]),4))
    # sys.exit()
    # fig1 = plt.figure(figsize=(9,6))
    # plt.scatter(np.real(F_origi),np.imag(F_origi))
    # fig1 = plt.figure(figsize=(9,6))
    # plt.scatter(np.real(F_index),np.imag(F_index))
    # plt.show()
    return Fout

def plot_together_show(x,xdata,ydata):
    # fig, axs = plt.subplots(1,1,figsize=(9, 6))
    # plt.plot(abs(ydata)**2/abs(max(abs(ydata)**2)),'r',label = 'theory sqaure')
    # plt.plot(abs(xdata)**2/abs(max(abs(xdata)**2)),'b--',label = 'sim sqaure')
    # plt.legend(loc='best',fontsize=10,frameon=False)

    #sim theory
    # fig, axs = plt.subplots(1,1,figsize=(9, 6))
    # plt.plot(x,np.real(xdata),'r',label = 'sim real')
    # plt.plot(x,np.real(ydata),'b--',label = 'theory real')
    # plt.legend(loc='best',fontsize=10,frameon=False)

    # fig, axs = plt.subplots(1,1,figsize=(9, 6))
    # plt.plot(x,np.imag(xdata),'r',label = 'sim imag')
    # plt.plot(x,np.imag(ydata),'b--',label = 'theory imag')
    # plt.legend(loc='best',fontsize=10,frameon=False)

    # fig, axs = plt.subplots(1,1,figsize=(9, 6))
    # plt.plot(x,np.real(xdata)**2 + np.imag(xdata)**2 - (np.real(ydata)**2 + np.imag(ydata)**2),'r',label = 'sim sqaure')
    # plt.plot(x,np.real(ydata)**2 + np.imag(ydata)**2,'b--',label = 'theory sqaure')
    # plt.legend(loc='best',fontsize=10,frameon=False)

    #obj withobj
    fig, axs = plt.subplots(1,1,figsize=(9, 6))
    plt.plot(x,np.real(xdata),'r',label = 'obj real')
    plt.plot(x,np.real(ydata),'b--',label = 'without obj real')
    plt.legend(loc='best',fontsize=10,frameon=False)

    fig, axs = plt.subplots(1,1,figsize=(9, 6))
    plt.plot(x,np.imag(xdata),'r',label = 'obj imag')
    plt.plot(x,np.imag(ydata),'b--',label = 'without obj imag')
    plt.legend(loc='best',fontsize=10,frameon=False)

    fig, axs = plt.subplots(1,1,figsize=(9, 6))
    plt.plot(x,np.real(xdata)**2 + np.imag(xdata)**2 ,'r',label = 'obj sqaure')
    plt.plot(x,np.real(ydata)**2 + np.imag(ydata)**2,'b--',label = 'without obj sqaure')
    plt.legend(loc='best',fontsize=10,frameon=False)

    fig, axs = plt.subplots(1,1,figsize=(9, 6))
    plt.plot(x,np.real(xdata)**2 + np.imag(xdata)**2 - (np.real(ydata)**2 + np.imag(ydata)**2) ,'r',label = 'obj sqaure - without obj sqaure')
    plt.legend(loc='best',fontsize=10,frameon=False)

def Propagation2d_scipy_convolve(Fin, distance, wave_length, grids):
    wave_number = 2.*np.pi/wave_length
    F_index = 1./np.sqrt(1j*wave_length*distance)*np.exp(1j*wave_number*(grids**2/2./distance + distance))
    Fout =  scipy.signal.fftconvolve(Fin,F_index,mode='same')*10./len(Fin)
    return Fout


def gauss_source(Detector,number,sigma,dx):
    # x=np.zeros([number])
    x = np.linspace(Detector[0],Detector[1],number)
    # for i in range(number):
    #     x[i] = Detector[0] + i*dx
    # print(x)
    source = np.zeros([number],dtype=complex)
    source= np.round(np.exp(-1*x**2/(2.0*sigma**2)),4) + 0.j
    # for i in range(number):
    #     print(x[i])
    # fig1 = plt.figure(figsize=(9,6))
    # plt.plot(x,source)
    # plt.show()
    return source


def delta_source(Detector,number):
    # x=np.zeros([number])
    x = np.linspace(Detector[0],Detector[1],number)
    # for i in range(number):
    #     x[i] = Detector[0] + i*dx
    # print(x)
    source = np.zeros([number],dtype=complex)
    source[int(number/2)]= 1.0 + 0.j
    # for i in range(number):
    #     print(x[i])
    fig1 = plt.figure(figsize=(9,6))
    plt.plot(x,source)
    plt.show()
    return source


def plot_show(xdata,ydata):
    fig1 = plt.figure(figsize=(9,6))
    plt.plot(xdata,np.real(ydata),'r',label = 'real')
    plt.plot(xdata,np.imag(ydata),'b',label = 'imag')
    # plt.plot(xdata,abs(ydata)**2,'black',label = 'square')
    plt.legend(loc='best',fontsize=10,frameon=False)


def two_gauss_convolve():
    # Function 1 Exp[-x^2/2], Function 1 Exp[-x^2/8]
    x1 = []
    y1 = []
    y2 = []
    y1_l = []
    y2_l = []

    n = 100000
    grids = np.zeros([1,n],dtype=complex)
    gridsy = np.zeros([1,n],dtype=complex)
    gridsy2 = np.zeros([1,n],dtype=complex)
    x1 = np.zeros([1,n])
    sigma_1 = 0.1
    sigma_2 = 0.2
    sigma_3 = sigma_1*sigma_1 + sigma_2*sigma_2
    for i in range(1): 
        for j in range(n):
            x = (j-n/2)*10 / n
            x1[i][j] = x
            grids[i][j]= np.exp(-1j*x**2/(2.0*sigma_1**2)) *np.exp(-1j*np.pi/2.)  #sigma_1 = 1
            gridsy[i][j] = np.exp(-1j*x**2/(2.0*sigma_2**2)) *np.exp(-1j*np.pi/2.)#sigma_1 = 1
            gridsy2[i][j] =  - np.sqrt(2*np.pi)*np.exp(-1j*x**2/(2.0*sigma_3))*np.sqrt(1.0/(1j*(1/sigma_1**2 + 1/sigma_2**2))) #sigma_1 = 1

    F1 = np.fft.fftshift(np.fft.fft(np.fft.ifftshift(grids)))
    F2 = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(gridsy)))
    # F2 = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(y2)))
    Fout = np.fft.ifftshift(np.fft.ifft2(np.fft.ifftshift(F2*F1)))*10/n
    # print(np.real(Fout))
    A = scipy.signal.fftconvolve(grids,gridsy,mode="same")*10./n*1.00
    # print(A)
    #Fout = scipy.signal.convolve2d(grids,grids)
    # print(grids[0])
    fig1 = plt.figure(figsize=(9,6))
    plt.plot(x1[0],np.real(A[0]),color = "blue",label='Convolve real part')
    plt.plot(x1[0],np.real(gridsy2[0]),color = "red",label='Theory real part')
    plt.legend(loc='best',fontsize=10,frameon=False)

    fig1 = plt.figure(figsize=(9,6))
    plt.plot(x1[0],np.imag(A[0]),color = "blue",label='Convolve imag part')
    plt.plot(x1[0],np.imag(gridsy2[0]),color = "red",label='Theory imag part')
    plt.legend(loc='best',fontsize=10,frameon=False)

    fig1 = plt.figure(figsize=(9,6))
    plt.plot(x1[0],abs(A[0])**2,color = "blue",label='Convolve square part')
    plt.plot(x1[0],abs(gridsy2[0])**2,color = "red",label='Theory square part')
    plt.legend(loc='best',fontsize=10,frameon=False)
    plt.show()
    # fig1 = plt.figure(figsize=(9,6))
    # plt.plot(x1[0],Fout[0],color = "blue",label='FFT method')
    # plt.plot(x1[0],gridsy2[0],color = "red",label='Theory')
    # plt.plot(x1[0],A[0],color = 'black',label="Scipy convolve")
    # plt.legend(loc='best',fontsize=10,frameon=False)
    # plt.grid()
    # plt.xlabel( "x direction " )
    # plt.ylabel("$F^{-1}[g_{1}(x)*g_{2}(x)]$")
    # plt.title("$F^{-1}[g_{1}(x)*g_{2}(x)]$")
    # plt.ylabel("Integrate")
    # plt.title("Integrate")
    plt.show()

if __name__ == '__main__':
    main()