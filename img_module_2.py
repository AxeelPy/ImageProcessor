import PIL
from PIL import Image, ImageStat, ImageEnhance
import os
import random


def imgprocessor(file: str, fixedbrightness: float=100, precision: float=0.5):
    if file == "": return {"error": True, "reason": "File path not given"}  # If error is True, there has to be a reason
    if fixedbrightness == "": fixedbrightness = 100
    if fixedbrightness > 250: fixedbrightness = 200
    if precision == "": precision = 0.5
    if not os.path.exists(file): return {"error": True, "reason": "File does not exist"}

    if not os.path.exists("temp/"):
        os.mkdir("temp/")

    print("on file", file)
    try:
        img = PIL.Image.open(file)
    except Exception:
        return {"error": True, "reason": "Probably not an image"}

    width, height = img.size[0], img.size[1]

    left_top = img.crop((0, 0, width//5, height//5))
    right_top = img.crop((width-width//5, 0, width, height//5))

    left_bottom = img.crop((0, height-height//5, width//5, height))
    right_bottom = img.crop((width-width//5, height-height//5, width, height))

    left_top_bw = left_top.convert("L")
    left_top_bw = ImageStat.Stat(left_top_bw).rms

    right_top_bw = right_top.convert("L")
    right_top_bw = ImageStat.Stat(right_top_bw).rms

    left_bottom_bw = left_bottom.convert("L")
    left_bottom_bw = ImageStat.Stat(left_bottom_bw).rms

    right_bottom_bw = right_bottom.convert("L")
    right_bottom_bw = ImageStat.Stat(right_bottom_bw).rms

    rmslist = [left_top_bw[0], left_bottom_bw[0], right_bottom_bw[0], right_top_bw[0]]
    print(rmslist)

    total = float(rmslist[0]) + float(rmslist[1]) + float(rmslist[2]) + float(rmslist[3])
    print(f"Total: {total}")
    average = total / len(rmslist)
    print(f"Average: {average}")
    enhanced = ImageEnhance.Brightness(img).enhance(100/average)

    while True:
        save = str(random.randint(100000, 999999))
        if not os.path.exists("temp/"+save+"-original") and not os.path.exists("temp/"+save+"-edited"):
            break
    extension = "."+file.split(".")[-1]
    print("extension:", extension)
    enhanced.save("temp/"+save+"-edited"+extension)
    img.save("temp/" + save+"-original"+extension)

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
        