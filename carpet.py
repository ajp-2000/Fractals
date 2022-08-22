"""Draw a Sierpinski carpet recursively"""

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