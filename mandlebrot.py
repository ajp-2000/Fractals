"""Draw the Mandlebrot set pixel by pixel"""

import math
import cmath
import re
import sys

from colour import Colour, parse_col, unparse_col
from shapes import Fractal

class MandlebrotSet(Fractal):
	x0 = -2
	x1 = 1
	y0 = -1.25
	y1 = 1.25
	shading = 1															# None, gradient, advanced

	def __init__(self):
		super().__init__()

	# Check if str is a number, including negative signs and decimal points
	def isnum(self, str):
		str = str.lstrip("-")
		dots = 0
		for ch in str:
			if ch == '.':
				dots += 1

		if dots < 2:
			if "".join(str.split(".")).isnumeric():
				return True

		return False

	# Apply the range given at the command line in the form "x0,y0 x1,y1"
	def parse_range(self, rangeStr):
		# Do the parsing
		list1 = rangeStr[0].split(",")
		list2 = rangeStr[1].split(",")

		if (len(list1) != 2) or (len(list2) != 2):
			print("Please specify range in form: x0,y0 x1,y1.")
			sys.exit(1)

		if self.isnum(list1[0]) and self.isnum(list1[1]) and self.isnum(list2[0]) and self.isnum(list2[1]):
			# Deal with negatives
			x0 = float(list1[0]) if (list1[0][0]!='-') else 0 - float(list1[0][1:])
			x1 = float(list2[0]) if (list2[0][0]!='-') else 0 - float(list2[0][1:])
			y0 = float(list1[1]) if (list1[1][0]!='-') else 0 - float(list1[1][1:])
			y1 = float(list2[1]) if (list2[1][0]!='-') else 0 - float(list2[1][1:])

			if x0==x1 or y0==y1:
				print("Range must be non-zero in both directions.")
				sys.exit(1)
		else:
			print("Please specify range in form: x0,y0 x1,y1.")
			sys.exit(1)

		# Set the range, allowing for different orderings
		if x0 < x1:
			self.x0 = x0
			self.x1 = x1
		else:
			self.x0 = x1
			self.x1 = x0

		if y0 < y1:
			self.y0 = y0
			self.y1 = y1
		else:
			self.y0 = y1
			self.y1 = y0

	# The logistic function for L = 1, k = 1, x0 = 0
	def sigmoid(self, x):
		return 1 / (1 + math.exp(-x))

	# Interpolate a value between a and b as on a +ve/-ve cube root graph
	def interp(self, a, b, sign, factor):
		xval = (((factor-a)/(b-a)) - 0.5) * 6
		if sign == 1:
			return self.sigmoid(xval) * 255
		else:
			return self.sigmoid(0-xval) * 255

	# Return a Colour object for advanced shading based on 0 <= factor <= 1
	# Algorithm adopted and simplified from Ultra Fractal 6
	def map_col(self, factor):
		factor *= 255
		
		# Red: slopes like an x^3 between 60 and 150, then down from 205 to 225
		red = 0
		if (factor>60) and (factor<=150):
			red = self.interp(60, 150, 1, factor)
		elif (factor>150) and (factor<=205):
			red = 255
		elif (factor>205) and (factor<=225):
			red = self.interp(205, 225, -1, factor)

		# Green: up from 40 to 150, then immediately down to 240
		green = 0
		if (factor>40) and (factor<=150):
			green = self.interp(40, 150, 1, factor)
		elif (factor>150) and (factor<=240):
			green = self.interp(150, 240, -1, factor)

		# Blue: up from 0 to 150, then down to 205
		blue = 0
		if factor <= 150:
			#blue = factor * (255/150)
			blue = self.interp(0, 150, 1, factor)
		elif factor <= 205:
			blue = self.interp(150, 205, -1, factor)

		return Colour(round(red), round(green), round(blue))

	# Test whether fc(0), fc(fc(0)) goes to infinity for c = a + bi
	# Where fc(z) = z^2 + c
	def diverges(self, a, b):
		z = complex(0, 0)
		c = complex(a, b)

		for iteration in range(0, self.depth):
			z = z**2 + c
			if (abs(z) > 2):
				return iteration

		return -1

	# self.size is the pixel height of the image; the width is worked out from x1-x0 and y1-y0
	def draw(self):
		# Assign a finite positive depth, by this rule of thumb reached by experimentation
		if self.depth == -1:
			pix_density = self.size / (self.y1-self.y0)
			self.depth = round(pix_density/6)

		maxx = round(self.size*((self.x1-self.x0)/(self.y1-self.y0)))
		maxy = self.size
		self.pixels = [[self.bkgd_colour for y in range(0, maxy)] for x in range(0, maxx)]
		scale = ((self.y1-self.y0)/self.size)

		for px in range(0, len(self.pixels)):
			for py in range(0, self.size):
				x = self.x0 + px*scale
				y = self.y0 + py*scale

				# Interpret the iteration count as a colour 
				# No shading: colour for the set, bkgd_colour for not
				# Gradient shading: colour for the set, closer to bkgd_colour for more iterations

				count = self.diverges(x, y)
				if self.shading == 1:
					# No shading
					if count == -1:
						col = self.colour
					else:
						col = self.bkgd_colour

					self.pixels[px][py] = col
				elif self.shading == 2:
					# Gradient shading
					if count == -1:
						col = self.colour
					else:
						r = self.bkgd_colour.red + (self.colour.red-self.bkgd_colour.red) * (count/self.depth)
						g = self.bkgd_colour.green + (self.colour.green-self.bkgd_colour.green) * (count/self.depth)
						b = self.bkgd_colour.blue + (self.colour.blue-self.bkgd_colour.blue) * (count/self.depth)
						col = Colour(round(r), round(g), round(b))

					self.pixels[px][py] = col
				elif self.shading == 3:
					# Advanced shading
					if count == -1:
						col = Colour(0, 0, 0)
					else:
						col = self.map_col(count/self.depth)

					self.pixels[px][py] = col

		"""Test the colour mapping
		for x in range(0, 255):
			for y in range(0, self.size):
				c = self.map_col(x/255)
				self.pixels[x][y] = c

			# Draw graphs
			self.pixels[x][100+c.red] = Colour(0, 0, 0)
			self.pixels[x][400+c.green] = Colour(0, 0, 0)
			self.pixels[x][700+c.blue] = Colour(0, 0, 0)"""

		return self.pixels