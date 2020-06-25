from ..utils.constants import *
from ..utils.vector3 import vec3, rgb, extract
from functools import reduce as reduce 
from ..ray import Ray, get_raycolor
from .. import lights
import numpy as np
from . import Material
from ..utils.image_functions import load_image

class ThinFilmInterference(Material):
    def __init__(self, thickness, noise = 0.,**kwargs):
        super().__init__(**kwargs)
        self.thickness = thickness

        # precomputed reflectance vs cosθI (vertical axis) and thickness (horizontal axis)
        self.thin_film_interference_reflectance = load_image("sightpy/textures/thin_film_interference_n=1.4.png")
        self.thickness_noise = load_image("sightpy/textures/noise.png")
        self.thickness_noise = (self.thickness_noise[:,:,0])
        self.noise_factor = noise

    def get_color(self, scene, ray, hit):
        
        hit.point = (ray.origin + ray.dir * hit.distance) # intersection point
        N = hit.material.get_Normal(hit)     # normal 

        # Ambient
        color = rgb(0.,0.,0.)

        V = ray.dir*-1.                            # direction to ray origin
        

        if ray.depth < hit.surface.max_ray_depth:

            """
            if hit_orientation== UPWARDS:
               #ray enter in the material
            if hit_orientation== UPDOWN:
               #ray get out of the material   
            """

            cosθi = V.dot(N)

            u,v = hit.get_uv()
            thickness = self.thickness 
            if self.noise_factor != 0.:
                thickness += self.noise_factor*(self.thickness_noise[-((v * self.thickness_noise.shape[0]*0.5 ).astype(int)% self.thickness_noise.shape[0]) , (u   * self.thickness_noise.shape[1]*0.5).astype(int) % self.thickness_noise.shape[1]  ].T - 0.5)
                Fim = self.thin_film_interference_reflectance[(cosθi* self.thin_film_interference_reflectance.shape[0]).astype(int),    thickness.astype(int)     ]
            else:
                Fim = self.thin_film_interference_reflectance[(cosθi* self.thin_film_interference_reflectance.shape[0]).astype(int),    int(thickness)    ]
            
            F = vec3(Fim[:,0],Fim[:,1],Fim[:,2])
            # compute reflection
            reflected_ray_dir = (ray.dir - N * 2. * ray.dir.dot(N)).normalize()

            nudged = hit.point + N * .000001                  # M nudged to avoid itself
            color += (scene.ambient_color + get_raycolor(Ray(nudged, reflected_ray_dir, ray.depth + 1, ray.n, ray.reflections + 1, ray.transmissions,  ray.diffuse_reflections), scene))*F
            


            # because the film is very thin (nm) we ignore refraction for transmitted ray.

            transmitted_ray_dir = ray.dir 
            nudged = hit.point - N * .000001  #nudged for transmitted ray
            T = 1. - F
            transmitted_color = get_raycolor( Ray(nudged, transmitted_ray_dir, ray.depth + 1, ray.n, ray.reflections, ray.transmissions + 1,  ray.diffuse_reflections), scene  )*T
            color += transmitted_color
        return color