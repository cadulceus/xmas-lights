import socket, board, neopixel
from pickle import loads, dumps

HOST = ''
PORT = 4141
PIXELS_COUNT = 500
pixels = neopixel.NeoPixel(board.D21, PIXELS_COUNT, auto_write = False, pixel_order = 'RGB')

def recv_full_object(sock):
    pickled_arr = b''
    for i in range(5):
        pickled_arr += sock.recv(4096)
        try:
            return loads(pickled_arr)
        except:
            pass

def update_pixels(new_pixels):
    for i in range(min(len(pixels), len(new_pixels))):
        pixels[i] = new_pixels[i]
    pixels.show()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        while 1:
            s.listen()
            conn, addr = s.accept()
            with conn:
                new_pixels = recv_full_object(conn)
                update_pixels(new_pixels)

main()