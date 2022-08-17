"""Draw a Sierpinski carpet
Size: the dimensions of the image. Images must be square
Depth: the maximum levels of Sierpinski-splitting. -1 by default, for going until we reach individual pixels.
Colour: The colour of the added squares. 0x000000 by default
Background colour: 0xFFFFFF by default"""

import math

class SierpinskiCarpet:

	def __init__(self, size=600, depth=-1, colour=0x000000, bkgd_colour=0xFFFFFF):
		self.pixels = [[bkgd_colour for y in range(size)] for x in range(size)]
		self.size = size
		self.depth = depth
		self.colour = colour
		self.bkgd_colour = bkgd_colour

	# Perform the ninth-ing operation upon a specified square
	def cut(self, x0, y0, length, depth):
		if length >= 3:
			unit = math.floor(length/3)

			# Colour the central square of the nine, i.e. switch the colour of its pixels
			for px in range(unit+1, unit*2+1):
				for py in range(unit+1, unit*2+1):
					if self.pixels[x0+px][y0+py] == self.colour:
						self.pixels[x0+px][y0+py] = self.bkgd_colour
					else:
						self.pixels[x0+px][y0+py] = self.colour

			# Then call cut on each of the eight remaining squares
			for x in range(0, unit*2+1, unit):
				for y in range(0, unit*2+1, unit):
					if x!=unit or y!= unit:
						if depth != self.depth:
							self.cut(x+x0, y+y0, unit, depth+1)


	def draw(self):
		# Divide until we don't have enough pixels to divide further (recursively)
		self.cut(0, 0, self.size, 1)


		return self.pixels