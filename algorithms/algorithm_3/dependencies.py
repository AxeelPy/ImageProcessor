import cv2
from time import sleep
from copy import deepcopy
import multiprocessing as mp
import os
import threading as th
import numpy
from datetime import datetime
from . import JIT
from memory_profiler import profile
# Expects a list in the format of NewNumArray in Get_Image_Brightness
@profile
async def Get_Pixel_Average(BrightnessArray):
    total_brightness: float = 0
    total_length = sum([len(i) for i in BrightnessArray])

    for value in BrightnessArray:
        total_brightness = total_brightness + sum(value)

    print(total_brightness, total_length, len(BrightnessArray))
    return total_brightness / total_length

@profile
async def Get_Image_Brightness(NumArray):

    def sRGBtoPerceivedBrightness(column):
        return JIT.sRGBtoPerceivedBrightness(column)
    
    NewNumArray = []
    for row in NumArray:
        TempRow = []
        for column in row:
            TempRow.append(await sRGBtoPerceivedBrightness(column))
        NewNumArray.append(TempRow)
    return NewNumArray

@profile
async def increase_saturation(_class, change, image, index):

    async def get_highest_numbers(tuple):
        try:
            return await JIT.get_highest_numbers(tuple)
        except Exception:
            print("Exception ocurred, but nothing stops us")
            return

    async def change_saturation(tuple, index: list, change=change):

        if not -100 <= change <= 100:
            raise Exception("The 'change' variable should be between -100 and 100")

        # print(f"Old ass tuple; {tuple}")
        #if _class.brightness[index[0]][index[1]] > 50:
        #    # print("Brightness is over treshold")
        #    return tuple
        
        if image[index[0]][index[1]][0] - image[index[0]][index[1]][1] in range(-5, 6):
            if image[index[0]][index[1]][0] - image[index[0]][index[1]][2] in range(-5, 6):
                tuple = [i * (change / 255 * 15) for i in image[index[0]][index[1]]]
                for i in tuple: 
                    if i > 255: i = 255
                    if i < 0: i = 0
                return tuple
            
        #if sum(image[index[0]][index[1]]) > 250:
        #    print("Found lowkey white")
        #    tuple = [i + (change / 255 * 15) for i in image[index[0]][index[1]]]
        #    return tuple 

        highest_to_lowest_index = await get_highest_numbers(tuple)
        
        # if highest_to_lowest_index is None:
        #     print("No change because of exception")
        #     return tuple
        
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
        for tup in tuple:
            if tup > 255:
                tup = 255
            elif tup < 0:
                tup = 0
        # print(f"New tuple: {tuple}")
        return tuple

    image_copy = deepcopy(image)

    Saturated_image = []
    print(type(image))
    for row in range(0, len(image_copy)):
        temp_list = []
        for column in range(0, len(image_copy[row])):
            # print(f"Column before: {column}")
            c = await change_saturation(image_copy[row][column], [row, column])
            temp_list.append(c)
            # print(f"Column after: {column}")
        Saturated_image.append(temp_list)
    # cv2.imshow('image', numpy.uint8(Saturated_image))
    # cv2.waitKey(0)
    if not os.path.exists("processing_images/"):
        os.makedirs("processing_images/")
    cv2.imwrite(f"processing_images/{index}_{_class.Image.name}_segment{_class.Image.extension}", numpy.uint8(Saturated_image))

class Multiprocessing_Functions:
    
    def __init__(self, processes: int = 4):
        self.processes = processes

    def Image_Processing_Assigner(self, _class, func, *args):
        
        pool = []
        for process in range(0, self.processes):
            pool.append(mp.Process(target=func, args=(*args,), kwargs={"process_num": process, "name": _class.Module_name}))
        [i.start() for i in pool]

        print(pool)
        print(pool[0].is_alive())
        self.regroup_image(_class, pool,)
        return

    async def segment_image(self, image):
        Image_Length = len(image)

        Segment_size = Image_Length // self.processes
        segments = []

        used_segments = 0
        
        while True:
            if used_segments + Segment_size * 2 > Image_Length:
                segments.append(image[used_segments:])
                break
            segments.append(image[used_segments:used_segments+Segment_size])
            used_segments = used_segments + Segment_size
        
        return segments

    def regroup_image(self, _class, pool):
        while True:
            if any([i.is_alive() for i in pool]):
                sleep(0.125)
            else:
                print("done")
                break

        refused_image = []
        for i in range(0, self.processes):
            print(f"processing_images/{i}_{_class.Image.name}_segment.png")
            if os.path.exists(f"processing_images/{i}_{_class.Image.name}_segment{_class.Image.extension}"):
                element = cv2.imread(f"processing_images/{i}_{_class.Image.name}_segment{_class.Image.extension}")
                refused_image = refused_image + list(element)
            else:
                print("Error detected, but the show goes on")
        file_time = datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
        cv2.imwrite(f'temp/{file_time}-original{_class.Image.extension}', numpy.array(_class.Image.raw))
        cv2.imwrite(f'temp/{file_time}-edited{_class.Image.extension}', numpy.array(refused_image))
        self.done = {"error": False, "path": f"temp/{file_time}", "extension": _class.Image.extension, "ofile": None, "efile": None}
        return