import re
import string
import sys
import os

from register import Register
from instructions import Instructions
from gui import Gui

# Create objects for different components of the simulator
registers = Register()
instructions = Instructions(registers)
gui = Gui(registers)

# This allows for a mapping that automatically removes all whitespace
# characters from a string using string.translate(whitespace_trans)
whitespace_trans = {ord(c):None for c in string.whitespace}

# Split each line of the file into two pieces:
#  the instruction name and the parameters to pass to any function
def parse_line(line_num, line):
	result = re.match(r'(\w+)[ \t]+(.+)', line)
	inst_name = result[1]
	params = result[2].translate(whitespace_trans)
	instructions[inst_name](params)

# Loop through file one line at a time each time user presses enter
file_path = 'test.asm'
if len(sys.argv) > 1:
	if os.path.isfile(sys.argv[1]):
		file_path = sys.argv[1]
	else:
		print(sys.argv[1], 'file not found.')
		sys.exit()

with open(file_path) as file:
	for line_num, line in enumerate(file):
		line = line.strip()
		if len(line) > 0:
			print(">>",line,input(), end='')
			parse_line(line_num, line)
			gui.update()

print("\nend of file. press enter to close")
input()