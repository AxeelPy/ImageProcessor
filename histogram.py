# importing required libraries of opencv 
import cv2 
  
# importing library for plotting 
from matplotlib import pyplot as plt 

def create_histogram(image_path: str, save_path):
    print(f"[HISTOGRAM] Reading file {image_path}")
    img = cv2.imread(image_path, 0)

    histr = cv2.calcHist([img], [0], None, [256], [0, 256])

    plt.plot(histr)
    try:
        plt.savefig(save_path)
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    # reads an input image 
    img = cv2.imread("images/6B5lT.jpg",0) 

    # find frequency of pixels in range 0-255 
    histr = cv2.calcHist([img],[0],None,[256],[0,256]) 

    # show the plotting graph of an image 

    plt.plot(histr)
    plt.savefig("pablo")
    plt.show()