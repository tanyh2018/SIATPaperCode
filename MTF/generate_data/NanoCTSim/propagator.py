import numpy as np
from units import *
import scipy.signal
import scipy.ndimage
import matplotlib.pyplot as plt 
import sys
#----------------------------------------
# Several useful function defined here
#----------------------------------------

def Propag_index2d(wave_length, distance, grids):
    '''

    This function serves as a part of the calculation of the free space propagation.
    Different approximations are considered for the following three calculation methods.
    The uncommented one is the common paraxial method.

    ----------Parameters----------
    :type wave_length: int, float
    :param distance: propagation distance
    :type distance: int, float
    :return: output field (N x N square array of complex numbers).

    '''
    wave_number = 2.*np.pi/wave_length
    print('wave_number=',wave_number,'wave_length=',wave_length)
    #return 1./(1j*wave_length*distance)*np.exp(1j*wave_number*(grids/2./distance + distance))
    return 1./(1j*wave_length*np.sqrt(distance**2.+grids))*np.exp(1j*wave_number*np.sqrt(distance**2.+grids))
    #return 1./np.sqrt(1j*wave_length*np.sqrt(distance**2.+grids))*np.exp(1j*wave_number*np.sqrt(distance**2.+grids))

def Propagation2d(Fin, distance, wave_length, grids):
    ''' two FFT'''
    F_origi = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(Fin)))
    F_index = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(Propag_index2d(wave_length, distance, grids))))
    Fout =  np.sqrt(1/wave_length/distance) * np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(F_origi*F_index)))
    draw_input_ria(F_origi)
    plt.show()
    sys.exit()
    return Fout
def draw_input_ria(input):
    fig, axs = plt.subplots(1,3,figsize=(9, 6))
    n  = int(len(input)/2.0)
    axs[0].plot(np.real(input[n]))
    axs[1].plot(np.imag(input[n]))
    axs[2].plot(abs(input[n])**2)

def Propagation_dfft(Fin, distance, l,wave_length,dx):
    ''' one FFT Angular Spectrum Transfer Function Method 
    ref:Common Diffraction Integral Calculation Based on a Fast Fourier Transform Algorithm'''
    wave_number = 2.*np.pi/wave_length
    N0 = len(Fin[0])
    x = np.linspace(-1/2.,1/2.,N0)/dx
    F_index = np.exp(1j*wave_number*distance*np.sqrt(1 - (wave_length*x)**2))
    F_origi = np.fft.fft(np.fft.fftshift(Fin[0]))
    F_index = np.fft.fftshift(F_index)
    Fout =  np.fft.fftshift(np.fft.ifft(F_origi*F_index))
    Fout = np.array([Fout])
    return Fout

def Propagation_point_source(pos_x,distance,total_count,total_length,wave_length):
    ''' Point source propogate '''
    print("pos_x=",pos_x)
    wave_number = 2.*np.pi/wave_length
    x = np.linspace(-total_length[1]/2.,total_length[1]/2.,total_count[1])
    Fout = 1.0*np.exp(1.j*wave_number*(distance + (x-pos_x)**2/2./distance))/(np.sqrt(1.j*distance*wave_length))
    return np.array([Fout])

def Propagation2d_scipy_convolve(Fin, distance,l, wave_length, grids):
    ''' convolve propogation'''
    F_index = Propag_index2d(wave_length, distance, grids)
    Fout =   scipy.signal.fftconvolve(Fin,F_index,mode='same')
    return Fout
    