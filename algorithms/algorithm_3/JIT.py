from numba import jit
from time import time
from numba.typed import List

@jit(nopython=True)
def Get_Pixel_Average(array):
    total_brightness = 0.0
    total_length = 0
    
    for value in array:
        value_sum = 0.0
        for i in range(len(value)):
            value_sum += value[i]
        total_brightness += value_sum
        total_length += len(value)

    return total_brightness / total_length

@jit(nopython=True)
def sRGBtoPerceivedBrightness(RGB): 
        # ========= Convert to luminance value ======
        colors = [RGB[0] / 255, RGB[1] / 255, RGB[2] / 255]
        LuminanceValues = []

        for color in colors:
            if color <= 0.04045:
                LuminanceValues.append(color/12.92)
            else:
                LuminanceValues.append(((color+0.055)/1.055) ** 2.4)

        Luminance = 0.2126 * LuminanceValues[0] + 0.7152 * LuminanceValues[1] + 0.0722 * LuminanceValues[2]

        # ========== Find perceived brightness ============
        if Luminance <= (216/24389):
            return Luminance * (216/24389)
        else:
            return (Luminance ** (1/3)) * 116 - 16

@jit(nopython=True)
def Get_Image_Brightness(NumArray):

    NewNumArray = []
    for row in NumArray:
        TempRow = []
        for column in row:
            TempRow.append(sRGBtoPerceivedBrightness(column))
        NewNumArray.append(TempRow)
    print("Went here")
    return NewNumArray

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

    elif blue >= green:
        if blue == green:
            return [[1, 2], 0]
        return [2, 1, 0]
    
    return [1, 2, 0]        

async def change_saturation(image, change, tuple, index: list):

    # print(f"Old ass tuple; {tuple}")
    #if _class.brightness[index[0]][index[1]] > 50:
    #    # print("Brightness is over treshold")
    #    return tuple
    
    if image[index[0]][index[1]][0] - image[index[0]][index[1]][1] in range(-5, 6):
        if image[index[0]][index[1]][0] - image[index[0]][index[1]][2] in range(-5, 6):
            print("White found")
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