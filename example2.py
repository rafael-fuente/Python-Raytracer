# Import the necessary modules


from sightpy import *


# Set Scene 

Sc = Scene()
angle = np.pi/2 * 0.3
Sc.add_Camera(look_from = vec3(2.5*np.sin(angle), 0.25, 2.5*np.cos(angle)  -1.5 ), look_at = vec3(0., 0.25, -1.5), 
	          screen_width = 400 ,screen_height =300,
	          samples_per_pixel = 4)


Sc.add_DirectionalLight(Ldir = vec3(0.0,0.5, 0.5),  color = rgb(0.5, 0.5, 0.5))

#blue_glass,red_glass and green_glass are defined in sightpy/materials/glasses.py
Sc.add_Surface(Sphere(material = blue_glass, center = vec3(-1.2, 0.0, -1.5), radius = .5, shadow = False))
Sc.add_Surface(Sphere(material = green_glass, center = vec3(0., 0.0, -1.5), radius = .5, shadow = False))
Sc.add_Surface(Sphere(material = red_glass, center = vec3(1.2, 0.0, -1.5), radius = .5, shadow = False))

#floor is defined in sightpy/materials/floor.py
floor.set_texture("checkered_floor.png", repeat = 2.)
Sc.add_Surface(Plane(material = floor,  center = vec3(0, -0.5, -1.5), width = 4.0,height = 4.0, pu = vec3(1.0, 0, 0), pv = vec3(0, 0, -1.0)))

#see sightpy\backgrounds
Sc.add_Background("miramar.jpeg")


# Render 
img = Sc.render()

img.save("EXAMPLE2.png")

img.show()