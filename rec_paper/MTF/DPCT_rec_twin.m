
clear all
clc

filePath = 'F:\Talbot_MTF\code_data\pv1_20221219\code_version\version_2022_12_19\matlab\'
filePathout=[filePath,'CTresult\']
filePath=fullfile(filePath);
dirOutput=dir(fullfile(filePath,'*-*.raw'));  
filename = {dirOutput.name};
%filename={'period_8.0000_sep_2.24_phi.raw'};
%filename={'period_8.0000_sep_2.24_pure_absor_absor.raw'};
%filename={'period_1.9000_sep_9.45_phi.raw'};_poly
%filename={'period_1.0000_sep_17.96_phi.raw'};
%filename={'period_0.9000_sep_19.95_phi.raw'};
%filename={'period_0.4000_sep_44.89_phi.raw'};

%filename={'period_8.0000_sep_2.24_absor.raw'};
%filename={'period_2.9000_sep_6.19_absor.raw'};
%filename={'period_1.9000_sep_9.45_absor.raw'};
%filename={'period_1.0000_sep_17.96_absor.raw'};
% filename={'period_0.9000_sep_19.95_absor.raw'};
%filename={'period_0.4000_sep_44.89_absor.raw'};


%model = 'ACT';
%model = 'DPC-CT';
if not(isfolder(filePathout))
    mkdir(filePathout)
end
%set(0,'DefaultFigureVisible', 'off')
set(0,'DefaultFigureVisible', 'on')
%% Read project images
for ii = 1:length(filename)
    filename(ii)
    period = regexp(char(filename(ii)),"_",'split');
    %systerm information
    d1=1.1563;d2=0.2023;d3=0.202; %unit m
    %pp = str2num(char(period(2)))*1e-6; %unit m
    pp = 10;
    p2 = (d1+d2+d3)/2/(d1+d2)*pp; % m peirod of the stripes
    %filename={'period_1.0000_sep_17.96_phi.raw'}
    if contains(filename(ii),'phi')
       model = 'DPC-CT';
    end
    if contains(filename(ii),'absor')
       model = 'ACT';
    end
    model = 'ACT';

    fid = fopen([filePath, filename{ii}],'r');
    img = fread(fid,'float32');
    fclose(fid);
    px = 600;
    py = 1;
    pz = 720;

    % fid = fopen('.\sum.raw','r');
    % img = fread(fid,'uint32');
    % fclose(fid);
    % px = 1200;
    % py = 150;
    % pz = 360;
    img = reshape(img,px,py,pz); %px,py: one proj image size, pz: total projections number

    % Proj = imresize(img,[4000 360]);

    % img = imresize(img, [2400 160 360]);
    % for k = 1:pz
    %     for i =1:px
    %         for j = 1:py
    %            A = typecast(img(i,j,k),'float32');
    %         end
    %     end
    % end

    % fid = fopen(['sum_32float.raw'], 'w');
    % fwrite(fid, img, 'float32');
    % fclose(fid);
    sigma = 10;
    gausFilter = fspecial('gaussian', [5, 1], sigma); % detector blurring

    for k =1:py
        Proj(:,:,k) = img(:,k,:);
        %     Proj(:,:,k) = imfilter(Proj(:,:,k), gausFilter, 'replicate');
    end
    % figure;imshow(Proj,[])
    % imshow(Proj(:,:,100),[0,70]);
    % A = Proj(:,:,100); 
    %% Parameter settings
    nx = 600;ny = nx; % DPCT image size
    dx = single(10E-6);dy= dx;  %pixel size: dx*dy; Default Unit: m dy_det/dx=nx/px
    dy_det=single(10E-6); %detector pixel size, Default Unit: m

    nv=360;% number of views (projections)
    SO=single(d1);% the distance from source to isocenter; Default Unit: m
    OD=single(d2+d3);% the distance from isocenter to detector; Default Unit: m

    % SO=single(68.688*1E-3);% the distance from source to isocenter; Default Unit: m
    % OD=single(10.607*1E-3);% the distance from isocenter to detector; Default Unit: m

    nd=px;% number of detector
    sd_phi=single(2*pi/nv*(-nv/2:nv/2-1));% view angles
    y_os=single(0*dy_det);% isocenter offset with respect to the detector center; Default Unit: m
    y_det=single(((-nd/2:nd/2-1)+0.5)*dy_det)+y_os;% detector coordinate; Default Unit: m
    y_det2=single((-nd/2:nd/2)*dy_det)+y_os;% Default Unit: m

    %% Atx Parameter
    nt=1;
    Id_v=cell(1,nt);
    Id_v{1}=uint32(0:nv-1);
    id_X=[];Nv=zeros(1,nt);
    for i=1:nt
        id_X=[id_X (i-1)*ones(1,numel(Id_v{i}))];
        Nv(i)=numel(Id_v{i});
    end
    tmp_size=max(Nv);
    id_Y=zeros(tmp_size,nt);
    for i=1:nt
        id_Y(1:Nv(i),i)=Id_v{i};
    end
    para=struct('version',[],'GPU',[],...
        'SO',single(SO),'OD',single(OD),'dx',single(dx),'dy',single(dy),'nx',uint32(nx),'ny',uint32(ny),'nv',uint32(nv),...
        'sd_phi',sd_phi,'y_det',y_det,'id_X',uint32(id_X),'nt',uint32(nt),'dy_det',dy_det,'y_os',y_os,...
        'id_Y',uint32(id_Y),'Nv',uint32(Nv),'tmp_size',uint32(tmp_size),...
        'cos_phi',cos(sd_phi),'sin_phi',sin(sd_phi),'cos_det',[],'sin_det',[]);
    para.version=uint32(1);para.GPU=uint32(1); % new algorithm - GP
    % para.sin_det[10]
    %% Hilbert filter, for DPC-CT
    N=nd*2;
    fh_HL=zeros(1, N+1);
    for k=1:N+1
        fh_HL(k)=-2/((k-(N+1)/2)*dy_det*(2*pi)^2);
        if mod(k-(N+1)/2,2)==0
            fh_HL(k)=0;
        end
    end
    fh_HL = fh_HL(1, 1:N);
    fh_HL=single(fh_HL);
    %figure, plot(fh_HL)

    %% Ramp filter, for ACT
    N=nd*2; % filter length is two times of detector total length
    fh_RL=zeros(1,N); % Ramp filter
    for k=1:N
        fh_RL(k)=-1/((pi*(k-N/2-1)*dy_det)^2);
        if mod(k-N/2-1,2)==0
            fh_RL(k)=0;
        end
    end
    fh_RL(N/2+1)=1/(4*dy_det^2);
    fh_RL=single(fh_RL);
    %figure, plot(fh_RL)

    %% DPCT Filtering and FBP
    d3; % m distance between grating to detector
    
    Stv = 2*pi*d3/p2; % scaling factor for DPC-CT
    % for k = 1:py
    %     DPC_diff = (Proj(1:nd-1,:,k ) - Proj(2:nd,:,k)) / dx;
    %     DPC = Stv * [zeros(1, nv); squeeze(DPC_diff)];
    DPC = Proj;
    %figure;imshow(DPC(:,:,100),[]);
    for i=1:nv
        if strcmpi(model,'ACT')
            DPC_f(:,i) =conv(DPC(:,i),fh_RL,'same');
        end
        if strcmpi(model,'DPC-CT')
            DPC_f(:,i) =conv(DPC(:,i),fh_HL,'same');
        end

    end

    %         for i=1:nv
    %             DPC_f(:,i) =conv(DPC(:,i),fh_RL,'same');
    %         end

    %     theta=0:359;
    %     rec=iradon(DPC_f, theta, 'none');
    %     figure, imshow(rec,[]);
    %     rec
    DPC_CT=Atx_fan_mf(single(DPC_f), para);

    DPCT=reshape(DPC_CT,[nx ny]);
    if strcmpi(model,'ACT')
       DPCT = DPCT/ nv * pi *((SO+OD)/SO)*dy_det;
    end
    if strcmpi(model,'DPC-CT')
       DPCT = DPCT / nv * pi * ((SO+OD)/SO) / Stv*dy_det;
    end


    theta = 0:359;

    figure;
    test(:,:) = img(:,1,:);
    subplot(2,2,1);
    imshow(test,[]);
    title('Raw figure');


%     subplot(2,2,2);
%     plot(DPCT)
%     rec1=iradon(DPC_f, theta,'linear', 'none');
%     imshow(rec1,[]);
%     title('iradon');

    % subplot(2,2,2);
    % rec2=iradon(DPC_f, theta,'nearest', 'none');
    % imshow(rec2,[]);
    % title('Unfiltered nearst Backprojection');

    subplot(2,2,3);
    plot(DPCT(length(DPCT)/2, :))

    subplot(2,2,4);
    imshow(DPCT,[]);
    title('Self Backprojection');
    %figure,imshow(DPCT,[]);
    file_name_prefix = regexp(filename{ii},".raw",'split');
    %saveas(gca,[filePathout char(file_name_prefix(1)) '_self_' model '.png']);
    % %% Save DPCT images

    %strcat([ filePathout,file_name_prefix(1),'_self_DPCT.raw'])
    fid = fopen([ filePathout char(file_name_prefix(1)) '_self_' model '.raw'], 'w');
    if strcmpi(model,'ACT')
       fwrite(fid, DPCT, 'float32');
    end
    if strcmpi(model,'DPC-CT')
       fwrite(fid, DPCT, 'float32');
    end

    fclose(fid);
%     fid = fopen([ filePathout char(file_name_prefix(1)) '_self_DPCT_iradon.raw'], 'w');
%     fwrite(fid, rec1., 'float32');
%     fclose(fid);
    % fid = fopen([ filename '_iradon_DPCT.raw'], 'w');
    % fwrite(fid, rec1.*(-1), 'float32');
    % fclose(fid);
end