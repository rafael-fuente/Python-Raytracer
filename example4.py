from sightpy import *


# Set Scene 

Sc = Scene(ambient_color = rgb(0.01, 0.01, 0.01))


angle = -np.pi*0.5 
Sc.add_Camera(screen_height =300,  screen_width = 400 , 
	          look_from = vec3(4.0*np.sin(angle), 0.00, 4.0*np.cos(angle)  ),  look_at = vec3(0., 0.05, 0.0), 
	          samples_per_pixel = 	10)


soap_bubble = Material(shader = ThinFilmInterference(thickness = 330, noise = 60., max_ray_depth = 5))
Sc.add_Surface(Sphere(material = soap_bubble, center = vec3(1., 0.0, 1.5), radius = 1.7, shadow = False))


Sc.add_Background("lake.png", light_intensity = 5., blur = 10.)


# Render 
img = Sc.render()

img.save("EXAMPLE4.png")

img.show()