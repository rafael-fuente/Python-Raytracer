from PIL import Image
import numpy as np
import time
import colour_functions as cf

from constants import *
from vector3 import vec3, rgb
from raytrace import raytrace
import surfaces
import lights


class Camera():
    def __init__(self, screen_width = 400 ,screen_height = 300, position = vec3(0., 0.25, 1.), look_at = vec3(0., 0.25, 0.), camera_width = 1.,  camera_depth = 1. ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.camera_screen_scale = float(screen_width) / screen_height

        self.position = position
        self.camera_width = camera_width
        self.camera_height = camera_width/self.camera_screen_scale
        self.camera_depth = camera_depth 
        self.cameraFwd = (look_at - position).normalize()
        self.cameraRight = (self.cameraFwd.cross(vec3(0.,1.,0.))).normalize()
        self.cameraUp = self.cameraRight.cross(self.cameraFwd)

        # Screen coordinates:
        x = np.linspace(-self.camera_width, self.camera_width, self.screen_width)
        y = np.linspace(self.camera_height, -self.camera_height, self.screen_height)

        xx,yy = np.meshgrid(x,y)
        x = xx.flatten()
        y = yy.flatten()

        self.ray_dir = (self.cameraUp*y  +  self.cameraRight*x  + self.cameraFwd*self.camera_depth ).normalize()


    def rotate(self, θ, u):
        
        u = u.normalize()
        θ = θ/180 *np.pi 
        cosθ = np.cos(θ)
        sinθ = np.sqrt(1-cosθ**2) * np.sign(θ)
        
        M = np.array([
                     [cosθ + u.x*u.x * (1-cosθ),      u.x*u.y*(1-cosθ) - u.z*sinθ,         u.x*u.z*(1-cosθ) +u.y*sinθ],
                     [u.y*u.x*(1-cosθ) + u.z*sinθ,    cosθ + u.y**2 * (1-cosθ),            u.y*u.z*(1-cosθ) -u.x*sinθ],
                     [u.z*u.x*(1-cosθ) -u.y*sinθ,     u.z*u.y*(1-cosθ) + u.x*sinθ,         cosθ + u.z*u.z*(1-cosθ)]
                    ])
        self.ray_dir = self.ray_dir.matmul(M)


class Scene():
    def __init__(self, ambient_color = rgb(0.01, 0.01, 0.01), n = vec3(1.0,1.0,1.0)) :
        # n = index of refraction (by default index of refraction of air)
        
        self.scene_surfaces = []
        self.collider_list = []
        self.shadowed_collider_list = []
        self.Light_list = []
        self.ambient_color = ambient_color
        self.n = n
 
    def add_Camera(self,camera):
        self.camera = camera


    def add_PointLight(self, pos, color):
        self.Light_list += [lights.PointLight(pos, color)]
        
    def add_DirectionalLight(self, Ldir, color):
        self.Light_list += [lights.DirectionalLight(Ldir.normalize() , color)]       
        
    def add_Surface(self,surface):
        self.scene_surfaces += [surface]
        self.collider_list += surface.collider_list
        
        if surface.shadow == True:
            self.shadowed_collider_list += surface.collider_list
            
        
    def add_SkyBox(self, cubemap):
        surface = surfaces.SkyBox(cubemap)
        self.scene_surfaces += [surface]        
        self.collider_list += surface.collider_list

        
    def render(self):

        t0 = time.time()
        color_RGBlinear = raytrace(ray_origin = self.camera.position, ray_dir = self.camera.ray_dir, scene = self, ray_depth = 0, ray_n = self.n)
        #gamma correction
        color = cf.sRGB_linear_to_sRGB(color_RGBlinear.to_array())
        
        print ("Took", time.time() - t0)

        img_RGB = [Image.fromarray((255 * np.clip(c, 0, 1).reshape((self.camera.screen_height, self.camera.screen_width))).astype(np.uint8), "L") for c in color]
        #Image.merge("RGB", XYZ_color).save("fig.png")
        return Image.merge("RGB", img_RGB)
