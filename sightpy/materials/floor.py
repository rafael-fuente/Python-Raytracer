from . import Material
from ..utils.vector3 import vec3, rgb
from ..shaders import Glossy

floor = Material(shader = Glossy(diff_color = rgb(1., 1., 1.), 
	                             n = vec3(1.2+ 0.3j, 1.2+ 0.3j, 1.1+ 0.3j), roughness = 0.2, spec_c = 0.3, diff_c = 0.9,
	                             max_ray_depth = 3))
