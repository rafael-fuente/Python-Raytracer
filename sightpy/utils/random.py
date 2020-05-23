import numpy as np
from ..utils.vector3 import vec3


def random_in_unit_disk(shape):
    r = np.random.rand(shape)
    phi = np.random.rand(shape)*2*np.pi
    return r * np.cos(phi), r * np.sin(phi)


def random_in_unit_sphere(shape):

	#https://mathworld.wolfram.com/SpherePointPicking.html
    phi = np.random.rand(shape)*2*np.pi
    u = 2.*np.random.rand(shape) - 1.
    r = np.sqrt(1-u**2)
    return vec3( r*np.cos(phi),  r*np.sin(phi), u)



def random_in_unit_hemisphere(shape,normal):
    r = random_in_unit_sphere(shape)
    return vec3.where( normal.dot(r) < 0. , r*-1., r )



def random_in_unit_cone(shape,cosθmax, normal):


    ax_w = normal
    a = vec3.where( np.abs(ax_w.x) > 0.9 , vec3(0,1,0) , vec3(1,0,0))
    ax_v = ax_w.cross(a).normalize()
    ax_u  = ax_w.cross(ax_v)

    phi = np.random.rand(shape)*2*np.pi
    r2 =  np.random.rand(shape)

    z = 1. + r2 * (cosθmax - 1.)
    x = np.cos(phi) * np.sqrt(1. - z**2)
    y = np.sin(phi) * np.sqrt(1. - z**2)




    return ax_u*x + ax_v*y + ax_w*z




def random_in_unit_cones(shape, origin, target_list):

    l = len(target_list)


    mask = (np.random.rand(shape) * l).astype(int)
    mask_list = [None]*l

    cosθmax_list = [None]*l
    ax_u_list = [None]*l
    ax_v_list = [None]*l
    ax_w_list = [None]*l

    for i in range(l):

        ax_w_list[i] = (target_list[i].center - origin).normalize()
        a = vec3.where( np.abs(ax_w_list[i].x) > 0.9 , vec3(0,1,0) , vec3(1,0,0))
        ax_v_list[i] = ax_w_list[i].cross(a).normalize()
        ax_u_list[i]  = ax_w_list[i].cross(ax_v_list[i])
        mask_list[i] = mask == i


        target_distance = np.sqrt((target_list[i].center - origin).dot(target_list[i].center - origin))

        cosθmax_list[i] = np.sqrt(1 - np.clip(target_list[i].radius / target_distance, 0., 1.)**2 )


    phi = np.random.rand(shape)*2*np.pi
    r2 =  np.random.rand(shape)

    cosθmax = np.select(mask_list, cosθmax_list)
    ax_w =  vec3.select(mask_list, ax_w_list)
    ax_v =  vec3.select(mask_list, ax_v_list)
    ax_u =  vec3.select(mask_list, ax_u_list)

    z = 1. + r2 * (cosθmax - 1.)
    x = np.cos(phi) * np.sqrt(1. - z**2)
    y = np.sin(phi) * np.sqrt(1. - z**2)

    ray_dir = ax_u*x + ax_v*y + ax_w*z 

    PDF = 0.
    for i in range(l):
        PDF +=  np.where( ray_dir.dot(ax_w_list[i]) > cosθmax_list[i] , 1/((1 - cosθmax_list[i])*2*np.pi) , 0. )
    PDF = PDF/l

    return ray_dir, PDF
