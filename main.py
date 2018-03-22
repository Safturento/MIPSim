import re
import string
import sys
import os

from register import Register
from instructions import Instructions
from memory import Memory
from gui import Gui

# This allows for a mapping that automatically removes all whitespace
# characters from a string using string.translate(whitespace_trans)
whitespace_trans = {ord(c):None for c in string.whitespace}

# Split each line of the file into two pieces:
#  the instruction name and the parameters to pass to any function
def parse_line(line_num, line):
	result = re.match(r'(\w+)(.*)', line)
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

lines = []
with open(file_path) as file:
	lines = list(file)

# Populate jumps
jumps = {}
for i,line in enumerate(lines):
	# Remove all comments while were pre-parsing
	lines[i] = line.split('#', 1)[0]

	# Check if line has a jump target
	jump_line = re.match(r'^(\w+):(.+)?', line.strip())
	if jump_line:
		jumps[jump_line[1]] = i
		lines[i] = '' if jump_line[2] == None else jump_line[2]

# Create objects for different components of the simulator
registers = Register(jumps)
memory = Memory()
instructions = Instructions(registers, memory)
gui = Gui(registers)

end = len(lines)
while registers['pc'] < end:
	line = lines[registers['pc']].strip()
	if line and len(line) > 0:
		print(">>",line) #,input, end='')
		parse_line(registers['pc'], line)
		gui.update()
	registers['pc'] += 1

print("\nend of file. press enter to close")
# input()