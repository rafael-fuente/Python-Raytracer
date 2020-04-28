from constants import *
from vector3 import vec3, rgb, extract
from functools import reduce as reduce 
from raytrace import raytrace
import lights
import numpy as np

class Material():
    def __init__(self, diff_color, max_ray_depth, roughness, diff_c, spec_c, n, texture = None, repeat = 1.0):
        

        self.diff_color = diff_color
        if isinstance(texture, np.ndarray):
            self.get_diffuse_color = self.get_texture_color

        
        self.texture = texture
        self.repeat = repeat
        self.texture = texture


        self.n = n
        # Instead of defining a index of refraction (n) for each wavelenght (computationally expensive) we aproximate defining the index of refraction
        # using a vec3 for red = 630 nm, green 555 nm, blue 475 nm, the most sensitive wavelenghts of human eye.
        
        # Index a refraction is a complex number. 
        # The real part is involved in how much light is reflected and model refraction direction via Snell Law.
        # The imaginary part of n is involved in how much light is reflected and absorbed. For non-transparent materials like metals is usually between (0.1j,3j)
        # and for transparent materials like glass is  usually between (0.j , 1e-7j)

        
        self.max_ray_depth = max_ray_depth    
        self.roughness = roughness
        self.spec_c = spec_c
        self.diff_c = diff_c
        
    def get_diffuse_color(self, M, collider, D, O):
        return self.diff_color
    
    def get_texture_color(self, M, collider, D, O):
        u,v = self.assigned_surface.get_uv(M, collider)
        im = self.texture[-((v * self.texture.shape[0]*self.repeat ).astype(int)% self.texture.shape[0]) , (u   * self.texture.shape[1]*self.repeat).astype(int) % self.texture.shape[1]  ].T
        color = vec3(im[0],im[1],im[2])
        return color*self.diff_color
    

    def shader(self, collider, ray_origin, ray_dir,  hit_distance ,hit_orientation, scene, ray_depth, ray_n):
        M = (ray_origin + ray_dir * hit_distance)                     # intersection point
        N = collider.get_Normal(M).normalize()  * hit_orientation                     # normal 
        

        diff_color = self.get_diffuse_color(M, collider, ray_dir, ray_origin) * self.diff_c

        # Ambient
        color = scene.ambient_color * diff_color

        for Light in scene.Light_list:

            if isinstance(Light, lights.DirectionalLight):
                dist_light = SKYBOX_DISTANCE
                L = Light.Ldir                                  # direction to light
                NdotL = np.maximum(N.dot(L), 0.)
                lv = NdotL
            elif isinstance(Light, lights.PointLight):
                dist_light = np.sqrt((Light.pos - M).dot(Light.pos - M))
                L = (Light.pos - M)*(1./(dist_light))            # direction to light
                NdotL = np.maximum(N.dot(L), 0.)
                lv = NdotL/(dist_light**2.) * 100.
                

                
            V = ray_dir*-1.                            # direction to ray origin
            nudged = M + N * .000001                  # M nudged to avoid itself
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
            color += Light.color * diff_color * lv * seelight 
            
            if self.roughness != 0.0:                
                #Fresnel Factor for specular highlight  (Schlick’s approximation)
                F0 = np.abs((ray_n - self.n)/(ray_n  + self.n))**2
                cosθ = np.clip(V.dot(H), 0.0, 1.)
                F = F0 + (1. - F0)*(1.- cosθ)**5

   
                # Phong shading (specular highlight)
                a = 2./(self.roughness**2.) - 2.
                Dphong =  np.power(np.clip(N.dot(H), 0., 1.), a) * (a + 2.)/(2.*np.pi)
                
                # Cook-Torrance model
                color += Light.color* F  * Dphong  /(4. * np.clip(N.dot(V) * NdotL, 0.001, 1.) ) * seelight * lv * self.spec_c

        # Reflection
        if ray_depth < self.max_ray_depth:

            # Fresnel Factor for reflections  (Schlick’s approximation)

            F0 = np.abs((scene.n - self.n)/(scene.n  + self.n))**2
            cosθ = np.clip(V.dot(N),0.0,1.)
            F = F0 + (1. - F0)*(1.- cosθ)**5
            reflected_ray_dir = (ray_dir - N * 2. * ray_dir.dot(N)).normalize()
            color += (raytrace(nudged, reflected_ray_dir, scene, ray_depth + 1, ray_n))*F
        return color






class RefractiveMaterial(Material):
    def shader(self, collider, ray_origin, ray_dir,  hit_distance ,hit_orientation, scene, ray_depth, ray_n):
        M = (ray_origin + ray_dir * hit_distance)                     # intersection point
        N = collider.get_Normal(M).normalize()  * hit_orientation     # normal 

        diff_color = self.get_diffuse_color(M, collider, ray_dir, ray_origin) * self.diff_c

        # Ambient
        color = scene.ambient_color * diff_color

                
        V = ray_dir*-1.                            # direction to ray origin
        nudged = M + N * .000001                  # M nudged to avoid itself


        # compute reflection and refraction 
        # a paper explaining formulas used: 
        # https://graphics.stanford.edu/courses/cs148-10-summer/docs/2006--degreve--reflection_refraction.pdf
        # reallistic refraction is expensive. (requires exponential complexity because each ray is divided in two)

        if ray_depth < self.max_ray_depth:

            """
            if hit_orientation== UPWARDS:
               #ray enter in the material
            if hit_orientation== UPDOWN:
               #ray get out of the material   
            """
            n1 = ray_n
            n2 = vec3.where(hit_orientation== UPWARDS,self.n,scene.n)

            n1_div_n2 =  vec3.real(n1)/vec3.real(n2) 
            cosθi = V.dot(N)
            sin2θt = (n1_div_n2)**2 * (1.-cosθi**2)

            # compute complete fresnel term
            cosθt = vec3.sqrt(1. - (n1/n2)**2 * (1.-cosθi**2)  )
            r_per = (n1*cosθi - n2*cosθt)/(n1*cosθi + n2*cosθt)
            r_par = -1.*(n1*cosθt - n2*cosθi)/(n1*cosθt + n2*cosθi) 
            F = (np.abs(r_per)**2 + np.abs(r_par)**2)/2.
            
            # compute reflection
            reflected_ray_dir = (ray_dir - N * 2. * ray_dir.dot(N)).normalize()
            color += (raytrace(nudged, reflected_ray_dir, scene, ray_depth + 1,ray_n))*F
            


            # compute refraction 
            # Spectrum dispersion is not implemented. 
            # We approximate refraction direction averaging index of refraction of each wavelenght
            n1_div_n2_aver = n1_div_n2.average()
            sin2θt = (n1_div_n2_aver)**2 * (1.-cosθi**2)

            non_TiR = (sin2θt <= 1.)
            if np.any(non_TiR): # avoid total internal reflection

                refracted_ray_dir = (ray_dir*(n1_div_n2_aver) + N*(n1_div_n2_aver * cosθi - np.sqrt(1-np.clip(sin2θt,0,1)))).normalize() 
                nudged = M - N * .000001  #nudged for refraction
                T = 1. - F
                refracted_color = (raytrace(nudged.extract(non_TiR), 
                                           refracted_ray_dir.extract(non_TiR), 
                                           scene, 
                                           ray_depth + 1, 
                                           n2.extract(non_TiR)))*T.extract(non_TiR) 
                color += refracted_color.place(non_TiR)
            
                
            # absorption:
            # approximation using wavelength for red = 630 nm, green 550 nm, blue 475 nm
            color = color *vec3.exp(-2.*vec3.imag(ray_n)*2.*np.pi/vec3(630,550,475) * 1e9* hit_distance)
        return color


class SkyBox_Material(Material):
    def __init__(self, cubemap):
        self.texture = cubemap
        self.repeat = 1.0
        
    def shader(self, collider, ray_origin, ray_dir,  hit_distance ,hit_orientation, scene, ray_depth, n):
        M = (ray_origin + ray_dir * hit_distance)  
        return self.get_texture_color(M, collider,ray_dir, ray_origin)

    def get_texture_color(self, M, collider, D, O):
        u,v = self.assigned_surface.get_uv(M, collider)
        im = self.texture[-((v * self.texture.shape[0]*self.repeat ).astype(int)% self.texture.shape[0]) , (u   * self.texture.shape[1]*self.repeat).astype(int) % self.texture.shape[1]  ].T
        color = vec3(im[0],im[1],im[2])
        return color 
