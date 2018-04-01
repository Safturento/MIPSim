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
 
	def get_params(self, query, params):
		"""
		Extracts parameters from line using tag-style string matching
		Args:
			query (str): String containing the items in the pattern to match. supported tags include:
				[reg] - matching a register name
				[imm] - matching an integer value
				[off] - matching a jump target for offset
			params (str): String containing parameters from assembly file to match with regex

		Example:
			params = '$v0,$v0,1'

			
		Returns:
		 	Regular expression groups containing individual values matching given tags
		"""

		regex = query \
			.replace('[reg]', '(\\$[a-z0-9]+)') \
			.replace('[imm]', '([0-9]+)') \
			.replace('[off]', '(\\w+)')

		return re.match(regex, params.translate(self.whitespace))


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

		self.register[dest] = int(imm)

	# Misc instructions
	def _move(self, dest, source, return_hex=False):
		if return_hex:
			return ''

		self.register[dest] = self.register[source]

	def _syscall(self, return_hex=False):
		service_number = int(self.register['$v0'])
		if return_hex:
			return ''

		service_map[service_number](self.register)

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


	def _ascii(self, string):
		print(string)

	# Assembler Directives
	def _asciiz(self, string):
		
		self.register['$sp']
		self._ascii(string + "\0")

	def _data(self, param):
		pass

	# Overloads self[key] to allow easy access to MIPS functions
	def __getitem__(self, key):
		try:
			# All functions are appended with an underscore to avoid
			# issues with overwriting python functions (e.g. or)
			return getattr(self, '_' + key)	
		except:
			raise Exception('{} function not implemented'.format(key))
