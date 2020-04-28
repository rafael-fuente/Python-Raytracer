import numpy as np
from constants import *
from vector3 import vec3

class Collider:    
    def __init__(self,assigned_surface, center):
        self.assigned_surface = assigned_surface
        self.center = center
        
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

    def get_Normal(self, M):
        # M = intersection point
        return (M - self.center) * (1. / self.radius) 
    
class Plane_Collider(Collider):
    def __init__(self, pu, pv, w, h, uv_shift = (0.,0.),**kwargs):
        super().__init__(**kwargs)
        self.normal = pu.cross(pv)
        
        
        self.w = w
        self.h = h
        self.pu = pu
        self.pv = pv
        self.uv_shift = uv_shift
        
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
        
    def get_uv(self, M):
        N = self.get_Normal(M)
        M_C = M - self.center
        u = ((self.pu.dot(M_C)/self.w + 1 ) /2 + self.uv_shift[0])
        v = ((self.pv.dot(M_C)/self.h + 1 ) /2  + self.uv_shift[1])
        return u,v


    def get_Normal(self, M):
        return self.normal



class Triangle_Collider(Collider):
    def __init__(self,assigned_surface, p1, p2, p3):


        self.assigned_surface = assigned_surface
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
        
    def get_uv(self, M):
        N = self.get_Normal(M)
        M_C = M - self.center
        u = ((self.pu.dot(M_C)/self.w + 1 ) /2 + self.uv_shift[0])
        v = ((self.pv.dot(M_C)/self.h + 1 ) /2  + self.uv_shift[1])
        return u,v


    def get_Normal(self, M):
        return self.normal




        