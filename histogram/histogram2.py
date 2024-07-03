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
        self.file_extension = "."+Image_path.split(".")[-1]
        self.staged_changes = []

    async def sRGBtoPerceivedBrightness(self, RGB): 
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
        
        NewNumArray = []
        for row in NumArray:
            TempRow = []
            for column in row:
                TempRow = TempRow + await self.sRGBtoPerceivedBrightness(column)
            NewNumArray.append(TempRow)
        self.Image_brightness = NewNumArray

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
            pool.append(mp.Process(target=self.Change_Image, args=(10, segments[process], process)))
        [i.start() for i in pool]

        print(pool)
        print(pool[0].is_alive())
        th.Thread(target=self.regroup_image, args=(processes, pool,)).start()


    async def increase_saturation(self, change, image):
        
        image_copy = deepcopy(image)

        async def get_highest_numbers(tuple):
            
            red, green, blue = tuple[0], tuple[1], tuple[2]

            if red >= green:
                if red == green:
                    if red > blue:
                        return [[0, 1], 2]
                    if red == blue:
                        return [[0, 1, 2]]
                    return [2, [0, 1]]
                if red > blue:
                    if blue > green:
                        return [0, 2, 1]
                    if blue == green:
                        return [0, [1, 2]]
                    return [0, 1, 2]
                if red == blue:
                    return [[0,2], 1]
                return [2, 0, 1]

            elif red >= blue:
                if red == blue:
                    return [1, [0, 2]]
                if green > blue:
                    return [1, 0, 2]
                raise Exception(f"Unexpected result in get_highest_number function")

            elif blue >= green:
                if blue == green:
                    return [[1, 2], 0]
                return [2, 1, 0]
            
            return [1, 2, 0]        
    
        async def change_saturation(tuple, change=change):

            if not -100 <= change <= 100:
                raise Exception("The 'change' variable should be between -100 and 100")

            # print(f"Old ass tuple; {tuple}")
            highest_to_lowest_index = await get_highest_numbers(tuple)
            plain_HtL_index = []


            high = 15
            medium = 14
            low = 13
            # All RGB values are different, like [0, 1, 2]
            if len(highest_to_lowest_index) == 3:
                h_change = change / 255 * high
                m_change = change / 255 * medium
                l_change = change / 255 * low
                plain_HtL_index = highest_to_lowest_index

            # 2 RGB values are the same
            elif len(highest_to_lowest_index) == 2:
                
                # [[0, 1], 2]
                if isinstance(highest_to_lowest_index[0], list):
                    h_change = change / 255 * high
                    m_change = change / 255 * medium
                    l_change = change / 255 * low
                    plain_HtL_index = [highest_to_lowest_index[0][0], highest_to_lowest_index[0][1], highest_to_lowest_index[1]]
                
                # [0, [1, 2]]
                else:
                    h_change = change / 255 * high
                    m_change = change / 255 * medium
                    l_change = change / 255 * low
                    plain_HtL_index = [highest_to_lowest_index[0], highest_to_lowest_index[1][0], highest_to_lowest_index[1][1]]
            
            # [[0, 1, 2]]
            elif len(highest_to_lowest_index) == 1:
                h_change = change / 255 * high
                m_change = change / 255 * medium
                l_change = change / 255 * low
                plain_HtL_index = [highest_to_lowest_index[0][0], highest_to_lowest_index[0][1], highest_to_lowest_index[0][2]]

            # print(h_change, m_change, l_change)
            # print(plain_HtL_index)
            tuple[plain_HtL_index[0]] = h_change*tuple[plain_HtL_index[0]]
            tuple[plain_HtL_index[1]] = m_change*tuple[plain_HtL_index[1]]
            tuple[plain_HtL_index[2]] = l_change*tuple[plain_HtL_index[2]]
            # print(f"New tuple: {tuple}")
            return tuple

        Saturated_image = []
        print(type(image))
        for row in list(image_copy):
            temp_list = []
            for column in row:
                # print(f"Column before: {column}")
                column = await change_saturation(column)
                temp_list.append(column)
                # print(f"Column after: {column}")
            Saturated_image.append(temp_list)

        cv2.imshow('image', numpy.uint8(Saturated_image))
        cv2.waitKey(0)
        if not os.path.exists("processed_images/"):
            os.makedirs("processed_images/")
        cv2.imwrite(f"processed_images/{self.Module_name}_{self.file_extension}", numpy.uint8(Saturated_image))

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

        print(f'processing_images/{Process_Number}_{self.Module_name}_segment{self.file_extension}')

        if not os.path.exists('processing_images/'):
            os.makedirs('processing_images/')

        cv2.imwrite(f'processing_images/{Process_Number}_{self.Module_name}_segment{self.file_extension}', image)

    def regroup_image(self, Processes, pool):
        while True:
            if any([i.is_alive() for i in pool]):
                sleep(0.125)
            else:
                print("done")
                break

        refused_image = []
        for i in range(0, Processes):
            print(f"processing_images/{i}_{self.Module_name}_segment.png")
            element = cv2.imread(f"processing_images/{i}_{self.Module_name}_segment{self.file_extension}")
            refused_image = refused_image + list(element)
        cv2.imshow('image', numpy.array(refused_image))
        cv2.waitKey(0)


if __name__ == "__main__":

    # TO DEBUG: Set rule to print all numbers without numpy truncation. Not efficient because the array contains every RGB value of every pixel
    # numpy.set_printoptions(threshold=sys.maxsize)

    main = Image_Edit("main", 'images/rndm.png')
    asyncio.run(main.increase_saturation(25, main.image))
    # main.Image_Processing_Assigner()
    # asyncio.run(Change_Image(img, 25))
    quit()
    # img[n][j] where n = width of image, it represents the ROW
    # meanwhile j is the COLUMN on a given row (n), j = height
    # Example: img[3][340] refers to pixel in row 3, column 340
    asyncio.run(Get_Image_Brightness(img))

