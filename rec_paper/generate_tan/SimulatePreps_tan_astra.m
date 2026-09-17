% function [y, A, M, S, T, V,fun_sin] = SimulatePreps_yuan(ObjectSize, noise, base_material,zhou_q,V,detector_num,SO,SD,scale,det_size,nv_pi,set_1,GuYihua_S,mode_b, a_up, a_do)
clearvars;
clc;
I_0=50000;
%%-------------------分解三种物质（聚苯乙烯-二氧化硅-水）
path_name ='./python/';
file_name_I ='absor_image.raw';

fid_1 = fopen([path_name file_name_I], 'r');   % 存为raw
row_1=fread(fid_1, [512 512],'float32','l');      % 注意将img转置
fclose('all');

x = cat(2, row_1(:));
%% 
tic
noise = 0;
V =720;
ForwardTheta = [0:V-1] * 360 / V;  %%把360度平均分90个视角，每个视角的读数
ObjectSize = 512;
detector_num = 600;
SO = 1156.3;  %%光源到物体的距离1156.3
SD = 1560.6;    %%系统总长1560.6
scale = 0.15e-4;     %%重建图像单个像素大小，单位mm  512/360*0.4
det_size = 0.25e-4;   %%探测器单个像素大小，单位mm
d = atand(detector_num*det_size/2/SD)*2;  %%射线张角（视角）
A = fanbeamtomo(ObjectSize,ForwardTheta,detector_num,SO/ObjectSize/scale,d)*scale;
%[y] = NoisyForwardModel(x, A, M, S, noise,V);
projs = A * x;
% Compute photon counts as seen by the detector

if contains(file_name_I,'absor')
    attenuationFactors = I_0*exp(-projs.');
    y = attenuationFactors.';
    sino_1 = y(:,1);
    sino_1= -log(sino_1/I_0);
    model = 'absor';
else
    y = projs;
    sino_1 = y(:,1);
    model = 'phase';
end

sino_1 = reshape(sino_1, [ detector_num, V ]);
figure;imshow(sino_1,[]);
out_file = "仿真聚苯乙烯-PMMA-水-"+model+".raw";
fid_1 = fopen([out_file], 'w');   % 存为raw仿真碘-骨头-水50hz_512x0.4-600x0.6.raw
fwrite(fid_1, sino_1,'float32'); 

% 相位图
% [maxvalue,index] = max(sino_11);
% sino_2 = sino_11/maxvalue;
% sino_2 = reshape(sino_2, [ detector_num, V ]);
% sino_3 = zeros(detector_num-1,V);
% for ii = 1:V
%     sino_3(:,ii) = sino_2(1:end-1,ii)-sino_2(2:end,ii);
% end    

% fid_3 = fopen('仿真碘-骨头-水-DPC-6000.raw', 'w');   % 存为raw仿真碘-骨头-水50hz_512x0.4-600x0.6.raw
% fwrite(fid_3, sino_3,'float32'); 
% figure;imshow(sino_3,[]);

% fid_2 = fopen('仿真碘-骨头-水-phase-6000.raw', 'w');   % 存为raw仿真碘-骨头-水50hz_512x0.4-600x0.6.raw
% fwrite(fid_2, sino_2,'float32'); 
% figure;imshow(sino_2,[]);
