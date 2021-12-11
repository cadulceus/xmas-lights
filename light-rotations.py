import time, sys
import tree

PIXELS_COUNT = 350
INIT_COLOR_SCALE = 5
STEP_COLOR_SCALE = 15
PORT = 4141

if len(sys.argv) == 2:
    HOST = sys.argv[1]
elif len(sys.argv) == 1:
    HOST = '127.0.0.1'
else:
    print("USAGE: python light_rotations.py <optional destination ip>")
    sys.exit(0)

# assumes that at least one color is 0 and r + g + b <= 255
def rotate_color(grb, count=1, scale=STEP_COLOR_SCALE):
        rotated_grb = [grb[0], grb[1], grb[2]]

        # I'm sure there's a way to compute this in constant time but I'm not about to implement that
        for i in range(count):
            if rotated_grb.count(0) == 2:
                i = next(rotated_grb.index(x) for x in rotated_grb if x != 0)
            else:
                i = (rotated_grb.index(0) + 1) % 3

            rotated_grb[i] = max(0, rotated_grb[i] - scale)
            rotated_grb[(i + 1) % 3] = min(255, rotated_grb[(i + 1) % 3] + scale)
        return rotated_grb

def init_pixels():
    pixels = [[255,0,0]]*PIXELS_COUNT
    for i, p in enumerate(pixels):
        pixels[i] = rotate_color(p, i, INIT_COLOR_SCALE)
    return pixels

if __name__ == "__main__":
    pixels = init_pixels()
    xmas_tree = tree.tree(HOST, PORT)
    while 1:
        # rotate each pixel by STEP_COLOR_SCALE
        for p_ind, p in enumerate(pixels):
            pixels[p_ind] = rotate_color(p)
        xmas_tree.write_pixels(pixels)
        time.sleep(0.03)
