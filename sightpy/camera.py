from .utils.vector3 import vec3, rgb
from .utils.random import random_in_unit_disk
import numpy as np
from .ray import Ray

class Camera():
    def __init__(self, look_from, look_at, screen_width = 400 ,screen_height = 300,  field_of_view = 90., aperture = 0., focal_distance = 1.):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.aspect_ratio = float(screen_width) / screen_height

        self.look_from = look_from
        self.look_at = look_at
        self.camera_width = np.tan(field_of_view * np.pi/180   /2.)*2.
        self.camera_height = self.camera_width/self.aspect_ratio

        #camera reference basis in world coordinates
        self.cameraFwd = (look_at - look_from).normalize()
        self.cameraRight = (self.cameraFwd.cross(vec3(0.,1.,0.))).normalize()
        self.cameraUp = self.cameraRight.cross(self.cameraFwd)



        #if you use a lens_radius >= 0.0 make sure that samples_per_pixel is a large number. Otherwise you'll get a lot of noise
        self.lens_radius =  aperture / 2;
        self.focal_distance = focal_distance



        # Pixels coordinates in camera basis:
        self.x = np.linspace(-self.camera_width/2., self.camera_width/2., self.screen_width)
        self.y = np.linspace(self.camera_height/2., -self.camera_height/2., self.screen_height)

        # we are going to cast a total of screen_width * screen_height * samples_per_pixel rays 
        # xx,yy store the origin of each ray in a 3d array where the first and second dimension are the x,y coordinates of each pixel
        # and the third dimension is the sample index of each pixel
        xx,yy = np.meshgrid(self.x,self.y)
        self.x = xx.flatten()
        self.y = yy.flatten()

    def get_ray(self,n): # n = index of refraction of scene main medium (for air n = 1.)

        # in each pixel, take a random position to avoid aliasing.
        x = self.x + (np.random.rand(len(self.x )) - 0.5)*self.camera_width/2.  /(self.screen_width)
        y = self.y + (np.random.rand(len(self.y )) - 0.5)*self.camera_height/2. /(self.screen_height)

        # set ray direction in world space:
        rx, ry = random_in_unit_disk(x.shape[0])
        ray_origin = self.look_from  +   self.cameraRight *rx* self.lens_radius   +   self.cameraUp *ry* self.lens_radius
        ray_dir = (self.look_from  +   self.cameraUp*y*self.focal_distance  +  self.cameraRight*x*self.focal_distance  + self.cameraFwd*self.focal_distance  - ray_origin  ).normalize()
        return Ray(origin=ray_origin, dir=ray_dir, depth=0,  n=n, reflections = 0, transmissions = 0, diffuse_reflections = 0)

