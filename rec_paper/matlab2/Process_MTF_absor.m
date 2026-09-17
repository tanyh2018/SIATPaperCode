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
c_row = 400; c_col =400; % # of rows and cols in the cropped image
max_cluster = 11;
c_pix = 50;

% Raw images
filePath = 'D:/xianjinyuan/reconstruction/tyh/DPC_rec/likelihood_tv/result/MTF_verify/';
%fileName = {'period_8.00_sep_2.248_sample_self_DPCT','period_1.20_sep_14.987_sample_self_DPCT','period_1.70_sep_10.579_sample_self_DPCT','period_2.90_sep_6.201_sample_self_DPCT','period_1.00_sep_17.984_sample_self_DPCT'};
fileName = {'I0_500_beta_0.1_iter_80_Nshift_1_B_tan_OBP'};
filePathout = [filePath,'result/']
for ii = 1:length(fileName)
    fid = fopen([filePath, fileName{ii}, '.raw']);
    img = fread(fid, 'float');
    img = reshape(img, [row col]);
    fclose(fid);
    figure;
    imshow(img,[])
    bkgIn = img(centerRow-c_row/2+1:centerRow+c_row/2, centerCol-c_col/2+1:centerCol+c_col/2);
    figure;
    imshow(bkgIn,[])    
    
    l_RadialAvrg = RadialAverage(bkgIn, 0);
    l_RadialAvrg = l_RadialAvrg(5:end-5);
    LSF = l_RadialAvrg(1:end-1) - l_RadialAvrg(:, 2:end);
   
    c_pix = length(l_RadialAvrg);
    fit_index = (140:1:length(LSF))';
    x2 = (1:1:length(l_RadialAvrg(1:end-1)))';
    f = fit(fit_index,LSF(140:end)','gauss2');
%     f = fit(x2, l_RadialAvrg(1:end-1)','poly6');
    figure;
    subplot(221);imshow(bkgIn, []);

    subplot(222), plot(bkgIn(length(bkgIn)/2, :));
    title('profile');
    xlabel('Pixel index');
    ylabel('Intensity (a.u.)');
    subplot(223), plot(l_RadialAvrg(1:end-1));
    title('Edge profile');
    xlabel('Radial pixel index');
    ylabel('Intensity (a.u.)');
    subplot(224), plot(l_RadialAvrg(:, 2:end));
    title('Edge profile');
    xlabel('Radial pixel index');
    ylabel('Intensity (a.u.)');
    saveas(gca,[filePath,fileName{ii},'_process.png']);

    figure;
    subplot(211), plot(LSF);
    title('Edge Difference profile');
    xlabel('Radial pixel index');
    ylabel('Intensity (a.u.)');
    subplot(212);
    plot(f,fit_index,LSF);
    legend('Data','gauss1')
    title('Fit Edge Difference profile');
    xlabel('Radial pixel index');
    ylabel('Intensity (a.u.)');
    saveas(gca,[filePath,fileName{ii},'_fit.png']);
    %LSF = f(fit_index);  
    [Imax,Pmax] = max(LSF); % maximum intensity value and its index
    LSF(Pmax+7:end) = 0;
    LSF(1:Pmax-7) = 0;
    
    LSF_ZeroPad = [zeros(1, (max_cluster-1)/2*c_pix), LSF, zeros(1, (max_cluster-1)/2*c_pix)];
    mtf = fftshift(fft(ifftshift(LSF_ZeroPad)));
    MTF(:,1) = abs(mtf) / max(abs(mtf)); % normalized mtf


    LSF_f = f(fit_index);

    LSF_ZeroPad_f = [zeros(1, (max_cluster-1)/2*c_pix), LSF_f', zeros(1, (max_cluster-1)/2*c_pix)];
    mtf_f = fftshift(fft(ifftshift(LSF_ZeroPad_f)));
    MTF_f(:,1) = abs(mtf_f) / max(abs(mtf_f));
%    figure;
%     subplot(121);plot(LSF_ZeroPad, 'k-', 'LineWidth', 1);
%     title('LSF_ZeroPad')
%     subplot(122);plot(MTF, 'k-', 'LineWidth', 1);
%     title('FFT of LSF')

    presampling_size = pixel_size ; % estimated mean shift size in presampling, unit: mm
    CutOffFrequency = 1 / pixel_size; % first zero point of presampling MTF: !!! Notice use pixel size, but not presampling shift
    df = 1 / presampling_size / (max_cluster*c_pix); % sampling rate in frequency domain
    
    PeakMid = find(MTF(:,1)>=1); % find the peak center of mtf curve
    PeakMid_f = find(MTF_f(:,1)>=1); % find the peak center of mtf fit curve

% PeakEnd = PeakMid + CutOffFrequency/df - 1;
% mMTF = MTF(PeakMid : PeakEnd);
%
% figure, plot(0:df:CutOffFrequency-df, mMTF)
% title('Measured MTF')
% xlabel('Spatial frequency (lp/mm)')
% xlim([0 CutOffFrequency/2])
% ylabel('MTF')
% grid minor
%%



    % ha = tight_subplot(2,4,[.20 .07],[.15 .03],[.08 .04]); % (Nh, Nw, gap, marg_h, marg_w)
    % legend_str = {'Label', 'FBP', 'FBPConvNet', 'PICCS', 'LEARN', 'DIR-I', 'DIR-II', 'DIR-III'};
    xindex0 = ((size(MTF_f,1)-1)/-2)*df:df:((size(MTF_f,1)-1)/2)*df;
    xindex1 = reshape(xindex0, [], 1);
    figure;
    plot(0:df:(size(MTF,1)-PeakMid)*df, MTF(PeakMid:end,1),'o--k','MarkerSize',1,'LineWidth',0.5);
    xlabel('lp/mm');
    ylabel('MTF');
    title('Not used fit curve');

    figure;
    plot(0:df:(size(MTF_f,1)-PeakMid_f)*df, MTF_f(PeakMid_f:end,1),'o--k','MarkerSize',1,'LineWidth',0.5);
    title('Used fit curve');
    xlabel('lp/mm');
    ylabel('MTF');

    saveas(gca,[filePathout,fileName{ii},'_MTF.png']);

    fid = fopen([filePathout, fileName{ii}, '.txt'],'wt');
    m = size(xindex1);
    for i = 1:1:m
        fprintf(fid, '%g,%g \n', xindex1(i), MTF_f(i));
    end
    
    fid0 = fopen([filePathout, fileName{ii}, '_LSF.txt'],'wt');
    m1 = size(LSF);
    for j = 1:1:m1(2)
        fprintf(fid0, '%g %g \n', j, LSF(j));
    end

end
%     
% for i = 1:1
% %     axes(ha(i));
%     plot(0:df:(size(MTF,1)-PeakMid)*df, MTF(PeakMid:end,1),'o--k','MarkerSize',1,'LineWidth',0.5)
%     hold on
%     plot(0:df:(size(MTF,1)-PeakMid)*df, MTF(PeakMid:end,i+1),'o-r','MarkerSize',1,'LineWidth',0.5)
%     xlabel('Spatial frequency (lp/mm)')
%     ylabel('MTF')
%     xlim([0 (size(MTF,1)-PeakMid)*df])
%     grid minor
%     legend([legend_str(1), legend_str(i+1)])
%     legend('boxoff')
% end
% axes(ha(8));axis off
