function DPCT = recfbp(projection,model,Nimg2)
% 投影重建
d1=11563111111111111111111;d2=0.2023;d3=0.202; %unit m
p2 = 1e-6; % m peirod of the stripes
px = Nimg2(1);
py=1;
pz = Nimg2(2);
img = reshape(projection,Nimg2(1),py,Nimg2(2));
for k =1:py
    Proj(:,:,k) = img(:,k,:);
end

%% Parameter settings
nx = 512;ny = nx; % DPCT image size
dx = single(0.1e-7);dy= dx;  %pixel size: dx*dy; Default Unit: m dy_det/dx=nx/px
dy_det=single(0.1e-7); %detector pixel size, Default Unit: m

nv=Nimg2(2);% number of views (projections)
SO=single(d1);% the distance from source to isocenter; Default Unit: m
OD=single(d2+d3);% the distance from isocenter to detector; Default Unit: m

nd=px;% number of detector
%sd_phi=single(pi/nv*(-nv/2.0:0.5*nv/180:nv/2.0));
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

%% DPCT Filtering and FBP
Stv = 2*pi*d3/p2; % scaling factor for DPC-CT
DPC = Proj;
for i=1:nv
    if strcmpi(model,'ACT')
        DPC_f(:,i) =conv(DPC(:,i),fh_RL,'same');
    end
    if strcmpi(model,'DPC-CT')
        DPC_f(:,i) =conv(DPC(:,i),fh_HL,'same');
    end
end

%% parallel

% theta = 0:0.5:359.5;
% N=512;
% DPCT=iradon(DPC_f, theta,'linear','none',512)*5e-19;
% DPCT=iradon(DPC_f, theta,'nearest');

DPC_CT=Atx_fan_mf(single(DPC_f), para);
DPCT=reshape(DPC_CT,[nx ny]);
if strcmpi(model,'ACT')
   DPCT = DPCT/ nv * pi *((SO+OD)/SO)*dy_det*2.4669e-11;
end
if strcmpi(model,'DPC-CT')
   DPCT = DPCT / nv * pi * ((SO+OD)/SO) *dy_det*4.9338e-4*2.5;
end