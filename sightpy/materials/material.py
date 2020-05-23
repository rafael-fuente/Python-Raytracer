from ..utils.constants import *
from ..utils.vector3 import vec3, rgb, extract
from functools import reduce as reduce 
from ..ray import Ray, raytrace
from .. import lights
from ..utils.image_functions import load_image, load_image_as_linear_sRGB
import numpy as np

class Material():
    def __init__(self,shader,  texture = None, normalmap = None,  repeat = 1.0):
        

        if texture != None:
            texture = load_image_as_linear_sRGB("sightpy/textures/" + texture)
        self.texture = texture

        if normalmap != None:
            normalmap = load_image("sightpy/normalmaps/" + normalmap)
        self.normalmap = normalmap


        self.repeat = repeat
        self.shader = shader
        # Instead of defining a index of refraction (n) for each wavelenght (computationally expensive) we aproximate defining the index of refraction
        # using a vec3 for red = 630 nm, green 555 nm, blue 475 nm, the most sensitive wavelenghts of human eye.
        
        # Index a refraction is a complex number. 
        # The real part is involved in how much light is reflected and model refraction direction via Snell Law.
        # The imaginary part of n is involved in how much light is reflected and absorbed. For non-transparent materials like metals is usually between (0.1j,3j)
        # and for transparent materials like glass is  usually between (0.j , 1e-7j)

    
    def get_texture_color(self, hit):
        u,v = hit.get_uv()
        im = self.texture[-((v * self.texture.shape[0]*self.repeat ).astype(int)% self.texture.shape[0]) , (u   * self.texture.shape[1]*self.repeat).astype(int) % self.texture.shape[1]  ].T
        color = vec3(im[0],im[1],im[2])
        return color

    def get_Normal(self, hit):
        N_coll = hit.collider.get_Normal(hit)
        if self.normalmap is not None:
            u,v = hit.get_uv()
            im = self.normalmap[-((v * self.normalmap.shape[0]*self.repeat ).astype(int)% self.normalmap.shape[0]) , (u   * self.normalmap.shape[1]*self.repeat).astype(int) % self.normalmap.shape[1]  ].T
            N_map = (vec3(im[0] - 0.5,im[1] - 0.5,im[2] - 0.5)) * 2.0 
            return N_map.matmul(hit.collider.inverse_basis_matrix).normalize()*hit.orientation
        else:
            return N_coll*hit.orientation



    def set_texture(self, texture, repeat = 1.0):
        self.texture = load_image_as_linear_sRGB("sightpy/textures/" + texture)
        self.repeat = repeat

    def set_normalmap(self, normalmap,repeat= 1.0):
        self.normalmap = load_image("sightpy/normalmaps/" + normalmap)
        self.repeat = repeat


