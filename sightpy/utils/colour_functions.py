import numpy as np

def sRGB_linear_to_sRGB(rgb_linear):

    '''sRGB standard for gamma inverse correction.'''
    rgb = np.where( rgb_linear <= 0.00304,  12.92 * rgb_linear,  1.055 * np.power(rgb_linear, 1.0/2.4) - 0.055)
    
    # clip intensity if needed (rgb values > 1.0) by scaling
    rgb_max =  np.amax(rgb, axis=0)  + 0.00001  # avoid division by zero
    intensity_cutoff = 1.0
    rgb = np.where(rgb_max > intensity_cutoff, rgb * intensity_cutoff / (rgb_max), rgb)
    
    return rgb


def sRGB_to_sRGB_linear(rgb):

    '''sRGB standard for gamma inverse correction.'''    
    rgb_linear = np.where( rgb <= 0.03928,  rgb / 12.92,  np.power((rgb + 0.055) / 1.055,  2.4))

    return rgb_linear

