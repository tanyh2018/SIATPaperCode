# -*- coding: utf-8 -*-

from math import pi as _pi

'''

Considering the case of nano CT,
the standard unit is set to be um.

One can modify the following code to change the reference unit.

'''

um = 1.0 # 1e-6*m
nm = 1e-3*um # 1e-9*m
m  = 1e6*um
cm = 1e4*um # 1e-2*m
mm = 1e3*um #1e-3*m

rad=1.0
mrad=1e-3*rad
urad=1e-6*rad

deg=(2*_pi*rad)/360 #[rad] assuming all math libs use rad, just write 123*deg

PI = _pi
