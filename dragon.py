"""Draw a Heighway Dragon curve iteratively"""

import math

from colour import Colour
from shapes import Fractal

class DragonCurve(Fractal):
	unit = 8
	lines = []

	def __init__(self):
		super().__init__()

	def turn(self, x, y, xpivot, ypivot):
		# Subtract the pivot from the point, then rotate (90 degrees anti-clockwise)
		x -= xpivot
		y -= ypivot

		# Imitate a rotation matrix
		x1 = 0 - y
		y1 = x + 0

		x1 += xpivot
		y1 += ypivot

		return [x1, y1]

	# Used by bevel() below: remove the 1/3 before the pivot and return the co-ordinate to be joined
	# Approaching is 0 for the line approaching the pivot, 2 for the line leaving it
	def shorten(self, linenum, approaching, xpivot, ypivot):
		# Find a sensible way to take a chunk off each unit line
		if self.unit%3 == 0:
			diff = self.unit / 3
		else:
			diff = math.ceil(self.unit/4)

		if self.lines[linenum][0+approaching] < xpivot:
			# The line is in the +ve x-direction
			self.lines[linenum][2-approaching] -= diff
		elif self.lines[linenum][0+approaching] > xpivot:
			# -ve x-direction
			self.lines[linenum][2-approaching] += diff
		elif self.lines[linenum][1+approaching] < ypivot:
			# +ve y-direction
			self.lines[linenum][3-approaching] -= diff
		else:
			# -ve y-direction
			self.lines[linenum][3-approaching] += diff

		return self.lines[linenum][(-2-approaching):]

	# Add a bevel at the pivot by reducing each incoming line by 1/3 and joining the stubs
	def bevel(self, xpivot, ypivot):
		# Find the relevant lines as indices of self.lines
		pivlines = [0, 0]
		for i in range(0, len(self.lines)):
			if self.lines[i][-2:] == [xpivot, ypivot]:
				# The line ending at the pivot
				pivlines[0] = i

			if self.lines[i][:2] == [xpivot, ypivot]:
				# The line starting at the pivot
				pivlines[1] = i

		stubs = [self.shorten(pivlines[0], 0, xpivot, ypivot), self.shorten(pivlines[1], 2, xpivot, ypivot)]
		bevel = [stubs[0][0], stubs[0][1], stubs[1][0], stubs[1][1]]

		self.lines.append(bevel)

	# Rotate existing lines about (xpivot, ypivot) by 90 degrees anti-clockwise
	# We make sure the line which ends with the new pivot is written last
	def add_lines(self, xpivot, ypivot):
		reflected = []
		end = [xpivot, ypivot]
		for line in self.lines:
			[x0, y0] = self.turn(line[2], line[3], xpivot, ypivot)
			[x1, y1] = self.turn(line[0], line[1], xpivot, ypivot)
			reflected.extend([[x0, y0, x1, y1]])

		# Append the new lines to the lines list
		self.lines.extend(reflected)
		self.bevel(xpivot, ypivot)

		return [reflected[0][2], reflected[0][3]]

	def draw(self):
		# An indefinite depth wouldn't make sense here, so set a default of 12
		if self.depth == -1:
			self.depth = 12
			print("Depth defaulting to 12.")

		# Write lines to list
		self.lines = [[0, 0, 0, self.unit]]
		xpivot = 0
		ypivot = self.unit
		for i in range(1, self.depth):
			newpivot = self.add_lines(xpivot, ypivot)
			[xpivot, ypivot] = newpivot

		# Normalise the lines
		minx = 0
		miny = 0
		maxx = 0
		maxy = 0
		for line in self.lines:
			if line[0]<minx:
				minx = line[0]
			if line[2]<minx:
				minx = line[2]

			if line[1]<miny:
				miny = line[1]
			if line[3]<miny:
				miny = line[3]

			if line[0]>maxx:
				maxx = line[0]
			if line[2]>maxx:
				maxx = line[2]

			if line[1]>maxy:
				maxy = line[1]
			if line[3]>maxy:
				maxy = line[3]

		self.size = (maxx-minx) if (maxx-minx>maxy-miny) else maxy-miny
		self.pixels = [[self.bkgd_colour for y in range(self.size+1)] for x in range(self.size+1)]

		# And draw them
		for line in self.lines:
			#print(f"{line[0] - minx}, {line[1] - miny} to {line[2] - minx}, {line[3] - miny}")
			self.draw_line(line[0] - minx, line[1] - miny, line[2] - minx, line[3] - miny)


		return self.pixels
