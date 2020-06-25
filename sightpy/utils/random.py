import numpy as np
from ..utils.vector3 import vec3
from abc import abstractmethod 

def random_in_unit_disk(shape):
    r = np.sqrt(np.random.rand(shape))
    phi = np.random.rand(shape)*2*np.pi
    return r * np.cos(phi), r * np.sin(phi)

def random_in_unit_sphere(shape):

    #https://mathworld.wolfram.com/SpherePointPicking.html
    phi = np.random.rand(shape)*2*np.pi
    u = 2.*np.random.rand(shape) - 1.
    r = np.sqrt(1-u**2)
    return vec3( r*np.cos(phi),  r*np.sin(phi), u) 



class PDF:    
    """Probability density function"""
    @abstractmethod 
    def value(self,ray_dir):
        """get probability density function value at direction ray_dir"""
        pass

    @abstractmethod 
    def generate(self):
        """generate random ray  directions according the probability density function"""
        pass




class hemisphere_pdf(PDF):    
    """Probability density Function"""
    def __init__(self,shape, normal):
        self.shape = shape
        self.normal = normal


    def value(self,ray_dir):
        return 1./(2.*np.pi)
    
    def generate(self):
        r = random_in_unit_sphere(self.shape)
        return vec3.where( self.normal.dot(r) < 0. , r*-1., r )


class cosine_pdf(PDF):    
    """Probability density Function"""
    def __init__(self,shape, normal):
        self.shape = shape
        self.normal = normal



    def value(self,ray_dir):
        return np.clip(ray_dir.dot(self.normal),0.,1.)/np.pi
    
    def generate(self):
        ax_w = self.normal
        a = vec3.where( np.abs(ax_w.x) > 0.9 , vec3(0,1,0) , vec3(1,0,0))
        ax_v = ax_w.cross(a).normalize()
        ax_u  = ax_w.cross(ax_v)

        phi = np.random.rand(self.shape)*2*np.pi
        r2 =  np.random.rand(self.shape)

        z = np.sqrt(1 - r2)
        x = np.cos(phi) * np.sqrt(r2)
        y = np.sin(phi) * np.sqrt(r2)

        return ax_u*x + ax_v*y + ax_w*z




class spherical_caps_pdf(PDF):    
    """Probability density Function"""
    def __init__(self,shape, origin, importance_sampled_list):
        self.shape = shape
        self.origin = origin
        self.importance_sampled_list = importance_sampled_list
        self.l = len(importance_sampled_list)

    def value(self, ray_dir):
        PDF_value = 0.
        for i in range(self.l):
            PDF_value +=  np.where( ray_dir.dot(self.ax_w_list[i]) > self.cosθmax_list[i] , 1/((1 - self.cosθmax_list[i])*2*np.pi) , 0. )
        PDF_value = PDF_value/self.l
        return PDF_value


    def generate(self):
        shape = self.shape
        origin = self.origin
        importance_sampled_list = self.importance_sampled_list
        l = self.l

        mask = (np.random.rand(shape) * l).astype(int)
        mask_list = [None]*l

        cosθmax_list = [None]*l
        ax_u_list = [None]*l
        ax_v_list = [None]*l
        ax_w_list = [None]*l

        for i in range(l):

            ax_w_list[i] = (importance_sampled_list[i].center - origin).normalize()
            a = vec3.where( np.abs(ax_w_list[i].x) > 0.9 , vec3(0,1,0) , vec3(1,0,0))
            ax_v_list[i] = ax_w_list[i].cross(a).normalize()
            ax_u_list[i]  = ax_w_list[i].cross(ax_v_list[i])
            mask_list[i] = mask == i


            target_distance = np.sqrt((importance_sampled_list[i].center - origin).dot(importance_sampled_list[i].center - origin))

            cosθmax_list[i] = np.sqrt(1 - np.clip(importance_sampled_list[i].bounded_sphere_radius / target_distance, 0., 1.)**2 )

        self.cosθmax_list = cosθmax_list
        self.ax_w_list = ax_w_list

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
        return ray_dir
    

class mixed_pdf(PDF):    
    """Probability density Function"""
    def __init__(self,shape, pdf1, pdf2, pdf1_weight = 0.5):

        self.pdf1_weight = pdf1_weight
        self.pdf2_weight = 1. - pdf1_weight
        self.shape = shape
        self.pdf1 = pdf1
        self.pdf2 = pdf2


    def value(self,ray_dir):
        return self.pdf1.value(ray_dir) * self.pdf1_weight  + self.pdf2.value(ray_dir) * self.pdf2_weight
    
    def generate(self):
        mask = np.random.rand(self.shape)
        return vec3.where( mask < self.pdf1_weight, self.pdf1.generate(), self.pdf2.generate() )







def random_in_unit_spherical_caps(shape, origin, importance_sampled_list):

    l = len(importance_sampled_list)


    mask = (np.random.rand(shape) * l).astype(int)
    mask_list = [None]*l

    cosθmax_list = [None]*l
    ax_u_list = [None]*l
    ax_v_list = [None]*l
    ax_w_list = [None]*l

    for i in range(l):

        ax_w_list[i] = (importance_sampled_list[i].center - origin).normalize()
        a = vec3.where( np.abs(ax_w_list[i].x) > 0.9 , vec3(0,1,0) , vec3(1,0,0))
        ax_v_list[i] = ax_w_list[i].cross(a).normalize()
        ax_u_list[i]  = ax_w_list[i].cross(ax_v_list[i])
        mask_list[i] = mask == i


        target_distance = np.sqrt((importance_sampled_list[i].center - origin).dot(importance_sampled_list[i].center - origin))

        cosθmax_list[i] = np.sqrt(1 - np.clip(importance_sampled_list[i].bounded_sphere_radius / target_distance, 0., 1.)**2 )


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

def random_in_unit_spherical_cap(shape,cosθmax,normal):


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