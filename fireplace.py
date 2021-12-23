import numpy as np
import sys, tree, math
from time import sleep
from lightrotations import rotate_color
from random import randint

class Flicker:
    def __init__(self, loc, velocity_vector, ttl, max_ttl):
        self.loc = loc
        self.velocity = velocity_vector
        self.ttl = ttl
        self.max_ttl = max_ttl
        life = (ttl / max_ttl) / 2
        self.color = rotate_color([255, 0, 0], times = ttl, scale = 100 // max_ttl)
        for i in range(len(self.color)):
            self.color[i] = round(min(life, 1) * self.color[i])

    def update(self):
        for i in range(len(self.loc)):
            self.loc[i] += self.velocity[i]
        self.ttl -= 1
        life = self.ttl / self.max_ttl
        self.color = rotate_color([255, 0, 0], times = self.ttl, scale = 100 // self.max_ttl)
        for i in range(len(self.color)):
            self.color[i] = round(min(life, 1) * self.color[i])


if __name__ == "__main__":
    if len(sys.argv) == 2:
        HOST = sys.argv[1]
    elif len(sys.argv) == 1:
        HOST = '127.0.0.1'
    else:
        print("Usage: python3 fireplace.py <optional IP>")
        sys.exit(0)

    xmas_tree = tree.tree(host = HOST, colors = [[0, 0, 0]] * 400)
    xmas_tree.load_mappings()

    live_flickers = []
    MAX_TTL = 20
    while 1:
        xmas_tree.colors = [[0,0,0]] * len(xmas_tree.colors)
        while len(live_flickers) < 50:
            if randint(0, 100) > 4:
                live_flickers.append(Flicker(loc = [randint(0, 100), 0, randint(0, 100)],
                                             velocity_vector = [0, randint(3, 8) / 2, 0],
                                             ttl = randint(8, MAX_TTL),
                                             max_ttl = MAX_TTL))
            else:
                live_flickers.append(Flicker(loc = [randint(0, 100), 0, randint(0, 100)],
                                             velocity_vector = [randint(-10, 10), randint(5, 15) / 2, 0, randint(-10, 10)],
                                             ttl = randint(4, MAX_TTL),
                                             max_ttl = MAX_TTL))
        for flicker in live_flickers:
            if flicker.loc[0] > xmas_tree.x_size or flicker.loc[1] > xmas_tree.y_size or flicker.loc[2] > xmas_tree.z_size or flicker.ttl <= 0:
                live_flickers.remove(flicker)
                continue
            xmas_tree.colors[xmas_tree.index_of_nearest(flicker.loc)] = flicker.color
            flicker.update()
        xmas_tree.write_pixels()
        sleep(0.15)