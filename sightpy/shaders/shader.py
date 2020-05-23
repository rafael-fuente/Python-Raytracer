from ..utils.constants import *
from ..utils.vector3 import vec3, rgb, extract
from functools import reduce as reduce 
from ..ray import Ray, raytrace
from .. import lights
from ..utils.image_functions import load_image
import numpy as np
from abc import abstractmethod 

class Shader:
    @abstractmethod   
    def get_color(self,material, collider, scene, ray, hit_distance ,hit_orientation):
        pass