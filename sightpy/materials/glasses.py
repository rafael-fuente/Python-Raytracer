from . import Material 
from ..utils.vector3 import vec3, rgb
from ..shaders import Refractive

blue_glass = Material(shader = Refractive(n = vec3(1.5 + 4e-8j,1.5 +  4e-8j,1.5 +  0.j), max_ray_depth = 3))
green_glass = Material(shader = Refractive(n = vec3(1.5 + 4e-8j,1.5 + 0.j,1.5 + 4e-8j),  max_ray_depth = 3))
red_glass = Material(shader = Refractive(n = vec3(1.5 + 0.j,1.5 +  5e-8j,1.5 +  5e-8j), max_ray_depth = 3))

