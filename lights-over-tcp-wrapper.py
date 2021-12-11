import socket, board, neopixel
from pickle import loads, dumps

HOST = ''
PORT = 4141
pixels = neopixel.NeoPixel(board.D21, PIXELS_COUNT, auto_write = false, pixel_order = 'RGB')

def update_pixels(new_pixels):
    for i in range(max(len(pixels), len(new_pixels)):
        pixels[i] = new_pixels[i]
    pixels.show()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    while 1:
        s.listen()
        conn, addr = s.accept()
        with conn:
            print("accepting connection from ", addr)
            data = conn.recv(4096)
            print("Receieved ", len(data), " bytes containing ", data)
            try:
                pixel_arr = loads(data)
            except BaseException as e:
                print("failed to load pickled array", data, str(e))
                pass
            update_pixels(pixel_arr)
