import numpy as np
from ..utils.constants import *
from ..utils.vector3 import vec3
from ..geometry import Primitive, Collider

class Sphere(Primitive): 
    def __init__(self,center,  material, radius, max_ray_depth = 5, shadow = True):
        super().__init__(center,  material, max_ray_depth, shadow = shadow)
        self.collider_list += [Sphere_Collider(assigned_primitive = self, center = center, radius = radius)]
        self.bounded_sphere_radius = radius

    def get_uv(self, hit):
        return hit.collider.get_uv(hit)

        
class Sphere_Collider(Collider):
    def __init__(self,  radius, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        
        
    def intersect(self, O, D):
        
        b = 2 * D.dot(O - self.center)
        c = self.center.square_length() + O.square_length() - 2 * self.center.dot(O) - (self.radius * self.radius)
        disc = (b ** 2) - (4 * c)
        sq = np.sqrt(np.maximum(0, disc))
        h0 = (-b - sq) / 2
        h1 = (-b + sq) / 2
        h = np.where((h0 > 0) & (h0 < h1), h0, h1)
        pred = (disc > 0) & (h > 0)
        M = (O + D * h)
        NdotD = ((M - self.center) * (1. / self.radius) ).dot(D)
        
        pred1 = (disc > 0) & (h > 0) & (NdotD > 0)
        pred2 = (disc > 0) & (h > 0) & (NdotD < 0)
        pred3 = True
        
        #return an array with hit distance and the hit orientation
        return np.select([pred1,pred2,pred3] , [[h, np.tile(UPDOWN, h.shape)], [h,np.tile(UPWARDS, h.shape)], FARAWAY])

    def get_Normal(self, hit):
        # M = intersection point
        return (hit.point - self.center) * (1. / self.radius) 

    def get_uv(self, hit):
        M_C = (hit.point - self.center) / self.radius
        phi = np.arctan2(M_C.z, M_C.x)
        theta = np.arcsin(M_C.y)
        u = (phi + np.pi) / (2*np.pi)
        v = (theta + np.pi/2) / np.pi
        return u,v