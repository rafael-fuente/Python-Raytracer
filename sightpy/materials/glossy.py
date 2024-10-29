from ..utils.constants import *
from ..utils.vector3 import vec3, rgb, extract
from functools import reduce as reduce 
from ..ray import Ray, get_raycolor
from .. import lights
import numpy as np
from . import Material
from ..textures import *

class Glossy(Material):
    def __init__(self, diff_color, roughness, spec_coeff, diff_coeff, n, **kwargs):
        super().__init__(**kwargs)

        if isinstance(diff_color, vec3):
            self.diff_texture = solid_color(diff_color)
        elif isinstance(diff_color, texture):
            self.diff_texture = diff_color

        self.roughness = roughness
        self.diff_coeff = diff_coeff
        self.spec_coeff = spec_coeff
        self.n = n # index of refraction


    def get_color(self, scene, ray, hit):

        hit.point = (ray.origin + ray.dir * hit.distance) # intersection point
        N = hit.material.get_Normal(hit)     # normal 
 
        diff_color = self.diff_texture.get_color(hit)* self.diff_coeff

        # Ambient
        color = scene.ambient_color * diff_color
        V = ray.dir*-1. 
        nudged = hit.point + N * .000001                  # M nudged to avoid itself
        
        for light in scene.Light_list:

            L = light.get_L(hit.point)                                         # direction to light
            dist_light = light.get_distance(hit.point)                # distance to light
            NdotL = np.maximum(N.dot(L), 0.)    
            lv = light.get_irradiance(dist_light, NdotL)              # amount of intensity that falls on the surface
            

                                      # direction to ray origin
            
            H = (L + V).normalize()                   # Half-way vector


            
            
            # Shadow: find if the point is shadowed or not.
            # This amounts to finding out if M can see the light
            # Shoot a ray from M to L and check what object is the nearest  
            if not scene.shadowed_collider_list == []:
                inters = [s.intersect(nudged, L) for s in scene.shadowed_collider_list]
                light_distances, light_hit_orientation = zip(*inters)
                light_nearest = reduce(np.minimum, light_distances)
                seelight = (light_nearest >= dist_light)
            else:
                seelight = 1.

            # Lambert shading (diffuse)
            color +=  diff_color * lv * seelight 
            
            if self.roughness != 0.0:                
                #Fresnel Factor for specular highlight  (Schlick’s approximation)
                F0 = np.abs((ray.n - self.n)/(ray.n  + self.n))**2
                cosθ = np.clip(V.dot(H), 0.0, 1.)
                F = F0 + (1. - F0)*(1.- cosθ)**5

   
                # Phong shading (specular highlight)
                a = 2./(self.roughness**2.) - 2.
                Dphong =  np.power(np.clip(N.dot(H), 0., 1.), a) * (a + 2.)/(2.*np.pi)
                
                # Cook-Torrance model
                color +=  F  * Dphong  /(4. * np.clip(N.dot(V) * NdotL, 0.001, 1.) ) * seelight * lv * self.spec_coeff

        # Reflection
        if ray.depth < hit.surface.max_ray_depth:

            # Fresnel Factor for reflections  (Schlick’s approximation)

            F0 = np.abs((scene.n - self.n)/(scene.n  + self.n))**2
            cosθ = np.clip(V.dot(N),0.0,1.)
            F = F0 + (1. - F0)*(1.- cosθ)**5
            reflected_ray_dir = (ray.dir - N * 2. * ray.dir.dot(N)).normalize()
            color += (get_raycolor(Ray(nudged, reflected_ray_dir, ray.depth + 1, ray.n, ray.reflections + 1, ray.transmissions, ray.diffuse_reflections), scene))*F

        return color