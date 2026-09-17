'''

This code is mainly designed to model a grating-based differential phase contrast (DPC) imaging device where the diffraction is essential.
The functions in this toolbox represent either optical elements or necessary steps during the propagation of the X-rays (or visible lights).
It contains different types of gratings, samples, calculation method of free space diffraction, extraction of phase signals and so on.
Such program operates on a large data structure. By default, square two-dimensional complex arrays of the optical field are considered.
Through the calculation, it would hopefully help estimate the output image from the DPC imaging system.
To enhance the robustness of the code, the framework of this program is referenced to the work of LightPipes by Gleb Vdovin.
However, the core functions and main research objectives are different from that work.

Written by Jiecheng @ Feb, 2022

'''


__all__ = [
    'Initialize'
]
#physical units like m, mm, rad, deg, ...
from units import *

__all__.extend([
    'm', 'cm', 'mm', 'um', 'nm',
    'rad', 'mrad', 'urad', 'deg',
    'PI'
])
# avoid modified
__all__ = tuple(__all__)

# import necessary modules
import numpy as np


import math
def Initialize(size, N):
    """
    *Initiates a field with a grid size, a wavelength and a grid dimension.*

    :param size: size of the square grid
    :type size: int, float
    :param labda: the wavelength of the output field
    :type labda: int, float
    :param N: the grid dimension 
    :type N: int

    """

    grids = np.zeros([N[0],N[1]])
    fsx = size[1] / N[1]
    fsy = size[0] / N[0]
    for i in range(N[0]):
        for j in range(N[1]):
            grids[i][j] =  (fsx * (j-N[1]/2.))**2.
    return grids

def Initialize_1D(size, N):
    rightmost_areay = (size[0] - 1.) / 2.
    leftmost_areay = -1. * size[0] / 2.
    rightmost_areax = (size[1] - 1.) / 2.
    leftmost_areax = -1. * size[1] / 2.
    gridsy = np.linspace(leftmost_areay,rightmost_areay,N[0])
    gridsx = np.linspace(leftmost_areax,rightmost_areax,N[1])
    return gridsx,gridsy 





