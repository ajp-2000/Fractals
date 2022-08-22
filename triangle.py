"""Draw a Sierpinski triangle reucrsively"""

import math
import sys

from colour import Colour
from carpet import Fractal

class SierpinskiTriangle(Fractal):

	def __init__(self):
		super().__init__()

	# Draw a line to pixels from (x0, y0) to (x1, y1) using Bresenham's line algorithm
	def draw_line(self, x0, y0, x1, y1):
		x0 = round(x0)
		y0 = round(y0)
		x1 = round(x1)
		y1 = round(y1)

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

	# Draw an equilateral triangle of side length, with a horizontal base extending right from (x0, y0)
	def next_triangle(self, x0, y0, length, depth):
		if length>=3:
			# Draw the triangle
			self.draw_line(x0, y0, x0+length, y0)

			x1 = (x0*2+length) / 2
			y1 = y0 + math.tan(math.pi/3) * (length/2)
			self.draw_line(x0, y0, x1, y1)
			self.draw_line(x0+length, y0, x1, y1)

			# Then recurse
			if depth != self.depth:
				unit = length / 2
				self.next_triangle(x0, y0, unit, depth+1)
				self.next_triangle(x0+unit, y0, unit, depth+1)
				self.next_triangle(x0+unit/2, y0+(y1-y0)/2, unit, depth+1)

	def draw(self):
		# Draw triangles, decreasing by three times each time, until we hit individual pixels
		self.next_triangle(0, 0, self.size-1, 1)

		return self.pixels