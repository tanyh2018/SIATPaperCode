
%% Get phase result when spliting distance is integer pixel   2023-4-23
%% Add non-integer pixel method   2023-4-23
clearvars;
clc;
%% 没有偏移没有噪声的相位原始投影

%% Get Data
%% Phase information
file_name_I ='./AI_data/outphase_ai_data_5t5.raw';
fid_2 = fopen([file_name_I], 'r');   %存为raw
sino_1=fread(fid_2, [600 720],'float32','l');
model = "ACT";

sino(sino_1<0) = 0;

%% 投影重建
DPCT = recfbp(sino_1,model,[600,720]);
DPCT(DPCT<0) = 0;
figure;
imshow(DPCT,[]);

out_file = "./AI_data/AI_FBP_result_f.raw";
fid = fopen([out_file], 'w');
fwrite(fid, DPCT, 'float32');
fclose(fid);
