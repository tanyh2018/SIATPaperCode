import numpy as np

#----------------------------------------
# Several useful function defined here
#----------------------------------------

def Delta_source(pos_x, pos_y, total_count, fs):
    source = np.zeros([int(total_count[0]),int(total_count[1])],dtype=complex)
    source[int(total_count[0]/2.+pos_y*fs[0]),int(total_count[1]/2.+pos_x*fs[1])] = (1.+0.*1j)
    return source

def gauss_source(pos_x,pos_y,sigma,total_count,fs):
    source = np.zeros([int(total_count[0]),int(total_count[1])],dtype=complex)
    x = np.linspace(float(total_count[1]/fs[1]*(-1)/2),float(total_count[1]/fs[1]/2),total_count[1])
    for i in range(int(total_count[1])):
        source[0][i]  = np.exp(-1*x[i]**2/(2.0*sigma**2))
    return source
def Delta_source2(pos_x, pos_y, total_count, fs):
    source = np.zeros([int(total_count[0]),int(total_count[1])],dtype=complex)
    source[int(total_count[0]/2.+pos_y*fs[0]),int(total_count[1]/2.+pos_x*fs[1])] = (1.+0.*1j)
    source[int(total_count[0]/2.+pos_y*fs[0]),int(total_count[1]/2.+pos_x*fs[1])+1] = (1.+0.*1j)
    return source

def GaussianAperture(total_count, diameter, width, area_length, x_shift, y_shift, fs):
    gaussaperture = np.ones([int(total_count),int(total_count)],dtype=complex)
    for i in range(int(diameter*fs)):
        for j in range(int(diameter*fs)):
            if (diameter*fs/2.-i)**2 + (diameter*fs/2.-j)**2 < (diameter*fs/2.)**2.:
                gaussaperture[int(area_length*fs/2.)+int(x_shift*fs)+i-int(diameter*fs/2.)][int(area_length*fs/2.)+int(y_shift*fs)+j-int(diameter*fs/2.)] = \
                1 - np.exp((-1)*((diameter/2.-i/fs)**2.+(diameter/2.-j/fs)**2.)/2/width/width)
                #-0.9*np.sqrt(0.01*((olength/2.)**2.-(olength/2.-i/fs)**2.-(olength/2.-j/fs)**2.)) + 0.05*1j*2*np.sqrt(0.01*((olength/2.)**2.-(olength/2.-i/fs)**2.-(olength/2.-j/fs)**2.))
    return gaussaperture

def Rect_source(total_count, pos, width,fs):
    source = np.zeros([int(total_count[0]),int(total_count[1])],dtype=complex)
    # for i in range(len(pos)):
    #     source[0][int(total_count[1]/2.  + pos[i]*fs[1])] = (1. + 0.*1j )
    # k=0
    for i in range(1):
        for j in range(int(width*fs[1])):
            # if (outlength*fs/2.-i)**2 + (outlength*fs/2.-j)**2 < (outlength*fs/2.)**2. and (outlength*fs/2.-i)**2 + (outlength*fs/2.-j)**2 > (ilength*fs/2.)**2.:
            source[0][int(total_count[1]/2. + j + pos*fs[1])] = (1. + 0.*1j ) #+ random() * np.pi/100. * 1j
    return source

def Rect_source_split(total_count,fs,pos_x):
    source = np.zeros([int(total_count[0]),int(total_count[1])],dtype=complex)
    # for i in range(len(pos)):
    #     source[0][int(total_count[1]/2.  + pos[i]*fs[1])] = (1. + 0.*1j )
    for i in range(len(pos_x)):
        source[0,int(total_count[1]/2.+pos_x[i]*fs[1])] = (1.+0.*1j)
    return source

def RingSource(total_count, pos, outlength, ilength, gap, fs):
    ringsource = np.zeros([int(total_count),int(total_count)],dtype=complex)
    for i in range(int(total_count/gap/fs)):
        index = i*gap*fs
        for j in range(int(total_count/gap/fs)):
            indexj = j*gap*fs
            if (outlength*fs/2.-index)**2 + (outlength*fs/2.-indexj)**2 < (outlength*fs/2.)**2. and (outlength*fs/2.-index)**2 + (outlength*fs/2.-indexj)**2 > (ilength*fs/2.)**2.:
                ringsource[int(total_count/2 + index + pos*fs - outlength/2.*fs)][int(total_count/2 + indexj + pos*fs - outlength/2.*fs)] = 1. + 0.*1j
    return ringsource

def Surface_source(total_count, pos, outlength, ilength, size, fs):
    source = np.ones([int(total_count),int(total_count)])
    for i in range(int(size*fs)):
        for j in range(int(size*fs)):
            if (outlength*fs/2.-i)**2 + (outlength*fs/2.-j)**2 < (outlength*fs/2.)**2. and (outlength*fs/2.-i)**2 + (outlength*fs/2.-j)**2 > (ilength*fs/2.)**2.:
                source[int(total_count/2 + i + pos*fs - outlength/2.*fs)][int(total_count/2 + j + pos*fs - outlength/2.*fs)] = 0.
    return source

def Surface_source1(total_count, pos, outlength, ilength, size, fs):
    source = np.zeros([int(total_count),int(total_count)],dtype=complex)
    for i in range(int(size*fs)):
        for j in range(int(size*fs)):
            if (outlength*fs/2.-i)**2 + (outlength*fs/2.-j)**2 < (outlength*fs/2.)**2. and (outlength*fs/2.-i)**2 + (outlength*fs/2.-j)**2 > (ilength*fs/2.)**2.:
                source[int(total_count/2 + i + pos*fs - outlength/2.*fs)][int(total_count/2 + j + pos*fs - outlength/2.*fs)] = 1. #+ random() * np.pi/100. * 1j
    return source

def GaussianSource(total_count, diameter, width, area_length, x_shift, y_shift, fs):
    gaussiansource = np.zeros([int(total_count),int(total_count)],dtype=complex)
    for i in range(int(diameter*fs)):
        for j in range(int(diameter*fs)):
            if (diameter*fs/2.-i)**2 + (diameter*fs/2.-j)**2 < (diameter*fs/2.)**2.:
                gaussiansource[int(area_length*fs/2.)+int(x_shift*fs)+i-int(diameter*fs/2.)][int(area_length*fs/2.)+int(y_shift*fs)+j-int(diameter*fs/2.)] = \
                np.exp((-1)*((diameter/2.-i/fs)**2.+(diameter/2.-j/fs)**2.)/2/width/width)
                #-0.9*np.sqrt(0.01*((olength/2.)**2.-(olength/2.-i/fs)**2.-(olength/2.-j/fs)**2.)) + 0.05*1j*2*np.sqrt(0.01*((olength/2.)**2.-(olength/2.-i/fs)**2.-(olength/2.-j/fs)**2.))
    return gaussiansource
