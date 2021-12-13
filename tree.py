import socket
from pickle import dumps
import numpy as np

class tree:
    def __init__(self, host, port, x_size = 100, y_size = 100, z_size = 100):
        self.HOST = host
        self.PORT = port
        self.x_size = x_size
        self.y_size = y_size
        self.z_size = z_size

    def write_pixels(self, pixels):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            s.send(dumps(pixels))
            s.close()
    
    # constrain and normalize an array of ints to 0-bound
    def normalize_arr(self, arr, bound, invert = False):
        min_x, max_x = np.nanmin(arr), np.nanmax(arr)
        max_x = max_x - min_x

        x_scale = bound / (max_x - min_x)

        # shift everything over, then scale it
        for i in range(len(arr)):
            arr[i] = arr[i] - min_x
            if invert:
                arr[i] = abs(arr[i] - max_x)
            arr[i] = arr[i] * x_scale

    def parse_readings(self, readings):
            readings = readings.split("\n")
            readings = [s.split(", ") for s in readings]
            readings = [[int(reading[0]), int(reading[1]), float(reading[2])] for reading in readings]
            np_readings = np.array(readings)
            np_readings[np_deg0 == -1] = round(np.nan, 3)
            return np_readings

def rotate(point, angle, origin = [0, 0]):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

    """
    Rotate point around origin given pitch, roll, and/or yaw in radians
    """
    def rotate(self, point, pitch = 0, roll = 0, yaw = 0, origin = [0, 0, 0]):
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

        px = point[0] - origin[0]
        py = point[1] - origin[1]
        pz = point[2] - origin[2]

        new_x = Axx*px + Axy*py + Axz*pz
        new_y = Ayx*px + Ayy*py + Ayz*pz
        new_z = Azx*px + Azy*py + Azz*pz
        return [round(new_x + origin[0], 4), round(new_y + origin[1], 4), round(new_z +  + origin[2], 4)]


    # this function only supports readings from 0, 90, 180, and 270 degrees because
    # anything more than 4 sides is too much math for me
    def load_mappings(self):
        with open("readings_0.txt", "r") as f:
            np_deg0 = parse_readings(f.read())
        with open("readings_90.txt", "r") as f:
            np_deg90 = parse_readings(f.read())
        with open("readings_180.txt", "r") as f:
            np_deg180 = parse_readings(f.read())
        with open("readings_270.txt", "r") as f:
            np_deg270 = parse_readings(f.read())

        normalize_arr(np_deg0[:, 0], self.x_size)
        normalize_arr(np_deg0[:, 1]. self.y_size)
        normalize_arr(np_deg0[:, 2]. self.z_size)

        # yawing at 90 degree increments can be achieved by just swapping x and z axises around
        # but wheres the fun in that
        angle = 0.5 * np.pi
        rotated_deg90 = np.array([rotate()])
        normalize_arr(np_deg90[:, 0], self.x_size)
        normalize_arr(np_deg90[:, 1]. self.y_size)
        normalize_arr(np_deg90[:, 2]. self.z_size)

        normalize_arr(np_deg180[:, 0], self.x_size)
        normalize_arr(np_deg180[:, 1]. self.y_size)
        normalize_arr(np_deg180[:, 2]. self.z_size)

        normalize_arr(np_deg270[:, 0], self.x_size)
        normalize_arr(np_deg270[:, 1]. self.y_size)
        normalize_arr(np_deg270[:, 2]. self.z_size)