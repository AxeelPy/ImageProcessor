import PIL
from PIL import Image, ImageStat, ImageEnhance
import os
import random
from histogram import create_histogram
# This module was 3x faster on a benchmark with more images (11 for this module, 7 for the other)

def imgprocessor(file: str, fixedbrightness: float=100, precision: float=0.5, histogram_switch: bool = False):
    if file == "": return {"error": True, "reason": "File path not given"}  # If error is True, there has to be a reason
    if fixedbrightness == "": fixedbrightness = 100
    if precision == "": precision = 0.5
    if not os.path.exists(file): return {"error": True, "reason": "File does not exist"}

    if not os.path.exists("temp/"):
        os.mkdir("temp/")

    try:
        img = PIL.Image.open(file)
    except Exception:
        return {"error": True, "reason": "Probably not an image"}

    img_bw = img.convert("L")
    img_rms = ImageStat.Stat(img_bw).rms

    enhanced = ImageEnhance.Brightness(img).enhance(fixedbrightness/float(img_rms[0]))

    while True:
        save = str(random.randint(100000, 999999))
        if not os.path.exists("temp/"+save+"-original") and not os.path.exists("temp/"+save+"-edited"):
            break
    extension = "."+file.split(".")[-1]
    enhanced.save("temp/"+save+"-edited"+extension)
    img.save("temp/" + save+"-original"+extension)
    if histogram_switch:
        create_histogram(file, "temp/"+save+"-original-histogram")
        create_histogram("temp/" + save+"-edited"+extension, "temp/"+save+"-edited-histogram")

    return {"error": False, "path": "temp/"+save, "extension": extension, "ofile": None, "efile": None}


if __name__ == "__main__":
    while True:
        inp = input("Select the file path to process\n> ")
        tweak = input("Would you like to tweak brightness or precision?\n1.Brightness Target"+
                    "\n2.Precision\n3.Brightness & Precision\n4.None\n> ")
        if tweak == "1":
            while True:
                try:
                    bright = input("Fixed brightness target input: ")
                    bright = float(bright)
                    break
                except ValueError:
                    print('Error. Please enter a number')
                    continue
            imgprocessor(inp, fixedbrightness=bright)
        elif tweak == "2":
            while True:
                try:
                    precision = input("Precision input (Default 0.5): ")
                    precision = float(precision)
                    break
                except ValueError:
                    print('Error. Please enter a number')
                    continue
            imgprocessor(inp, precision=precision)
        elif tweak == "3":
            while True:
                try:
                    bright = input("Fixed brightness target input (Default 100): ")
                    bright = float(bright)
                    precision = input("Precision input (Default 0.5): ")
                    precision = float(precision)
                    break
                except ValueError:
                    print('Error. Please enter a number')
                    continue
            imgprocessor(inp, precision=precision, fixedbrightness=bright)
        elif tweak == "4":
            imgprocessor(inp)
        elif tweak == "exit":
            quit("Exit called")
        else:
            print("Please input a number from 1 to 4.")
        