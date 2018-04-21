import re
import sys
import os
import string
import argparse

from register import Register
from instructions import Instructions, twos_comp
from memory import Memory
from gui import Gui


parser = argparse.ArgumentParser()
parser.add_argument('file_path', help='path to assembly file')
parser.add_argument('-c', '--console', help='force cli interface instead of gui', action='store_true')
parser.add_argument('-s', '--step', help='step through program line by line', action='store_true')
args = parser.parse_args()

# Create objects for different components of the simulator
register = Register()
memory = Memory()
instructions = Instructions(register, memory)

if not (os.path.isfile(args.file_path) and args.file_path.lower().endswith('.asm')):
	print(args.file_path, 'file not found.')
	sys.exit()

def to_int(input):
	try:
		return int(input)
	except ValueError:
		return input.strip('"\'').strip('\'"')

def iter_file(file_path):
	'''
		generator that allows iteration through a sanitized assembly
		file removing comments, extra whitespaces, and empty
	'''
	for line in open(file_path):
		line = line.split('#', 1)[0]
		line = line.translate({ord(c):' ' for c in string.whitespace})
		line = re.sub(' +', ' ', line)
		line.strip()

		if len(line) > 0:
			yield line

# Load file into a list of individual lines
text_lines = []
data_lines = []
current_section = 'text'

# text_loc = 0x00400000
# data_loc = 0x10010001
# loc = text_loc

# Populate jump targets for easier access when needed
jumps = {}

for line in iter_file(args.file_path):
	# Separate line into target, instruction, and paramaters
	jump_target, instruction, params = re.match(r'^(\w+:)?\s?(\.?\w+)?\s?(.+)?', line).groups()
	if jump_target:
		jumps[jump_target[:-1:]] = len(text_lines)

	if instruction:
		if instruction == '.data':
			current_section = 'data'
		elif instruction == '.text':
			current_section = 'data'
		else: 
			instruction = instruction.replace('.', '').lower()
			if params:
				# Remove any remaining whitespace between parameters
				params = params.translate({ord(c):None for c in string.whitespace})
				params = params.split(',')
				params = list(map(to_int, params))
			else:
				params = []
			# Rejoin line without targets
			# text_lines.append([instruction, params])
			text_lines.append({
				'inst': instruction,
				'params': params
			})

# This second pass swaps jump targets for memory locations
# and load instructions into memory
for i,line in enumerate(text_lines):
	# swap target for memory location if it's a jump
	if line['inst'] in instructions.jump_instructions:
		if line['params'][-1] in jumps:
			# replace target string with  memory location
			text_lines[i]['params'][-1] = register['pc'] + jumps[line['params'][-1]] * 4
		else:
			print("Invalid jump target", line['params'])
			sys.exit()

	# swap target for offset if it's a branch
	if line['inst'] in instructions.branch_instructions:
		if line['params'][-1] in jumps:
			target_loc = jumps[line['params'][-1]]
			text_lines[i]['params'][-1] = target_loc - i - 1

	# We want to ensure that values are set to 2's complement for this so that
	# we show the actual jump values correpsonding to memory locations
	params = []
	for item in line['params']:
		if type(item) is int:
			params.append(twos_comp(item)[-4::])
		else: params.append(item)

	line['line'] = line['inst'] + ' ' + ', '.join(params)
	text_lines[i]['code'] = instructions[line['inst']](return_hex=True, *line['params'])

	# populate memory. It's important to remember that any value stored or accessed in memory
	# has a multiple of 4 in order to be consistent with actual memory simulation 
	memory[register['pc'] + i*4] = line

# Get marker for end of file to know when to quit
end = register['pc'] + (len(text_lines)-1)*4
memory.set_text_section(end)

# Start program counter loop to run through program
if args.console:
	while register['pc'] <= end:
		line = memory[register['pc']]

		if args.step:
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
			return True
		else:
			return False

	gui.set_loop(loop, args.step)
	gui.root.mainloop()