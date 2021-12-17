import sys
import tree
import numpy as np

# constrain and normalize an array of ints to 0-bound
def normalize_arr(arr, bound, invert = False):
    for i in range(len(arr[0])):
        curr_arr = arr[:, i]
        min_x, max_x = np.nanmin(curr_arr), np.nanmax(curr_arr)
        
        #convert max to max after left shifting to 0
        max_x = max_x - min_x

        x_scale = bound[i] / max_x

        # shift everything over, then scale it
        for i in range(len(curr_arr)):
            curr_arr[i] = curr_arr[i] - min_x
            if invert:
                curr_arr[i] = abs(curr_arr[i] - max_x)
            curr_arr[i] = curr_arr[i] * x_scale

def parse_readings(readings, min_magnitude):
        readings = readings.split("\n")
        readings = [s.split(", ") for s in readings]
        for i, reading in enumerate(readings):
            if float(reading[2]) < min_magnitude:
                readings[i][0] = '-1'
                readings[i][1] = '-1'

        # We could try to use the magnitude to estimate a z depth but I think thats more trouble than its worth
        readings = [[int(reading[0]), int(reading[1]), -1] for reading in readings]
        np_readings = np.array(readings).astype(float)
        np_readings[np_readings == -1] = np.nan
        return np_readings

def yaw_90_deg(arr, times = 1, origin = [0, 0, 0]):
    """
    use some cheap tricks to rotate a 3d array along the y axis while still preserving
    NaN values.
    """
    # This really shouldn't be a loop but i'm too lazy to do the math
    for i in range(times):
        # x should become -z, and z should become x
        arr[:, [0, 2]] = arr[:, [2, 0]] - [origin[2], origin[0]]
        arr[:, 2] = arr[:, 2] * -1
        arr[:, [0, 2]] += [origin[0], origin[2]]

def merge_arrays(dest, source):
    """
    copies all values into source from dest that are NaN in source.
    if the value of a coordinate is known in both arrays, add them together.
    returns a mask of all indeces that already existed in both arrays.
    """
    unknown_final_pixels = np.isnan(dest)
    unknown_incoming_pixels = np.isnan(source)
    both_known = ~unknown_final_pixels & ~unknown_incoming_pixels

    dest[unknown_final_pixels] = source[unknown_final_pixels]
    dest[both_known] = source[both_known] + dest[both_known]
    
    return both_known.astype(int)

def load_mappings(f1, f2, f3, f4, magnitude_filter = 100):
    """
    Load in 4 mapping files that contain x, y, and magnitude CSVs that tree-mapper.py outputs.
    Each file is expected to be a 90 degree increment counter-clockwise rotation from the 'front'.
    Calling this method on a tree object will set tree.pixel_coords to a numpy array of x, y, and z
    coordinates, where the index of a given point corresponds with the position of the LED in the strip.
    """
    with open("readings_0_deg.txt", "r") as f:
        np_deg0 = parse_readings(f.read(), magnitude_filter)
    with open("readings_90_deg.txt", "r") as f:
        np_deg90 = parse_readings(f.read(), magnitude_filter)
    with open("readings_180_deg.txt", "r") as f:
        np_deg180 = parse_readings(f.read(), magnitude_filter)
    with open("readings_270_deg.txt", "r") as f:
        np_deg270 = parse_readings(f.read(), magnitude_filter)

    x_size, y_size, z_size = 100, 100, 100
    normalize_arr(np_deg0, [x_size, y_size, z_size])

    # we'll treat the 0 degree measurements as the 'final tree' and merge other measurements into it
    final_arr = np_deg0

    normalize_arr(np_deg90, [x_size, y_size, z_size])
    normalize_arr(np_deg180, [x_size, y_size, z_size])
    normalize_arr(np_deg270, [x_size, y_size, z_size])
    yaw_90_deg(np_deg90, times = 1, origin=[x_size/2, y_size/2, z_size/2])
    yaw_90_deg(np_deg180, times = 2, origin=[x_size/2, y_size/2, z_size/2])
    yaw_90_deg(np_deg270, times = 3, origin=[x_size/2, y_size/2, z_size/2])

    averages = merge_arrays(final_arr, np_deg90) + merge_arrays(final_arr, np_deg180) + merge_arrays(final_arr, np_deg270) + 1
    final_arr = final_arr / averages
    return final_arr

if (len(sys.argv) != 7):
    print("Usage: python3 generate-mapping-file.py <tree ip> <input-0-degrees>" +
          " <input-90-degrees> <input-180-degrees> <input-270-degrees> <output>")
    exit(0)
ip, f1, f2, f3, f4, fout = sys.argv[1:]
coords = load_mappings(f1, f2, f3, f4)

# load up a second array populated with "best guesses"
guessy_coords = load_mappings(f1, f2, f3, f4, 0)

xmas_tree = tree.tree(host = ip)

print(coords)
nans = np.isnan(coords)
for i, coord in enumerate(coords):
    debug_pixels = [[0, 0, 0]] * len(coords)
    for j, axis in enumerate(coord):
        if nans[i][j]:
            print("\nIndex", j, "in", coord, "is unknown, absolute location", i)
            print("Surrounding values:")
            for curr_pixel_ind in range(i - 5, i + 6):
                if curr_pixel_ind == i:
                    print("\t", np.around(coord, 4), "<current pixel>")
                    debug_pixels[curr_pixel_ind] = [255, 255, 255]
                    continue
                elif curr_pixel_ind >= 0 and curr_pixel_ind < i:
                    print("\t", np.around(coords[curr_pixel_ind], 4), "(green)")
                    debug_pixels[curr_pixel_ind] = [0, 255, 0]
                elif curr_pixel_ind >= 0 and curr_pixel_ind > i:
                    print("\t", np.around(coords[curr_pixel_ind], 4), "(red)")
                    debug_pixels[curr_pixel_ind] = [255, 0, 0]
            xmas_tree.write_pixels(debug_pixels)
            print("Opencv's best guess is:", np.around(guessy_coords[i], 4))
            print("Enter best guess for the current axis", j, "or press enter to use best guess:")
            guess = input()
            if guess:
                coords[i][j] = guess
            else:
                coords[i][j] = guessy_coords[i][j]

with open(fout, "w") as f:
    f.write(str(coords).replace("[[", "").replace("]]", "").replace("[ ", "").replace("]", ""))
