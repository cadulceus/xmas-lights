import pyvista as pv
import numpy as np
import sys, tree
from time import sleep

def scale(col, lower, upper):
    rng = col.max() - col.min()
    a = (col - col.min()) / rng
    return a * (upper - lower) + lower

if __name__ == "__main__":
    if len(sys.argv) == 3:
        HOST = sys.argv[2]
    elif len(sys.argv) == 2:
        HOST = '127.0.0.1'
    else:
        print("Usage: python3 rendestatic3d.py <3d file> <optional IP>")
        sys.exit(0)
    SHAPE_FNAME = sys.argv[1]
        
    xmas_tree = tree.tree(host = HOST, colors = [[0, 0, 0]] * 400)
    xmas_tree.load_mappings()

    shape = pv.read(SHAPE_FNAME)
    
    # make a copy of the tree's pixel coordinates so we can transform it for ease of use
    transformed_coords = xmas_tree.pixel_coords.copy()

    # shift everything over so we're working with the tree's midpoint as 0, 0, 0
    #transformed_coords -= [50, 50, 50]

    # scale the coordinates down to some arbitrary scales to work with our shape
    scale_upper = 1
    scale_lower = -scale_upper
    transformed_coords[:, 0] = scale(transformed_coords[:, 0], scale_lower, scale_upper)
    transformed_coords[:, 1] = scale(transformed_coords[:, 1], -2, 2)
    transformed_coords[:, 2] = scale(transformed_coords[:, 2], -4, 4)
    print(transformed_coords)

    transformed_coords[:, 1] -= 1
    transformed_coords[:, 0] += 0.25
    # create a pyvista set of coordinates out of the transformed pixel map
    pv_pixels = pv.PolyData(transformed_coords)

    angle = 5
    while 1:
        # transformed_coords[:, 1] += .05
        print("current angle:", angle, shape.points)
        shape.rotate_z(angle)
        enclosed_points = pv_pixels.select_enclosed_points(shape)['SelectedPoints']

        for i, is_present in enumerate(enclosed_points):
            if is_present:
                xmas_tree.colors[i] = [255, 255, 255]
            else:
                xmas_tree.colors[i] = [0, 0, 0]
        xmas_tree.write_pixels()
        sleep(0.1)