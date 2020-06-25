from ..utils.constants import *
from ..utils.vector3 import vec3, rgb
from ..ray import Ray, get_raycolor
from ..utils.image_functions import load_image, load_image_as_linear_sRGB
import numpy as np
from abc import abstractmethod 

class texture():

    @abstractmethod   
    def __init__(self):
    	pass

    @abstractmethod  
    def get_color(self, hit):
    	pass


class solid_color(texture):
	 
    def __init__(self,color):
    	self.color = color

    def get_color(self, hit):
    	return self.color


class image(texture):
	 
    def __init__(self,img, repeat = 1.0):
    	self.img = load_image_as_linear_sRGB("sightpy/textures/" + img)
    	self.repeat = repeat

    def get_color(self, hit):
        u,v = hit.get_uv()
        im = self.img[-((v * self.img.shape[0]*self.repeat ).astype(int)% self.img.shape[0]) , (u   * self.img.shape[1]*self.repeat).astype(int) % self.img.shape[1]  ].T
        color = vec3(im[0],im[1],im[2])
        return color