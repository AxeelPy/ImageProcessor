# importing required libraries of opencv 
import cv2 
import asyncio
import numpy
from copy import deepcopy
# importing library for plotting 
from matplotlib import pyplot as plt 

class Numpy_index:
    def __init__(self, array):
        array.where()

def create_histogram(image_path: str, save_path):
    print(f"[HISTOGRAM] Reading file {image_path}")
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    histr = cv2.calcHist([img], [0], None, [256], [0, 256])

    plt.plot(histr)
    try:
        plt.savefig(save_path)
    except Exception as e:
        print(f"Exception: {e}")

async def find_middle(histogram_list):
    highest = 0
    for index in histogram_list:
        print(index[0])
        if index[0] > highest:
            highest = index[0]
    print("highest", highest)
    return highest

# top points, average number distance between points
# !!MISSING!! Calculate difference of peak and points around, probably of 5 layers deep
async def process_points(histogram_list):
    top_points = []
    index = 1

    if histogram_list[0] > histogram_list[1]:
        top_points.append(histogram_list[0])
    while index < len(histogram_list)-1:
        if histogram_list[index-1] < histogram_list[index] > histogram_list[index+1]:
            print(f"{histogram_list[index-1]} {histogram_list[index]} {histogram_list[index+1]}")
            top_points.append(histogram_list[index])
        index = index + 1
    if histogram_list[-1] > histogram_list[-2]:
        top_points.append(histogram_list[-1])

    print(f"There are {len(top_points)} top points")
    
    iterations = 1
    total = 0
    index = 0
    while index < len(histogram_list)-1:
        total = total + histogram_list[index]
        iterations = iterations + 1
        index = index + 1
    average = total/iterations
    print("Total:", total, "Iterations:", iterations)
    print("Average difference is", average)

    return top_points

if __name__ == "__main__":
    # reads an input image 
    img = cv2.imread("images/Untitled.png",0) 

    # find frequency of pixels in range 0-255 
    histr = cv2.calcHist([img],[0],None,[256],[0,256]) 

    # show the plotting graph of an image 
    hist = deepcopy(histr)
    print(histr, len(histr))
    asyncio.run(process_points(hist))
    # histr[100] = histr[100] + 3e+2
    plt.plot(histr)
    
    # plt.savefig("pablo")
    plt.show()