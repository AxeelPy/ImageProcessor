from numba import jit
from time import time
from numba.typed import List
from numba.pycc import CC

#cc = CC("algorithm3")

@jit(nopython=True)
#@cc.export("Get_Pixel_Average", "f8(f8)")
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
# @cc.export("sRGBtoPerceivedBrightness", "f8(f8)")
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
#@cc.export("Get_Image_Brightness", "f8(f8)")
def Get_Image_Brightness(NumArray):

    NewNumArray = []

    for row in NumArray:
        TempRow = []
        for column in row:
            TempRow.append(sRGBtoPerceivedBrightness(column))
        NewNumArray.append(TempRow)
    print("Went here")
    return NewNumArray

@jit(nopython=True)
def get_highest_numbers(tuple):
        
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
            return None

        elif blue >= green:
            if blue == green:
                return [[1, 2], 0]
            return [2, 1, 0]
        
        return [1, 2, 0] 

#if __name__ == "__main__":
#   cc.compile()