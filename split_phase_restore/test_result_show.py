# change 2D profile to 1D profile: 2D means the split distance is larger with different pixels
import matplotlib.pyplot as plt 
import numpy as np
import os
from config import *
def main():

    for file_name in os.listdir(pre_path):
        file_name = 'phase_5.66_45915_label_wrap.raw'
        pre_path_name = pre_path + file_name
        out_path_name = out_fig_path + file_name
        raw_path_name = wrap_path + 'raw_20230712_test/' + file_name
        wrap_path_name = wrap_path + '/wrap_20230712_test/' + file_name   
        read_data_spc(pre_path_name,raw_path_name,wrap_path_name,out_path_name)
        plt.show()

def print_path_file(path):
    i=0
    for file_name in os.listdir(path):
        if i < 5: 
            print(file_name)
            i = i + 1
    print("end")

def read_data_spc(input_path,ref_path,wrap_path,out_path_name):
    repeated_matrix = read_file(input_path)
    refs_matrix = read_file(ref_path)
    wraps_matrix = read_file(wrap_path)

    repeated_matrix_FBP = read_raw_file(input_path.replace('20230712_test','20230712_FBP'))
    refs_matrix_FBP = read_raw_file(ref_path.replace('20230712_test','20230712_FBP'))
    wraps_matrix_FBP = read_raw_file(wrap_path.replace('20230712_test','20230712_FBP'))

    out_path_name1 = out_path_name.replace('.raw','1.png')
    out_path_name2 = out_path_name.replace('.raw','2.png')
    out_path_name3 = out_path_name.replace('.raw','3.png')
    out_path_name4 = out_path_name.replace('.raw','4.png')

    fig, axs = plt.subplots(1,3,figsize=(9, 6))
    axs[1].imshow(repeated_matrix,cmap='gray')
    axs[1].set_title('Predict')
    axs[2].imshow(refs_matrix,cmap='gray')
    axs[2].set_title('Ref')
    axs[0].imshow(wraps_matrix,cmap='gray')
    axs[0].set_title('Wrap')
    plt.savefig(out_path_name1)
    sdex = 250

    fig, axs = plt.subplots(1,1,figsize=(9, 6))
    plt.plot(repeated_matrix[sdex,:],'#F38624',label='Deep-Learn')
    plt.plot(refs_matrix[sdex,:],'#3DACC4',label='Ref')
    plt.plot(wraps_matrix[sdex,:],'#595959',label='Wrap')
    plt.xlabel('Pixels')
    plt.ylabel('Phase')
    plt.legend(fontsize=15,frameon=False)
    plt.savefig(out_path_name2)

    fig, axs = plt.subplots(1,3,figsize=(9, 6))
    axs[1].imshow(repeated_matrix_FBP,cmap='gray',vmin=np.min(repeated_matrix_FBP)*0.8,vmax=np.max(repeated_matrix_FBP)*0.8)
    axs[1].set_title('Predict')
    axs[2].imshow(refs_matrix_FBP,cmap='gray',vmin=np.min(refs_matrix_FBP)*0.8,vmax=np.max(refs_matrix_FBP)*0.8)
    axs[2].set_title('Ref')
    axs[0].imshow(wraps_matrix_FBP,cmap='gray',vmin=np.min(wraps_matrix_FBP)*0.8,vmax=np.max(wraps_matrix_FBP)*0.8)
    axs[0].set_title('Wrap')
    plt.savefig(out_path_name3)

    fig, axs = plt.subplots(1,1,figsize=(9, 6))
    plt.plot(repeated_matrix_FBP[sdex,:],'#F38624',label='Deep-Learn')
    plt.plot(refs_matrix_FBP[sdex,:],'#3DACC4',label='Ref')
    plt.plot(wraps_matrix_FBP[sdex,:],'#595959',label='Wrap')
    plt.xlabel('Pixels')
    plt.ylabel('Phase')
    plt.legend(fontsize=15,frameon=False)
    plt.savefig(out_path_name4)

def create_file_path(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)  

def read_file(inputf):
    data_type = 'float32'
    raw_image = np.fromfile(inputf,data_type)
    raw_image = raw_image.reshape(720,600) 
    return raw_image

def read_raw_file(inputf):
    data_type = 'float32'
    raw_image = np.fromfile(inputf,data_type)
    raw_image = raw_image.reshape(pixels,pixels) 
    return raw_image

if __name__ == '__main__':
      main()