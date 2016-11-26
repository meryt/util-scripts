#!/usr/bin/python

import sys
import getopt
from numpy import random as rnd
import colorsys

MAX_HUE = float(65535)

def hex_to_RGB(hex):
  ''' "#FFFFFF" -> [255,255,255] '''
  # Pass 16 to the integer function for change of base
  return [int(hex[i:i+2], 16) for i in range(1,6,2)]


def RGB_to_hex(RGB):
  ''' [255,255,255] -> "#FFFFFF" '''
  # Components need to be integers for hex to make sense
  RGB = [int(x) for x in RGB]
  return "#"+"".join(["0{0:x}".format(v) if v < 16 else
            "{0:x}".format(v) for v in RGB])

def rand_rgb_color(num=1):
  ''' Generate random rgb colors, default is one,
      returning an array. If num is greater than
      1, an array of arrays is returned. '''
  colors = [
    [x*255 for x in rnd.rand(3)]
    for i in range(num)
  ]
  if num == 1:
    return colors[0]
  else:
    return colors

def rand_rgb_color_unscaled(num=1):
  ''' Generate random rgb colors, default is one,
      returning an array. If num is greater than
      1, an array of arrays is returned. '''
  colors = [
    [x for x in rnd.rand(3)]
    for i in range(num)
  ]
  if num == 1:
    return colors[0]
  else:
    return colors

def rand_hsl_color(num=1):
  ''' Generate random hex colors, default is one,
      returning a string. If num is greater than
      1, an array of arrays is returned. '''
  randcolors = rand_rgb_color_unscaled(num)
  colors = []
  for rgbs in randcolors:
      colors += [(colorsys.rgb_to_hls(rgbs[0], rgbs[1], rgbs[2]))]

  if num == 1:
    return colors[0]
  else:
    return colors    

def rand_hex_color(num=1):
  ''' Generate random hex colors, default is one,
      returning a string. If num is greater than
      1, an array of strings is returned. '''
  colors = [
    RGB_to_hex([x*255 for x in rnd.rand(3)])
    for i in range(num)
  ]
  if num == 1:
    return colors[0]
  else:
    return colors

def hues_to_hex(hues):
	print hues
	hexes = []
	for hue in hues:
		hue = float(hue)
		normalized_hue = hue/MAX_HUE
		r, g, b = colorsys.hls_to_rgb(normalized_hue, 0.5, 1.0)
		#print (r, g, b)
		hexes += [RGB_to_hex((r, g, b))]
	return hexes

def color_dict(gradient):
  ''' Takes in a list of RGB sub-lists and returns dictionary of
    colors in RGB and hex form for use in a graphing function
    defined later on '''
  return {"hex":[RGB_to_hex(RGB) for RGB in gradient],
      "r":[RGB[0] for RGB in gradient],
      "g":[RGB[1] for RGB in gradient],
      "b":[RGB[2] for RGB in gradient]}

def linear_gradient(start_hex, finish_hex="#FFFFFF", n=10):
  ''' returns a gradient list of (n) colors between
    two hex colors. start_hex and finish_hex
    should be the full six-digit color string,
    including the number sign ("#FFFFFF") '''
  # Starting and ending colors in RGB form
  s = hex_to_RGB(start_hex)
  f = hex_to_RGB(finish_hex)
  # Initialize a list of the output colors with the starting color
  RGB_list = [s]
  # Calculate a color at each evenly spaced value of t from 1 to n
  for t in range(1, n):
    # Interpolate RGB vector for color at the current value of t
    curr_vector = [
      int(s[j] + (float(t)/(n-1))*(f[j]-s[j]))
      for j in range(3)
    ]
    # Add it to our list of output colors
    RGB_list.append(curr_vector)

  return color_dict(RGB_list)

def polylinear_gradient(colors, n):
  ''' returns a list of colors forming linear gradients between
      all sequential pairs of colors. "n" specifies the total
      number of desired output colors '''
  # The number of colors per individual linear gradient
  n_out = int(float(n) / (len(colors) - 1))
  # returns dictionary defined by color_dict()
  gradient_dict = linear_gradient(colors[0], colors[1], n_out)

  if len(colors) > 1:
    for col in range(1, len(colors) - 1):
      next = linear_gradient(colors[col], colors[col+1], n_out)
      for k in ("hex", "r", "g", "b"):
        # Exclude first point to avoid duplicates
        gradient_dict[k] += next[k][1:]

  return gradient_dict

def rgb_to_json(r, g, b):
	r, g, b = (r / 255.0, g / 255.0, b / 255.0)
	h, l, s = (colorsys.rgb_to_hls(r, g, b))
	h = int(h * MAX_HUE)
	l = int(l * 255)
	s = int(s * 255)
	json = '{"hue": ' + str(h) + ', "bri": ' + str(l) + ', "sat": ' + str(s) + '}'
	return json


def generate_test_file(gradients):

    print("<html><head><style>table { min-width: 300px; color: white }</style></head><body><table>")
    for i in range(0, len(gradients['hex']) -1):
    	col = gradients['hex'][i]
    	json = rgb_to_json(gradients['r'][i], gradients['g'][i], gradients['b'][i])
        print("<tr><td style=\"background-color:" + col + "\">&nbsp;&nbsp;&nbsp;" + col + "&nbsp;" + json + "&nbsp;&nbsp;</td></tr>")
    print("</table></body></html>")

def help():
    print '''
Usage: interpolate-colors.py [-t] [-h] -i <index> -n <num-colors> [-c <colors>]

num-colors: desired number of elements in the output gradient array
colors:     a comma-delimited list of hex colors along which
            the gradient will be interpolated. If not present, a gradient 
            along a random sequence of 3 colors will be produced.
index:      the item (nominally between 0 and (total-colors-1)) to return as 
            a hue value between 0 and 65535, and a sat and lightness between 
            0 and 255

-t will output a test HTML page showing the generated colors instead of 
   outputting a single hue value

-h will show this help
'''


def main(argv):
    numColors = 10
    colorIndex = 0
    testMode = False

    hex_colors = rand_hex_color(3)
    try:
        opts, args = getopt.getopt(argv,"htn:i:c:",["num-colors=","index=","colors="])
    except getopt.GetoptError:
        help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            help()
            sys.exit()
        elif opt == '-t':
      	    testMode = True
        elif opt in ("-i", "--index"):
            colorIndex = int(arg)
        elif opt in ("-c", "--colors"):
            hex_colors = arg.split(',')
        elif opt in ("-n", "--num-colors"):
            numColors = int(arg)

    gradient = polylinear_gradient(hex_colors, int(numColors) + len(hex_colors))

    if colorIndex < 0:
     	colorIndex = 0
    elif colorIndex >= len(gradient['hex']):
    	colorIndex = len(gradient['hex']) - 1

    if testMode:
    	generate_test_file(gradient)
    else:
    	print rgb_to_json(gradient['r'][colorIndex], gradient['g'][colorIndex], gradient['b'][colorIndex])


if __name__ == "__main__":
   main(sys.argv[1:])
