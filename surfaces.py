from constants import *
from vector3 import vec3
import colliders
import numpy as np
import materials





class Surface:    
    def __init__(self, center, material, shadow = True):
        self.center = center
        self.material = material
        self.material.assigned_surface = self
        self.shadow = shadow
        self.collider_list = [] 

        
    def rotate(self, θ, u):
        
        u = u.normalize()
        θ = θ/180 *np.pi 
        cosθ = np.cos(θ)
        sinθ = np.sqrt(1-cosθ**2) * np.sign(θ)
        
        M = np.array([
                       [cosθ + u.x*u.x * (1-cosθ),      u.x*u.y*(1-cosθ) - u.z*sinθ,         u.x*u.z*(1-cosθ) +u.y*sinθ],
                       [u.y*u.x*(1-cosθ) + u.z*sinθ,        cosθ + u.y**2 * (1-cosθ),       u.y*u.z*(1-cosθ) -u.x*sinθ],
                       [u.z*u.x*(1-cosθ) -u.y*sinθ,             u.z*u.y*(1-cosθ) + u.x*sinθ,         cosθ + u.z*u.z*(1-cosθ)]
                      ])
        for c in self.collider_list:
            c.rotate(M, self.center)
            

class Sphere(Surface): 
    def __init__(self,center,  material, radius, shadow = True):
        super().__init__(center,  material, shadow = shadow)
        self.collider_list += [colliders.Sphere_Collider(assigned_surface = self, center = center, radius = radius)]


        


class Cube(Surface): 
    def __init__(self,center,  material, width,height, length, shadow = True):
        super().__init__(center,  material, shadow = shadow)
        self.height = height
        self.length = length
        
        #we model a cube as six planes
        w,h,l  = width/2, height/2, length/2
        
        #BOTTOM                                                                                                                                       #BOTTOM
        self.collider_list += [colliders.Plane_Collider(assigned_surface = self, center = center + vec3(0.0,-h, 0.0), pu = vec3(1.0, 0.0, 0.0), pv = vec3(0.0, 0.0, 1.0), w = w, h = l, uv_shift = (1,0))]
        #TOP                                                                                                                                       #TOP
        self.collider_list += [colliders.Plane_Collider(assigned_surface = self, center = center + vec3(0.0,h, 0.0), pu = vec3(1.0, 0.0, 0.0), pv = vec3(0.0, 0.0, -1.0), w = w, h = l, uv_shift= (1,2))]
        #RIGHT                                                                                                                                       #RIGHT
        self.collider_list += [colliders.Plane_Collider(assigned_surface = self, center = center + vec3(w,0.0, 0.0), pu = vec3(0.0, 0.0,  -1.0), pv = vec3(0.0, 1.0, 0.0), w = l, h = h, uv_shift= (2,1))]
        #LEFT                                                                                                                                       #LEFT
        self.collider_list += [colliders.Plane_Collider(assigned_surface = self, center = center + vec3(-w,0.0, 0.0), pu = vec3(0.0, 0.0,  1.0), pv = vec3(0.0, 1.0, 0.0), w = l, h = h, uv_shift= (0,1))]
        #FRONT                                                                                                                                       #FRONT
        self.collider_list += [colliders.Plane_Collider(assigned_surface = self, center = center + vec3(0,0, l), pu = vec3(1.0, 0.0, 0.0), pv = vec3(0.0, 1.0, 0.0), w = w, h = h, uv_shift= (1,1))]
        #BACK                                                                                                                                       #BACK
        self.collider_list += [colliders.Plane_Collider(assigned_surface = self, center = center + vec3(0,0, -l), pu = vec3(-1.0, 0.0, 0.0), pv = vec3(0.0, 1.0, 0.0), w = w, h = h, uv_shift= (3,1))]
        
        
        
    def get_uv(self, M, collider):
        u,v = collider.get_uv(M)
        u,v = u/4,v/3
        return u,v
    
    

class Plane(Surface): 
    def __init__(self,center,  material, width,height, pu, pv, shadow = True):
        super().__init__(center,  material, shadow = shadow)  
        self.collider_list += [colliders.Plane_Collider(assigned_surface = self, center = center, pu = pu, pv = pv, w= width/2, h=height/2)]
        self.width = width   
        self.height = height
    def get_uv(self, M, collider):
        return collider.get_uv(M)
class Triangle(Surface): 
    def __init__(self,center,  material, p1 , p2, p3, shadow = True):
        super().__init__(center,  material, shadow = shadow)  
        self.collider_list += [colliders.Triangle_Collider(assigned_surface = self, p1 =p1, p2 = p2, p3 = p3)]

    def get_uv(self, M, collider):
        return collider.get_uv(M)


class TriangleMesh(Surface): 
    def __init__(self,file_name, center,  material, shadow = True):
        super().__init__(center,  material, shadow = shadow)
        self.collider_list += []
        vs = []
        fs = []
        with open(file_name, 'r') as f:
            r = f.read()
            r = r.split('\n')
            for i in r:
                i = i.split()
                if not i:
                    continue
                elif i[0] == 'v':
                    x = float(i[1])
                    y = float(i[2])
                    z = float(i[3])
                    vs.append(vec3(x, y, z))
                elif i[0] == 'f':
                    f1 = int(i[1].split('/')[0]) - 1
                    f2 = int(i[2].split('/')[0]) - 1
                    f3 = int(i[3].split('/')[0]) - 1
                    fs.append([f1, f2, f3])
        for i in fs:
            p1 = vs[i[0]] + center
            p2 = vs[i[1]] + center
            p3 = vs[i[2]] + center
            self.collider_list += [colliders.Triangle_Collider(assigned_surface = self, p1 =p1, p2 = p2, p3 = p3)]

class SkyBox(Surface):
    def __init__(self,cubemap, center = vec3(0.,0.,0.)):
        super().__init__(center,  materials.SkyBox_Material(cubemap), shadow = False)
        l = SKYBOX_DISTANCE

        # 1.005 factor to avoid skybox corners
        #BOTTOM                                                                                                                                       #BOTTOM
        self.collider_list += [colliders.Plane_Collider(assigned_surface = self, center = center + vec3(0,-l, 0.0), pu = vec3(1.0, 0.0, 0.0), pv = vec3(0.0, 0.0, -1.0), w = l*1.005, h = l*1.005, uv_shift = (1,0))]
        #TOP                                                                                                                                           #TOP
        self.collider_list += [colliders.Plane_Collider(assigned_surface = self, center = center + vec3(0,l, 0.0), pu = vec3(1.0, 0.0, 0.0), pv = vec3(0.0, 0.0, 1.0), w = l*1.005, h = l*1.005, uv_shift= (1,2))]
        #RIGHT                                                                                                                                       #RIGHT
        self.collider_list += [colliders.Plane_Collider(assigned_surface = self, center = center + vec3(l,0, 0), pu = vec3(0.0, 0.0,  1.0), pv = vec3(0.0, 1.0, 0.0), w = l*1.005, h = l*1.005, uv_shift= (2,1))]
        #LEFT                                                                                                                                       #LEFT
        self.collider_list += [colliders.Plane_Collider(assigned_surface = self, center = center + vec3(-l,0, 0), pu = vec3(0.0, 0.0,  -1.0), pv = vec3(0.0, 1.0, 0.0), w = l*1.005, h = l*1.005, uv_shift= (0,1))]
        #FRONT                                                                                                                                       #FRONT
        self.collider_list += [colliders.Plane_Collider(assigned_surface = self, center = center + vec3(0,0, l), pu = vec3(-1.0, 0.0, 0.0), pv = vec3(0.0, 1.0, 0.0), w = l*1.005, h = l*1.005, uv_shift= (3,1))]
        #BACK                                                                                                                                       #BACK
        self.collider_list += [colliders.Plane_Collider(assigned_surface = self, center = center + vec3(0,0, -l), pu = vec3(1.0, 0.0, 0.0), pv = vec3(0.0, 1.0, 0.0), w = l*1.005, h = l*1.005, uv_shift= (1,1))]
    
    def get_uv(self, M, collider):
        u,v = collider.get_uv(M)
        u,v = u/4,v/3
        return u,v
