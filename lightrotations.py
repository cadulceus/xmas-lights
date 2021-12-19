import time, sys
import tree

PIXELS_COUNT = 400
INIT_COLOR_SCALE = 5
STEP_COLOR_SCALE = 12
PORT = 4141

if len(sys.argv) == 2:
    HOST = sys.argv[1]
elif len(sys.argv) == 1:
    HOST = '127.0.0.1'
else:
    print("USAGE: python light_rotations.py <optional destination ip>")
    sys.exit(0)

# assumes that at least one color is 0 and r + g + b <= 255
def rotate_color(rgb, times=1, scale=STEP_COLOR_SCALE):
        rotated_rgb = [rgb[0], rgb[1], rgb[2]]

        # I'm sure there's a way to compute this in constant time but I'm not about to implement that
        for i in range(times):
            if rotated_rgb.count(0) == 2:
                i = next(rotated_rgb.index(x) for x in rotated_rgb if x != 0)
            else:
                i = (rotated_rgb.index(0) + 1) % 3

            rotated_rgb[i] = max(0, rotated_rgb[i] - scale)
            rotated_rgb[(i + 1) % 3] = min(255, rotated_rgb[(i + 1) % 3] + scale)
        return rotated_rgb

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
