"""Some common resources"""

import math
from colour import Colour

# A generic fractal class which each particular class extends, allowing us to set the options
# for the fractal in main() with the same code regardless of which child class it is
class Fractal:
	def __init__(self):
		self.size = 1024
		self.depth = -1
		self.colour = Colour(0, 0, 0)
		self.bkgd_colour = Colour(255, 255, 255)
		self.pixels = [[self.bkgd_colour for y in range(self.size)] for x in range(self.size)]

	# Rebild the pixels array to take into account any size changes from outside
	def config(self):
		self.pixels = [[self.bkgd_colour for y in range(self.size)] for x in range(self.size)]

	# Draw a line to pixels from (x0, y0) to (x1, y1) using Bresenham's line algorithm
	def draw_line(self, x0, y0, x1, y1):
		x0 = math.floor(x0)
		y0 = math.floor(y0)
		x1 = math.floor(x1)
		y1 = math.floor(y1)

		dx = abs(x1-x0)
		dy = -abs(y1-y0)
		sx = 1 if (x0<x1) else -1
		sy = 1 if (y0<y1) else -1
		error = dx + dy

		while True:
			self.pixels[x0][y0] = self.colour
			if x0==x1 and y0==y1:
				break

			e2 = 2 * error
			if e2>=dy:
				if x0==x1:
					break
				error += dy
				x0 += sx
			if e2<=dx:
				if y0==y1:
					break
				error += dx
				y0 += sy