% ===== Tilted edge MTF =====
% ===== !!!!Gain corrections are needed!!!! =====
% ===== !!!!Only consider the edge region!!!! =====

clear all
clc

% Change default axes fonts.
set(0,'DefaultAxesFontName', 'Times New Roman')
set(0,'DefaultAxesFontSize', 10)

% Change default text fonts.
set(0,'DefaultTextFontname', 'Times New Roman')
set(0,'DefaultTextFontSize', 10)

%% ===== Read in files =====
pixel_size = 10E-3; % pixel dimension, unit: mm
row = 480;
col = 480;
%%% catphan
centerRow = row/2; centerCol = col/2; % center coordinates of the insert
% centerRow = 293; centerCol = 153; % center coordinates of the insert
c_row = 280; c_col =280; % # of rows and cols in the cropped image
max_cluster = 11;
c_pix = 50;
%%% simulated data with a 15x15 bright insert
% centerRow = 384; centerCol = 345; % center coordinates of the insert
% % centerRow = 146; centerCol = 210; % center coordinates of the insert
% c_row = 40; c_col = 40; % # of rows and cols in the cropped image
% max_cluster = 11;
% % c_pix = 13;


% Raw images
filePath = 'D:/xianjinyuan/Jiecheng/NanoCT/Simulation/ReconCT/add/yuhang/talbot_result/paper_version_2022_12_19/dpc_sample_size/CTresult/'
filePathout_png = [filePath,'MTF_result_png/']
filePathout_txt = [filePath,'MTF_result_txt/']
filePathout_LSF = [filePath,'MTF_result_LSF_txt/']
if not(isfolder(filePathout_png))
    mkdir(filePathout_png)
end
if not(isfolder(filePathout_txt))
    mkdir(filePathout_txt)
end
if not(isfolder(filePathout_LSF))
    mkdir(filePathout_LSF)
end
filePath=fullfile(filePath);
dirOutput=dir(fullfile(filePath,'*p*.raw'));      
fileName={dirOutput.name};

set(0,'DefaultFigureVisible', 'off')
%set(0,'DefaultFigureVisible', 'on')
for ii = 1:length(fileName)
    
    file_name_prefix = regexp(fileName{ii},".raw",'split');
%     period = regexp(char(filename(ii)),"_",'split');
    fileName(ii)
    if contains(fileName(ii),'period')
        fileName(ii)
        fid = fopen([filePath, fileName{ii}]);
        img = fread(fid, 'float');
        img = reshape(img, [row col]);
        fclose(fid);

        bkgIn = img(centerRow-c_row/2+1:centerRow+c_row/2, centerCol-c_col/2+1:centerCol+c_col/2);
        clear img;

        l_RadialAvrg = RadialAverage(bkgIn, 0);
        l_RadialAvrg = l_RadialAvrg(3:end-5);
        c_pix = length(l_RadialAvrg);
        LSF = l_RadialAvrg(1:end-1) - l_RadialAvrg(:, 2:end);
        fit_index = (1:1:length(LSF));
        
        fid_LSF = fopen([filePathout_LSF,char(file_name_prefix(1)) '.raw']);
        LSF_f = fread(fid_LSF, 'float');
        fclose(fid_LSF);
        LSF_in = reshape(LSF_f, [length(LSF_f)/2 2 ]);
        LSF_f = LSF_in(:,2);
        length(LSF_f)
        length(LSF)
        fit_index2 = LSF_in(:,1);
        figure;
        
        subplot(221);imshow(bkgIn, []);
        if contains(fileName(ii),'phi')
            title_s = '\delta';
        else
            title_s = '\mu [m^{-1}]';
        end
        title(char(file_name_prefix(1)));
        subplot(222), plot(bkgIn(length(bkgIn)/2, :));
        title('profile');
        xlabel('Pixel index');
        ylabel(title_s);
        subplot(223), plot( l_RadialAvrg(1:end-1));
        title('Edge profile');
        xlabel('Radial pixel index');
        ylabel(title_s);
        subplot(224), plot(l_RadialAvrg(:, 2:end));
        title('Edge profile');
        xlabel('Radial pixel index');
        ylabel(title_s);
        saveas(gca,[filePathout_png,char(file_name_prefix(1)),'_process.png']);
        figure;
        plot(fit_index,LSF,'o');
        hold on
        plot(fit_index2,LSF_f);
        legend('Data','gauss');
        hold off
        title('Fit Edge Difference profile');
        xlabel('Radial pixel index');
        ylabel(title_s);
        saveas(gca,[filePathout_png,char(file_name_prefix(1)),'_fit.png']);
        c_pix = length(LSF);
        LSF_ZeroPad = [zeros(1, (max_cluster)*c_pix), LSF, zeros(1, (max_cluster)*c_pix)];
        mtf = fftshift(fft(ifftshift(LSF_ZeroPad)));
        MTF(:,1) = abs(mtf) / max(abs(mtf)); % normalized mtf

        c_pix_fit = length(LSF_f);
        LSF_ZeroPad_f = [zeros(1, (max_cluster)*c_pix_fit), LSF_f', zeros(1, (max_cluster)*c_pix_fit)];
        mtf_f = fftshift(fft(ifftshift(LSF_ZeroPad_f)));
        MTF_f(:,1) = abs(mtf_f) / max(abs(mtf_f));
        figure;
        subplot(121);plot(LSF_ZeroPad_f, 'k-', 'LineWidth', 1);
        title('LSF_ZeroPad_f')
        subplot(122);plot(MTF_f, 'k-', 'LineWidth', 1);
        title('FFT of LSF_f')
% 
%         figure;
%         subplot(121);plot(LSF_ZeroPad, 'k-', 'LineWidth', 1);
%         title('LSF_ZeroPad')
%         subplot(122);plot(MTF, 'k-', 'LineWidth', 1);
%         title('FFT of LSF')
        PeakMid = find(MTF(:,1)>=1); % find the peak center of mtf curve
        PeakMid_fit = find(MTF_f(:,1)>=1); % find the peak center of mtf fit curve    

        %fit
        fit_scale_number = 4; %fit function and scale number to times 4
        presampling_size_fit = pixel_size/fit_scale_number ; % estimated mean shift size in presampling, unit: mm
        CutOffFrequency_fit = 1 / pixel_size; % first zero point of presampling MTF: !!! Notice use pixel size, but not presampling shift
        df_fit = 1 / presampling_size_fit / (max_cluster*c_pix_fit); % sampling rate in frequency domain

        PeakEnd_fit = PeakMid_fit + CutOffFrequency_fit/df_fit - 1;
        mMTF_f = MTF_f(PeakMid_fit : PeakEnd_fit);
        
        figure, plot((0:df_fit:CutOffFrequency_fit-df_fit)/2, mMTF_f)
        title('Measured MTF fit')
        xlabel('Spatial frequency (lp/mm)')
        xlim([0 CutOffFrequency_fit/2])
        ylabel('MTF')
        grid minor

        %not fit
        presampling_size = pixel_size ; % estimated mean shift size in presampling, unit: mm
        CutOffFrequency = 1 / pixel_size; % first zero point of presampling MTF: !!! Notice use pixel size, but not presampling shift
        df = 1 / presampling_size / (max_cluster*c_pix); % sampling rate in frequency domain  

        PeakEnd = PeakMid + CutOffFrequency/df - 1;
        mMTF = MTF(PeakMid : PeakEnd);
        
        figure, plot((0:df:CutOffFrequency-df)/2, mMTF)
        title('Measured MTF ')
        xlabel('Spatial frequency (lp/mm)')
        xlim([0 CutOffFrequency/2])
        ylabel('MTF')
        grid minor
        %%
        % ha = tight_subplot(2,4,[.20 .07],[.15 .03],[.08 .04]); % (Nh, Nw, gap, marg_h, marg_w)
        % legend_str = {'Label', 'FBP', 'FBPConvNet', 'PICCS', 'LEARN', 'DIR-I', 'DIR-II', 'DIR-III'};
        xindex0 = (((size(MTF_f,1)-1)/-2)*df_fit:df_fit:((size(MTF_f,1)-1)/2)*df_fit)/2;
        xindex1 = reshape(xindex0, [], 1);
        figure('visible','off');
        subplot(121),plot((0:df:(size(MTF,1)-PeakMid)*df)/2, MTF(PeakMid:end,1),'o--k','MarkerSize',1,'LineWidth',0.5);
        xlabel('lp/mm');
        ylabel('MTF');
        title('Not used fit curve');
        subplot(122),plot((0:df_fit:(size(MTF_f,1)-PeakMid_fit)*df_fit)/2, MTF_f(PeakMid_fit:end,1),'o--k','MarkerSize',1,'LineWidth',0.5);
        title('Used fit curve');
        xlabel('lp/mm');
        ylabel('MTF');

        saveas(gca,[filePathout_png,char(file_name_prefix(1)),'_MTF.png']);

        fid = fopen([filePathout_txt, char(file_name_prefix(1)), '.txt'],'wt');
        m = size(xindex1);
        for i = 1:1:m
            fprintf(fid, '%g,%g \n', xindex1(i), MTF_f(i));
        end
        fclose(fid);
        
        xindex0 = (((size(MTF,1)-1)/-2)*df:df:((size(MTF,1)-1)/2)*df)/2;
        xindex1 = reshape(xindex0, [], 1);
        fid = fopen([filePathout_txt, char(file_name_prefix(1)), 'notfit.txt'],'wt');
        m = size(xindex1);
        for i = 1:1:m
            fprintf(fid, '%g,%g \n', xindex1(i), MTF(i));
        end
        fclose(fid);
    end
end
% clear all;
%     

