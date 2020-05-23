from sightpy import *


# Set Scene 

Sc = Scene()
Sc.add_Camera(look_from = vec3(0., 0.25, 1. ), look_at = vec3(0., 0.25, -3.),
	          screen_width = 400 ,screen_height = 300,
	          samples_per_pixel = 4)


Sc.add_DirectionalLight(Ldir = vec3(0.0,0.5, 0.5),  color = rgb(0.5, 0.5, 0.5))

floor = Material(shader = Glossy(diff_color = rgb(1.0, 1., 1.),  roughness = 0.2, spec_c = 0.3, diff_c = 0.7, max_ray_depth = 5, n = vec3(2.2, 2.2, 2.2)))
floor.set_texture("checkered_floor.png", repeat = 2.)
Sc.add_Surface(Plane(material = floor,  center = vec3(0, -0.5, -3.0), width = 6.0,height = 6.0, pu = vec3(1.0, 0, 0), pv = vec3(0, 0, -1.0)))


green_glass = Material(shader = Refractive(n = vec3(1.5 + 4e-8j,1.5 + 0.j,1.5 + 4e-8j),  max_ray_depth = 5))
cb = Cuboid( material = green_glass, center = vec3(0.00, 0.0001, -0.8), width = 0.9,height = 1.0, length = 0.4, shadow = False)
cb.rotate(θ = 30, u = vec3(0,1,0))
Sc.add_Surface(cb)


#see sightpy\backgrounds
Sc.add_Background("stormydays.png")

# Render 
img = Sc.render()

img.save("EXAMPLE3.png")

img.show()