import PIL
from PIL import Image, ImageStat

im = PIL.Image.open("images/light.jpg")
bw = im.convert("L")

bw.show()
