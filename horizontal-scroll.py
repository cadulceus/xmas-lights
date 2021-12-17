import time, tree, sys
import numpy as np

if len(sys.argv) == 2:
    HOST = sys.argv[1]
elif len(sys.argv) == 1:
    HOST = '127.0.0.1'
else:
    sys.exit(0)

def scroll_sequence(tree, iterations = 3, axis = 0, c1 = [255, 0, 0], c2 = [0, 255, 0]):
    split = 50
    pixels_to_write = np.array([[0,0,0]] * len(tree.pixel_coords))
    i = 0
    while i < iterations:
        split += 5
        if split == 50:
            i += 1

        if split >= 120:
            c1, c2 = c2, c1
            split = 0
        green_mask = tree.pixel_coords[:, axis] < split
        red_mask = tree.pixel_coords[:, axis] > split
        pixels_to_write[red_mask] = c1
        pixels_to_write[green_mask] = c2
        tree.write_pixels([list([int(c) for c in pixel]) for pixel in pixels_to_write])
        time.sleep(0.05)

def rotate_sequence(tree, iterations = 3, axis = 0, c1 = [255, 0, 0], c2 = [0, 255, 0]):
    split = 50
    angle = 0
    pixels_to_write = np.array([[0,0,0]] * len(tree.pixel_coords))
    i = 0
    while i < iterations:
        angle += .05
        if round(angle, 2) % 2 == 0:
            i += 1

        rotated_tree = tree.rotate(tree.pixel_coords, pitch = angle*np.pi, origin = tree.midpoint)
        green_mask = rotated_tree[:, axis] < split
        red_mask = rotated_tree[:, axis] > split
        pixels_to_write[red_mask] = c1
        pixels_to_write[green_mask] = c2
        tree.write_pixels([list([int(c) for c in pixel]) for pixel in pixels_to_write])
        time.sleep(0.05)


if __name__ == "__main__":
    xmas_tree = tree.tree(host = HOST)
    xmas_tree.load_mappings()
    np.set_printoptions(threshold=sys.maxsize)
    time.sleep(0.5)

    while 1:
        # rotate_sequence(xmas_tree)
        scroll_sequence(xmas_tree, axis = 0)
        scroll_sequence(xmas_tree, axis = 1)
        scroll_sequence(xmas_tree, axis = 2)