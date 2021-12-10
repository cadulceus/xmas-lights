import neopixel, board, time, code

PIXELS_COUNT = 250
INIT_COLOR_SCALE = 5
STEP_COLOR_SCALE = 15

pixels = neopixel.NeoPixel(board.D21, PIXELS_COUNT)
pixels.auto_write = False
# pixels.fill((255, 255, 0))
# pixels.brightness = 0.1
# exit(0)

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
            #print(rotated_grb)
        return rotated_grb

pixels.fill((255,0,0))
print("initializing colors")
for i, p in enumerate(pixels):
    pixels[i] = rotate_color(p, i, INIT_COLOR_SCALE) # (p[0] - (i * INIT_COLOR_SCALE), (i * INIT_COLOR_SCALE), 0)
print(pixels)
pixels.show()

# rotate each pixel by STEP_COLOR_SCALE
print("rotating colors")
while 1:
    for p_ind, p in enumerate(pixels):
        pixels[p_ind] = rotate_color(p)
    print(pixels, "\n\n")
    time.sleep(0.01)
    pixels.show()

#p.show()
#code.interact(local = locals())
#p.deinit()