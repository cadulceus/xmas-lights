import time, tree, sys
import numpy as np

if len(sys.argv) == 2:
    HOST = sys.argv[1]
elif len(sys.argv) == 1:
    HOST = '127.0.0.1'
else:
    print("USAGE: python light_rotations.py <optional destination ip>")
    sys.exit(0)

if __name__ == "__main__":
    test_tree = tree.tree(host = HOST)
    test_tree.load_mappings()

    pixels_to_write = np.array([[0,0,0]] * 400)
    split = 50
    c1 = [255, 0, 0]
    c2 = [0, 255, 0]
    while 1:
        split += 5
        if split >= 120:
            c1, c2 = c2, c1
            print("left: ", c1, "right: ", c2)
            split = 0
        green_mask = test_tree.pixel_coords[:, 0] < split
        red_mask = test_tree.pixel_coords[:, 0] > split
        pixels_to_write[red_mask] = c1
        pixels_to_write[green_mask] = c2
        test_tree.write_pixels([list([int(c) for c in pixel]) for pixel in pixels_to_write])
        time.sleep(0.05)