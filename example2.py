from sightpy import *


# define materials to use

blue_glass = Refractive(n = vec3(1.5 + 4e-8j,1.5 +  4e-8j,1.5 +  0.j)) # n = index of refraction
green_glass = Refractive(n = vec3(1.5 + 4e-8j,1.5 + 0.j,1.5 + 4e-8j))
red_glass = Refractive(n = vec3(1.5 + 0.j,1.5 +  5e-8j,1.5 +  5e-8j))

floor = Glossy(diff_color = image("checkered_floor.png", repeat = 80.), n = vec3(1.2+ 0.3j, 1.2+ 0.3j, 1.1+ 0.3j), roughness = 0.2, spec_coeff = 0.3, diff_coeff = 0.9)

# Set Scene 

Sc = Scene(ambient_color = rgb(0.05, 0.05, 0.05))

angle = np.pi/2 * 0.3
Sc.add_Camera(look_from = vec3(2.5*np.sin(angle), 0.25, 2.5*np.cos(angle)  -1.5 ), 
			  look_at = vec3(0., 0.25, -1.5), 
	          screen_width = 400 ,
	          screen_height =300)


Sc.add_DirectionalLight(Ldir = vec3(0.52,0.45, -0.5),  color = rgb(0.15, 0.15, 0.15))


Sc.add(Sphere(material = blue_glass, center = vec3(-1.2, 0.0, -1.5), radius = .5, shadow = False ,max_ray_depth = 3))
Sc.add(Sphere(material = green_glass, center = vec3(0., 0.0, -1.5), radius = .5, shadow = False,max_ray_depth = 3))
Sc.add(Sphere(material = red_glass, center = vec3(1.2, 0.0, -1.5), radius = .5, shadow = False,max_ray_depth = 3))

Sc.add(Plane(material = floor,  center = vec3(0, -0.5, -3.0), width = 120.0,height = 120.0, u_axis = vec3(1.0, 0, 0), v_axis = vec3(0, 0, -1.0) ,max_ray_depth = 3))


#see sightpy/backgrounds
Sc.add_Background("miramar.jpeg")


# Render 
img = Sc.render(samples_per_pixel = 7)

img.save("EXAMPLE2.png")

img.show()