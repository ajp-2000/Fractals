# Fractals
fractals.py: A command-line Python 3 script for rendering various fractals to .bmp files. In v1.0.0, the fractals implemented are: the Sierpinski carpet and triangle, the Mandlebrot set, and Heighway's Dragon curve. All images are saved as 32-bit BGRA .bmp files, with default size 1024x1024px, but any size can be specified at the command line.

This program was also submitted as my final project for Harvard's course CS50x.

#### Video: https://www.youtube.com/watch?v=YfEFtpZUQZo&ab_channel=ArunPrabhakar

# Command line usage:
python3 ./fractals.py [FRACTAL] [PARAMETERS (all optional)]

Fractals:
   sc - Sierpinski carpet
   st - Sierpinski triangle
   m  - Mandlebrot set
   h  - Heighway dragon curve

Options:
   -size [height in pixels]  (all fractals are drawn to a square, except the Mandlebrot set if a non-square range is specified, in which case the -size paramater is taken to specify the height of the image, and the width is calculated accordingly. Size defaults to 1024.)
   
   -depth [maximum iterations]  (defaults to -1, which is interpreted as iterate until we reach individual pixels. The exceptions are the Mandlebrot set, for which an iteration count is approximated based on the -size and -range paramaters, unless a different count is specified with this parameter; and the dragon curve, which defaults to 12. This is because with the dragon curve, adding iterations expands the image, rather than creating increasingly finer detail, so there is no natural limit to how far we can iterate it.)
   
   -bkgd_colour [colour in format 0xRRGGBB]  (all fractals are drawn in one colour, aganist another colour. These default to 0x000000 and 0xFFFFFF respectively, but ccan be specified otherwise with this and the next option.)
   
   -colour [0xRRGGBB]
   
   -out [filename]  (defaults to output.bmp. Must be a .bmp.)
   
   -unit [length of unit in pixels]  (for the dragon curve only: specified the length of the base line to build the dragon up from. Defaults to 8.)
   
   -range [bottom-left corner of range, top-right corner] (for the Mandlebrot set only: the user can draw a particular range of the set, to simulate zooming in. The range must be given in the format x0,y0 x1,y1, e.g. "-range -0.5,0 0,0.5". Computation times increase as -range is narrowed while -size stays the same, because the nature of the set itself is such that the finer the resolution of our image, the greater the number of iterations are required to reach a given level of precision.)
   
   -shading [none/gradient/advanced]  (Mandlebrot only. No shading (the default) simply draws the set in [colour] against [bkgd_colour]. Gradient shading draws the set in [colour], and pixels which are not in the set are shaded along a gradient between [colour] and [bkgd_colour] according to how many iterations the complex number they represent took to go to infinity. Advanced shading is my approximation of the most famous colour scheme for the Mandlebrot set, which makes it dark blue, orange, and white. The algorithm in mandlebrot.py was written using the colour map used by Ultra Fractal 6 as a reference.)

# Copyright
Copyright <2022> <Arun James Prabhakar>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
