import PIL
from PIL import Image, ImageStat, ImageEnhance
import os
import random


def imgprocessor(file: str, fixedbrightness=100, precision=0.5):
    if file == "": return {"error": True, "reason": "File path not given"}
    if fixedbrightness == "": fixedbrightness = 100
    if fixedbrightness > 250: fixedbrightness = 200
    if precision == "": precision = 0.5
    if not os.path.exists(file):
        return {"error": True, "reason": "File does not exist"}
    if not os.path.exists("temp/"):
        os.mkdir("temp/")

    print("on file", file)
    im = PIL.Image.open(file)
    bw = im.convert("L")
    imagebr = ImageStat.Stat(bw)
    imagebr = imagebr.rms

    print("Dark image RMS:", imagebr, "\nFrom 1: " + str(float(imagebr[0]) / 100))
    Enhanceamount = 2 - float(imagebr[0]) / fixedbrightness
    enhanced = ImageEnhance.Brightness(im).enhance(Enhanceamount)
    enhancedbw = enhanced.convert("L")
    enhancedbw = ImageStat.Stat(enhancedbw).rms
    print(f"Enhanced from {str(float(imagebr[0]) / fixedbrightness)} to {Enhanceamount}")
    print(f"Current brightness is {enhancedbw}")
    lastenhance = str(float(imagebr[0]))
    print("hello")
    i = 2
    if enhancedbw[0] < 100:
        while enhancedbw[0] < fixedbrightness:
            Enhanceamount = i - float(enhancedbw[0]) / fixedbrightness
            print(Enhanceamount)
            enhanced = ImageEnhance.Brightness(im).enhance(Enhanceamount)
            enhancedbw = enhanced.convert("L")
            enhancedbw = ImageStat.Stat(enhancedbw).rms
            print(f"Enhanced from {lastenhance} to {Enhanceamount}")
            print(f"Current brightness is {enhancedbw}")
            lastenhance = enhancedbw
            i = i + precision
    elif enhancedbw[0] > 100:
        while enhancedbw[0] > fixedbrightness:
            Enhanceamount = i - float(enhancedbw[0]) / fixedbrightness
            print(Enhanceamount)
            enhanced = ImageEnhance.Brightness(im).enhance(Enhanceamount)
            enhancedbw = enhanced.convert("L")
            enhancedbw = ImageStat.Stat(enhancedbw).rms
            print(f"Enhanced from {lastenhance} to {Enhanceamount}")
            print(f"Current brightness is {enhancedbw}")
            lastenhance = enhancedbw
            i = i - precision/5
    while True:
        save = str(random.randint(100000, 999999))
        if not os.path.exists("temp/"+save+"-original") and not os.path.exists("temp/"+save+"-edited"):
            break
    extension = "."+file.split(".")[-1]
    print("extension:", extension)
    enhanced.save("temp/"+save+"-edited"+extension)
    im.save("temp/" + save+"-original"+extension)
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
        