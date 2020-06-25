from ..geometry import Sphere_Collider, Primitive
from ..materials import Material
from ..utils.vector3 import vec3
from ..utils.constants import SKYBOX_DISTANCE
from ..utils.image_functions import load_image, load_image_as_linear_sRGB
from .util.blur_background import blur_skybox
from .skybox import SkyBox_Material

class Panorama(Primitive):
    def __init__(self, panorama, center = vec3(0.,0.,0.), light_intensity = 0.0, blur = 0.0):
        super().__init__(center,  SkyBox_Material(panorama, light_intensity, blur), shadow = False)
        l = SKYBOX_DISTANCE
        self.light_intensity = light_intensity 
        self.collider_list += [Sphere_Collider(assigned_primitive = self, center = center , radius = SKYBOX_DISTANCE)]
        
    
    def get_uv(self, hit):
        return hit.collider.get_uv(hit)