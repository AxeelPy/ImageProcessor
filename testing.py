import PIL
from PIL import Image, ImageStat, ImageEnhance

im = Image.open("images/rndm2.jpg")
bw = im.convert("L")
imagebr = ImageStat.Stat(bw)
imagebr = imagebr.rms
print(imagebr)

Enhanceamount = 2
enhanced = ImageEnhance.Brightness(im).enhance(Enhanceamount)
enhancedbw = enhanced.convert("L")
enhancedbw = ImageStat.Stat(enhancedbw).rms
print(enhancedbw)

