from PIL import Image, ImageFilter
import numpy as np
from ...utils.colour_functions import sRGB_to_sRGB_linear



def to_image(arr):
    img = [Image.fromarray((255 * arr[:,:,i]).astype(np.uint8), "L") for i in range(0,3)]
    return Image.merge("RGB", img)

def to_array(img):
    return np.asarray(img)/256. 





def blur_skybox(img_array, blur, cubemap):

	print("blurring " + cubemap)

	N = int(img_array.shape[0]/3)

	left = img_array[ 1*N:2*N,  0*N:1*N]
	front = img_array[N:2*N,  N:2*N]
	right =  img_array[  N:2*N, 2*N:3*N]
	back = img_array[N:2*N, 3*N:4*N]
	top = img_array[0:1*N, 1*N:2*N]
	bottom = img_array[2*N:3*N, 1*N:2*N] 


	cubelist = [[None,top,None, None],
	            [left,front,right, back],
	            [None,bottom,None, None]]



	back_blur = np.zeros((N*3, N*3,3))


	back_blur[ 1*N:2*N,  0*N:1*N] =   cubelist[1][0-2]      #left
	back_blur[N:2*N,  N:2*N] =   cubelist[1][1-2]      #front
	back_blur[  N:2*N, 2*N:3*N] =   cubelist[1][2-2]      # right
	back_blur[2*N:3*N, 1*N:2*N] =  np.rot90(cubelist[2][1] ,  k=2)       #bottom 
	back_blur[0:1*N, 1*N:2*N] =   np.rot90(cubelist[0][1], k=2)     #top


	back_blur =  to_image(back_blur) 
	back_blur = (back_blur).filter(ImageFilter.GaussianBlur(radius=blur))

	back_blur = to_array(back_blur)

	back_blur = back_blur[N:2*N,  N:2*N]


	top_blur = np.zeros((N*3, N*3,3))
	top_blur[ 1*N:2*N,  0*N:1*N] =   np.rot90(cubelist[1][0], k=-1)      #left
	top_blur[N:2*N,  N:2*N] =   cubelist[1-1][1]      #front
	top_blur[  N:2*N, 2*N:3*N] =   np.rot90(cubelist[1][2], k=1)      # right
	top_blur[2*N:3*N, 1*N:2*N] =  cubelist[1][1]       #bottom 
	top_blur[0:1*N, 1*N:2*N] =   np.rot90(cubelist[1][3], k=2)      #top
	top_blur =  to_image(top_blur) 
	top_blur = (top_blur).filter(ImageFilter.GaussianBlur(radius=blur))

	top_blur = to_array(top_blur)

	top_blur = top_blur[N:2*N,  N:2*N]




	bottom_blur = np.zeros((N*3, N*3,3))


	bottom_blur[ 1*N:2*N,  0*N:1*N] =   np.rot90(cubelist[1][0], k=1)      #left
	bottom_blur[N:2*N,  N:2*N] =   cubelist[1+1][1]      #front
	bottom_blur[  N:2*N, 2*N:3*N] =   np.rot90(cubelist[1][2], k=-1)      # right
	bottom_blur[2*N:3*N, 1*N:2*N] =  np.rot90(cubelist[1][3], k=2)       #bottom 
	bottom_blur[0:1*N, 1*N:2*N] =   cubelist[1][1]      #top

	bottom_blur =  to_image(bottom_blur) 
	bottom_blur = (bottom_blur).filter(ImageFilter.GaussianBlur(radius=blur))

	bottom_blur = to_array(bottom_blur)

	bottom_blur = bottom_blur[N:2*N,  N:2*N]



	right_blur = np.zeros((N*3, N*3,3))

	right_blur[ 1*N:2*N,  0*N:1*N] =   cubelist[1][0+1]      #left
	right_blur[N:2*N,  N:2*N] =   cubelist[1][1+1]      #front
	right_blur[  N:2*N, 2*N:3*N] =   cubelist[1][2+1]      # right
	right_blur[2*N:3*N, 1*N:2*N] =  np.rot90(cubelist[2][1] )       #bottom 
	right_blur[0:1*N, 1*N:2*N] =   np.rot90(cubelist[0][1], k=-1)     #top

	right_blur =  to_image(right_blur).filter(ImageFilter.GaussianBlur(radius=blur)) 


	right_blur = to_array(right_blur)

	right_blur = right_blur[N:2*N,  N:2*N]



	front_blur  = np.zeros((N*3, N*3,3))


	front_blur [ 1*N:2*N,  0*N:1*N] =   cubelist[1][0]      #left
	front_blur [N:2*N,  N:2*N] =   cubelist[1][1]      #front
	front_blur [  N:2*N, 2*N:3*N] =   cubelist[1][2]      # right
	front_blur [2*N:3*N, 1*N:2*N] =  cubelist[2][1]       #bottom 
	front_blur [0:1*N, 1*N:2*N] =   cubelist[0][1]      #top

	front_blur =  to_image(front_blur)

	front_blur = (front_blur).filter(ImageFilter.GaussianBlur(radius=blur))

	front_blur = to_array(front_blur)

	front_blur = front_blur[N:2*N,  N:2*N]




	left_blur = np.zeros((N*3, N*3,3))

	left_blur[ 1*N:2*N,  0*N:1*N] =   cubelist[1][0-1]      #left
	left_blur[N:2*N,  N:2*N] =   cubelist[1][1-1]      #front
	left_blur[  N:2*N, 2*N:3*N] =   cubelist[1][2-1]      
	left_blur[2*N:3*N, 1*N:2*N] =  np.rot90(cubelist[2][1], k=-1 )       #bottom 
	left_blur[0:1*N, 1*N:2*N] =   np.rot90(cubelist[0][1], k=1)     #top


	left_blur =  to_image(left_blur).filter(ImageFilter.GaussianBlur(radius=blur)) 


	left_blur = to_array(left_blur)

	left_blur = left_blur[N:2*N,  N:2*N]






	skybox_blurred = np.zeros((N*3, N*4,3))

	skybox_blurred[ 1*N:2*N,  0*N:1*N] = left_blur
	skybox_blurred[N:2*N,  N:2*N] = front_blur
	skybox_blurred[  N:2*N, 2*N:3*N] =  right_blur
	skybox_blurred[N:2*N, 3*N:4*N] = back_blur
	skybox_blurred[0:1*N, 1*N:2*N] = top_blur
	skybox_blurred[2*N:3*N, 1*N:2*N] = bottom_blur 

	return sRGB_to_sRGB_linear(skybox_blurred)

