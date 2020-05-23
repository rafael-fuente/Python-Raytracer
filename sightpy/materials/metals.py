from . import Material
from ..utils.vector3 import vec3, rgb
from ..shaders import Glossy

gold_metal = Material(shader = Glossy(diff_color = rgb(1., .572, .184), n = vec3(0.15+3.58j, 0.4+2.37j, 1.54+1.91j), roughness = 0.0, spec_c = 0.2, diff_c = 0.8, max_ray_depth = 3))
bluish_metal = Material(shader = Glossy(diff_color = rgb(0.0, 0, 0.1), n = vec3(1.3+1.91j, 1.3+1.91j, 1.4+2.91j), roughness = 0.2,spec_c = 0.5, diff_c = 0.3, max_ray_depth = 3))
