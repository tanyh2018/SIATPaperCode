import numpy as np
import sys
import os
#----------------------------------------
# Several useful function defined here
#----------------------------------------

def mat_delta_beta (material,xenergy):
    beta_list,delta_list = read_para(material.split('_')[0])
    for i in range(len(beta_list)):
        if(float_def(beta_list[i][0]) and float_def(delta_list[i][1])):
            if abs(float(beta_list[i][0])/1000. - xenergy) < 1e-6:    #kev
                if 'graphite' in material:
                    delta = float(delta_list[i][1])*0.52
                    beta = float(beta_list[i][1])
                else:
                    delta = float(delta_list[i][1])
                    beta = float(beta_list[i][1])
    if "pure_phase" in material:
        beta = 0.0      
    elif "pure_absor" in material:
        delta = 0.0 
    print("delta=%s,beta=%s"%(delta,beta))
    return delta,beta

def read_para(material):
    mater_name_pre = os.getcwd().replace('\\','/') + '/para/'
    mater_beta_file = mater_name_pre + material + '_beta_4_40.txt'
    mater_delta_file = mater_name_pre + material + '_delta_4_40.txt'

    beta_list = para_split(mater_beta_file)
    delta_list = para_split(mater_delta_file)
    return beta_list,delta_list

def para_split(mater_file):
    file_v = open(mater_file,'r')
    v_info = file_v.readlines()
    v_list = [v_info[i].split(' ')[:] for  i in range(len(v_info))]
    return v_list

def float_def(input):
    try:
        float(input)
        return True
    except Exception as exc:
        return False