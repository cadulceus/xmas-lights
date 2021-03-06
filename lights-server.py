import socket, board, neopixel, sys
from pickle import loads, dumps
import sys

HOST = ''
PORT = 4141

def recv_full_object(sock):
    pickled_arr = b''
    for i in range(5):
        pickled_arr += sock.recv(4096)
        try:
            return loads(pickled_arr)
        except:
            pass

def update_pixels(lights, new_pixels):
    for i in range(min(len(lights), len(new_pixels))):
        lights[i] = new_pixels[i]
    lights.show()

def main():
    if len(sys.argv) != 2:
        print("Usage: sudo python3 lights-server.py <pixel_count>")
        return
    pixel_count = int(sys.argv[1])
    lights = neopixel.NeoPixel(board.D21, pixel_count, auto_write = False, pixel_order = 'RGB')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        while 1:
            try:
                s.listen()
                conn, addr = s.accept()
                with conn:
                    new_pixels = recv_full_object(conn)
                    update_pixels(lights, new_pixels)
            except Exception as e:
                print("Exception occurred, continuing anyways: ", str(e))
                continue

main()