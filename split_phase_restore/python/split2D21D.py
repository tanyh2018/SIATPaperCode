# change 2D profile to 1D profile: 2D means the split distance is larger with different pixels
import matplotlib.pyplot as plt 
import numpy as np
import os

def main():
    input_path = "/home/amax/Public/tanyh/V1/train_data/raw_20230613_1D_cuboid/"
    output_path = '/home/amax/Public/tanyh/V1/train_data/raw_20230613_1D_cuboid_data/'
    split_data_main(input_path,output_path)
    input_path = "/home/amax/Public/tanyh/V1/train_data/wrap_20230613_1D_cuboid/"
    output_path = '/home/amax/Public/tanyh/V1/train_data/wrap_20230613_1D_cuboid_data/'
    split_data_main(input_path,output_path)

def split_data_main(input_path,output_path):
    create_file_path(output_path)
    input_names = []
    output_path_names = []
    for file_name in os.listdir(input_path):
        input_names.append(input_path + file_name)
        output_path_names.append(output_path + file_name)
        split_data(output_path_names,input_names)

def split_data(output_path_names,input_names):
   for i in range(len(input_names)):
        print(input_names[i])
        raw_image = read_data_spc(input_names[i])
        nview = int(len(raw_image)/600)
        raw_image = raw_image.reshape(nview,600)
        for j in range(nview):
            out_file = ((output_path_names[i]).split('.raw')[0]) + '_shift_' + str(j) + '.raw'
            raw_image[j,:].tofile(out_file)
def read_data_spc(input_path):
      data_type = 'float32'
      raw_image = np.fromfile(input_path,data_type)
      return raw_image

def create_file_path(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)     

if __name__ == '__main__':
      main()