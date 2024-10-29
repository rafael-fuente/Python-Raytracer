import numpy as np
from ..utils.constants import *
from ..utils.vector3 import vec3
from ..geometry import Primitive, Triangle_Collider


# WORK IN PROGRESS. 
# We need to implement a bounding volume hierarchy to make TriangleMesh collision efficient.
# Without a bounding volume hierarchy a model with 200 triangles takes around 3 minutes to be rendered

class TriangleMesh(Primitive): 
    def __init__(self,file_name, center,  material, max_ray_depth,shadow = True):
        super().__init__(center,  material,max_ray_depth, shadow = shadow)
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
            self.collider_list += [Triangle_Collider(assigned_primitive = self, p1 =p1, p2 = p2, p3 = p3)]

