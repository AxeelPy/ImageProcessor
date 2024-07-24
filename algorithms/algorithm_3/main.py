import cv2
from time import sleep
import asyncio
from copy import deepcopy
import multiprocessing as mp
import os
import threading as th
import numpy
from algorithms.algorithm_3.dependencies import Get_Image_Brightness, Get_Pixel_Average, increase_saturation, Multiprocessing_Functions
import time
import algorithms.algorithm_3.JIT as JIT
from numba.typed import List
import PIL
from PIL import ImageEnhance, ImageStat
from random import randint

class ImageProcessor:

    def assigner(MainClass, file):
        
        PROCESSING_CLASS = Multiprocessing_Functions(6)
        # Formula is 50 / average * 6

        returnage = ImageProcessor.imgprocessor(MainClass.tx3 + "/" + file, PROCESSING_CLASS)

        if returnage["error"] is False:
            # Returnlist for other functions being updated, along with the counter to calculate the %
            MainClass.returnlist.append(PROCESSING_CLASS.cooked_image)
            MainClass.done = MainClass.done + 1
            MainClass.imgnum.setText(str(MainClass.index+1) + " of " + str(len(MainClass.returnlist)))
            MainClass.imgprc.setText(f"{MainClass.done}/{MainClass.fromlen}\n{int((MainClass.done)/(MainClass.fromlen)*100)}% Done")

            MainClass.nextBtn.setEnabled(True)
            return False
        else:
            print("ERROR DETECTED IN IMAGE BRUV")
            MainClass.fromlen = MainClass.fromlen - 1
            return True

    def imgprocessor(file: str, PROCESSING_CLASS):

        if not os.path.exists(file): return {"error": True, "reason": "File does not exist"}

        if not os.path.exists("temp/"):
            os.mkdir("temp/")

        main = Image_Edit('main', file)
        main.brightness = JIT.Get_Image_Brightness(main.image)
        # with open("algo4_log.txt", "w") as f: f.write(str(main.brightness)); f.close()
        
        MCList = List()
        for i in main.brightness:
            MCList.append(i)

        main.average = JIT.Get_Pixel_Average(MCList)
        SATURATION_CHANGE = 100/main.average*3
        
        print(f"Saturation change is {SATURATION_CHANGE} points")

        start = time.time()
        
        segments = asyncio.run(PROCESSING_CLASS.segment_image(main.image))
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
        
        return PROCESSING_CLASS.returnage


class ImageProcessor: 
    def assigner(self, Image_path):
        self.Module_name = "temp"
        self.path = Image_path
        self.image = cv2.imread(Image_path)
        self.file_extension = "."+Image_path.split(".")[-1]
        self.brightness = JIT.Get_Image_Brightness(self.image)

        MachineList = List()
        for l in self.brightness:
            MachineList.append(l)
        
        self.average = JIT.Get_Pixel_Average(MachineList)
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
    
    segments = asyncio.run(PROCESSING_CLASS.segment_image(main.image))
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