from ..utils.constants import *
from ..utils.vector3 import vec3
import numpy as np


class Primitive:    
    def __init__(self, center, material, max_ray_depth = 1, shadow = True):
        self.center = center
        self.material = material
        self.material.assigned_primitive = self
        self.shadow = shadow
        self.collider_list = [] 
        self.max_ray_depth = max_ray_depth
        
    def rotate(self, θ, u):
        
        u = u.normalize()
        θ = θ/180 *np.pi 
        cosθ = np.cos(θ)
        sinθ = np.sqrt(1-cosθ**2) * np.sign(θ)
        
        #rotation matrix along u axis
        M = np.array([
                       [cosθ + u.x*u.x * (1-cosθ),      u.x*u.y*(1-cosθ) - u.z*sinθ,         u.x*u.z*(1-cosθ) +u.y*sinθ],
                       [u.y*u.x*(1-cosθ) + u.z*sinθ,        cosθ + u.y**2 * (1-cosθ),       u.y*u.z*(1-cosθ) -u.x*sinθ],
                       [u.z*u.x*(1-cosθ) -u.y*sinθ,             u.z*u.y*(1-cosθ) + u.x*sinθ,         cosθ + u.z*u.z*(1-cosθ)]
                      ])
        for c in self.collider_list:
            c.rotate(M, self.center)
            
