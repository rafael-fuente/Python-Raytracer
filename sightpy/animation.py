from .scene import Scene
import numpy as np
from pathlib import Path


def create_animation(scene,samples_per_pixel, fps, start_time, final_time, update_scene, name):

    """
	this function render a list of frames and saves them in ./frames folder. You can make an animation the using ffmpeg running
	from the command prompt:
    """
    #ffmpeg -r 60 -f image2 -s 854x480 -i your_image_%d.png -vcodec libx264 -crf 1 -pix_fmt yuv420p your_video.mp4
              #fps          #resoluion                                      #crf = quality (less is better)


    number_of_frames = int(fps*(final_time - start_time))
    dt = (final_time - start_time)/number_of_frames
    t = start_time

    try:
    	Path("./frames").mkdir()

    except FileExistsError:
        pass


    for i in range(0,number_of_frames):
        update_scene(scene, t)
        img = scene.render(samples_per_pixel)
        t += dt
        img.save("frames/" + name + "_" + str(i) + ".png")




def create_animation_using_opencv(scene, samples_per_pixel , fps, start_time, final_time, update_scene, name):

    import cv2
    number_of_frames = int(fps*(final_time - start_time))
    dt = (final_time - start_time)/number_of_frames
    t = start_time


    videodims = (scene.camera.screen_width, scene.camera.screen_height)
    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')    
    video = cv2.VideoWriter(name,fourcc, fps,videodims)

    for i in range(0,number_of_frames):
        update_scene(scene, t)
        frame = scene.render(samples_per_pixel)
        video.write(cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR))       
        t += dt

    video.release()
