import numpy as np
from ..utils.constants import *
from ..utils.vector3 import vec3
from ..geometry.primitive import Primitive
from ..geometry.collider import Collider


class Triangle(Primitive): 
    def __init__(self,center,  material, p1 , p2, p3, max_ray_depth,shadow = True):
        super().__init__(center,  material, max_ray_depth, shadow = shadow)  
        self.collider_list += [Triangle_Collider(assigned_primitive = self, p1 =p1, p2 = p2, p3 = p3)]

    def get_uv(self, M, collider):
        return collider.get_uv(M)


class Triangle_Collider(Collider):
    def __init__(self,assigned_surface, p1, p2, p3):


        self.assigned_primitive = assigned_surface
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.normal = ((self.p2 - self.p1).cross( self.p3 - self.p1)).normalize()


        self.centroid = (self.p1 + self.p2  + self.p3)/3  #one possible definition of center. Used for intersect().


        self.n31 = (self.p3 - self.p1).cross(self.normal)
        self.n12 = (self.p1- self.p2).cross(self.normal)
        self.n23 = (self.p2 - self.p3).cross(self.normal)



    def intersect(self, O, D):
        N = self.normal  
        
        NdotD = N.dot(D) 
        NdotD = np.where(NdotD == 0., NdotD + 0.0001, NdotD) #avoid zero division
        
        NdotC_O = N.dot(self.centroid - O)
        d =  D * NdotC_O / NdotD
        M = O +  d     # intersection point
        dis =  d.length()
        M_C = M - self.centroid
        hit_inside = (self.n31.dot(M-self.p1) >= 0) & (self.n12.dot(M-self.p2) >= 0)& (self.n23.dot(M-self.p3) >= 0) & (NdotC_O * NdotD > 0) 
        hit_UPWARDS  = (NdotD < 0)
        hit_UPDOWN  = np.logical_not(hit_UPWARDS)


        pred1 = hit_inside & hit_UPWARDS
        pred2 = hit_inside & hit_UPDOWN
        pred3 = True
        return np.select([pred1,pred2,pred3] , [[dis, np.tile(UPWARDS, dis.shape) ], [dis,np.tile(UPDOWN, dis.shape)], FARAWAY])

    def rotate(self,M, center):
        self.p1 = center + (self.p1 -center).matmul(M)
        self.p2 = center + (self.p2 -center).matmul(M)
        self.p3 = center + (self.p3 -center).matmul(M)

        self.n31 = self.n31.matmul(M)
        self.n12 = self.n12.matmul(M)
        self.n23 = self.n23.matmul(M)
        self.normal = self.normal.matmul(M)
        self.centroid = center + (self.centroid-center).matmul(M)
        
    def get_uv(self, hit):
        M_C = hit.point - self.center
        u = ((self.pu.dot(M_C)/self.w + 1 ) /2 + self.uv_shift[0])
        v = ((self.pv.dot(M_C)/self.h + 1 ) /2  + self.uv_shift[1])
        return u,v


    def get_Normal(self, hit):
        return self.normal
