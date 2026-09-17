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
    input_path = '/data4/tanyuhang/data/talbot_result/graphite_sd/20221212_graphite/'
    out_path = '/data4/tanyuhang/data/talbot_result/graphite_sd/20221212_graphite_raw/mono_30/'
    file_name_list = os.listdir(input_path)
    for i in range(len(file_name_list)):
        path = input_path + file_name_list[i] + '/'
        file_name_list2 = os.listdir(path)
        for j in range(len(file_name_list2)):
            if 'mono.raw' in file_name_list2[j] and 'raw' in file_name_list2[j]:
                in_path = path + file_name_list2[j]
                runcmd('cp ' + in_path + ' ' + out_path )

def runcmd(command):
    ret = subprocess.run([command],shell=True)

if __name__ == '__main__':
    main()