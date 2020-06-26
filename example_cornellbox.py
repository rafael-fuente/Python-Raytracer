from sightpy import *


# Set Scene 

Sc = Scene(ambient_color = rgb(0.00, 0.00, 0.00))


angle = -0

Sc.add_Camera(screen_width = 100 ,screen_height = 100, 
			  look_from = vec3(278, 278, 800), look_at = vec3(278,278,0), 
			  focal_distance= 1., field_of_view= 40)


# define materials to use

green_diffuse=Diffuse(diff_color = rgb(.12, .45, .15))
red_diffuse=Diffuse(diff_color = rgb(.65, .05, .05))
white_diffuse=Diffuse(diff_color = rgb(.73, .73, .73))
emissive_white =Emissive(color = rgb(15., 15., 15.))
emissive_blue =Emissive(color = rgb(2., 2., 3.5))
blue_glass =Refractive(n = vec3(1.5 + 0.05e-8j,1.5 +  0.02e-8j,1.5 +  0.j))



# this is the light
Sc.add(Plane(material = emissive_white,  center = vec3(213 + 130/2, 554, -227.0 - 105/2), width = 130.0, height = 105.0, u_axis = vec3(1.0, 0.0, 0), v_axis = vec3(0.0, 0, 1.0)), 
					 importance_sampled = True)



Sc.add(Plane(material = white_diffuse,  center = vec3(555/2, 555/2, -555.0), width = 555.0,height = 555.0, u_axis = vec3(0.0, 1.0, 0), v_axis = vec3(1.0, 0, 0.0)))

Sc.add(Plane(material = green_diffuse,  center = vec3(-0.0, 555/2, -555/2), width = 555.0,height = 555.0,  u_axis = vec3(0.0, 1.0, 0), v_axis = vec3(0.0, 0, -1.0)))

Sc.add(Plane(material = red_diffuse,  center = vec3(555.0, 555/2, -555/2), width = 555.0,height = 555.0,  u_axis = vec3(0.0, 1.0, 0), v_axis = vec3(0.0, 0, -1.0)))

Sc.add(Plane(material = white_diffuse,  center = vec3(555/2, 555, -555/2), width = 555.0,height = 555.0,  u_axis = vec3(1.0, 0.0, 0), v_axis = vec3(0.0, 0, -1.0)))

Sc.add(Plane(material = white_diffuse,  center = vec3(555/2, 0., -555/2), width = 555.0,height = 555.0,  u_axis = vec3(1.0, 0.0, 0), v_axis = vec3(0.0, 0, -1.0)))


cb = Cuboid( material = white_diffuse, center = vec3(182.5, 165, -285-160/2), width = 165,height = 165*2, length = 165, shadow = False)
cb.rotate(θ = 15, u = vec3(0,1,0))
Sc.add(cb)




Sc.add(Sphere( material = blue_glass, center = vec3(370.5, 165/2, -65-185/2), radius = 165/2, shadow = False, max_ray_depth = 3),
					 importance_sampled = True)
# Render 

img = Sc.render(samples_per_pixel = 10, progress_bar = True)
# you are going to need more than 10 samples to remove the noise. At least 1000 for a nice image.

img.save("cornell_box.png")

img.show()