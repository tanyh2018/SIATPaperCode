import numpy as np
import os
from config import *
import sys
import matplotlib.pyplot as plt 

# from skimage.measure import block_reduce

def mian():
    input = '/data/tanyh/twin_img_AL/twin_data/twin_sino_check/phase_3.14_93211_label_twin.raw'
    output = '/data/tanyh/twin_img_AL/twin_data/manual_result/phase_3.14_93211_label_twin.raw'
    split_phase_restore_process(input,output)

def split_phase_restore_process(input,output):
    with open(input, 'rb') as fid_3:
        data = np.fromfile(fid_3, dtype=np.float32).reshape([rotate_num,detector_num])

    phase = data
    priors = split_restore_1D(data)
    # priors[:,-N_shift:-1] = 0
    A_sum = construct_A_sum()
    priors = iteration(phase,priors,A_sum)

    priors.astype(np.float32).tofile(output)

def split_restore_1D(phase):
    N_s = N_shift
    prior = np.zeros_like(phase)
    for j in range(N_s):
        prior[:,j] = 0

    for j in range(N_s, 2*N_s):
        prior[:,j] = -phase[:,j-N_s]

    for j in range(2*N_s, 600):
        prior[:,j] = prior[:,j-2*N_s] - phase[:,j-N_s]
    return prior

def construct_A_sum():
    N = detector_num
    N_s = N_shift
    A_1 = np.zeros((N, N))
    A_2 = np.zeros((N, N))
    A_1[N_s:, :N-N_s] = np.eye(N-N_s)
    A_2[:N-N_s, N_s:] = -np.eye(N-N_s)
    A_sum = A_1 + A_2
    for i in range(N):
        for j in range(N):
            if i==j and A_sum[i][j]!=0:
                A_sum[i][j] = 1e-8
    return A_sum

def iteration(phase,prior,A_sum):
    #
    nx = rotate_num
    ny = detector_num
    I = prior
    A = A_sum
    phase_T = phase.T
    A_inv = np.linalg.pinv(A)
    a = 1e-12
    beta = 0.2
    dt = 1
    tau = 1e-3
    iter = 80
    for i in range(iter):
        g = A_inv @ (A @ I.T - phase_T)
        Is1It = np.vstack((I[nx-1, :].reshape(1, -1), I[0:nx-1, :]))
        Isn1It = np.vstack((I[1:nx, :], I[0, :].reshape(1,-1)))
        I_f = np.vstack((I[nx-1, :].reshape(1, -1), I[0:nx-1, :])) - I
        I_b = I - Is1It
        I_u = I - np.hstack((I[:, ny-1].reshape(-1, 1), I[:, 0:ny-1]))
        I_d = np.hstack((I[:, 1:ny], I[:, 0].reshape(-1, 1))) - I

        I_x_1 = np.vstack((I[nx-1, :].reshape(1, -1), I[0:nx-1, :])) - np.hstack((Is1It[:, ny-1].reshape(-1, 1), Is1It[:, 0:ny-1]))
        I_y_1 = np.hstack((I[:, 1:ny], I[:, 0].reshape(-1,1))) - np.hstack((Isn1It[:, 1:ny], Isn1It[:, 0].reshape(-1, 1)))

        den1 = (a + I_b ** 2 + I_u ** 2) ** 0.5
        den2 = (a + I_f ** 2 + I_x_1 ** 2) ** 0.5
        den3 = (a + I_d ** 2 + I_y_1 ** 2) ** 0.5

        v = (I_b + I_u) / den1 - I_f / den2 - I_d / den3
        norm = np.sqrt(np.sum(v ** 2))
        v = v / norm
        u = tau * g.T + beta * dt * v
        I = I - u

    return I

# def get_test_part():
#     with open(path_Zero_Phase_one_image_fine, 'rb') as fid_3:
#         priors = np.fromfile(fid_3, dtype=np.float32).reshape([Views,NumDetx,NumDety]) 
#     data = priors[:,450:452,:]
#     data.astype(np.float32).tofile(path_Zero_Phase_one_image_fine.split('.raw')[0]+'test_part.raw')
# def Phase_change2_Dark():
#     with open(path_Zero_Phase_one_image_fine, 'rb') as fid_3:
#         data1 = np.fromfile(fid_3, dtype=np.float32).reshape([Views,1000,920]) 
#     # with open(path_Dark_minus_noise, 'rb') as fid_3:
#     #     data2 = np.fromfile(fid_3, dtype=np.float32).reshape([Views,NumDet,NumDet]) 
#     # data2[np.isnan(data2)] = 0
#     # data2[data2<-10] = 0
#     # data2[data2>10] = 0
#     data = np.zeros([Views,NumDet,NumDet])
#     data[:,:1000,:920] = data1
#     datal = np.roll(data,N_shift,axis=2)
#     datar = np.roll(data,-N_shift,axis=2)
#     datat = np.abs(data - datal*0.5 - datar*0.5)
#     # data[0,:1000,:920] = data1[0]
#     # datal = np.roll(data,N_shift,axis=2)
#     # datar = np.roll(data,-N_shift,axis=2)
#     # datat = np.abs(data - datal*0.5*0.494 - datar*0.5*0.494)
#     # tools.draw_2D_fig(datat[0])
#     # tools.draw_2D_fig(data2[0])
#     datat.astype(np.float32).tofile(path_Dark_test)
#     plt.show()

# def Phase_change2_Dark_test():
#     with open(path_Zero_Phase_one_image_fine, 'rb') as fid_3:
#         data1 = np.fromfile(fid_3, dtype=np.float32).reshape([Views,1000,920]) 
#     with open(path_Dark_minus_noise, 'rb') as fid_3:
#         data2 = np.fromfile(fid_3, dtype=np.float32).reshape([Views,NumDet,NumDet]) 
#     data2[np.isnan(data2)] = 0
#     data2[data2<-10] = 0
#     data2[data2>10] = 0
#     data = np.zeros([1,NumDet,NumDet])
#     data[:,:1000,:920] = data1[0]
#     datal = np.roll(data,N_shift,axis=2)
#     datar = np.roll(data,-N_shift,axis=2)
#     #datat = np.abs(data - datal*0.5*0.494 - datar*0.5*0.494)
#     datat = data - datal*0.5*0.494 - datar*0.5*0.494 + 2*(datal*0.5*0.494 + datar*0.5*0.494)
#     # data[0,:1000,:920] = data1[0]
#     # datal = np.roll(data,N_shift,axis=2)
#     # datar = np.roll(data,-N_shift,axis=2)
#     # datat = np.abs(data - datal*0.22 - datar*0.22)*2
#     tools.draw_1D_fig(np.mean(datat[0,460:480,:],axis=0))
#     tools.draw_1D_fig(np.mean(data2[0,460:480,:],axis=0))
#     datat.astype(np.float32).tofile(path_Dark_test)
#     plt.show()

# def Atten_remove_streaks():
#     with open(path_A_raw, 'rb') as fid_3:
#         Adata = np.fromfile(fid_3, dtype=np.float32).reshape([Views,NumDet,NumDet])  

#     Adata[np.isnan(Adata)] = 0
#     Adata[Adata<-10] = 0
#     outfile = './fig/Atten/streaks/'
#     os.makedirs(outfile, exist_ok=True)
#     x = np.array(np.linspace(0, NumDet-1, NumDet))
#     for i in range(Views):
#         print("Views=",i)
#         tmpdata = np.mean(Adata[i,:,::-1],axis=0)
#         p0 = [-1.7e-2,8.65e-3,3.643,2.28e-3]
#         y,y_pre,popt = tools.fit_data(x,tmpdata,'Sin',p0)
#         Adata[i,:,::-1] -= y_pre
#         plt.savefig(outfile + 'Views_'+str(i)+'_sreaks.png')
#         # plt.show()
#         plt.close()
#     Adata.astype(np.float32).tofile(path_Atten_remove_streaks)


# def phase_fine_tuning():
#     with open(path_Zero_Phase_one_image_zeroside, 'rb') as fid_3:
#         priors = np.fromfile(fid_3, dtype=np.float32).reshape([Views,NumDetx,NumDety])    
#     priors[priors>=0] = 0
#     priors = np.abs(priors)
#     import scipy
#     priors= scipy.ndimage.gaussian_filter(priors,sigma=1.0)
#     priors.astype(np.float32).tofile(path_Zero_Phase_one_image_fine)

# def remove_Phase_streaks():
#     data = read_data(path_Phase_raw)
#     data[np.isnan(data)] = 0
#     outfile = './fig/Phase/streaks/'
#     os.makedirs(outfile, exist_ok=True)
#     x = np.array(np.linspace(0, NumDetx-1, NumDety))
#     for i in range(Views):
#         print("Views=",i)
#         tmpdata = np.mean(data[i,:,:],axis=0)
#         p0 = [-9e-3,0.0176,3.338,7.38e-4]
#         y,y_pre,popt = tools.fit_data(x,tmpdata,'Sin',p0)
#         data[i,:,:] -= y_pre
#         tools.draw_fit_data2(x, tmpdata, y_pre)
#         plt.savefig(outfile + 'Views_'+str(i)+'_sreaks.png')
#         # plt.show()
#         plt.close()
#     data.astype(np.float32).tofile(path_Phase_remove_streaks)
#     return data

# def minux_Phase_noise():
#     data = read_data(path_Phase_remove_streaks)
#     data[np.isnan(data)] = 0
#     for i in range(Views):
#         # Fit method minus noise
#         noise = data[i, 980:1000, 40:990].flatten().tolist()
#         x,y,y_pre,popt = tools.fit_histrogram(noise,(-0.2,1.0),'gauss')
#         print('Views=',i,',mean=',popt[1])
#         data[i,:,:] -= popt[1]
#         mnoise = ((data[i,980:1000, 40:990]).mean(0)).mean(0)
#         data[i,:,:] -= mnoise
#         print('mnoise=',mnoise)
#         # tools.draw_fit_data2(x,y,y_pre)
#     data.astype(np.float32).tofile(path_Phase_minus_noise)

# def remove_break_point_inpaint():
#     data = read_data(path_Phase_remove_streaks)
#     data_diff = np.zeros_like(data)
#     # for i in range
#     for i in range(Views):
#         print("Views=",i)
#         datat = data[i]
#         # 创建掩膜
#         threshold = 1.5
#         threshold_diff = 0.25
#         sigma = 10
#         sigma_diff = 10
#         # 根据两边的值平滑异常值
#         smoothed_data = datat.copy()
#         mask = np.abs(datat) > threshold
#         smoothed_data[mask] = gaussian_filter(datat, sigma)[mask]
#         smoothed_data = mask_diff_gauss(smoothed_data,threshold_diff,sigma_diff)
#         smoothed_data = mask_diff_gauss(smoothed_data,threshold_diff,sigma_diff)
#         smoothed_data = mask_diff_gauss(smoothed_data,threshold_diff,sigma_diff)
#         smoothed_data = mask_diff_gauss(smoothed_data,threshold_diff,sigma_diff)
#         data[i] = smoothed_data
#         data_diff[i] = smoothed_data - np.roll(smoothed_data, 1, axis=1)
#     data.astype(np.float32).tofile(path_Phase_break_inpaint)
#     data_diff.astype(np.float32).tofile(path_Phase_break_inpaint_diff)
#     # plt.show()

# def mask_value_gauss2(datat,threshold,sigma):
#     smoothed_data = datat.copy()
#     mask = datat > threshold
#     smoothed_data[mask] = gaussian_filter(datat, sigma)[mask]
#     return smoothed_data

# def mask_value_gauss(datat,threshold_diff,sigma,r1,r2,diff):
#     smoothed_data = datat.copy()
#     mask = np.abs(diff)<0
#     mask[r1:r2,:] = np.abs(diff[r1:r2,:]) > threshold_diff
#     smoothed_data[mask] = gaussian_filter(datat, sigma)[mask]
#     return smoothed_data

# def mask_diff_gauss(smoothed_data,threshold_diff,sigma_diff):
#     diff = np.abs(smoothed_data - np.roll(smoothed_data, 1, axis=1))
#     mask = diff > threshold_diff
#     data_smoothed_diff = smoothed_data.copy()
#     data_smoothed_diff[mask] = gaussian_filter(data_smoothed_diff, sigma_diff)[mask]
#     return data_smoothed_diff

# def partial_differential():
#     sino_path = '/data/tanyh/momose_twin/data/diff_remove_streaks.raw'
#     with open(sino_path, 'rb') as fid_3:
#         data = np.fromfile(fid_3, dtype=np.float32).reshape([Views,NumDet,NumDetsub])

#     data = diff_roll(data)
#     diff = data - np.roll(data[:,:,:], 1, axis=2)
#     diff.astype(np.float32).tofile('./data/diff_partial_diff.raw')
#     data.astype(np.float32).tofile('./data/Remove_dead_pixels.raw')

# def diff_roll(data):
#     data[:,0,:] = 0
#     max_value = 100
#     data[np.abs(data)>1.4] = 0
#     while max_value > 0.6:
#         diff = np.abs(data - np.roll(data[:,:,:], 1, axis=2))
#         mask = diff > 0.45
#         data[mask] = (np.roll(data, shift=1, axis=2)[mask] + np.roll(data, shift=-1, axis=2)[mask]) / 2.0
#         max_value = np.max(diff)
#         print(max_value)
#     return data

# def remove_Dark_streaks():
#     data = read_data(sino_path_name)
#     data[np.isnan(data)] = 0
#     outfile = './fig/Dark/streaks/'
#     os.makedirs(outfile, exist_ok=True)
#     x = np.array(np.linspace(0, NumDetsub-1, NumDetsub))
#     for i in range(Views):
#         tmpdata = np.mean(data[i,:,:],axis=0)
#         y,y_pre,popt = tools.fit_data(x,tmpdata,'Sin')
#         data[i,:,:] -= y_pre
#         tools.draw_fit_data2(x, tmpdata, y_pre)
#         plt.savefig(outfile + 'Views_'+str(i)+'_sreaks.png')
#         plt.show()
#         plt.close()
#     data.astype(np.float32).tofile('./data/Dark/diff_remove_Dark_streaks.raw')
#     return data
#     # plt.show()
# # 定义理想的正弦函数
# def ideal_sine(x, amplitude, frequency, phase,a):
#     return amplitude * np.sin(2 * np.pi * frequency * x + phase) + a

# # 定义拟合函数
# def fit_func(x, amplitude, frequency, phase,a):
#     return ideal_sine(x, amplitude, frequency, phase,a)


# def mian_process(path_name,name_out):
#     A_sum = construct_A_sum()
#     # for i in range(NumDet):
#     #     phase = ((read_data(path_name))[:,i,:]).reshape([Views,NumDet])
#     #     prior = split_restore(phase)
#     phase = (read_data2(path_name)).reshape([Views,NumDet])
#     prior = split_restore(phase)
#     prior.astype(np.float32).tofile('register_667_' + name_out + '_0629_2D.raw')
#     # iter_phase = iteration(phase,prior,A_sum)
#     # result = FBP_process(iter_phase)      
#     # # phase = np.flip(phase, axis=1)
#     # # # phase_j = phase[0]
#     # # reshaped_matrix = block_reduce(phase, (2, 2), np.mean)
#     # # result = FBP_process(prior)
#     # result[result < -100] = 0
#     # tools.draw_twoD_figure(iter_phase)
#     # # tools.draw_twoD_figure(prior)
#     # prior.astype(np.float32).tofile('test_' + name_out + '_.raw')
#     # iter_phase = iteration(phase,prior,A_sum)
#     # result = FBP_process(iter_phase)
#     # result[result < -100] = 0
#     # tools.draw_twoD_figure(result)
#     # result.astype(np.float32).tofile('test_' + name_out + '_.raw')

# def minux_Dark_noise():
#     data = read_data(path_Dark_raw)
#     data[np.isnan(data)] = 0
#     for i in range(Views):
#         # Fit method minus noise
#         noise = data[i, 40:990, 980:1000].flatten().tolist()
#         x,y,y_pre,popt = tools.fit_histrogram(noise,(-0.3,0.3),'gauss')
#         print('Views=',i,',mean=',popt[1])
#         data[i,:,:] -= popt[1]
#         # Mean method minus noise
#         mnoise = ((data[i,40:990,980:1000]).mean(0)).mean(0)
#         data[i,:,:] -= mnoise
#     data.astype(np.float32).tofile(path_Dark_minus_noise)

# def minux_Phase_noise2():
#     data = read_data(path_Phase_remove_streaks)
#     for i in range(Views):
#         # Fit method minus noise
#         noise = data[i, 980:1000, 40:990].flatten().tolist()
#         print(noise)
#         x,y,y_pre,popt = tools.fit_histrogram(noise,(-0.3,0.3),'gauss')
#         print('Views=',i,',mean=',popt[1])
#         data[i,:,:] -= popt[1]
#         mnoise = ((data[i,980:1000, 40:990]).mean(0)).mean(0)
#         data[i,:,:] -= mnoise
#         tools.draw_fit_data2(x,y,y_pre)
#         plt.show()
#     data.astype(np.float32).tofile(path_Phase_minus_noise2)

# def minux_noise_process(path_name,name_out):
#     # A_sum = construct_A_sum()
#     # priors = np.zeros([Views,NumDet,NumDet])
#     data = read_data(path_name)
#     data = minus_noise(data)
#     # for i in range(NumDet):
#     #     print(i)
#     #     phase = (data[:,i,:]).reshape([Views,NumDet])
#     #     prior = split_restore(phase)
#     #     priors[:, i, :] = np.tile(prior, (1, 1, 1))
#     # tools.draw_twoD_figure(priors[:,90,:])
#     # priors.astype(np.float32).tofile('test_' + name_out + '_.raw')
# def Zero_Phase_both_sides(model):
#     data = read_data(path_Phase_break_inpaint)
#     data = data[:,:NumDety,:NumDety]
#     avern = 10
#     ny = int(data.shape[1] / avern)
#     data_mean = data[:, :ny*avern, :].reshape((Views, ny, avern, NumDety)).mean(axis=2)
#     rxmin = np.zeros((Views,ny))
#     rxmax = np.zeros((Views,ny))

#     for i in range(Views):
#         print("views:",i)
#         for j in range(ny):
#             dt = data_mean[i,j,:]
#             if (j>=26 and j<42) or (j<=63 and j>50):
#                 offset = 20
#             elif j>=40 and j<=50:
#                 offset = 30
#             else:
#                 offset = 60
#             if np.max(dt) > 0.16:
#                 max_i = p_max_threshold(dt)
#                 min_i = p_min_threshold(dt)
#                 data[i,j*avern:j*avern+avern,:max_i-offset] = 0
#                 data[i,j*avern:j*avern+avern,min_i+offset:] = 0
#                 rxi,rxa = merge_img_range(min_i,max_i)
#                 rxmin[i][j] = rxi - offset/2.0
#                 rxmax[i][j] = rxa + offset/2.0
#             else:
#                 rxmin[i][j] = 1
#                 rxmax[i][j] = 979                
#     # Lower part noise correction
#     rxmin2 = np.zeros(Views)
#     rxmax2 = np.zeros(Views)
#     data_mean = np.mean(data[:,780:980,:],axis=1)
#     for i in range(Views):
#             dt = data_mean[i]
#             if np.max(dt) > 0.05:
#                 max_i = p_max_threshold(dt)
#                 min_i = p_min_threshold(dt)
#                 data[i,780:980,:max_i-80] = 0
#                 data[i,780:980,min_i+80:] = 0
#                 rxi,rxa = merge_img_range(min_i,max_i)
#                 rxmin2[i] = rxi - 40
#                 rxmax2[i] = rxa + 40
#             else:
#                 rxmin2[i] = 1
#                 rxmax2[i] = 979                 
#     data.astype(np.float32).tofile(path_Zero_Phase_both_side)

#     if model =='1':
#         with open(path_Zero_Phase_one_image, 'rb') as fid_3:
#             priors = np.fromfile(fid_3, dtype=np.float32).reshape((Views,NumDetx,NumDety))
#         # priors = priors[:,:1000,:]
#         for i in range(Views):
#             for j in range(ny):
#                 if (ny>=25 and ny < 43) or (ny>=51 and ny < 59):
#                     priors[i,j*avern:j*avern+avern,:int(rxmin[i,j])+10] = 0
#                     priors[i,j*avern:j*avern+avern,int(rxmax[i,j])-40:] = 0 
#                 else:           
#                     priors[i,j*avern:j*avern+avern,:int(rxmin[i,j])] = 0
#                     priors[i,j*avern:j*avern+avern,int(rxmax[i,j])-20:] = 0
#         for i in range(Views):
#             priors[i,780:980,:int(rxmin2[i])] = 0
#             priors[i,780:980,int(rxmax2[i]):] = 0        
#         priors.astype(np.float32).tofile(path_Zero_Phase_one_image_zeroside)

# def split_dark_2D_restore_process():
#     with open(path_Dark_minus_noise, 'rb') as fid_3:
#         data = np.fromfile(fid_3, dtype=np.float32).reshape([Views,detector_num,detector_num])
#     data[np.isnan(data)] = 0
#     data[data<-10] = 0
#     data[data>10] = 0
#     data[:,:,0:190] = 0
#     data[:,:,780:] = 0
#     # tools.draw_2D_fig(data)
#     # plt.show()
#     priors = split_restore_Dark_2D(data)
#     # priors = mask_value_gauss2(priors,0.2,10)
#     priors.astype(np.float32).tofile(path_Zero_Phase_one_image)


#     # Zero_Phase_both_sides('1') 

# def inter_minus_noise():
#     with open(path_Zero_Phase_both_side, 'rb') as fid_3:
#         phase = np.fromfile(fid_3, dtype=np.float32).reshape([Views,1000,NumDetsub])
#     with open(path_Zero_Phase_one_image, 'rb') as fid_3:
#         prior = np.fromfile(fid_3, dtype=np.float32).reshape([Views,1000,NumDetsub])
#     # phase = phase[:,500,:]
#     # prior = prior[:,500,:]
#     A_sum = construct_A_sum()
#     phaser = iteration_2D(phase,prior,A_sum)
#     phaser.astype(np.float32).tofile(path_Zero_Phase_one_image_inter)

# def test():
#     path_name = './data/remove_streaks_phase_merge_img.raw'
#     with open(path_name, 'rb') as fid_3:
#         priors = np.fromfile(fid_3, dtype=np.float32).reshape([Views,1000,NumDetsub])
#     # priors = priors[:,:1000,:]
#     for i in range(Views):
#         for j in range(ny):
#             priors[i,j*avern:j*avern+avern,:int(rxmin[i,j])] = 0
#             priors[i,j*avern:j*avern+avern,int(rxmax[i,j]):] = 0
#     for i in range(Views):
#         priors[i,800:1000,:int(rxmin2[i])] = 0
#         priors[i,800:1000,int(rxmax2[i]):] = 0        
#     # tools.draw_twoD_figure(priors[:,90,:])
#     priors.astype(np.float32).tofile('./data/remove_streaks_phase_merge_img2.raw')

# def merge_img_range(min_i,max_i):
#     center = (max_i + min_i)/2 
#     clength = (min_i - max_i)/2 
#     rxmin = center - clength 
#     rxmax = center + clength 
#     return rxmin,rxmax


# def p_max_threshold(data):
#     max_v = np.max(data)
#     max_v_0_1 = max_v*0.1
#     index = np.argmax(data)
#     conv = 10000
#     while conv > max_v_0_1: 
#         conv = data[index]
#         index -= 1
#         if index >= 920:
#             index = 920
#             break
#     return index

# def p_min_threshold(data):
#     min_v = np.min(data)
#     min_v_0_1 = min_v*0.1
#     index = np.argmin(data)
#     conv = -10000
#     while conv < min_v_0_1:
#         conv = data[index]
#         index += 1
#         if index >= 920:
#             index = 920
#             break
#     return index

# def minus_noise(data):
#     for i in range(Views):
#         noise = ((data[i,40:990,980:1000]).mean(0)).mean(0)
#         data[i,:,:] = data[i,:,:] - noise
#     data.astype(np.float32).tofile('test_minus_noise.raw')
#     return data

# def signal_FBP():
#     path_name = '/data/tanyh/V1/code_zhu/PPT/check/Sino/65740_label_wrap.raw'
#     phase = read_data(path_name)
#     result = FBP_process(phase)
#     tools.draw_twoD_figure(result)
#     # plt.show()


# def FBP_process(Sino_img):

#     os.environ["CUDA_VISIBLE_DEVICES"] = "0"
#     sess = tf.Session()

#     MODULE_ATX = tf.load_op_library('/data/tanyh/V1/code_zhu/CBCT/fanbeam/Atx/Atx.so')

#     # input_img = tf.placeholder(tf.float32, [rotate_num, detector_num], name="input_CT")

#     Sino_img = np.reshape(Sino_img, [rotate_num, detector_num])
#     out = MODULE_ATX.atx(Sino_img, BATCH_SIZE, SO, OD, scale, img_size, img_size,
#                         detector_num, det_size / factor_ray, y_os, nt, tmp_size, rotate_num, nv_pi, 0)
#     result = sess.run(out)
#     return np.reshape(result,[img_size, img_size])



# def iteration_2D(phase,prior,A_sum):
#     #
#     I = prior.T
#     A = A_sum
#     phase_T = phase.T
#     A_inv = np.linalg.pinv(A)
#     a = 1e-12
#     beta = 0.4
#     dt = 1
#     tau = 1e-3
#     iter = 80
#     for i in range(Views):
#         print(i)
#         for mm in range(iter):
#             Ii = I[:,:,i]
#             g = A_inv @ (A @ Ii - phase_T[:,:,i])
#             Is1t = np.roll(Ii,-1,axis=0)
#             Ist1 =  np.roll(Ii,-1,axis=1)
#             I_a = Ii - np.roll(Ii,1,axis=0)
#             I_b = Ii - np.roll(Ii,1,axis=1)
#             I_c = Is1t - Ii
#             I_d = Is1t - np.roll(Is1t,1,axis=1)
#             I_e = Ist1 - Ii
#             I_f = np.roll(Ii,-1,axis=1) - np.roll(Ist1,1,axis=0)
#             den1 = (a + I_a ** 2 + I_b ** 2) ** 0.5
#             den2 = (a + I_c ** 2 + I_d ** 2) ** 0.5
#             den3 = (a + I_e ** 2 + I_f ** 2) ** 0.5
#             v = (I_a + I_b) / den1 - I_c / den2 - I_e / den3
#             norm = np.sqrt(np.sum(v ** 2))
#             v = v / norm
#             u = tau * g + beta * dt * v
#             I[:,:,i] = I[:,:,i] - u
#     return I.T




# def split_Dark_restore(phase,Ny):
#     Nx = Views
#     N_s = N_shift
#     prior = np.zeros_like(phase)
#     for k in range(Nx):
#         for j in range(Ny):
#             if j <= N_s-1:
#                 prior[k, j] = 0
#             elif j <= 2*N_s-1:
#                 prior[k, j] = (phase[k, j - N_s] - prior[k , j - N_s])/0.5*0.494
#             else:
#                 prior[k, j] = (phase[k, j - N_s] - prior[k , j - N_s] - 0.5*0.494*prior[k , j - 2*N_s])/0.5*0.494
#     return prior

# def split_restore(phase):
#     Nx = Views
#     Ny = NumDetsub
#     N_s = N_shift
#     prior = np.zeros_like(phase)
#     for i in range(X):
#         for k in range(Nx):
#             for j in range(Ny):
#                 if j <= N_s-1:
#                     prior[i,k, j] = 0
#                 elif j <= 2*N_s-1:
#                     prior[i,k, j] = -phase[i,k, j - N_s]
#                 else:
#                     prior[i,k, j] = prior[i,k , j - N_s] -  phase[i,k , j - 2*N_s]
#     return prior

# def split_restore_Dark_2D(phase):
#     N_s = N_shift
#     prior = np.zeros_like(phase)
#     print(phase.shape)
#     for j in range(N_s):
#         prior[:,:,j] = 0

#     for j in range(N_s, 2*N_s):
#         prior[:,:,j] = phase[:,:,j-N_s]/0.247

#     for j in range(2*N_s, phase.shape[2]):
#         prior[:, :, j] = (prior[:,:,j-N_s] - phase[:,:,j-N_s] - phase[:,:,j-2*N_s]*0.247)/0.247
#     return prior



# def read_data(sino_path_name):
#     with open(sino_path_name, 'rb') as fid_3:
#         sino_2 = np.fromfile(fid_3, dtype=np.float32).reshape([Views,NumDetx,NumDety])
#     return sino_2

# def read_data2(sino_path_name):
#     with open(sino_path_name, 'rb') as fid_3:
#         sino_2 = np.fromfile(fid_3, dtype=np.float32).reshape([Views,NumDet])
#     return sino_2
if __name__ == '__main__':
    mian()