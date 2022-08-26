"""Draw a Sierpinski carpet recursively"""

from colour import Colour
from shapes import Fractal

class SierpinskiCarpet(Fractal):

	def __init__(self):
		super().__init__()

	# Perform the ninth-ing operation upon a specified square
	def cut(self, x0, y0, length, depth):
		if length >= 3:
			unit = round(length/3)

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