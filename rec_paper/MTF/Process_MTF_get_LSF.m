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
pixel_size = 0.1E-4; % pixel dimension, unit: mm
row = 512;
col = 512;
%%% catphan
centerRow = row/2; centerCol = col/2; % center coordinates of the insert
% centerRow = 293; centerCol = 153; % center coordinates of the insert
c_row = 200; c_col =200; % # of rows and cols in the cropped image
max_cluster = 11;
c_pix = 50;
%%% simulated data with a 15x15 bright insert
% centerRow = 384; centerCol = 345; % center coordinates of the insert
% % centerRow = 146; centerCol = 210; % center coordinates of the insert
% c_row = 40; c_col = 40; % # of rows and cols in the cropped image
% max_cluster = 11;
% % c_pix = 13;

filePath = './data/'
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
dirOutput=dir(fullfile(filePath,'*phase_MTF_image_delta*.raw'));      
fileName={dirOutput.name};

%set(0,'DefaultFigureVisible', 'off')
set(0,'DefaultFigureVisible', 'on')
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
        %l_RadialAvrg = [fliplr(l_RadialAvrg(3:end)),l_RadialAvrg(3:end)];
        l_RadialAvrg = l_RadialAvrg(3:end-5);
        c_pix = length(l_RadialAvrg);
        LSF = l_RadialAvrg(1:end-1) - l_RadialAvrg(:, 2:end);
        % fit edge of radial avrg
        fit_index1  = (1:1:length(l_RadialAvrg(1:end-1)));
%         y_val1 = l_RadialAvrg(1:end-1);
%         y_val2 = l_RadialAvrg(:, 2:end);
%         f2 = fit(fit_index1',y_val1',"fourier8");
%         f3 = fit(fit_index1',y_val2',"fourier8");
%         LSF_fit = f2(fit_index1) - f3(fit_index1);
%         %LSF_fit = LSF';
% %         LSF(LSF<=0) = 0;
        fid = fopen([filePathout_LSF, char(file_name_prefix(1)), 'notfit.txt'],'wt');
        m = size(LSF');
        for i = 1:1:m
            fprintf(fid, '%g \n', LSF(i));
        end
        fclose(fid);

%         fid = fopen([filePathout_LSF, char(file_name_prefix(1)), 'RadialAverage.txt'],'wt');
%         m = length(l_RadialAvrg);
%         for i = 1:1:m
%             fprintf(fid, '%g \n', l_RadialAvrg(1,i));
%         end
%         fclose(fid);
        figure;
%         subplot(221), plot(fit_index1,y_val1);
%         legend('Data','gauss');
%         subplot(222), plot(fit_index1,y_val2);
%         legend('Data','gauss');
        subplot(223), plot(fit_index1,LSF,'o');
        subplot(224), plot(bkgIn(length(bkgIn)/2, :));
    end
end
% clear all;
%     

