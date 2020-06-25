from sightpy import *

# define materials to use

floor = Glossy(diff_color = image("checkered_floor.png", repeat = 2.),  roughness = 0.2, spec_coeff = 0.3, diff_coeff = 0.7, n = vec3(2.2, 2.2, 2.2)) # n = index of refraction
green_glass = Refractive(n = vec3(1.5 + 4e-8j,1.5 + 0.j,1.5 + 4e-8j)) 


# Set Scene 

Sc = Scene()
Sc.add_Camera(look_from = vec3(0., 0.25, 1. ), look_at = vec3(0., 0.25, -3.),
	          screen_width = 400 ,
	          screen_height = 300)


Sc.add_DirectionalLight(Ldir = vec3(0.0,0.5, 0.5),  color = rgb(0.5, 0.5, 0.5))

Sc.add(Plane(material = floor,  center = vec3(0, -0.5, -3.0), width = 6.0,height = 6.0, u_axis = vec3(1.0, 0, 0), v_axis = vec3(0, 0, -1.0) , max_ray_depth = 5))


cb = Cuboid( material = green_glass, center = vec3(0.00, 0.0001, -0.8), width = 0.9,height = 1.0, length = 0.4, shadow = False,  max_ray_depth = 5)
cb.rotate(θ = 30, u = vec3(0,1,0))
Sc.add(cb)


#see sightpy/backgrounds
Sc.add_Background("stormydays.png")

# Render 
img = Sc.render(samples_per_pixel = 4)

img.save("EXAMPLE3.png")

img.show()