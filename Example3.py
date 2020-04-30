# Import the necessary modules

from PIL import Image
import numpy as np
from pathlib import Path

from constants import *
from vector3 import *
from raytrace import *
from scene import *
from surfaces import *
from lights import *
from colliders import *
from materials import *


# Create some materials to use

img = Image.open(Path("images/checkered_floor_linear_sRGB.png"))
checkered_floor = np.asarray(img)/256.
checkered_floor_material = Material(texture = checkered_floor, repeat = 2.0, diff_color = rgb(1.0, 1., 1.), n = vec3(2.6, 2.6, 2.6), roughness = 0.2, spec_c = 0.3, diff_c = 0.7, max_ray_depth = 5)
green_glass = RefractiveMaterial(diff_color = rgb(1.0, 1.0, 1.0), n = vec3(1.5 + 4e-8j,1.5 + 0.j,1.5 + 4e-8j), roughness = 0.0,spec_c = 0.2, diff_c = 0.8, max_ray_depth = 5)



# Import skyboxes

img = Image.open(Path("images/stormydays_linear_sRGB.png"))
stormydays = np.asarray(img)/256.

# Set Scene 

Sc = Scene()
Sc.add_Camera(Camera(screen_width = 400 ,screen_height = 300, position = vec3(0., 0.25, 1. ), look_at = vec3(0., 0.25, -3.) ))
Sc.add_DirectionalLight(Ldir = vec3(0.0,0.5, 0.5),  color = rgb(0.5, 0.5, 0.5))

Sc.add_Surface(Plane(material = checkered_floor_material,  center = vec3(0, -0.5, -3.0), width = 6.0,height = 6.0, pu = vec3(1.0, 0, 0), pv = vec3(0, 0, -1.0)))
cb = Cube( material = green_glass, center = vec3(0.00, 0.0, -0.8), width = 0.9,height = 1.0, length = 0.4, shadow = False)
cb.rotate(θ = 30, u = vec3(0,1,0))
Sc.add_Surface(cb)


Sc.add_SkyBox(stormydays)

# Render 
img = Sc.render()

img.save("EXAMPLE3.png")

img.show()