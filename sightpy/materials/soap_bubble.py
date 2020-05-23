from . import Material
from ..utils.vector3 import vec3, rgb
from ..shaders import ThinFilmInterference

soap_bubble = Material(shader = ThinFilmInterference(thickness = 330, noise = 60., max_ray_depth = 5))
