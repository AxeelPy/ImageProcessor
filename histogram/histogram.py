# importing required libraries of opencv 
import cv2 
import asyncio
import numpy
from copy import deepcopy
# importing library for plotting 
import histogram.histogram_edit as histogram_edit
from matplotlib import pyplot as plt 

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
        # print(index[0])
        if index[0] > highest:
            highest = index[0]
    # print("highest", highest)
    return highest

# top points, average number distance between points
# Calculates difference of peak and points around, probably of 5 layers deep
async def process_points(histogram_list):
    top_points = []
    index = 1

    if histogram_list[0] > histogram_list[1]:
        top_points.append(histogram_list[0])
    while index < len(histogram_list)-1:
        if histogram_list[index-1] < histogram_list[index] > histogram_list[index+1]:
            # print(f"{histogram_list[index-1]} {histogram_list[index]} {histogram_list[index+1]}")
            top_points.append(histogram_list[index])
        index = index + 1
    if histogram_list[-1] > histogram_list[-2]:
        top_points.append(histogram_list[-1])

    # print(f"There are {len(top_points)} top points")
    
    average = await get_average(histogram_list)
    # print("Average difference is", average)
    max_points = await max_point_differences(histogram_list, top_points)
    return {"top points": top_points, "max_dif": max_points}


async def max_point_differences(histogram_list, tops, depth: int = 5):
    point_differences = []
    # print("Tops:", tops)
    for i in tops:
        tops_pos = numpy.where(i == histogram_list)[0]
        # print(f"tops_pos {tops_pos} shows value {histogram_list[tops_pos]}")
        
        dif = 1
        point_data = []

        # Gets difference of 5 points up and down of the selected index
        while True:
            
            if dif >= depth:
                break
            
            if tops_pos[0]+dif < len(histogram_list)-1:
                point_data.append(histogram_list[tops_pos+dif])
                point_data.append(histogram_list[tops_pos+dif*-1])
            dif = dif + 1

        # Gets average of point_data, to append to point_differences
        average = await get_average(point_data)
        point_differences.append(average)
    # print("Point differences:", i)
    return point_differences


async def get_average(array):
    iterations = 1
    total = 0
    index = 0
    while index < len(array)-1:
        total = total + array[index]
        iterations = iterations + 1
        index = index + 1
    # print("Returning:", total/iterations)
    return total/iterations


if __name__ == "__main__":
    # reads an input image 
    img = cv2.imread("images/rndm.png",0) 

    # find frequency of pixels in range 0-255 
    histr = cv2.calcHist([img],[0],None,[256],[0,256]) 

    # show the plotting graph of an image 
    hist = deepcopy(histr)
    plt_info = asyncio.run(process_points(hist))
    # histr[100] = histr[100] + 3e+2
    plt.plot(histr)
    
    # plt.savefig("pablo")
    plt.show()