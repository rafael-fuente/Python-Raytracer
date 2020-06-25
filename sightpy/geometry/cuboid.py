import numpy as np
from ..utils.constants import *
from ..utils.vector3 import vec3
from ..geometry import Primitive, Collider

class Cuboid(Primitive): 
    def __init__(self,center,  material, width,height, length,max_ray_depth = 5, shadow = True):
        super().__init__(center,  material,  max_ray_depth, shadow = shadow)
        self.width = width
        self.height = height
        self.length = length
        self.bounded_sphere_radius = np.sqrt((self.width/2)**2 + (self.height/2)**2 + (self.length/2)**2)

        self.collider_list += [Cuboid_Collider(assigned_primitive = self, center = center, width = width, height =height ,length =length )]
        
        
    def get_uv(self, hit):
        u,v = hit.collider.get_uv(hit)
        u,v = u/4,v/3
        return u,v
    
    
"""        
        This was the old approach, but remplaced by a Box collider that is more efficient
        #we model a cuboid as six planes
        
        
        #BOTTOM                                                                                                                                       #BOTTOM
        self.collider_list += [Plane_Collider(assigned_primitive = self, center = center + vec3(0.0,-h, 0.0), u_axis = vec3(1.0, 0.0, 0.0), v_axis = vec3(0.0, 0.0, 1.0), w = w, h = l, uv_shift = (1,0))]
        #TOP                                                                                                                                       #TOP
        self.collider_list += [Plane_Collider(assigned_primitive = self, center = center + vec3(0.0,h, 0.0), u_axis = vec3(1.0, 0.0, 0.0), v_axis = vec3(0.0, 0.0, -1.0), w = w, h = l, uv_shift= (1,2))]
        #RIGHT                                                                                                                                       #RIGHT
        self.collider_list += [Plane_Collider(assigned_primitive = self, center = center + vec3(w,0.0, 0.0), u_axis = vec3(0.0, 0.0,  -1.0), v_axis = vec3(0.0, 1.0, 0.0), w = l, h = h, uv_shift= (2,1))]
        #LEFT                                                                                                                                       #LEFT
        self.collider_list += [Plane_Collider(assigned_primitive = self, center = center + vec3(-w,0.0, 0.0), u_axis = vec3(0.0, 0.0,  1.0), v_axis = vec3(0.0, 1.0, 0.0), w = l, h = h, uv_shift= (0,1))]
        #FRONT                                                                                                                                       #FRONT
        self.collider_list += [Plane_Collider(assigned_primitive = self, center = center + vec3(0,0, l), u_axis = vec3(1.0, 0.0, 0.0), v_axis = vec3(0.0, 1.0, 0.0), w = w, h = h, uv_shift= (1,1))]
        #BACK                                                                                                                                       #BACK
        self.collider_list += [Plane_Collider(assigned_primitive = self, center = center + vec3(0,0, -l), u_axis = vec3(-1.0, 0.0, 0.0), v_axis = vec3(0.0, 1.0, 0.0), w = w, h = h, uv_shift= (3,1))]
"""


class Cuboid_Collider(Collider):
    def __init__(self, width, height,length,**kwargs):
        super().__init__(**kwargs)
        
        self.lb = self.center - vec3(width/2, height/2, length/2)
        self.rt = self.center + vec3(width/2, height/2, length/2)

        self.lb_local_basis = self.lb
        self.rt_local_basis = self.rt

        self.width = width
        self.height = height
        self.length = length

        # basis vectors
        self.ax_w = vec3(1.,0.,0.)
        self.ax_h = vec3(0.,1.,0.)
        self.ax_l = vec3(0.,0.,1.)

        self.inverse_basis_matrix = np.array([[self.ax_w.x,       self.ax_h.x,         self.ax_l.x],
                                              [self.ax_w.y,       self.ax_h.y,         self.ax_l.y],
                                              [self.ax_w.z,       self.ax_h.z,         self.ax_l.z]])

        self.basis_matrix = self.inverse_basis_matrix.T


    def rotate(self,M, center):
        self.ax_w = self.ax_w.matmul(M)
        self.ax_h = self.ax_h.matmul(M)
        self.ax_l = self.ax_l.matmul(M)

        self.inverse_basis_matrix = np.array([[self.ax_w.x,       self.ax_h.x,         self.ax_l.x],
                                              [self.ax_w.y,       self.ax_h.y,         self.ax_l.y],
                                              [self.ax_w.z,       self.ax_h.z,         self.ax_l.z]])

        self.basis_matrix = self.inverse_basis_matrix.T

        self.lb = center + (self.lb-center).matmul(M)
        self.rt = center + (self.rt-center).matmul(M)

        self.lb_local_basis = self.lb.matmul(self.basis_matrix)
        self.rt_local_basis = self.rt.matmul(self.basis_matrix)

    def intersect(self, O, D):


        O_local_basis = O.matmul(self.basis_matrix)
        D_local_basis = D.matmul(self.basis_matrix)

        dirfrac = 1.0 / D_local_basis
  
        # lb is the corner of AABB with minimal coordinates - left bottom, rt is maximal corner
        t1 = (self.lb_local_basis.x - O_local_basis.x)*dirfrac.x;
        t2 = (self.rt_local_basis.x - O_local_basis.x)*dirfrac.x;
        t3 = (self.lb_local_basis.y - O_local_basis.y)*dirfrac.y;
        t4 = (self.rt_local_basis.y - O_local_basis.y)*dirfrac.y;
        t5 = (self.lb_local_basis.z - O_local_basis.z)*dirfrac.z;
        t6 = (self.rt_local_basis.z - O_local_basis.z)*dirfrac.z;

        tmin = np.maximum(np.maximum(np.minimum(t1, t2), np.minimum(t3, t4)), np.minimum(t5, t6))
        tmax = np.minimum(np.minimum(np.maximum(t1, t2), np.maximum(t3, t4)), np.maximum(t5, t6))

        # if tmax < 0, ray (line) is intersecting AABB, but the whole AABB is behind us
        # if tmin > tmax, ray doesn't intersect AAB
        mask1 = (tmax < 0) | (tmin > tmax)

        # if tmin < 0 then the ray origin is inside of the AABB and tmin is behind the start of the ray so tmax is the first intersection
        mask2 = tmin < 0
        return np.select([mask1,mask2,True] , [FARAWAY , [tmax,  np.tile(UPDOWN, tmin.shape)] ,  [tmin,  np.tile(UPWARDS, tmin.shape)]])
        

    def get_Normal(self, hit):

        P = (hit.point-self.center).matmul(self.basis_matrix)
        absP = vec3(1./self.width, 1./self.height, 1./self.length)*np.abs(P)
        Pmax = np.maximum(np.maximum(absP.x, absP.y), absP.z)
        P.x = np.where(Pmax == absP.x, np.sign(P.x),  0.)
        P.y = np.where(Pmax == absP.y, np.sign(P.y),  0.)
        P.z = np.where(Pmax == absP.z, np.sign(P.z),  0.)

        return P.matmul(self.inverse_basis_matrix)

    def get_uv(self, hit):
        hit.N = self.get_Normal(hit)
        M_C = hit.point - self.center

        BOTTOM = (hit.N == vec3(0.,-1.,0.))
        TOP =  (hit.N == vec3(0., 1.,0.))
        RIGHT =  (hit.N == vec3(1.,0.,0.))
        LEFT = (hit.N == vec3(-1.,0.,0.) )
        FRONT = (hit.N == vec3(0.,0.,1.))
        BACK = (hit.N == vec3(0.,0.,-1.))
               
        #0.985 to avoid corners
        u = np.select([BOTTOM , TOP,  RIGHT, LEFT , FRONT , BACK],  [((self.ax_w.dot(M_C)/self.width*2 *0.985  + 1 ) /2  + 1),   ((self.ax_w.dot(M_C)/self.width*2 *0.985  + 1 ) /2  + 1),   ((self.ax_l.dot(M_C)/self.width*2 *0.985  + 1 ) /2  + 2),    (((self.ax_l*-1).dot(M_C)/self.width*2 *0.985  + 1 ) /2  + 0),    (((self.ax_w*-1).dot(M_C)/self.width*2 *0.985  + 1 ) /2  + 3),     (( self.ax_w.dot(M_C)/self.width*2 *0.985  + 1 ) /2  + 1)])
        v = np.select([BOTTOM , TOP,  RIGHT, LEFT , FRONT , BACK],  [(((self.ax_l*-1).dot(M_C)/self.width*2 *0.985  + 1 ) /2  + 0),   ((self.ax_l.dot(M_C)/self.width*2 *0.985  + 1 ) /2  + 2),   ((self.ax_h.dot(M_C)/self.width*2 *0.985  + 1 ) /2  + 1),    (((self.ax_h).dot(M_C)/self.width*2 *0.985  + 1 ) /2  + 1),    (((self.ax_h).dot(M_C)/self.width*2 *0.985  + 1 ) /2  + 1),     (( self.ax_h.dot(M_C)/self.width*2 *0.985  + 1 ) /2  + 1)])
        return u,v






