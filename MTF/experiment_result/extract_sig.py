import numpy as np
import matplotlib.pyplot as plt 
from scipy.ndimage import gaussian_filter
import os
# from skimage.measure import block_reduce

def mian():
    
    #gold_line_4000s()
    gold_line_G("G0G1")
    gold_line_G("G0")
    gold_line_G("noG")

def gold_line_4000s():
    path = "D:/xianjinyuan/工作内容/NanoCT/experiment/process_data/Gs/result/" 
    nstr = "3"
    sig_path = path + "/sig" + nstr + ".raw"
    bkg_path = path + "/bkg"+ nstr +".raw"

    size = [2950,2950]
    numsteps=5
    sig_data = read_data2(sig_path,size,numsteps)
    bkg_data = read_data2(bkg_path,size,numsteps)

    sig_data = paintimg(sig_data,0,'xiaoyu',numsteps)
    bkg_data = paintimg(bkg_data,0,'xiaoyu',numsteps)

    sig_data = paintimg(sig_data,2000,'dayu',numsteps)
    bkg_data = paintimg(bkg_data,2000,'dayu',numsteps)

    sig_data,sig_diff = diffpainting(sig_data,8000,numsteps)
    bkg_data,bkg_diff = diffpainting(bkg_data,8000,numsteps)

    phi_final,absor_final,normalizedDark = fft_result(sig_data,bkg_data)

    opath = "D:/xianjinyuan/工作内容/NanoCT/experiment/result/Gs/"
    create_dir(opath)
    sig_data.astype(np.float32).tofile(opath +"sig" + nstr + ".raw")
    bkg_data.astype(np.float32).tofile(opath+"bkg" + nstr + ".raw")
    sig_diff.astype(np.float32).tofile(opath+"diff_sig" + nstr + ".raw")
    bkg_diff.astype(np.float32).tofile(opath+"diff_bkg" + nstr + ".raw")
    phi_final.astype(np.float32).tofile(opath+"phi" + nstr + ".raw")
    absor_final.astype(np.float32).tofile(opath+"absor" + nstr + ".raw")
    normalizedDark[np.abs(normalizedDark)>100] = 0
    normalizedDark.astype(np.float32).tofile(opath+"Dark" + nstr + ".raw")

def gold_line_G(fname):
    path = "D:/xianjinyuan/工作内容/NanoCT/experiment/process_data/" + fname
    if fname == "G0G1":
        sig_path = path + "/G0G1_0.5mmAl_sig4.raw"
        bkg_path = path + "/G0G1_0.5mmAl_bkg4.raw"
        dn = 3000
    elif fname == "G0":
        sig_path = path + "/G0_1.0mmAl_sig4.raw"
        bkg_path = path + "/G0_1.0mmAl_bkg4.raw"
        dn = 3000
    elif fname == "noG":
        sig_path = path + "/NoGrid_sample_1p5mmAl4.raw"
        bkg_path = path + "/NoGrid_bkg_1p5mmAl4.raw"
        dn = 6000
    size = [2950,2950]
    numsteps=1
    sig_data = read_data2(sig_path,size,numsteps)
    bkg_data = read_data2(bkg_path,size,numsteps)

    sig_data = paintimg(sig_data,0,'xiaoyu',numsteps)
    bkg_data = paintimg(bkg_data,0,'xiaoyu',numsteps)

    # sig_data = paintimg(sig_data,dn,'dayu',numsteps)
    # bkg_data = paintimg(bkg_data,dn,'dayu',numsteps)

    sig_data,sig_diff = diffpainting(sig_data,100000,numsteps)
    bkg_data,bkg_diff = diffpainting(bkg_data,100000,numsteps)
    absor_final = - np.log(sig_data/bkg_data)
    opath = "D:/xianjinyuan/工作内容/NanoCT/experiment/result/" + fname + "/"
    create_dir(opath)
    sig_data.astype(np.float32).tofile(opath +"sig.raw")
    bkg_data.astype(np.float32).tofile(opath+"bkg.raw")
    # sig_diff.astype(np.float32).tofile(opath+"diff_sig.raw")
    # bkg_diff.astype(np.float32).tofile(opath+"diff_bkg.raw")

    absor_final.astype(np.float32).tofile(opath+"absor.raw")

    # phi_final,absor_final,normalizedDark = fft_result(sig_data,bkg_data)

    # opath = "./result/" + fname + "/"
    # sig_data.astype(np.float32).tofile(opath +"sig_2950_2950.raw")
    # bkg_data.astype(np.float32).tofile(opath+"bkg.raw")
    # sig_diff.astype(np.float32).tofile(opath+"diff_sig.raw")
    # bkg_diff.astype(np.float32).tofile(opath+"diff_bkg.raw")
    # phi_final.astype(np.float32).tofile(opath+"phi.raw")
    # absor_final.astype(np.float32).tofile(opath+"absor.raw")
    # normalizedDark[np.abs(normalizedDark)>100] = 0
    # normalizedDark.astype(np.float32).tofile(opath+"Dark.raw")

def gold_line_4000s_nograte():
    path = "./4000s_gold_line_data/result"
    name = "G0G1_0.5mmAl_2810_2810"
    # sig_path = path + "/G0_1.0mmAl_sig_2810_2810.raw"
    # bkg_path = path + "/G0_1.0mmAl_bkg_2810_2810.raw"

    sig_path = path + "/G0G1_0.5mmAl_sig_2810_2810.raw"
    bkg_path = path + "/G0G1_0.5mmAl_bkg_2810_2810.raw"

    size = [2810,2810]
    numsteps=1
    sig_data = read_data2(sig_path,size,numsteps)
    bkg_data = read_data2(bkg_path,size,numsteps)

    sig_data = paintimg(sig_data,0,'xiaoyu',numsteps)
    bkg_data = paintimg(bkg_data,0,'xiaoyu',numsteps)

    # sig_data = paintimg(sig_data,500,'xiaoyu',numsteps)
    # bkg_data = paintimg(bkg_data,500,'xiaoyu',numsteps)

    # # sig_data = paintimg(sig_data,1000,'xiaoyu',numsteps)
    # # bkg_data = paintimg(bkg_data,1000,'xiaoyu',numsteps)

    sig_data = paintimg(sig_data,4000,'dayu',numsteps)
    bkg_data = paintimg(bkg_data,4000,'dayu',numsteps)

    sig_data,sig_diff = diffpainting(sig_data,3000,numsteps)
    bkg_data,bkg_diff = diffpainting(bkg_data,3000,numsteps)
    #phi_final,absor_final,normalizedDark = fft_result(sig_data,bkg_data)

    opath = "./4000s_gold_line_result_5step/"
    absor_final = - np.log(sig_data/bkg_data)
    sig_data.astype(np.float32).tofile(opath +"sig_"+name+".raw")
    bkg_data.astype(np.float32).tofile(opath+"bkg_"+name+".raw")
    sig_diff.astype(np.float32).tofile(opath+"diff_"+name+".raw")
    bkg_diff.astype(np.float32).tofile(opath+"diff_"+name+".raw")

    absor_final.astype(np.float32).tofile(opath+"absor_"+name+".raw")


def paintimg(data,value,itype,numsteps):
    for i in range(numsteps):
        tmp = data[i,:,:]
        tmp=solve_nan(tmp)
        if itype == 'dayu':
            mask = tmp > value
        else:
            mask = tmp <= value
        tmp[mask] = gaussian_filter(tmp, 1.0)[mask]
        data[i,:,:]=tmp
    return data

def solve_nan(data):
    mask = np.isnan(data)
    data[mask] = gaussian_filter(data,1.0)[mask]
    return data
def diffpainting(data,value,numsteps):
    data_diff = np.zeros_like(data)
    for i in range(numsteps):
        tmp = data[i,:,:]
        diff = np.roll(tmp,3,axis=1)-tmp
        mask = np.abs(diff) > value
        tmp[mask] = gaussian_filter(tmp,1.0)[mask]
        diff = np.roll(tmp,3,axis=1)-tmp
        data[i,:,:]=tmp
        data_diff[i,:,:] = diff
    return data,data_diff

def fft_result(sdata,bgdata):
    FTout_obj =  get_phi_with_fft(sdata)
    FTout_bkg =  get_phi_with_fft(bgdata)
    phi_final,absor_final,normalizedDark = result_info(FTout_obj,FTout_bkg)
    return phi_final,absor_final,normalizedDark

def get_phi_with_fft(input_datas):
    input_datas = np.array(input_datas)
    FTout = np.fft.fft(input_datas,int(len(input_datas)),0)
    return FTout

def result_info(fin_obj, fin_bkg):
    obj_phi = np.angle(fin_obj[1,:])
    bkg_phi = np.angle(fin_bkg[1,:])
    eps = 1e-10
    phi_final = obj_phi - bkg_phi
    phi_final = (phi_final + np.pi)%(2.*np.pi) - np.pi
    obj_absor = fin_obj[0,:]    
    bkg_absor = fin_bkg[0,:]
    absor_final = -np.log(obj_absor/(bkg_absor+eps))
    epsilon_bkg = 2*np.abs(fin_bkg[1,:])/(fin_bkg[0,:]+eps)
    epsilon_obj = 2*np.abs(fin_obj[1,:])/(fin_obj[0,:]+eps)
    normalizedDark = -np.log(epsilon_obj/(epsilon_bkg+eps))
    return phi_final,np.real(absor_final),np.real(normalizedDark)
def create_dir(folder_path):
    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        # 如果不存在，则创建文件夹
        os.makedirs(folder_path)
def read_data2(sino_path_name,size,numsteps):
    with open(sino_path_name, 'rb') as fid_3:
        sino_2 = np.fromfile(fid_3, dtype=np.float32).reshape([numsteps,size[0],size[1]])
    sino_2 = sino_2.astype(float)
    return sino_2
if __name__ == '__main__':
    mian()