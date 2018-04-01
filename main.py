import re
import sys
import os
import string

from register import Register
from instructions import Instructions
from memory import Memory
from gui import Gui

CONSOLE_OUTPUT = False

# Create objects for different components of the simulator
register = Register()
memory = Memory()
instructions = Instructions(register, memory)

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
line_components = []
lines = list(open(file_path))

def to_int(input):
	try:
		return int(input)
	except ValueError:
		return input.strip('"\'').strip('\'"')

# Populate jump targets for easier access when needed
jumps = {}
line_num = 0
for line in lines:
	# Remove all comments and extra whitespaces
	line = line.split('#', 1)[0]
	line = line.translate({ord(c):' ' for c in string.whitespace})
	line = re.sub(' +', ' ', line)

	# If the line is empty we don't need to parse it for code
	if len(line.strip()) > 0:

		# Separate line into target, instruction, and paramaters
		jump_target, instruction, params = re.match(r'^(\w+:)?\s?\.?(\w+)?\s?(.+)?', line.strip()).groups()

		if jump_target:
			jumps[jump_target[:-1:]] = line_num

		if instruction:
			if params:
				# Remove any remaining whitespace between parameters
				params = params.translate({ord(c):None for c in string.whitespace})
				params = params.split(',')
				params = list(map(to_int, params))
				print(params)
			# Rejoin line without targets
			# line_components.append([instruction, params])
			line_components.append({
				'inst': instruction,
				'params': params,
			})
			line_num += 1

# This second pass swaps jump targets for memory locations
# and load instructions into memory
for i,line in enumerate(line_components):

	# swap target for memory location if it's a jump or branch
	if line['inst'] in instructions.jump_instructions:
		if line['params'][-1] in jumps:
			# replace target string with  memory location
			line_components[i]['params'][-1] = register['pc'] + (jumps[line['params'][-1]]-1) * 4
		else:
			print("Invalid jump target", line['params'])
			sys.exit()

	# This line is pretty mess but is able to parse jump locations into
	# hex for display without overwriting the actual jump value in memory
	# while simply passing everything else as its normal value
	line['line'] = line['inst'] + ' ' + ', '.join(['{:08x}'.format(x) if type(x) is int else x for x in (line['params'] or [])])

	# populate memory. It's important to remember that any value stored or accessed in memory
	# has a multiple of 4 in order to be consistent with actual memory simulation 

	memory[register['pc'] + i*4] = line

# print(memory.dump(register['pc'], len(line_components)-1))

# Get marker for end of file to know when to quit
end = register['pc'] + (len(line_components)-1)*4
memory.set_text_section(end)


# Start program counter loop to run through program
if CONSOLE_OUTPUT:
	while register['pc'] <= end:

		line = memory[register['pc']]
		print('{:08x}'.format(register['pc']), ">>", line['line'], input(), end='')
		if line['params']:
			instructions[line['inst']](*line['params'])
		else:
			instructions[line['inst']]()
		register['pc'] += 4

	print("\nend of file. press enter to close")
	input()
else:
	gui = Gui(register, memory)

	# Used for piping syscall output to gui console
	instructions.set_gui(gui)

	def loop(self):
		if register['pc'] <= end:
			line = memory[register['pc']]
			if line['params']:
				instructions[line['inst']](*line['params'])
			else:
				instructions[line['inst']]()
			register['pc'] += 4
			gui.update()

	gui.set_loop(loop)
	gui.root.mainloop()