% function [y, A, M, S, T, V,fun_sin] = SimulatePreps_yuan(ObjectSize, noise, base_material,zhou_q,V,detector_num,SO,SD,scale,det_size,nv_pi,set_1,GuYihua_S,mode_b, a_up, a_do)
clearvars;
clc;
addpath("D:\software\matlab_ASTRA\astra-2.1.0-matlab-win-x64\astra-2.1.0\tools\")
addpath("D:\software\matlab_ASTRA\astra-2.1.0-matlab-win-x64\astra-2.1.0\mex\")

I_0=50000;
%%-------------------分解三种物质（聚苯乙烯-二氧化硅-水）
path_name ='./python/';
file_name_I ='phase_image.raw';

fid_1 = fopen([path_name file_name_I], 'r');   % 存为raw
row_1=fread(fid_1, [512 512],'float32','l');      % 注意将img转置
fclose('all');

x = cat(2, row_1(:));
%% 
tic
noise = 0;
V =720;
ObjectSize = 512;
detector_num = 1200;
scale = 0.15e-4;     %% Sample Size 
det_size = 0.25e-4;   %%探测器单个像素大小，单位mm

%% create geometries and projector
proj_geom = astra_create_proj_geom('parallel', 0.5, 1200, linspace2(0,2*pi,V));
vol_geom = astra_create_vol_geom(512,512);
proj_id = astra_create_projector('linear', proj_geom, vol_geom);
%% create forward projection
[sinogram_id, sinogram] = astra_create_sino(row_1, proj_id);

projs = sinogram*det_size;

% Compute photon counts as seen by the detector
if contains(file_name_I,'absor')
    attenuationFactors = I_0*exp(-projs.');
    y = attenuationFactors.';
    sino_1 = y;
    sino_1= -log(sino_1/I_0);
    model = 'absor';
else
    y = projs;
    sino_1 = y;
    model = 'phase';
end

sino_1 = reshape(sino_1', [ detector_num, V ]);
figure;imshow(sino_1,[]);
out_file = "仿真聚苯乙烯-PMMA-水-"+model+".raw";
fid_1 = fopen([out_file], 'w');   % 存为raw仿真碘-骨头-水50hz_512x0.4-600x0.6.raw
fwrite(fid_1, sino_1,'float32'); 

% %% reconstruct
% sino_1 = sino_1';
% proj_geom = astra_create_proj_geom('parallel', 0.5, 1200, linspace2(0,2*pi,V));
% vol_geom = astra_create_vol_geom(1200,1200);
% sinogram_id = astra_mex_data2d('create', '-sino', proj_geom, sino_1);
% proj_id = astra_create_projector('linear', proj_geom, vol_geom);
% recon_id = astra_mex_data2d('create', '-vol', vol_geom);
% cfg = astra_struct('FBP');
% cfg.ProjectorId = proj_id;
% cfg.ProjectionDataId = sinogram_id;
% cfg.ReconstructionDataId = recon_id;
% fbp_id = astra_mex_algorithm('create', cfg);
% astra_mex_algorithm('run', fbp_id);
% V = astra_mex_data2d('get', recon_id)/1e-5;
% imshow(V, []);
% out_file = "仿真聚苯乙烯-PMMA-水-"+model+"1.raw";
% fid_1 = fopen([out_file], 'w');   % 存为raw仿真碘-骨头-水50hz_512x0.4-600x0.6.raw
% fwrite(fid_1, V,'float32'); 
