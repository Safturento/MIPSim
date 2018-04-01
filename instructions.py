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
	def _addi(self, params, return_hex=False):
		# if return_hex:
			# return int('0x000000' + \
			# self.registers.encode(params[0]) + \
			# self.registers.encode(params[0]) + \
			# int(params[1],16) + \

		self.register[params[0]] = self.register[params[1]] + int(params[2])

	def _add(self, params, return_hex=False):
		if return_hex:
			return ''

		self.register[params[0]] = self.register[params[1]] + self.register[params[2]]

	def _sub(self, params, return_hex=False):
		if return_hex:
			return ''

		self.register[params[0]] = self.register[params[1]] - self.register[params[2]]


	def _mult(self, params, return_hex=False):
		if return_hex:
			return ''

		product = params[0] * params[1]

		self.register['lo'] = bin(product)[34:]
		self.register['hi'] = bin(product)[2:34]

	# Shift instructions
	def _sll(self, params, return_hex=False):
		if return_hex:
			return ''

		self.register[params[0]] = self.register[params[1]] << params[2]

	def _srl(self, params, return_hex=False):
		if return_hex:
			return ''

		self.register[params[0]] = self.register[params[1]] >> params[2]

	# Load instructions
	def _li(self, params, return_hex=False):
		if return_hex:
			return ''

		self.register[params[0]] = int(params[1])

	# Misc instructions
	def _move(self, params, return_hex=False):
		if return_hex:
			return ''

		self.register[params[0]] = self.register[params[1]]

	def _syscall(self, params, return_hex=False):
		service_number = int(self.register['$v0'])
		if return_hex:
			return ''

		service_map[service_number](self.register)

	# Logical operators
	def _and(self, params, return_hex=False):
		self.registers[params[0]] = self.registers[params[1]] & self.registers[params[2]]
		if return_hex:
			return ''


	def _or(self, params, return_hex=False):
		self.registers[params[0]] = self.registers[params[1]] | self.registers[params[2]]
		if return_hex:
			return ''


	def _xor(self, params, return_hex=False):
		self.registers[params[0]] = self.registers[params[1]] ^ self.registers[params[2]]
		if return_hex:
			return ''


	def _nor(self, params, return_hex=False):
		self.registers[params[0]] = ~ (self.registers[params[1]] | self.registers[params[2]])
		if return_hex:
			return ''


	# Branches
	def _beq(self, params, return_hex=False):
		if return_hex:
			return ''

		if self.register[params[0]] == self.register[params[1]]:
			self.register['pc'] = params[2]
		
	def _bne(self, params, return_hex=False):
		if return_hex:
			return ''

		if self.register[params[0]] != self.register[params[1]]:
			self.register['pc'] = params[2]

	def _bgez(self, params, return_hex=False):
		if return_hex:
			return ''

		if self.register[params[0]] >= 0:
			self.register['pc'] = params[1]
		
	def _bgtz(self, params, return_hex=False):
		if return_hex:
			return ''

		if self.register[params[0]] > 0:
			self.register['pc'] = params[1]
		
	def _blez(self, params, return_hex=False):
		if return_hex:
			return ''

		if self.register[params[0]] <= 0:
			self.register['pc'] = params[1]
		
	def _bltz(self, params, return_hex=False):
		if return_hex:
			return ''

		if self.register[params[0]] < 0:
			self.register['pc'] = params[1]
		
	def _bgezal(self, params, return_hex=False):
		if return_hex:
			return ''

		self.register['$ra'] = self.register['pc']

		self.bgez(params)

	def _bltzal(self, params, return_hex=False):
		if return_hex:
			return ''

		self.register['$ra'] = self.register['pc']

		self.blez(params)

	# Jump
	def _j(self, params, return_hex=False):
		if return_hex:
			return ''
		self.register['pc'] = params[0]


	def _jal(self, params, return_hex=False):
		if return_hex:
			return ''

		self.register['$ra'] = self.register['pc']

		self._j(params)

	def _jr(self, params, return_hex=False):
		if return_hex:
			return ''

		self.register['pc'] = self.register['$ra']


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
