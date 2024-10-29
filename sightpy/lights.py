from .utils.constants import SKYBOX_DISTANCE
import numpy as np
from abc import abstractmethod 


# lights only have effect on Glossy materials
class Light:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color

    @abstractmethod   
    def get_L(self, M):
        pass

    @abstractmethod   
    def get_irradiance(self, dist_light, NdotL):
        pass

    @abstractmethod       
    def get_distance(self, M):
        pass


class PointLight(Light):
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color
    def get_L(self, M):
        Ldir = self.pos - M
        Ldir = Ldir / np.linalg.norm(Ldir)
        return Ldir

    def get_distance(self, M):
        return np.sqrt((self.pos - M).dot(self.pos - M))

    def get_irradiance(self,dist_light, NdotL):
        return self.color * NdotL/(dist_light**2.) * 100
        
class DirectionalLight(Light):
    def __init__(self, Ldir, color):
        self.Ldir = Ldir
        self.color = color
    def get_L(self, M):
        return self.Ldir

    def get_distance(self, M):
        return SKYBOX_DISTANCE

    def get_irradiance(self, dist_light, NdotL):
        return self.color * NdotL