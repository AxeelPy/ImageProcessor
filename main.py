import PIL
from PIL import Image, ImageStat, ImageEnhance
import multiprocessing as mp

im = PIL.Image.open("images/rndm2.jpg")
bw = im.convert("L")
imagebr = ImageStat.Stat(bw)
imagebr = imagebr.rms

print("Dark image RMS:", imagebr, "\nFrom 1: " + str(float(imagebr[0]) / 100))
Enhanceamount = 2 - float(imagebr[0]) / 100
enhanced = ImageEnhance.Brightness(im).enhance(Enhanceamount)
enhancedbw = enhanced.convert("L")
enhancedbw = ImageStat.Stat(enhancedbw).rms
print(f"Enhanced from {str(float(imagebr[0]) / 100)} to {Enhanceamount}")
print(f"Current brightness is {enhancedbw}")

lastenhance = str(float(imagebr[0]))
i = 2
while enhancedbw[0] < 100:
    Enhanceamount = i - float(enhancedbw[0]) / 100
    print(Enhanceamount)
    enhanced = ImageEnhance.Brightness(im).enhance(Enhanceamount)
    enhancedbw = enhanced.convert("L")
    enhancedbw = ImageStat.Stat(enhancedbw).rms
    print(f"Enhanced from {lastenhance} to {Enhanceamount}")
    print(f"Current brightness is {enhancedbw}")
    lastenhance = enhancedbw
    i = i + .5

enhanced.show()
enhanced.save("images/newimg.jpg")