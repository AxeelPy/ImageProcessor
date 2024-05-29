from PIL import Image, ImageStat, ImageEnhance
import asyncio
from random import randint


# if image is 1800x1000
# 256 masks would be 1800/256 and height max, so 1000
async def change_image(path, enhance):
    image = Image.open(path)
    image_bw = image.convert("L")

    width, height = image.size[0], image.size[1]
    print(f"width: {width}, height: {height}")

    masks = []
    constant_mask_len: int = width/256
    print("Actual length is", width/256)
    one_mask_len: int = 0
    
    while len(masks) < 255:
        masks.append((int(one_mask_len), 0, int(constant_mask_len)+int(one_mask_len), height))
        one_mask_len = one_mask_len + constant_mask_len

    masks.append((int(one_mask_len), 0, width, height))

    print(masks)
    print(f"Length of masks: {len(masks)}")

    new_im = Image.new(mode="RGB", size=(width, height), color="black")
    pixels = new_im.load()
    enhance_index = 0
    for i in masks:
        im = image.crop(i)
        ImageEnhance.Brightness(im).enhance(enhance[enhance_index])
        for j in range(im.size[0]):
            for l in range(im.size[1]):
                pixels[j, l] = (j, l, 100)
    new_im.load()
    new_im.show()

enhanceamount = []
for i in range(256):
    enhanceamount.append(randint(1, 5))

print(enhanceamount)
asyncio.run(change_image("images/rndm.png", enhanceamount))
