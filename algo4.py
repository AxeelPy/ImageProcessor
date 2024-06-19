import cv2
from time import sleep
import asyncio
from copy import deepcopy
import multiprocessing as mp
import os
import threading as th
import numpy
from algo4_dep import Get_Image_Brightness, Get_Pixel_Average, increase_saturation, Multiprocessing_Functions
import time

class Image_Edit:

    def __init__(self, Module_Name, Image_path):
        self.Module_name = Module_Name
        self.path = Image_path
        self.image = cv2.imread(Image_path)
        self.file_extension = "."+Image_path.split(".")[-1]
        self.staged_changes = []

def asrun(func, *args):
    asyncio.run(func(*args))

if __name__ == "__main__":

    IMAGE = "images/rndm2.jpg"

    main = Image_Edit('main', IMAGE)
    main.brightness = asyncio.run(Get_Image_Brightness(main.image))
    main.average = asyncio.run(Get_Pixel_Average(main.brightness))

    PROCESSING_CLASS = Multiprocessing_Functions(6)
    # Formula is 50 / average * 6
    SATURATION_CHANGE = 100/main.average*3
    print(f"Saturation change is {SATURATION_CHANGE} points")

    start = time.time()
    
    segments = asyncio.run(PROCESSING_CLASS.segment_image(main.image))
    print(f"Average is {main.average}")
    process_pool = []
    index = 0
    for segment in segments:
        process_pool.append(mp.Process(target=asrun, args=(increase_saturation, main, SATURATION_CHANGE, segment, index)))
        index += 1
    [i.start() for i in process_pool]

    thr = th.Thread(target=PROCESSING_CLASS.regroup_image, args=(main, process_pool,))
    thr.start()
    while thr.is_alive():
        time.sleep(0.125)
    end = time.time()
    print(f"Process took {end-start} seconds") 
# 7 cores: 18.15181 seconds
# 6 cores: 17.87884 seconds <-
# 5 cores: 19.15749 seconds
# 4 cores: 26.29836 seconds