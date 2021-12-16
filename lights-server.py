import socket, board, neopixel, sys
from pickle import loads, dumps

HOST = ''
PORT = 4141
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
    if len(sys.argv) != 2:
        print("Usage: sudo python3 lights-server.py <pixel_count>")
        return
    pixel_count = sys.argv[1]
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        try:
            while 1:
                s.listen()
                conn, addr = s.accept()
                with conn:
                    new_pixels = recv_full_object(conn)
                    update_pixels(new_pixels)
        except Exception as e:
            print("Exception occurred, continuing anyways: ", str(e))
            continue

main()