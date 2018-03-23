import re
import sys
import os

from register import Register
from instructions import Instructions
from memory import Memory
from gui import Gui

def parse_line(line):
	"""
		Split each line of the file into two pieces:
			1. the instruction name 
			2. the parameters to pass to any function

		params:
			line (str): the assembly code line to parse and execute
	"""
	result = re.match(r'\.?(\w+)(.*)', line)
	inst_name = result[1]
	instructions[inst_name](result[2])

# Default file if none is given
file_path = 'test.asm'
# Loop through file one line at a time each time user presses enter
if len(sys.argv) > 1:
	if os.path.isfile(sys.argv[1]):
		file_path = sys.argv[1]
	else:
		print(sys.argv[1], 'file not found.')
		sys.exit()

# Load file into a list of individual lines
lines = []
with open(file_path) as file:
	lines = list(file)

# Populate jump targets for easier access when needed
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

# Get marker for end of file to know when to quit
end = len(lines)

# Start program counter loop to run through program
while registers['pc'] < end:

	line = lines[registers['pc']].strip()
	
	if line and len(line) > 0:
		print(">>", line)#, input(), end='')
		parse_line(line)
		gui.update()

	registers['pc'] += 1

print("\nend of file. press enter to close")
# input()