import numpy as np
import matplotlib.pyplot as plt 
from scipy.ndimage import gaussian_filter
from PIL import Image
import os

def mian():
    # 
    #extract_ps_main()
    G0G1()
    G0()
    noG()
    # Gs()    

##### extract phase step data #####

def extract_ps_main():
    tpath = "D:/xianjinyuan/工作内容/NanoCT/experiment/process_data/Gs/"
    Nstep=5
    data_dict = {'M0_s': [], 'M0_b': [], 'M6_b': [], 'M6_s': [], 'M12_s': [], 'M12_b': [], 'M18_s': [], 'M18_b': [], 'M24_s': [], 'M24_b': []}
    fnames = read_diraw(tpath)
    Nf = len(fnames)
    Ns = int(Nf/Nstep/2/2)
    Pstep = ["M0","M6","M12","M18","M24"]
    
    for i in range(len(fnames)):
        if  "diff" not in fnames[i]:
            if "sample" in fnames[i]:
                for ps in Pstep:
                    tname = ps + "_s"
                    if tname in fnames[i]:
                        data_dict[tname].append(fnames[i])
            else:
                for ps in Pstep:
                    tname = ps + "_b"
                    if tname in fnames[i]:
                        data_dict[tname].append(fnames[i])
    outp = "D:/xianjinyuan/工作内容/NanoCT/experiment/process_data/Gs/result/"

    m_sig = [[] for _ in range(Ns)]
    m_bkg = [[] for _ in range(Ns)]
    for condition, files in data_dict.items():
        for i in range(Ns):
            if "sample" in files[i]:
                m_sig[i].append(files[i])
            else:
                m_bkg[i].append(files[i])
    size=[2950,2950]
    
    for i in range(Ns):
        osig = []
        obkg = []
        for j in range(len(m_sig[0])):
            osig.append(read_data2(tpath + m_sig[i][j],size))
            obkg.append(read_data2(tpath + m_bkg[i][j],size))
        osig = np.array(osig)
        obkg = np.array(obkg)
        osig.astype(np.float32).tofile(outp+"sig"+str(i)+".raw")
        obkg.astype(np.float32).tofile(outp+"bkg"+str(i)+".raw")

##### data avg and minus dark #####
def G0G1():
    tpath = "D:/xianjinyuan/工作内容/NanoCT/experiment/4000s_gold_line_data/20240130_files/"
    i_sig_names = ["G0G1_0.5mmAl_sig"]
    i_bkg_names = ["G0G1_0.5mmAl_bkg"]
    outpath = "D:/xianjinyuan/工作内容/NanoCT/experiment/process_data/G0G1/"
    Ncom = 5
    save_data(tpath,i_sig_names,Ncom,outpath,'sig')
    save_data(tpath,i_bkg_names,Ncom,outpath,'bkg')

def G0():
    tpath = "D:/xianjinyuan/工作内容/NanoCT/experiment/4000s_gold_line_data/20240130_files/"
    i_sig_names = ["G0_1.0mmAl_sig"]
    i_bkg_names = ["G0_1.0mmAl_bkg"]
    outpath = "D:/xianjinyuan/工作内容/NanoCT/experiment/process_data/G0/"
    Ncom = 5
    save_data(tpath,i_sig_names,Ncom,outpath,'sig')
    save_data(tpath,i_bkg_names,Ncom,outpath,'bkg')

def noG():
    tpath = "D:/xianjinyuan/工作内容/NanoCT/experiment/4000s_gold_line_data/20240129_files/"
    i_sig_names = ["NoGrid_sample_1p5mmAl"]
    i_bkg_names = ["NoGrid_bkg_1p5mmAl"]
    outpath = "D:/xianjinyuan/工作内容/NanoCT/experiment/process_data/noG/"
    Ncom = 5
    save_data(tpath,i_sig_names,Ncom,outpath,'sig')
    save_data(tpath,i_bkg_names,Ncom,outpath,'bkg')

def Gs():
    ### 处理步进结果
    tpath = "D:/xianjinyuan/工作内容/NanoCT/experiment/4000s_gold_line_data/"
    i_sig_names = ["M0_sample","M6_sample","M12_sample","M18_sample","M24_sample"]
    i_bkg_names = ["M0_bkg","M6_bkg","M12_bkg","M18_bkg","M24_bkg"]
    outpath = "D:/xianjinyuan/工作内容/NanoCT/experiment/process_data/Gs/"
    Ncom = 5
    save_data(tpath,i_sig_names,Ncom,outpath,"sig")
    save_data(tpath,i_bkg_names,Ncom,outpath,"bkg")

def save_data(tpath,inames,Ncom,outpath,type):
    r1=[2450,350]
    r2=[5400,3300]
    rs = [r2[1]-r1[1],r2[0]-r1[0]]
    size = [6056,8464]
    fd = tpath + "AVG_dark_200s.tif"
    dark = read_tiff(fd,size)
    for i in range(len(inames)):
        ipath = tpath + inames[i]
        fnames = read_dir(ipath)
        dlength = int(len(fnames)/Ncom)
        for j in range(dlength*Ncom):
            if j%Ncom == 0:
                ods=np.zeros([Ncom,rs[0],rs[1]])
            od = read_tiff(ipath +  "/" +  fnames[j],size) - dark
            od = solve_nan(od)
            ods[j%Ncom,:,:] = od[r1[1]:r2[1],r1[0]:r2[0]]
            if j%Ncom == Ncom-1:
                dods = diff_data(ods)
                outp = outpath +"/"
                outn = inames[i]+str(j)+".raw"
                outn2 = inames[i]+str(j)+"_diff.raw"
                create_dir(outp)
                mods = np.sum(ods,axis=0)
                mods.astype(np.float32).tofile(outp + outn)
                dods.astype(np.float32).tofile(outp + outn2)
                print(outp + outn)

def create_dir(folder_path):
    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        # 如果不存在，则创建文件夹
        os.makedirs(folder_path)

def diff_data(ods):
    ###所有图减去第一张
    tmp = np.copy(ods)
    for i in range(1,len(ods)):
        tmp[i] = tmp[i] - tmp[0]
    return tmp

def solve_nan(data):
    mask = np.isnan(data)
    data[mask] = gaussian_filter(data,4.0)[mask]
    return data

def read_dir(path):
    fnames = []
    files = os.listdir(path)
    for fname in files:
        if ".tif" in fname:
            fnames.append(fname)
    return np.array(fnames)

def read_diraw(path):
    fnames = []
    files = os.listdir(path)
    for fname in files:
        if ".raw" in fname:
            fnames.append(fname)
    return np.array(fnames)

def read_tiff(path,size):
    image = Image.open(path)
    values = list(image.getdata())
    values = np.array(values)
    values = values.reshape(size)
    image.close()
    return  values
def read_data2(sino_path_name,size):
    with open(sino_path_name, 'rb') as fid_3:
        sino_2 = np.fromfile(fid_3, dtype=np.float32).reshape([size[0],size[1]])
    sino_2 = sino_2.astype(float)
    return sino_2
if __name__ == '__main__':
    mian()