import numpy as np
from ..utils.constants import *
from ..utils.vector3 import vec3
from ..geometry import Surface, Collider


class Plane(Surface): 
    def __init__(self,center,  material, width,height, pu, pv, shadow = True):
        super().__init__(center,  material, shadow = shadow)  
        self.collider_list += [Plane_Collider(assigned_surface = self, center = center, pu = pu, pv = pv, w= width/2, h=height/2)]
        self.width = width   
        self.height = height
    def get_uv(self, hit):
        return hit.collider.get_uv(hit)


class Plane_Collider(Collider):
    def __init__(self, pu, pv, w, h, uv_shift = (0.,0.),**kwargs):
        super().__init__(**kwargs)
        self.normal = pu.cross(pv).normalize()
        
        
        self.w = w
        self.h = h
        self.pu = pu
        self.pv = pv
        self.uv_shift = uv_shift
        self.inverse_basis_matrix =  np.array([[self.pu.x,       self.pv.x,         self.normal.x],
                                               [self.pu.y,       self.pv.y,         self.normal.y],
                                               [self.pu.z,       self.pv.z,         self.normal.z]])
        self.basis_matrix = self.inverse_basis_matrix.T




    def intersect(self, O, D):
        N = self.normal  
        
        NdotD = N.dot(D) 
        NdotD = np.where(NdotD == 0., NdotD + 0.0001, NdotD) #avoid zero division
        
        NdotC_O = N.dot(self.center - O)
        d =  D * NdotC_O / NdotD
        M = O +  d     # intersection point
        dis =  d.length()

        M_C = M - self.center
        
        #plane basis coordinates
        u = self.pu.dot(M_C)
        v = self.pv.dot(M_C)


        hit_inside = (np.abs(u)  <= self.w) & (np.abs(v) <= self.h) & (NdotC_O * NdotD > 0) 
        hit_UPWARDS  = (NdotD < 0)
        hit_UPDOWN  = np.logical_not(hit_UPWARDS)


        pred1 = hit_inside & hit_UPWARDS
        pred2 = hit_inside & hit_UPDOWN
        pred3 = True
        return np.select([pred1,pred2,pred3] , [[dis, np.tile(UPWARDS, dis.shape) ], [dis,np.tile(UPDOWN, dis.shape)], FARAWAY])
    
    def rotate(self,M, center):
        self.pu = self.pu.matmul(M)
        self.pv = self.pv.matmul(M)
        self.normal = self.normal.matmul(M)
        self.center = center + (self.center-center).matmul(M)
        
    def get_uv(self, hit):
        M_C = hit.point - self.center
        u = ((self.pu.dot(M_C)/self.w + 1 ) /2 + self.uv_shift[0])
        v = ((self.pv.dot(M_C)/self.h + 1 ) /2  + self.uv_shift[1])
        return u,v


    def get_Normal(self, hit):
        return self.normal

