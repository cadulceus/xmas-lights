import cv2, sys
import numpy as np
import tree

def take_picture(cam):
    s, img = cam.read()
    if s:
        gs = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gs = cv2.GaussianBlur(gs, (11, 11), 0)
        return gs

    raise Exception("camera no work")

def find_brightest(gs_img):
        # locates the brightest and darkest pixel in the image
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gs_img)
        render = gs_img.copy()
        cv2.circle(render, maxLoc, 10, 255, 3)
        cv2.imshow("visualize-led", render)

        circle_mask = np.zeros((gs_img.shape[0], gs_img.shape[1]), np.uint8)
        cv2.circle(circle_mask, maxLoc, 4, 255, -1) # 6 is radius, 255 is color, -1 is thickness
        magnitude = cv2.mean(gs_img, mask = circle_mask)[0]
        print("maxLoc: ", maxLoc, "magnitude: ", magnitude)
        # if magnitude < 100: # arbitrary threshold of deciding if pixel is a false positive
        #     return [-1, -1], 0

        return maxLoc, magnitude

def main():
    if len(sys.argv) != 4:
        print("Usage: python tree-mapper.py <tree ip> <light count> <output file>")
        return
    fname = sys.argv[3]
    num_lights = sys.argv[2]
    host_ip = sys.argv[1]
    
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("visualize-led", cv2.WINDOW_AUTOSIZE)

    xmas_tree = tree.tree(host_ip, 4141)

    readings = []
    pixels = [[0,0,0]] * num_lights
    for i in range(len(pixels)):
        pixels[i - 1] = [0, 0, 0]
        pixels[i] = [255, 255, 255]
        xmas_tree.write_pixels(pixels)
        print("current pixel: ", i)
        gs = take_picture(cam)
        brightest_loc, magnitude = find_brightest(gs)
        readings.append([brightest_loc[0], brightest_loc[1], magnitude])
        cv2.waitKey(50)

    with open(fname, "w") as f:
        f.write("\n".join([", ".join([str(val) for val in reading]) for reading in readings]))
main()



    
