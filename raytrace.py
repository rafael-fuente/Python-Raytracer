from constants import *
from vector3 import vec3, extract, rgb
import numpy as np
from functools import reduce as reduce 

def raytrace(ray_origin, ray_dir, scene, ray_depth, ray_n):
    # ray_depth is the number of the refrections and refractions, starting at zero for camera rays
    # ray_n is the index of refraction in which the ray is travelling
    

    inters = [s.intersect(ray_origin, ray_dir) for s in scene.collider_list]
    distances, hit_orientation = zip(*inters)
    
    # si no hay interseccion con ningun objeto devuelve FARAWAY

    
    
    # get the shotest distance collision
    nearest = reduce(np.minimum, distances)
    color = rgb(0, 0, 0)
    
    #este trozo de codigo devuelve la distancia al objeto y la colorea es una escala de blancos
    #FARAWAY es demasiado grande asi que usamos max_r_distance
    """max_r_distance = 10
    r_distance = np.where(nearest <= max_r_distance, nearest, max_r_distance)
    norm_r_distance = r_distance/max_r_distance
    return rgb(norm_r_distance, norm_r_distance, norm_r_distance)"""
    
    
    for (s, d , h) in zip(scene.collider_list, distances, hit_orientation):
        hit = (nearest != FARAWAY) & (d == nearest)
        if np.any(hit):
            
            hit_distance_extracted = extract(hit, d)
            hit_orientation_extracted = extract(hit, h)            
            ray_origin_extracted = ray_origin.extract(hit)
            ray_dir_extracted = ray_dir.extract(hit)
            ray_n_extracted = ray_n.extract(hit)
            
            cc = s.assigned_surface.material.shader(s, ray_origin_extracted, ray_dir_extracted, hit_distance_extracted,hit_orientation_extracted, scene, ray_depth, ray_n_extracted)
            color += cc.place(hit)
    return color
    


    
    

