from ..utils.constants import *
from ..utils.vector3 import vec3, rgb, extract
from functools import reduce as reduce 
from ..ray import Ray, raytrace
from .. import lights
import numpy as np
from . import Shader

class Refractive(Shader):
    def __init__(self, n, max_ray_depth):
        self.n = n # index of refraction
        self.max_ray_depth = max_ray_depth


    def get_color(self, scene, ray, hit):
        
        hit.point = (ray.origin + ray.dir * hit.distance) # intersection point
        N = hit.material.get_Normal(hit)     # normal 

        color = rgb(0.,0.,0.)

        V = ray.dir*-1.                            # direction to ray origin
        nudged = hit.point + N * .000001                  # M nudged to avoid itself
        # compute reflection and refraction 
        # a paper explaining formulas used: 
        # https://graphics.stanford.edu/courses/cs148-10-summer/docs/2006--degreve--reflection_refraction.pdf
        # reallistic refraction is expensive. (requires exponential complexity because each ray is divided in two)

        if ray.depth < self.max_ray_depth:

            """
            if hit_orientation== UPWARDS:
               #ray enter in the material
            if hit_orientation== UPDOWN:
               #ray get out of the material   
            """
            n1 = ray.n
            n2 = vec3.where(hit.orientation== UPWARDS,self.n,scene.n)

            n1_div_n2 =  vec3.real(n1)/vec3.real(n2) 
            cosθi = V.dot(N)
            sin2θt = (n1_div_n2)**2 * (1.-cosθi**2)

            # compute complete fresnel term
            cosθt = vec3.sqrt(1. - (n1/n2)**2 * (1.-cosθi**2)  )
            r_per = (n1*cosθi - n2*cosθt)/(n1*cosθi + n2*cosθt)
            r_par = -1.*(n1*cosθt - n2*cosθi)/(n1*cosθt + n2*cosθi) 
            F = (np.abs(r_per)**2 + np.abs(r_par)**2)/2.
            
            # compute reflection
            reflected_ray_dir = (ray.dir - N * 2. * ray.dir.dot(N)).normalize()
            color += (raytrace(Ray(nudged, reflected_ray_dir, ray.depth + 1, ray.n, ray.reflections + 1, ray.transmissions), scene))*F
            


            # compute refraction 
            # Spectrum dispersion is not implemented. 
            # We approximate refraction direction averaging index of refraction of each wavelenght
            n1_div_n2_aver = n1_div_n2.average()
            sin2θt = (n1_div_n2_aver)**2 * (1.-cosθi**2)

            non_TiR = (sin2θt <= 1.)
            if np.any(non_TiR): # avoid total internal reflection

                refracted_ray_dir = (ray.dir*(n1_div_n2_aver) + N*(n1_div_n2_aver * cosθi - np.sqrt(1-np.clip(sin2θt,0,1)))).normalize() 
                nudged = hit.point - N * .000001  #nudged for refraction
                T = 1. - F
                refracted_color = (raytrace( Ray(nudged, refracted_ray_dir, ray.depth + 1, n2, ray.reflections, ray.transmissions + 1).extract(non_TiR), scene)  )*T.extract(non_TiR) 
                color += refracted_color.place(non_TiR)
            
                
            # absorption:
            # approximation using wavelength for red = 630 nm, green 550 nm, blue 475 nm
            color = color *vec3.exp(-2.*vec3.imag(ray.n)*2.*np.pi/vec3(630,550,475) * 1e9* hit.distance)
        return color