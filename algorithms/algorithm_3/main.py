import cv2
from time import sleep
import asyncio
from copy import deepcopy
import multiprocessing as mp
import os
import threading as th
import numpy
from algorithms.algorithm_3.dependencies import increase_saturation, Multiprocessing_Functions
import time
import algorithms.algorithm_3.JIT as JIT
from numba.typed import List
import PIL
from PIL import ImageEnhance, ImageStat
from random import randint

    


class ImageProcessor:

    def assigner(self, MainClass, Image_path):

        self.Image = Image_Edit(Image_path.split(".")[0], MainClass.tx3 + "/" + Image_path)

        self.Process = Multiprocessing_Functions(6)
        
        self.imgprocessor(MainClass.tx3 + "/" + Image_path)

        print(self.Process.done)
        if self.Process.done["error"] is False:
            print("Appending to returnlist:", self.Process.done)
            # Returnlist for other functions being updated, along with the counter to calculate the %
            MainClass.returnlist.append(self.Process.done)
            MainClass.done = MainClass.done + 1
            MainClass.imgnum.setText(str(MainClass.index+1) + " of " + str(len(MainClass.returnlist)))
            MainClass.imgprc.setText(f"{MainClass.done}/{MainClass.fromlen}\n{int((MainClass.done)/(MainClass.fromlen)*100)}% Done")

            MainClass.nextBtn.setEnabled(True)
            return False
        else:
            print("ERROR DETECTED IN IMAGE BRUV")
            MainClass.fromlen = MainClass.fromlen - 1
            return True
    
    def imgprocessor(self, file: str):

        if not os.path.exists(file): return {"error": True, "reason": "File does not exist"}

        if not os.path.exists("temp/"):
            os.mkdir("temp/")

        self.Image.saturation_change = 100/self.Image.average*3
        
        print(f"Saturation change is {self.Image.saturation_change} points")

        process_pool = []
        start = time.time()
        
        segments = asyncio.run(self.Process.segment_image(self.Image.raw))

        print(f"Average is {self.Image.average}")
        process_pool = []
        index = 0
        for segment in segments:
            process = mp.Process(target=asrun, args=(increase_saturation, self, self.Image.saturation_change, segment, index))
            process_pool.append(process)
            index += 1
        [i.start() for i in process_pool]

        thr = th.Thread(target=self.Process.regroup_image, args=(self, process_pool,))
        thr.start()
        while thr.is_alive():
            time.sleep(0.125)
        end = time.time()
        print(f"Process took {end-start} seconds")

class Image_Edit:

    def __init__(self, Module_Name, Image_path):
        self.name = Module_Name
        self.path = Image_path
        self.raw = cv2.imread(Image_path)
        self.extension = "."+Image_path.split(".")[-1]
        self.staged = []

        self.brightness = JIT.Get_Image_Brightness(self.raw)
        MCList = List()
        for i in self.brightness:
            MCList.append(i)
        self.average = JIT.Get_Pixel_Average(MCList)
    

def asrun(func, *args):
    asyncio.run(func(*args))

if __name__ == "__main__":

    IMAGE = "images/rndm.png"
    main = Image_Edit('main', IMAGE)
    main.brightness = JIT.Get_Image_Brightness(main.image)
    # with open("algo4_log.txt", "w") as f: f.write(str(main.brightness)); f.close()

    MCList = List()
    for i in main.brightness:
        MCList.append(i)
    main.average = JIT.Get_Pixel_Average(MCList)

    PROCESSING_CLASS = Multiprocessing_Functions(6)
    # Formula is 50 / average * 6
    SATURATION_CHANGE = 100/main.average*3
    print(f"Saturation change is {SATURATION_CHANGE} points")

    start = time.time()
    
    # segments = asyncio.run(PROCESSING_CLASS.segment_image(main.image))
    segments = []

    print(f"Average is {main.average}")
    process_pool = []
    index = 0
    for segment in segments:
        process = mp.Process(target=asrun, args=(increase_saturation, main, SATURATION_CHANGE, segment, index))
        process_pool.append(process)
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