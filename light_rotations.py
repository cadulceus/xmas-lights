import time, socket, sys
from pickle import dumps

PIXELS_COUNT = 250
INIT_COLOR_SCALE = 5
STEP_COLOR_SCALE = 15
PORT = 4141

if len(sys.argv) != 2:
    print("USAGE: python light_rotations.py <host ip>")
    sys.exit(0)
HOST = sys.argv[1]

# assumes that at least one color is 0 and r + g + b <= 255
def rotate_color(grb, count=1, scale=STEP_COLOR_SCALE):
        rotated_grb = [grb[0], grb[1], grb[2]]
        for i in range(count): # I'm sure there's a way to compute this in constant time but i'm not about to implement that
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

def main():
    pixels = init_pixels()
    while 1:
        # rotate each pixel by STEP_COLOR_SCALE
        for p_ind, p in enumerate(pixels):
            pixels[p_ind] = rotate_color(p)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.send(dumps(pixels))
            s.close()
        time.sleep(0.03)

main()