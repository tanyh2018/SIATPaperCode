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
    # time.sleep(30000)
    dir_paths = '/data4/tanyuhang/data/talbot_result/20240522_graphite/'
    dir_path_prexs = os.listdir(dir_paths)
    print(len(dir_path_prexs))
    for i in range(len(dir_path_prexs)):
        runcmd("nohup python3 draw_data.py  %s &" %(dir_path_prexs[i]) )

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