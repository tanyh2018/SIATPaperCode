import numpy as np
import matplotlib.pyplot as plt 
#----------------------------------------
# Several useful function defined here
#----------------------------------------

def Cal_Resolution(focus, zpradius, wave_length):
    res = 1.22 * focus * wave_length / 4. / (zpradius * 2./4.) 
    return res

def Phi_info(phi_prj, phi_bkg, total_count):
    phi_final = phi_prj-phi_bkg
    for ik in range(1):
        for jk in range(total_count):
            if phi_final[ik,jk] > np.pi/2.:
                phi_final[ik,jk] = phi_final[ik,jk]-np.pi
            elif phi_final[ik,jk] < -np.pi/2.:
                phi_final[ik,jk] = phi_final[ik,jk]+np.pi
    return phi_final

def Sep_Cal(wave_length, distance3, period,amp):
    return 2*wave_length*distance3/period

def result_info(fin_obj, fin_bkg):
    obj_phi = np.angle(fin_obj[1,:])
    bkg_phi = np.angle(fin_bkg[1,:])
    phi_final = obj_phi - bkg_phi
    phi_final = (phi_final + np.pi)%(2.*np.pi) - np.pi
    obj_absor = fin_obj[0,:]    
    bkg_absor = fin_bkg[0,:]
    absor_final = -np.log(obj_absor/bkg_absor)
    return phi_final,np.real(absor_final)

