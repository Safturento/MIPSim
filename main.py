import re
from register import Register
from instructions import Instructions

registers = Register()
instructions = Instructions(registers)

# Split each line of the file into two pieces:
#  the instruction name and the parameters to pass to any function
def parse_line(line_num, line):
	result = re.match(r'(\w+) (.+)', line)
	inst_name = result[1]
	params = result[2]

	# Ensure that instruction exists and then execute it
	# if inst_name in instructions:
	instructions[inst_name](params)

with open('test.asm') as file:
	for line_num, line in enumerate(file):
		if len(line.strip()) > 0:
			parse_line(line_num, line)

print(registers)