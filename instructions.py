import re
from syscall import service_map
import string

class Instructions:
	def __init__(self, register, memory):
		self.register = register
		self.memory = memory
		self.jump_instructions = ["beq","bne","bgez","bgtz","blez","bltz","bgezal","bltzal","j","jal","jr"]

		# This allows for a mapping that automatically removes all whitespace
		# characters from a string using string.translate(whitespace_trans)
		self.whitespace = {ord(c):None for c in string.whitespace}
		self.escaped = {
			'\\n': '\n'
			# '\\"': '\'',
			# "\\'": '\"',
		}
	def set_gui(self, gui):
		self.gui = gui


	# Arithmetic instructions
	def _addi(self, dest, source, imm, return_hex=False):
		# if return_hex:
			# return int('0x000000' + \
			# self.registers.encode(params[0]) + \
			# self.registers.encode(params[0]) + \
			# int(params[1],16) + \

		self.register[dest] = self.register[source] + int(imm)

	def _add(self, dest, source, target, return_hex=False):
		if return_hex:
			return ''

		self.register[dest] = self.register[source] + self.register[target]

	def _sub(self, dest, source, target, return_hex=False):
		if return_hex:
			return ''

		self.register[dest] = self.register[source] - self.register[target]


	def _mult(self, source, target, return_hex=False):
		if return_hex:
			return ''

		product = '{:064b}'.format((source * target))

		self.register['lo'] = bin(product)[32:]
		self.register['hi'] = bin(product)[:32]

	# Shift instructions
	def _sll(self, dest, target, shift, return_hex=False):
		if return_hex:
			return ''

		self.register[dest] = self.register[source] << shift

	def _srl(self, dest, target, shift, return_hex=False):
		if return_hex:
			return ''

		self.register[dest] = self.register[source] >> shift

	# Load instructions
	def _li(self, dest, imm, return_hex=False):
		if return_hex:
			return ''

		# self.register[dest] = int(imm)
		if type(imm) is str:
			# I haven't found a better way to do this,
			# re-escaping keys is a weird problem..
			imm = imm.replace('\\"', '\'')
			imm = imm.replace("\\'", '\"')
			imm = imm.replace('\\a', '\a')
			imm = imm.replace('\\b', '\b')
			imm = imm.replace('\\f', '\f')
			imm = imm.replace('\\n', '\n')
			imm = imm.replace('\\r', '\r')
			imm = imm.replace('\\t', '\t')
			imm = imm.replace('\\v', '\v')

			imm = ord(imm)
		self.register[dest] = int(imm)

	# Misc instructions
	def _move(self, dest, source, return_hex=False):
		if return_hex:
			return ''

		self.register[dest] = self.register[source]

	def _syscall(self, return_hex=False):
		if return_hex:
			return ''

		service_number = int(self.register['$v0'])

		output = service_map[service_number](self.register)
		if output != None:
			if hasattr(self, 'gui'):
				self.gui.print(output)
			else:
				print('\n', output)

	# Logical operators
	def _and(self, dest, source, target, return_hex=False):
		self.registers[dest] = self.registers[source] & self.registers[target]
		if return_hex:
			return ''


	def _or(self, dest, source, target, return_hex=False):
		self.registers[dest] = self.registers[source] | self.registers[target]
		if return_hex:
			return ''


	def _xor(self, dest, source, target, return_hex=False):
		self.registers[dest] = self.registers[source] ^ self.registers[target]
		if return_hex:
			return ''


	def _nor(self, dest, source, target, return_hex=False):
		self.registers[dest] = ~ (self.registers[source] | self.registers[target])
		if return_hex:
			return ''


	# Branches
	def _beq(self, source, target, offset, return_hex=False):
		if return_hex:
			return ''

		if self.register[source] == self.register[target]:
			self.register['pc'] = offset
		
	def _bne(self, source, target, offset, return_hex=False):
		if return_hex:
			return ''

		if self.register[source] != self.register[target]:
			self.register['pc'] = offset

	def _bgez(self, source, offset, return_hex=False):
		if return_hex:
			return ''

		if self.register[source] >= 0:
			self.register['pc'] = offset
		
	def _bgtz(self, source, offset, return_hex=False):
		if return_hex:
			return ''

		if self.register[source] > 0:
			self.register['pc'] = offset
		
	def _blez(self, source, offset, return_hex=False):
		if return_hex:
			return ''

		if self.register[source] <= 0:
			self.register['pc'] = offset
		
	def _bltz(self, source, offset, return_hex=False):
		if return_hex:
			return ''

		if self.register[source] < 0:
			self.register['pc'] = offset
		
	def _bgezal(self, source, offset, return_hex=False):
		if return_hex:
			return ''

		self.register['$ra'] = self.register['pc']

		self.bgez(source, offset)

	def _bltzal(self, source, offset, return_hex=False):
		if return_hex:
			return ''

		self.register['$ra'] = self.register['pc']
		self.blez(source, offset)

	# Jump
	def _j(self, target, return_hex=False):
		if return_hex:
			return ''
		self.register['pc'] = target


	def _jal(self, target, return_hex=False):
		if return_hex:
			return ''

		self.register['$ra'] = self.register['pc']

		self._j(target)

	def _jr(self, source, return_hex=False):
		if return_hex:
			return ''

		self.register['pc'] = self.register[source]


	def _sw(self, source, target):
		word_offset, reg = re.match(r'(\d+)\((\$\w+)\)', target).groups()
		# Offset is word offset, so we need to multiply by 4 to get actual mem address
		loc = self.register[reg] + int(word_offset)
		self.memory[loc] = self.register[source]


	def _lw(self, dest, target):
		word_offset, reg = re.match(r'(\d+)\((\$\w+)\)', target).groups()
		# Offset is word offset, so we need to multiply by 4 to get actual mem address
		loc = self.register[reg] + int(word_offset)
		self.register[dest] = self.memory[loc]

	def _ascii(self, string):
		# print(string)
		pass

	# Assembler Directives
	def _asciiz(self, string):
		
		self.register['$sp']
		self._ascii(string + "\0")

	def _globl(self, target, return_hex=False):
		pass

	def _data(self):
		pass

	def _text(self):
		pass

	def _nop(self):
		pass

	# Overloads self[key] to allow easy access to MIPS functions
	def __getitem__(self, key):
		try:
			# All functions are appended with an underscore to avoid
			# issues with overwriting python functions (e.g. or)
			return getattr(self, '_' + key)	
		except:
			raise Exception('{} function not implemented'.format(key))
