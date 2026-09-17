% not considerting horizontal lines
% angle in radian
function f = RadialAverage(Spectrum, AngularRange)

Im = Spectrum; % spectrum, assume a squared size
theta = AngularRange; % start from 0, unit: radian

cen_x = floor(length(Im(:, 1))/2) + 1;
cen_y = cen_x;
r = floor(length(Im(:, 1))/2); % Max radius, unit: pixel

Im = [Im, Im(:, 1)];
Im = [Im; Im(1, :)];
Im(cen_x, cen_y) = 0; % set center to zero

d_theta = 0.1; % unit: radian

f = zeros(1, r+1);
N = 0;
ra = 3.14/180;
% 0 degree is along the up-vertical image direction
for angle = [30*ra:d_theta:60*ra, 120*ra:d_theta:150*ra, 210*ra:d_theta:240*ra, 300*ra:d_theta:330*ra]
    N = N + 1;
    for radius = 0:1:r
        u = radius * cos(angle) + cen_x;
        v = radius * sin(angle) + cen_y;
        u_m = floor(u);
        u_p = ceil(u);
        v_m = floor(v);
        v_p = ceil(v);
        
        l1 = sqrt((u_m-u)^2+(v_p-v)^2);
        l2 = sqrt((u_p-u)^2+(v_p-v)^2);
        l3 = sqrt((u_p-u)^2+(v_m-v)^2);
        l4 = sqrt((u_m-u)^2+(v_m-v)^2);
        
        data1 = Im(u_m, v_p);
        data2 = Im(u_p, v_p);
        data3 = Im(u_p, v_m);
        data4 = Im(u_m, v_m);
        
        % inverse distance weighting
        if l1*l2*l3*l4 == 0
            f(1, radius+1) = f(1, radius+1) + (data1 + data2 + data3 + data4) / 4;
        else
            f(1, radius+1) = f(1, radius+1) + (data1/l1 + data2/l2 + data3/l3 + data4/l4) / (1/l1 + 1/l2 + 1/l3 + 1/l4);
        end
    end
end
f = f / N;
end