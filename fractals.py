"""A command-line script for drawing various fractal patterns, and saving them as 32-bit .bmp images.
fractal.py handles command-line arguments and bmp generation, and each kind of fractal has a class
of its own with a draw() function returning a two-dimensional array of pixels
Written for Python 3.73
"""

#!/usr/bin/python3

import sys

from colour import Colour, parse_col
from carpet import SierpinskiCarpet
from triangle import SierpinskiTriangle
from mandlebrot import MandlebrotSet

#The pixels array is such that pixels[x][0] is the bottom of the image, to make things graph-like
FILEHEADERSIZE = 14
INFOHEADERSIZE = 40

# Dictionary for the codes and classnames of each fractal
fractal_names = {
	"sc" : SierpinskiCarpet,
	"st" : SierpinskiTriangle,
	"m" : MandlebrotSet
}

# And for the command-line options and epxlanations
cmd_options = {
	"-size" : "[height in pixels]\t\t(for best results use a multiple of 3)",
	"-depth" : "[number of levels]\t(defaults to maximum)",
	"-colour" : "[hex code]",
	"-bkgd_colour" : "[hex code]",
	"-out" : "[output file]\t\t(defaults to output.bmp)",
	"-range" : "[(x0, y0) (x1, y1)]",
	"-shading" : "[none/gradient/advanced]"
}

def write_image(pixels, dest):
	# Parse image
	width = len(pixels)
	height = len(pixels[0])

	# Open output file
	file = open(dest, "wb")

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
			file.write(pixels[px][py].blue.to_bytes(1, "little"))
			file.write(pixels[px][py].green.to_bytes(1, "little"))
			file.write(pixels[px][py].red.to_bytes(1, "little"))
			file.write(int(0x00).to_bytes(1, "little"))

	# Wrap up
	file.close()
	print("Image successfully written to " + dest + ".")

# Parse command line arguments
def main():
	# The usage text
	if len(sys.argv) < 2:
		print("fractals.py: a script for generating various fractals as .BMP images.\n\n" + 
			"Usage: python3 fractals.py [FRACTAL] [OPTIONS]\n\n" +  
			"Fractals:\n" + 
			"\tsc\tSierpinski carpet\n" + 
			"\tst\tSierpinski triangle\n" + 
			"\tm\tMandlebrot set\n\n" + 
			"Options:\n")
		for key in cmd_options:
			print("\t" + key + " " + cmd_options[key])
			if key == "-out":
				print("\nMandlebrot only:\n")

		print("")

		sys.exit(1)

	# Else check which fractal we're dealing with
	if (sys.argv[1] not in fractal_names):
		print("Fractal not recognised: " + sys.argv[1] + ".")
		sys.exit(1)

	frac = fractal_names[sys.argv[1]]()
	output = "output.bmp"

	# And parse the options in turn - a for loop would make the skipping forward impossible
	i = 2
	while i < len(sys.argv):
		arg = sys.argv[i]
		if arg in cmd_options:
			if i < len(sys.argv)-1:
				i += 1

				# Switch (arg)
				if arg=="-size":
					if sys.argv[i].isnumeric() and int(sys.argv[i])>0:
						frac.size = int(sys.argv[i])
						frac.config()
					else:
						print("Option -size should be followed by a positive number.")
						sys.exit(1)
				elif arg=="-depth":
					if sys.argv[i].isnumeric() and int(sys.argv[i])>0:
						frac.depth = int(sys.argv[i])
						frac.config()
					else:
						print("Option -depth should be followed by a positive number.")
						sys.exit(1)
				elif arg=="-colour" or arg=="-bkgd_colour":
					if len(sys.argv[i])==8 and sys.argv[i][:2]=="0x":
						if arg=="-colour":
							frac.colour = parse_col(int(sys.argv[i], 0))
						else:
							frac.bkgd_colour = parse_col(int(sys.argv[i], 0))

						frac.config()
					else:
						print("Colours should be specified in six-digit 0x format.")
						sys.exit(1)
				elif arg=="-out":
					if sys.argv[i][-4:] == ".bmp":
						output = sys.argv[i]
					else:
						print("The output file should end in .bmp.")
						sys.exit(1)
				elif arg=="-range":
					if i < len(sys.argv)-1:
						if sys.argv[1] == "m":
							frac.parse_range(sys.argv[i:i+2])
						else:
							print("WARNING: -range only applies to the Madlebrot set.")
						i += 1
					else:
						print("Please specify range in form: x0,y0 x1,y1.")
						sys.exit(1)
				elif arg=="-shading":
					if sys.argv[i]=="none":
						frac.shading = 1
					elif sys.argv[i]=="gradient":
						frac.shading = 2
					elif sys.argv[i]=="advanced":
						frac.shading = 3
					else:
						print("Shading option should be \"none\", \"gradient\", or \"advanced\".")
						sys.exit(1)
			else:
				print("Please provide a value for option " + arg + ".")
				sys.exit(1)
		else:
			print("Option not recognised: " + arg + ".")
			sys.exit(1)

		i += 1
		

	# Render and 
	print("Rendering...")
	img = frac.draw()
	print("Saving...")
	write_image(img, output)

if __name__ == '__main__':
	main()