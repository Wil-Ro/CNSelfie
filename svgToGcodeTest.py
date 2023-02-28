'''
Code taken from https://pypi.org/project/svg-to-gcode/ and repurposed by
Rosia Evans 18/02/2023

Originally written by Alexander Padula 
https://pypi.org/user/Padlex/
'''

import svg_to_gcode.svg_parser as parser
import svg_to_gcode.compiler as compiler_class
import svg_to_gcode.compiler.interfaces as interfaces

compiler = compiler_class.Compiler(interfaces.Gcode, movement_speed=1000, cutting_speed=300, pass_depth=5)

curves = parser.parse_file("test.svg")

compiler.append_curves(curves)

compiler.compile_to_file("test.gcode")
