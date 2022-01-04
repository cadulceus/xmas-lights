# xmas-lights

This project contains some useful scripts for interacting with a christmas tree lined with any RGB lights compatible with adafruit's neopixel library.

Some important files:

## lights-server.py

This script is intended to be run on a raspberry pi. It sets up a TCP port (default 4141) and will render any pickle-encoded python lists of RGB values (i.e. \[\[r, g, b\], \[r, g, b\], \[r, g, b\]\]) onto the tree over a GPIO pin (default is GPIO 21). **Be warned that this is not secure at all and the pi should absolutely not be exposed to the internet while running this script. Not only does this provide easy arbitrary code execution, but the script has to run as root in order to access GPIO pins. Even if its exposed only to LAN there are still security risks involved and you should only use this script if you know what you're doing.**

## tree.py

This module contains a single class *tree* which encapsulates the christmas tree.
```
import tree
xmas tree = tree.tree(host = '127.0.0.1', port = 4141)
tree.write_pixels([[255,255,255]] * 20)
```
will connect to a tree listening to 127.0.0.1 on port 4141 (these are the default values if nothing is passed in) and set the first 20 pixels on the tree to white.
An example of interacting with write_pixels() can be found in light-rotations.py

## tree-mapper.py

Running this script with an IP and file name `python3 tree-mapper.py 127.0.0.1 500 ./readings/readings_0_deg.txt` will iterate through the first 500 lights on the tree hosted at the ip, setting each pixel to (255,255,255) on each iteration and turning off all others. The script will then use the first camera it was able to find and take a picture, and attempt to identify the light that was turned on. It will dump the x, y, and magnitude values of what it identified as a light into the file specified as the third argument.

You will want to run this script 4 times in a dark room with as few reflective surfaces as possible (use a rug to block light bouncing off the floor between the camera and tree if you have a reflective floor). Position the camera to have the entire tree in its field of view, and run the tree-mapper script. The script will print each reading as its taken, and also visualize where it thinks the currrent pixel is on screen in an opencv window by circling it with a white circle. Every time you run the script, you will want to rotate the tree *counter-clockwise* by as close to 90 degrees as possible, and output the readings to a new file (e.g. readings_0_deg.txt, readings_90_deg.txt, etc). Try to eliminate as many variables as possible (reflective surfaces, straightness of tree, distance from camera) to get as accurate a mapping as possible.

Once you have 4 reading files, replace the mapping files in the repo and call tree.load_mappings(). This will set self.pixel_coords to a 3d numpy array formatted as [[pixel_0_x_float, pixel_0_y_float, pixel_0z_float], [pixel_1_x_float, pixel_1_y_float, pixel_1_z_float], ...]. These coordinates are scaled to the tree dimensions (default 100, 100, 100). An example of interacting with the tree in a 3d context can be seen in horizontal-scroll.py

# Final Notes

I've found that the raspberry pi does not handle the consistent ~50kb/s coming from light pattern scripts over wifi, so for the most stable lightshow just clone this whole repo ono the pi and have the lighting scripts connect to localhost. The wifi functionality is still useful for the tree mapping script and for testing new scripts though.

This project was based heavily on Matt Parker/Stand Up Math's 3d christmas tree from last year https://www.youtube.com/watch?v=TvlpIojusBE

Here is some footage of some of these scripts running:
<blockquote class="imgur-embed-pub" lang="en" data-id="a/p1ajV8s" data-context="false" ><a href="//imgur.com/a/p1ajV8s"></a></blockquote><script async src="//s.imgur.com/min/embed.js" charset="utf-8"></script>
