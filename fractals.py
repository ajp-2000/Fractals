"""A command-line script for drawing various fractal patterns, and saving them as 32-bit .bmp images.
fractal.py handles command-line arguments and bmp generation, and each kind of fractal has a class
of its own with a draw() function returning a two-dimensional array of pixels
"""

#!/usr/bin/python3

import sys

from carpet import SierpinskiCarpet

"""The pixels array is such that pixels[x][0] is the bottom of the image, to make things graph-like"""
FILEHEADERSIZE = 14
INFOHEADERSIZE = 40

def write_image(pixels):
	# Parse image
	width = len(pixels)
	height = len(pixels[0])

	# Open output file
	file = open("output.bmp", "wb")

	# Write Bitmap file header (14 bytes)
	file.write(b'\x42\x4D')												# Header field (BM)
	file.write((width*height + FILEHEADERSIZE + INFOHEADERSIZE).to_bytes(4, "little"))
	file.write(int(0).to_bytes(2, "little"))							# Application-dependent
	file.write(int(0).to_bytes(2, "little"))							# Application-dependent
	file.write((FILEHEADERSIZE+INFOHEADERSIZE).to_bytes(4, "little"))

	# Write Bitmap info header
	file.write(INFOHEADERSIZE.to_bytes(4, "little"))
	file.write(width.to_bytes(4, "little"))
	file.write(height.to_bytes(4, "little"))
	file.write(int(1).to_bytes(2, "little"))							# Number of colour planes
	file.write(int(32).to_bytes(2, "little"))							# 32 bits per pixel
	file.write(int(0).to_bytes(4, "little"))							# No compression
	file.write(int(0).to_bytes(4, "little"))							# Image size
	file.write(int(0).to_bytes(4, "little"))							# Horizontal resolution
	file.write(int(0).to_bytes(4, "little"))							# Vertical resolution
	file.write(int(0).to_bytes(4, "little"))							# Colours in palette
	file.write(int(0).to_bytes(4, "little"))							# No. of important colours

	# Write pixels, one dword (4 bytes) at a time
	for py in range(0, height):
		for px in range(0, width):
			# Break down the int into each value, in byte form
			red = (pixels[px][py] >> 2) & 0xFF
			green = (pixels[px][py] >> 1) & 0xFF
			blue = pixels[px][py] & 0xFF
			alpha = 0x00

			# Write
			file.write(blue.to_bytes(1, "little"))
			file.write(green.to_bytes(1, "little"))
			file.write(red.to_bytes(1, "little"))
			file.write(alpha.to_bytes(1, "little"))

	# Wrap up
	file.close()

def main():
	if len(sys.argv) < 2:
		print("fractals.py: a script for generating various fractals as .BMP images.\n" +
			"Usage: python3 fractals.py [FRACTAL] [OPTIONAL: OUTPUT] [OPTIONS]\n\n" +
			"Output defaults to output.bmp.\n\n" +
			"-sc\t\tSierpinski carpet\n" +
			"-st\t\tSierpinski triangle\n" +
			"-k\t\tKoch snowflake\n" +
			"-m\t\tMandlebrot set\n")

		sys.exit(1)

	# Render the specified fractal to pixels
	if (sys.argv[1] == "-sc"):
		img = SierpinskiCarpet(size=2000, depth=5).draw()

	# And write pixels to output.bmp
	write_image(img)

if __name__ == '__main__':
	main()