import PIL
from PIL import Image, ImageStat, ImageEnhance
import sys

img = Image.open("images/OIP.jpg")
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
ImageEnhance.Brightness(img).enhance(100/average).show()
e = ImageEnhance.Brightness(img).enhance(100/average).convert("L")
print(ImageStat.Stat(e).rms)