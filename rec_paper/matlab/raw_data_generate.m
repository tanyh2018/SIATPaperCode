
%% Get phase result when spliting distance is integer pixel   2023-4-23
%% Add non-integer pixel method   2023-4-23
clearvars;
clc;
%% 没有偏移没有噪声的相位原始投影
for k=1
    %N_shift = 19.9 + k*0.1
    N_shift = 0
    k = N_shift;

%% Get Data
%% Phase information
path_name ='.\data\';
file_name_I ='仿真聚苯乙烯-PMMA-水-phase-fanbeamtomo-6000-parall.raw';
fid_2 = fopen([path_name file_name_I], 'r');   %存为raw
sino_1=fread(fid_2, [6000 720],'float32','l');


%% Absor information
file_name_I ='仿真聚苯乙烯-PMMA-水-absor-fanbeamtomo-6000-parall.raw';
fid_3 = fopen([path_name file_name_I], 'r');   %存为raw
sino_2=fread(fid_3, [6000 720],'float32','l');
modeln = "No_noise";
%modeln = "Noise";
model = "ACT";
non_integer_model = "nini";    % ini: integer solve non-integer; nini: non-integer solve non-integer
run_model = 'SLOW';      %FAST: quick run;   SLOW: slow run;

%% 构造变换矩阵A  AX=Y
date = datestr(datetime, 'yyyy.mm.dd.HH.MM.ss');
set(0,'DefaultFigureVisible', 'on')
amp=10;

%% 对相位投影图进行偏移
Nimg2 = size(sino_1);
Nimg1 = [Nimg2(1)/amp Nimg2(2)];
sino_e=sino_1;
if amp > 1
    pp = reshape(sino_e,amp,Nimg1(1),Nimg1(2));
    ori_phase = mean(pp,1);
end
ori_phase = reshape(ori_phase,Nimg1(1),Nimg1(2));

%% 对吸收投影图进行偏移
sino_e=exp(-sino_2);
if amp > 1
    pp = reshape(sino_e,amp,Nimg1(1),Nimg1(2));
    ori_e = mean(pp,1);
end
ori_e = reshape(ori_e,Nimg1(1),Nimg1(2));


%% 对偏移图加泊松噪声
Nimg2 = size(ori_e);
I_0=5000;
M=8;
I_1=ones(M,Nimg2(1),Nimg2(2));
epsilon = 0.7;

for i=1:M
    for j =1:Nimg2(1)
        for k=1:Nimg2(2)
            I_1(i,j,k)=I_0*ori_e(j,k)*(1+epsilon*cos(2*pi*i/M + ori_phase(j,k)));     %偏移后光强投影图I_0*exp（-ul）
        end
    end
end

if strcmpi(modeln,'No_noise')
    img_shifted=I_1/I_0;   
else
    img_shifted=poissrnd(I_1)/I_0;        
end

phase = zeros(Nimg2(1),Nimg2(2));
I1s=zeros(Nimg2);
I1c=zeros(Nimg2);

for i=1:M
    for j =1:Nimg2(1)
        for k=1:Nimg2(2)
            I1s(j,k) = I1s(j,k) + img_shifted(i,j,k)*sin(2*pi*i/M);
            I1c(j,k) = I1c(j,k) + img_shifted(i,j,k)*cos(2*pi*i/M);
        end
    end
end

for j =1:Nimg2(1)
    for k=1:Nimg2(2)
        phase(j,k)= atan(-I1s(j,k)/I1c(j,k));
    end
end
a = 2
% if amp > 1
%     phase = reshape(phase,amp,Nimg1(1),Nimg1(2));
%     phase = mean(phase,1);
% end
phase = reshape(phase,Nimg1(1),Nimg1(2));
Nimg2 = size(phase);
prior = zeros(Nimg2);
figure;
imshow(phase,[]);
DPCT = recfbp(phase,"ACT",size(phase));
figure;
imshow(DPCT,[]);

out_file = "./data/phase_image_6000.raw";
fid = fopen([out_file], 'w');
fwrite(fid, DPCT, 'float32');
fclose(fid);


if strcmpi(non_integer_model,'ini')
    N_shift1 = round(N_s);
    sr1 = 0;
else
    N_s = N_shift;
    sr1 = abs(fix(N_s)-N_s);
    sr2 = 1-abs(fix(N_s)-N_s);
    N_shift1 = fix(N_s);
end
% 
if sr1 <= 0.5
    for k=1:Nimg2(2)
        for j =1:Nimg2(1)
            if j <= N_shift1
                prior(j,k)= 0;
            elseif j <= 2*N_shift1
                prior(j,k)= -phase(j-N_shift1,k);
            else
                prior(j,k)= prior(j-2*N_shift1,k)-phase(j-N_shift1,k);
            end
        end
    end
else
    for k=1:Nimg2(2)
        for j =1:Nimg2(1)
            if j <= N_shift1+1
                prior(j,k)= 0;
            elseif j<=2*N_shift1+1
                prior(j,k)= (- sr2*prior(j-1,k)- phase(j-N_shift1-1,k))/sr1 ;
            elseif j<=2*N_shift1+2
                prior(j,k)= (sr2*prior(j-2*N_shift1-1,k) - sr2*prior(j-1,k)- phase(j-N_shift1-1,k))/sr1;
            else
                prior(j,k) = (sr1*prior(j-2*N_shift1-2,k) + sr2*prior(j-2*N_shift1-1,k)- sr2*prior(j-1,k) - phase(j-N_shift1-1,k))/sr1;
            end
        end
    end
end

% prior = A_sum \ phase;
figure;
imshow(prior, [])
title('prior projection');
a=3
%% 求解X
N = Nimg2(1);
Nx = Nimg2(2);
Ny = Nimg2(1);
iter = 60; % iter = 10 when di = 1; iter = 40 for di = 481; iter = 45 for di = 526; 迭代次数
beta = 0.05; dt = 1; % paper: 500, 0.05, 1e-5 80
a = 10.^(-10);% a  - data small enough
tau = 1e-5;
tic
A = B_sum;

%% 2D reconstrution
for j = 1:Nx
      b= phase(:,j); 
      I= prior(:,j);       
%% MI
    if strcmpi(run_model,'SLOW')        
        theta=eye(Ny);
        for i=1:Ny
            pi=mean(img_shifted(:,i,j));
            theta(i,i) = 1./(2./(pi*M*epsilon*epsilon));
        end
    end
        for i=1:iter  %% do iterations
            if strcmpi(run_model,'SLOW')
                g=A'*theta*(A*I(:)-b); 
                tau=g'*g/((A*g)'*(theta*A*g));
            else
                g = A'*(A*I(:)-b);           
            end
            I_f=0-I;
            I_b=I;
            I_u=I-I([1 1:N-1]);
            I_d=I([2:N N])-I;
            I_x_1=0;
            I_y_1=I([2:N N]);
            den1=(a+I_u.^2).^(0.5);
            den3=(a+I_d.^2).^(0.5);
            v=(I_u)./den1-I_d./den3;
            norm=(sum(sum(v.^2))).^(0.5);
            v=v./norm;
            u=tau*g+beta*dt*v;
            I=I-u;
        end
        x_TV(:,j) = I;
end
toc

figure;
imshow(x_TV, [])
title('x_TV projection3');

%% 投影重建
a=1
DPCT = recfbp(x_TV,model,Nimg2);
DPCT_linear = recfbp(prior,model,Nimg2);
DPCT_phase = recfbp(phase,"DPC-CT",Nimg2)/N_shift;
figure;
subplot(2,2,1);
imshow(DPCT_linear,[]);
title('Linear equations rec');
subplot(2,2,2);
% DPCT(DPCT<0) = 0;
imshow(DPCT,[]);
title('Iterative rec');
subplot(2,2,3);
imshow(DPCT_phase,[]);
title('Direct rec');

date = datestr(datetime, 'yyyy.mm.dd.HH.MM.ss');
filePathout="result/" +char(date)+"/";
if not(isfolder(filePathout))
    mkdir(filePathout)
end
% 
out_file = filePathout  + "I0_" + num2str(I_0) + "_beta_" + num2str(beta) + "_iter_" + num2str(iter)  + "_Nshift_"   + num2str(N_shift) + "_B_tan_OBP+PWLS-TV.raw";
fid = fopen([out_file], 'w');
fwrite(fid, DPCT, 'float32');
fclose(fid);

out_file = filePathout  + "I0_" + num2str(I_0) + "_beta_" + num2str(beta) + "_iter_" + num2str(iter)  + "_Nshift_"   + num2str(N_shift) + "_B_tan_OBP.raw";
fid = fopen([out_file], 'w');
fwrite(fid, DPCT_linear, 'float32');
fclose(fid);

out_file = filePathout  + "I0_" + num2str(I_0) + "_beta_" + num2str(beta) + "_iter_" + num2str(iter)  + "_Nshift_"   + num2str(N_shift) +"_B_tan_FBP.raw";
fid = fopen([out_file], 'w');
fwrite(fid, DPCT_phase, 'float32');
fclose(fid);
% 
% clear all
end