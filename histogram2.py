import cv2 
import asyncio
import numpy
import sys
from copy import deepcopy
import time
# importing library for plotting 
from matplotlib import pyplot as plt
import multiprocessing as mp
import os
import threading as th
from time import sleep

class Image_Edit:
    def __init__(self, Module_Name, Image_path):
        self.Module_name = Module_Name
        self.path = Image_path
        self.image = cv2.imread(Image_path)

    async def sRGBtoPerceivedBrightness(self, RGB):
        start = time.time()  
        # ========= Convert to luminance value ======
        colors = [RGB[0] / 255, RGB[1] / 255, RGB[2] / 255]
        LuminanceValues = []

        for color in colors:
            if color <= 0.04045:
                LuminanceValues.append(color/12.92)
            else:
                LuminanceValues.append(numpy.power(((color+0.055)/1.055), 2.4))
        
        Luminance = 0.2126 * LuminanceValues[0] + 0.7152 * LuminanceValues[1] + 0.0722 * LuminanceValues[2]

        # ========== Find perceived brightness ============
        if Luminance <= (216/24389):
            return Luminance * (216/24389)
        else:
            return numpy.power(Luminance, (1/3)) * 116 - 16

    # Expects a list in the format of NewNumArray in Get_Image_Brightness
    async def Get_Pixel_Average(self, BrightnessArray):
        
        total_brightness: float = 0
        total_length = 0
        
        for value in BrightnessArray:
            total_brightness = total_brightness + sum(value)
            total_length = total_length + 1

        return total_brightness / total_length

    async def Get_Image_Brightness(self, NumArray):
        
        start = time.time()
        NewNumArray = []
        for row in NumArray:
            TempRow = []
            for column in row:
                TempRow = TempRow + await self.sRGBtoPerceivedBrightness(column)
            NewNumArray.append(TempRow)
        print(NewNumArray)
        print("")
        print(NumArray)
        print(sum(NumArray[0][0]))
        end = time.time()
        print(end-start)

    def Image_Processing_Assigner(self, processes: int = 4):
        
        Image_Length = len(self.image)

        Segment_size = Image_Length // processes
        segments = []

        used_segments = 0
        while True:
            if used_segments + Segment_size * 2 > Image_Length:
                segments.append(self.image[used_segments:])
                break
            segments.append(self.image[used_segments:used_segments+Segment_size])
            used_segments = used_segments + Segment_size
        
        pool = []
        for process in range(0, processes):
            pool.append(mp.Process(target=self.Change_Image, args=(10, segments[process], process)).start())

        th.Thread(target=self.regroup_image, args=(processes, pool,))


    def Change_Image(self, change, image, Process_Number: int):

        for row in list(image):
            for column in row:
                column[0], column[1], column[2] = column[0] + change, column[1] + change, column[2] + change
                
                if column[0] > 255:
                    column[0] = 255
                elif column[0] < 0:
                    column[0] = 0

                if column[1] > 255:
                    column[1] = 255
                elif column[1] < 0:
                    column[1] = 0
                
                if column[2] > 255:
                    column[2] = 255
                elif column[2] < 0:
                    column[2] = 0

        #cv2.imshow('image',image)
        #cv2.waitKey(0)

        print(f'processing_images/{Process_Number}_{self.Module_name}_segment.png')

        if not os.path.exists('processing_images/'):
            os.makedirs('processing_images/')

        cv2.imwrite(f'processing_images/{Process_Number}_{self.Module_name}_segment.png', image)

    def regroup_image(self, Processes, pool):
        if any([i.is_alive for i in pool]):
            sleep(0.125)
        else:
            print("done")

if __name__ == "__main__":

    # TO DEBUG: Set rule to print all numbers without numpy truncation. Not efficient because the array contains every RGB value of every pixel
    # numpy.set_printoptions(threshold=sys.maxsize)

    main = Image_Edit("main", 'images/rndm.png')
    main.Image_Processing_Assigner()
    # asyncio.run(Change_Image(img, 25))
    quit()
    # img[n][j] where n = width of image, it represents the ROW
    # meanwhile j is the COLUMN on a given row (n), j = height
    # Example: img[3][340] refers to pixel in row 3, column 340
    asyncio.run(Get_Image_Brightness(img))

