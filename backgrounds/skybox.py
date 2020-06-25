from ..geometry import Cuboid_Collider, Primitive
from ..materials import Material
from ..utils.vector3 import vec3
from ..utils.constants import SKYBOX_DISTANCE
from ..utils.image_functions import load_image, load_image_as_linear_sRGB
from .util.blur_background import blur_skybox

class SkyBox(Primitive):
    def __init__(self, cubemap, center = vec3(0.,0.,0.), light_intensity = 0.0, blur = 0.0):
        super().__init__(center,  SkyBox_Material(cubemap, light_intensity, blur), shadow = False)
        l = SKYBOX_DISTANCE
        self.light_intensity = light_intensity
                                                                                                                              #BOTTOM
        self.collider_list += [Cuboid_Collider(assigned_primitive = self, center = center, width = 2*l, height =2*l ,length =2*l )]
        
    
    def get_uv(self, hit):
        u,v = hit.collider.get_uv(hit)
        u,v = u/4,v/3
        return u,v


class SkyBox_Material(Material):
    def __init__(self, cubemap, light_intensity, blur):
        self.texture = load_image_as_linear_sRGB("sightpy/backgrounds/" + cubemap)

        if light_intensity != 0.0:
            self.lightmap = load_image("sightpy/backgrounds/lightmaps/" + cubemap)

        if blur != 0.0:
            self.blur_image = blur_skybox(load_image("sightpy/backgrounds/" + cubemap), blur, cubemap)

        self.blur = blur
        self.light_intensity = light_intensity
        self.repeat = 1.0

    def get_texture_color(self, hit, ray):
        u,v = hit.get_uv()

        if (self.blur != 0.0) :
            im = self.blur_image[-((v * self.blur_image.shape[0]*self.repeat ).astype(int)% self.blur_image.shape[0]) , (u   * self.blur_image.shape[1]*self.repeat).astype(int) % self.blur_image.shape[1]  ].T
        else:
            im = self.texture[-((v * self.texture.shape[0]*self.repeat ).astype(int)% self.texture.shape[0]) , (u   * self.texture.shape[1]*self.repeat).astype(int) % self.texture.shape[1]  ].T

        if (ray.depth != 0) and (self.light_intensity != 0.0):
            ls = self.lightmap[-((v * self.texture.shape[0]*self.repeat ).astype(int)% self.texture.shape[0]) , (u   * self.texture.shape[1]*self.repeat).astype(int) % self.texture.shape[1]  ].T
            color = vec3(im[0] + self.light_intensity * ls[0],  im[1] + self.light_intensity * ls[1],  im[2] + self.light_intensity * ls[2])

        else:
            color = vec3(im[0] ,  im[1] ,  im[2] )
        return color


    def get_color(self, scene, ray, hit):
        hit.point = (ray.origin + ray.dir * hit.distance)
        return hit.material.get_texture_color(hit,ray)

