#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Description:  Run batch model     
@Date       : 2021/09/02 17:13:04
@Author     : tanyuhang
@version    : 1.0
'''
import os
import sys
import time
import json
import subprocess
import numpy as np
import time
def main():

    xspec=read_xenergy('para/x_ray_spe_1mm_al.txt')
    periods = [8.0]
    t = time.time()
    # time.sleep(600)
    # for j in range(20):
    for i in range(len(xspec[0])):
        xenergy_ratio = xspec[1][i]
        xenergy = xspec[0][i]
        # if abs(xenergy-25)<1e-3:
        sep = 2.24
        print("nohup python3 talbot_withoutzp.py  %s %s %s > txt/period_%s_%s.txt&" %(xenergy,xenergy_ratio,sep,sep,int(t)) )
        runcmd("nohup python3 talbot_withoutzp.py  %s %s %s > txt/period_%s_%s.txt 2>&1 &" %(xenergy,xenergy_ratio,sep,sep,int(t)) )
    time.sleep(1)

def runcmd(command):
    ret = subprocess.run([command],shell=True)

def read_xenergy(dir_path_name):
    file_v = open(dir_path_name,'r')
    v_info = file_v.readlines()
    xenergy_list = [float(v_info[i].split('  ')[0]) for  i in range(len(v_info))]
    v_list_y = [float(v_info[i].split('  ')[1]) for  i in range(len(v_info))]
    xenergy_ratio = [v_list_y[i]/sum(v_list_y) for i in range(len(v_list_y))]
    return [xenergy_list,xenergy_ratio]

if __name__ == '__main__':
    main()