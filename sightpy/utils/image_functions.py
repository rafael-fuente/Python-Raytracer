from PIL import Image, ImageFilter
import numpy as np
from pathlib import Path
from .colour_functions import sRGB_to_sRGB_linear


def load_image(path):
    img = Image.open(Path(path))
    return np.asarray(img)/256.


def load_image_with_blur(path, blur = 0.):
    img = Image.open(Path(path))
    img = img.filter(ImageFilter.GaussianBlur(radius=blur))

    return np.asarray(img)/256.




def load_image_as_linear_sRGB(path, blur = 0.0):

    path = Path(path)
    location = str(path.parents[0])
    name = str(path.name)#be sure that image doesn't lose quality

    print("proccesing " + name)
    img = Image.open(path) 

    if blur != 0.0:
        img = img.filter(ImageFilter.GaussianBlur(radius=blur))

    img_array = np.asarray(img)/256. 
    img_sRGB_linear_array = sRGB_to_sRGB_linear(img_array)
    return img_sRGB_linear_array





