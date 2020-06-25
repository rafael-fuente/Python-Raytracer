from ..utils.constants import *
from ..utils.vector3 import vec3, rgb, extract
from functools import reduce as reduce 
from ..ray import Ray, get_raycolor
from .. import lights
from ..utils.image_functions import load_image, load_image_as_linear_sRGB
import numpy as np
from abc import abstractmethod 

class Material():
    def __init__(self,normalmap = None):
        
        if normalmap != None:
            normalmap = load_image("sightpy/normalmaps/" + normalmap)
        self.normalmap = normalmap


    def get_Normal(self, hit):
        N_coll = hit.collider.get_Normal(hit)
        if self.normalmap is not None:
            u,v = hit.get_uv()
            im = self.normalmap[-((v * self.normalmap.shape[0]*self.repeat ).astype(int)% self.normalmap.shape[0]) , (u   * self.normalmap.shape[1]*self.repeat).astype(int) % self.normalmap.shape[1]  ].T
            N_map = (vec3(im[0] - 0.5,im[1] - 0.5,im[2] - 0.5)) * 2.0 
            return N_map.matmul(hit.collider.inverse_basis_matrix).normalize()*hit.orientation
        else:
            return N_coll*hit.orientation

    def set_normalmap(self, normalmap,repeat= 1.0):
        self.normalmap = load_image("sightpy/normalmaps/" + normalmap)
        self.repeat = repeat

    @abstractmethod   
    def get_color(self, scene, ray, hit):
        pass
