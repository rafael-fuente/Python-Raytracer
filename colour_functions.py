import numpy as np

def sRGB_linear_to_sRGB(rgb_linear):

    def srgb_gamma(x):
        '''sRGB standard for gamma inverse correction.'''
        return np.where( x <= 0.00304,  12.92 * x,  1.055 * np.power(x, 1.0/2.4) - 0.055)
    
    rgb = srgb_gamma(rgb_linear)
    
    # clip intensity if needed (rgb values > 1.0) by scaling
    rgb_max =  np.amax(rgb, axis=0)
    intensity_cutoff = 1.0
    rgb = np.where(rgb_max > intensity_cutoff, rgb * intensity_cutoff / rgb_max, rgb)
    
    return rgb


def sRGB_to_sRGB_linear(rgb):

    def srgb_gamma_invert (x):
        '''sRGB standard for gamma inverse correction.'''
        return np.where( x <= 0.03928,  x / 12.92,  np.power((x + 0.055) / 1.055,  2.4))
    
    rgb_linear = srgb_gamma_invert(rgb)

