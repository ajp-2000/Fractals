"""A class for colours, with r, g, and b values between 0 and 255"""

# Return a Colour object corresponding to a six-digit RGB hex code
def parse_col(hexcode):
	return Colour((hexcode>>2) & 0xFF, (hexcode>>1) & 0xFF, hexcode & 0xFF)

class Colour:
	def __init__(self, red, green, blue):
		self.red = red
		self.green = green
		self.blue = blue

# Turn a Colour object into an int from 0x000000 to 0xFFFFFF
def unparse_col(col):
	return (col.red * 16**4) + (col.green * 16**2) + (col.blue)