import time, tree, sys
import numpy as np
from lightrotations import rotate_color
from random import randint

if len(sys.argv) == 2:
    HOST = sys.argv[1]
elif len(sys.argv) == 1:
    HOST = '127.0.0.1'
else:
    sys.exit(0)

class Ripple:
    def __init__(self, origin, xmas_tree, color, max_distance = None, color_map = None):
        self.origin = origin
        self.xmas_tree = xmas_tree
        self.color = color
        self.max_distance = max_distance if max_distance else (xmas_tree.x_size**2 + xmas_tree.y_size**2 + xmas_tree.z_size**2) ** 0.5
        self.color_map = color_map if color_map else xmas_tree.colors
        self.__dict__['progress'] = 0

    def __setattr__(self, name, value):
        self.__dict__[name] = value
        if not self.__dict__.get("_locked", False) and name == "progress":
            distances = self.xmas_tree.distances_to_point(self.origin)
            for i, distance in enumerate(distances):
                if distance < self.progress * self.max_distance:
                    self.color_map[i] = self.color

if __name__ == "__main__":
    xmas_tree = tree.tree(host = HOST, colors = [[0, 255, 0]] * 400)
    xmas_tree.load_mappings()
    xmas_tree.write_pixels()
    while 1:
        origin = [randint(0, xmas_tree.x_size), randint(0, xmas_tree.y_size), randint(0, xmas_tree.z_size)]
        start_color = xmas_tree.colors[xmas_tree.index_of_nearest(origin)]
        color_rotation_steps = randint(12, 25)
        ripples = []
        for steps in range(color_rotation_steps):
            ripples.append(Ripple(origin, xmas_tree, rotate_color(start_color, times = steps, scale = 20)))
        ripple_queue = []
        ripple_queue.append(ripples.pop(0))
        ripple_spacing = 1
        timer = 0
        while ripple_queue:
            if timer == 0:
                if ripples:
                    ripple_queue.append(ripples.pop(0))
                    timer = ripple_spacing
            timer -= 1
            for i in range(len(ripple_queue)):
                if i >= len(ripple_queue):
                    break
                ripple_queue[i].progress = ripple_queue[i].progress + 0.02
                if ripple_queue[i].progress >= 1:
                    ripple_queue.remove(ripple_queue[i])
            xmas_tree.write_pixels()
            time.sleep(.05)