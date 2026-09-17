# two sphere to see the reslution of the system
amp = 1 
olength1 = 2.93*um  *amp            # Size of spherical sample
opos_x1 = -1.*olength1/2.      # Position of the object
opos_y1 = -1.*olength1/2.
sphere_1 = [olength1,opos_x1,opos_y1+0.3*um*amp-1.*olength1-1.0*um*amp]
sphere_11 = [olength1,opos_x1,opos_y1-0.3*um*amp-1.*olength1-1.0*um*amp]
sphere_2 = [olength1,opos_x1,opos_y1+0.4*um*amp]
sphere_21 = [olength1,opos_x1,opos_y1-0.4*um*amp]
sphere_3 = [olength1,opos_x1,opos_y1+0.5*um*amp+1.*olength1+1.0*um*amp]
sphere_31 = [olength1,opos_x1,opos_y1-0.5*um*amp+1.*olength1+1.0*um*amp]
Object_sphere_1 = Object_sphere(total_count, wave_number, sphere_1, total_length, fs,material,xenergy)
Object_sphere_11 = Object_sphere(total_count, wave_number, sphere_11, total_length, fs,material,xenergy)

Object_sphere_2 = Object_sphere(total_count, wave_number, sphere_2, total_length, fs,material,xenergy)
Object_sphere_21 = Object_sphere(total_count, wave_number, sphere_21, total_length, fs,material,xenergy)

Object_sphere_3 = Object_sphere(total_count, wave_number, sphere_3, total_length, fs,material,xenergy)
Object_sphere_31 = Object_sphere(total_count, wave_number, sphere_31, total_length, fs,material,xenergy)
# Object_cylinder_1 = Object_cylinder_side(total_count, wave_number, cylinder_1, total_length, fs,material,xenergy)
Object_sphere_to = Object_sphere_1 + Object_sphere_11 +  Object_sphere_2 + Object_sphere_21 + Object_sphere_3 + Object_sphere_31
sourceAobj = source2obj * Object_sphere_to