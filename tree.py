import socket, math
from pickle import dumps
import numpy as np

class tree:
    def __init__(self, host = '127.0.0.1', port = 4141, x_size = 100, y_size = 100, z_size = 100, colors = [[0, 0, 0]] * 400):
        self.HOST = host
        self.PORT = port
        self.x_size = x_size
        self.y_size = y_size
        self.z_size = z_size
        self.midpoint = [x_size / 2, y_size / 2, z_size / 2]
        self.colors = colors

    def write_pixels(self, pixels = None):
        for i in range(min(len(pixels), len(self.colors))):
            self.colors[i] = pixels[i]
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            s.send(dumps(self.colors))
            s.close()
    
    def nan_to_neg(self, arr):
        arr[np.isnan(arr)] = -1
    
    def neg_to_nan(self, arr):
        arr[arr == -1] = np.nan

    # constrain and normalize an array of ints to 0-bound
    def normalize_arr(self, arr, bound, invert = False):
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

    def parse_readings(self, readings, min_magnitude = 100):
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

    def all_pixels_within(self, point, distance):
        """
        returns a mask for pixel_coords that is true for all pixels within a given distance to a point
        """
        idx = np.abs(self.pixel_coords - point)
        return [math.dist(point, pixel) < distance for pixel in self.pixel_coords]

    def distances_to_point(self, point):
        """
        returns the euclidean distance to every pixel in tree from a given point
        """
        return [math.dist(point, pixel) for pixel in self.pixel_coords]

    def index_of_nearest(self, point):
        """
        returns the index of the nearest pixel in 3d space to a given point
        """
        idx = np.abs(self.pixel_coords - point)
        distances = self.distances_to_point(point)
        return distances.index(min(distances))

    def yaw_90_deg(self, arr, times = 1, origin = [0, 0, 0]):
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
        

    def rotate_2d(self, point, angle, origin = [0, 0]):
        """
        Rotate a point counterclockwise by a given angle around a given origin.

        The angle should be given in radians.
        """
        if np.nan in point:
            return point

        ox, oy = origin
        px, py = point

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return qx, qy

    def rotate(self, point, pitch = 0, roll = 0, yaw = 0, origin = [0, 0, 0]):
        """
        Rotate point around origin given pitch, roll, and/or yaw in radians.
        Also supports rotation of an entire numpy ndarray.
        Note that the top of the tree is treated as the 'front' with regards to the rotational axis
        """
        if np.nan in point:
            return point

        cosa = math.cos(yaw)
        sina = math.sin(yaw)

        cosb = math.cos(pitch)
        sinb = math.sin(pitch)

        cosc = math.cos(roll)
        sinc = math.sin(roll)

        Axx = cosa*cosb
        Axy = cosa*sinb*sinc - sina*cosc
        Axz = cosa*sinb*cosc + sina*sinc

        Ayx = sina*cosb
        Ayy = sina*sinb*sinc + cosa*cosc
        Ayz = sina*sinb*cosc - cosa*sinc

        Azx = -sinb
        Azy = cosb*sinc
        Azz = cosb*cosc

        # support rotating entire numpy arrays too
        if isinstance(point, np.ndarray):
            # Don't modify the original
            new_array = point.copy()
            new_array -= origin
            new_array[:, 0] =  Axx*new_array[:, 0] +  Axy*new_array[:, 1] + Axz*new_array[:, 2]
            new_array[:, 1] =  Ayx*new_array[:, 0] +  Ayy*new_array[:, 1] + Ayz*new_array[:, 2]
            new_array[:, 2] =  Azx*new_array[:, 0] +  Azy*new_array[:, 1] + Azz*new_array[:, 2]
            new_array += origin
            return new_array 

        # If we reach this point, assume we've got a normal set of coordinates

        px = point[0] - origin[0]
        py = point[1] - origin[1]
        pz = point[2] - origin[2]

        new_x = Axx*px + Axy*py + Axz*pz
        new_y = Ayx*px + Ayy*py + Ayz*pz
        new_z = Azx*px + Azy*py + Azz*pz
        return [new_x + origin[0], new_y + origin[1], new_z +  + origin[2]]

    def merge_arrays(self, dest, source):
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

    def load_mappings(self, path = "mapping.txt"):
        with open(path, "r") as f:
            raw_str = f.read().replace("[", "").replace("]", "").split('\n')
        # its a bit ugly but we need to replace multiple spaces with single space
        self.pixel_coords = np.array([[float(num) for num in list(filter(None, line.split(' ')))] for line in raw_str])



    # this function only supports readings from 0, 90, 180, and 270 degrees because
    # anything more than 4 sides is too much math for me
    def load_mappings_old(self):
        """
        Load in 4 mapping files that contain x, y, and magnitude CSVs that tree-mapper.py outputs.
        Each file is expected to be a 90 degree increment counter-clockwise rotation from the 'front'.
        Calling this method on a tree object will set tree.pixel_coords to a numpy array of x, y, and z
        coordinates, where the index of a given point corresponds with the position of the LED in the strip.
        """
        with open("readings_0_deg.txt", "r") as f:
            np_deg0 = self.parse_readings(f.read())
        with open("readings_90_deg.txt", "r") as f:
            np_deg90 = self.parse_readings(f.read())
        with open("readings_180_deg.txt", "r") as f:
            np_deg180 = self.parse_readings(f.read())
        with open("readings_270_deg.txt", "r") as f:
            np_deg270 = self.parse_readings(f.read())

        self.normalize_arr(np_deg0, [self.x_size, self.y_size, self.z_size])

        # we'll treat the 0 degree measurements as the 'final tree' and merge other measurements into it
        final_arr = np_deg0

        self.normalize_arr(np_deg90, [self.x_size, self.y_size, self.z_size])
        self.normalize_arr(np_deg180, [self.x_size, self.y_size, self.z_size])
        self.normalize_arr(np_deg270, [self.x_size, self.y_size, self.z_size])
        self.yaw_90_deg(np_deg90, times = 1, origin=[self.x_size/2, self.y_size/2, self.z_size/2])
        self.yaw_90_deg(np_deg180, times = 2, origin=[self.x_size/2, self.y_size/2, self.z_size/2])
        self.yaw_90_deg(np_deg270, times = 3, origin=[self.x_size/2, self.y_size/2, self.z_size/2])

        averages = self.merge_arrays(final_arr, np_deg90) + self.merge_arrays(final_arr, np_deg180) + self.merge_arrays(final_arr, np_deg270) + 1
        final_arr = final_arr / averages
        self.pixel_coords = final_arr
