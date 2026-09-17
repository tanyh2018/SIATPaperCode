import numpy as np
import matplotlib.pyplot as plt 
import scipy.signal
import sys

def main():
    simulation_condition_judge()
    #xray_propag_process()
    # fourier_change()
    #simulation_condition_judge()
    progation_p = xray_propag_process()
    progation_t = xray_propag_theory()
    plot_together_show(progation_p,progation_t)
    plt.show()
    pass


def simulation_condition_judge():
    dx = 1e-8 #m
    det_l = 0.5 #m
    N_sim = det_l/dx
    lambda_min = 1.239842/40*1e-9
    lambda_max = 1.239842/4*1e-9
    # print(lambda_max)

    d_max = det_l**2/N_sim/lambda_max
    
    print("distance max = ",d_max)

    print("condition factor=",det_l**2 /(lambda_min**2*N_sim**2/2.))
    pass

def fourier_change():
    wave_length = 4.96*10**(-5)
    distance = 1382000
    wave_number = 2.*np.pi/wave_length 
    Detector = [-2500,2500]   #um
    number = 100*5000
    grids = np.linspace(Detector[0],Detector[1],number)
    Fin_index = 1./np.sqrt(1j*wave_length*distance)*np.exp(1j*wave_number*(grids**2/2./distance + distance))
    Fin_index = np.fft.fftshift(np.fft.fft(np.fft.ifftshift(Fin_index)))
    N0 = number
    x = np.linspace(-N0/2.,N0/2-1,N0)/N0/1.
    F_index1 = np.exp(-1.j*np.pi*wave_length*x**2*distance)

    fig1 = plt.figure(figsize=(9,6))
    plt.plot(Fin_index,'r')
    plt.plot(F_index1,'blue')
    plt.show()

def xray_propag_process():
    det_l = 0.5
    dx=1e-8
    Detector = [-det_l/2.,det_l/2.]   #um
    number = int(det_l/dx)
    sigma = 1e-8
    source  = gauss_source(Detector,number,sigma)
    d1 = 0.1382#um*10e6
    d2 = 0.104#um
    wavelength = 4.96*10**(-11)
    print(wavelength)
    grids = np.linspace(Detector[0],Detector[1],number)
    # print(number)
    # print(len(grids))
    # sys.exit()
    #progation1 = Propagation2d_scipy_convolve(source, d1, wavelength, grids)
    progation1 = Propagation2d_zhangran(source, d1, wavelength, dx)
    progation2 = Propagation2d_zhangran(progation1, d2,wavelength, dx)
    # sys.exit()
    return progation2
    #plot_show(grids,progation1)

def xray_propag_theory():
    det_l = 0.5
    dx=1e-8
    Detector = [-det_l/2.,det_l/2.]   #um
    number = int(det_l/dx)
    sigma = 1e-8
    source  = gauss_source(Detector,number,sigma)
    d1 = 0.1382#um
    d2 = 0.104#um
    wavelength = 4.96*10**(-11)
    print(wavelength)
    wave_number = 2.*np.pi/wavelength 
    x = np.linspace(Detector[0],Detector[1],number)
    progation1 = 2.50663*np.exp(1j*d1*wave_number - wave_number*x**2/(2.j*d1 + 2.*wave_number*sigma**2))/np.sqrt(1.j * d1 *wavelength)/np.sqrt(-1.j*wave_number/d1 + 1./sigma**2)
    progation2 = 2.50663*np.exp(1j*(d1+d2)*wave_number - wave_number*x**2/(2.j*(d1+d2) + 2.*wave_number*sigma**2))/np.sqrt(1.j * (d1+d2) *wavelength)/np.sqrt(-1.j*wave_number/d1 + 1./sigma**2)
    return progation2

def Propagation2d_scipy_convolve(Fin, distance, wave_length, grids):
    wave_number = 2.*np.pi/wave_length
    F_index = 1./np.sqrt(1j*wave_length*distance)*np.exp(1j*wave_number*(grids**2/2./distance + distance))
    # distance = 1382000
    # AA =np.exp( 1j*wave_number*(grids**2/2./distance + distance))
    # distance = 138200
    # BB = np.exp((1j*wave_number*(grids**2/2./distance + distance)))
    # plot_together_show(AA,BB)
    #F_index = 1./np.sqrt(1j*wave_length*np.sqrt(distance**2.+grids**2))*np.exp(1j*wave_number*np.sqrt(distance**2.+grids**2))
    #F_index = np.cos(wave_number*(grids**2/2./distance + distance)) + 1j*np.sin(wave_number*(grids**2/2./distance + distance))
    # print(1j*wave_number*(grids**2/2./distance + distance))
    Fout =  scipy.signal.fftconvolve(Fin,F_index,mode='same')*10./len(Fin)
    #Fout =  np.convolve(Fin,F_index,mode='same')*10./len(Fin)
    return Fout

def Propagation2d_zhangran(Fin, distance, wave_length, dx):

    wave_number = 2.*np.pi/wave_length
    N0 = len(Fin)
    Wf_zpad = np.zeros(N0)
    Wf_zpad[:] = Fin
    x = np.linspace(-1/2.,1/2,N0)/dx
    F_index = np.exp(1j*wave_number*distance*np.sqrt(1 - (wave_length*x)**2))

    F_origi = np.fft.fft(np.fft.fftshift(Wf_zpad))
    F_index = np.fft.fftshift(F_index)
    Fout =  np.fft.fftshift(np.fft.ifft((F_origi*F_index)))

    return Fout

def Propagation2d(Fin, distance, wave_length, grids):


    F_origi = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(Fin)))
    F_index = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(Propag_index2d(wave_length, distance, grids))))
    Fout =  np.sqrt(2.*np.pi) * np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(F_origi*F_index)))
    # F_index = Propag_index2d(wave_length, distance, grids)
    # Fout =   scipy.signal.fftconvolve(Fin,F_index,mode='same')
    # print("test")
    return Fout
def Propagation2d_scipy_convolve_c(Fin, d1,d2,wave_length, grids):
    wave_number = 2.*np.pi/wave_length/10.
    F_index = 1./np.sqrt(1j*wave_length*d2)*np.exp(1j*wave_number*(grids**2/2./d2 + d2))
    #F_index = 1./np.sqrt(1j*wave_length*np.sqrt(distance**2.+grids**2))*np.exp(1j*wave_number*np.sqrt(distance**2.+grids**2))
    #F_index = np.cos(wave_number*(grids**2/2./distance + distance)) + 1j*np.sin(wave_number*(grids**2/2./distance + distance))
    # print(1j*wave_number*(grids**2/2./distance + distance))
    Fout =  scipy.signal.fftconvolve(Fin,F_index,mode='same',method='direct')*10./len(Fin)
    return Fout


def gauss_source(Detector,number,sigma):
    x = np.linspace(Detector[0],Detector[1],number)
    source = np.zeros([number],dtype=complex)
    source= np.exp(-1*x**2/(2.0*sigma**2))*1000000

    # fig1 = plt.figure(figsize=(9,6))
    # plt.plot(x,source)
    # plt.show()
    return source
def plot_show(xdata,ydata):
    fig1 = plt.figure(figsize=(9,6))
    plt.plot(xdata,np.real(ydata),'r',label = 'real')
    plt.plot(xdata,np.imag(ydata),'b',label = 'imag')
    # plt.plot(xdata,abs(ydata)**2,'black',label = 'square')
    plt.legend(loc='best',fontsize=10,frameon=False)

def plot_together_show(xdata,ydata):
    fig, axs = plt.subplots(2,2,figsize=(9, 6))

    axs[0,0].plot(np.real(ydata)/max(abs((np.real(ydata)))),'r',label = 'theory real')
    axs[0,0].plot(np.real(xdata)/max(abs((np.real(xdata)))),'b--',label = 'sim real')
    axs[0,0].set_title('real part compare')
    axs[0,1].plot(np.imag(ydata)/max(abs((np.imag(ydata)))),'r',label = 'theory imag')
    axs[0,1].plot(np.imag(xdata)/max(abs((np.imag(xdata)))),'b--',label = 'sim imag')
    axs[0,1].set_title('imag part compare')
    axs[1,0].plot(abs(ydata)**2/abs(max(abs(ydata)**2)),'r',label = 'theory sqaure')
    axs[1,0].plot(abs(xdata)**2/abs(max(abs(xdata)**2)),'b--',label = 'sim sqaure')

    # axs[0,0].plot(np.real(ydata),'r',label = 'theory real')
    # axs[0,0].plot(np.real(xdata),'b--',label = 'sim real')
    # axs[0,0].set_title('real part compare')
    # axs[0,1].plot(np.imag(ydata),'r',label = 'theory  imag')
    # axs[0,1].plot(np.imag(xdata),'b--',label = 'sim imag')
    # axs[0,1].set_title('imag part compare')
    # axs[1,0].plot(abs(ydata)**2,'r',label = 'theory   sqaure')
    # axs[1,0].plot(abs(xdata)**2,'b--',label = 'sim square')
    # axs[1,0].set_title('sqaure part compare')


    axs[0,0].legend(loc='best',fontsize=10,frameon=False)
    axs[0,1].legend(loc='best',fontsize=10,frameon=False)
    axs[1,0].legend(loc='best',fontsize=10,frameon=False)

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