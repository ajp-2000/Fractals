"""Draw a Sierpinski triangle reucrsively"""

import math
import sys

from colour import Colour
from shapes import Fractal

class SierpinskiTriangle(Fractal):

	def __init__(self):
		super().__init__()

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