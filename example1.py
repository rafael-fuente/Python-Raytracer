from sightpy import *


# Set Scene 
Sc = Scene(ambient_color = rgb(0.05, 0.05, 0.05))


angle = -np.pi/2 * 0.3
Sc.add_Camera(look_from = vec3(2.5*np.sin(angle), 0.25, 2.5*np.cos(angle)  -1.5 ), look_at = vec3(0., 0.25, -3.), 
	          screen_width = 400 ,screen_height = 300,  
	          samples_per_pixel = 4) #antialiasing



Sc.add_DirectionalLight(Ldir = vec3(0.52,0.45, -0.5),  color = rgb(0.15, 0.15, 0.15))


#gold_metal and bluish_metal are defined in sightpy/materials/metals.py
Sc.add_Surface(Sphere(material = gold_metal, center = vec3(-.75, .1, -3.),radius =  .6))
Sc.add_Surface(Sphere(material = bluish_metal, center = vec3(1.25, .1, -3.), radius = .6))

#floor is defined in sightpy/materials/floor.py
floor.set_texture("checkered_floor.png", repeat = 80.)
Sc.add_Surface(Plane(material = floor,  center = vec3(0, -0.5, -3.0), width = 120.0,height = 120.0, pu = vec3(1.0, 0, 0), pv = vec3(0, 0, -1.0)))

#see sightpy\backgrounds
Sc.add_Background("stormydays.png")




# Render 
img = Sc.render()

img.save("EXAMPLE1.png")

img.show()