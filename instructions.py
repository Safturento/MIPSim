import re
from syscall import service_map
import string

class Instructions:
	def __init__(self, register, memory):
		self.register = register
		self.memory = memory

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
			results = self.get_params('[reg],[reg],[imm]'], params)
			
		Returns:
		 	Regular expression groups containing individual values matching given tags
		"""

		regex = query \
			.replace('[reg]', '(\\$[a-z0-9]+)') \
			.replace('[imm]', '([0-9]+)') \
			.replace('[off]', '(\\w+)')

		return re.match(regex, params.translate(self.whitespace))


	# Arithmetic instructions
	def addi(self, params):
		results = self.get_params('[reg],[reg],[imm]', params)
		self.register[results[1]] = self.register[results[2]] + int(results[3])

	def add(self, params):
		results = self.get_params('[reg],[reg],[reg]', params)
		self.register[results[1]] = self.register[results[2]] + self.register[results[3]]

	def mult(self, params):
		results = self.get_params('[reg],[reg]', params)
		product = results[1] * results[2]

		self.register['lo'] = bin(product)[34:]
		self.register['hi'] = bin(product)[2:34]


	# Load instructions
	def li(self, params):
		results = self.get_params('[reg],[imm]', params)
		self.register[results[1]] = int(results[2])

	# Misc instructions
	def move(self, params):
		results = self.get_params('[reg],[reg]', params)
		self.register[results[1]] = self.register[results[2]]

	def syscall(self, params):
		service_number = int(self.register['$v0'])
		service_map[service_number](self.register)

	# Branches
	def beq(self, params):
		results = self.get_params('[reg],[reg],[off]', params)
		if self.register[results[1]] == self.register[results[2]]:
			self.j(results[3])
		
	def bne(self, params):
		results = self.get_params('[reg],[reg],[off]', params)
		if self.register[results[1]] != self.register[results[2]]:
			self.j(results[3])

	def bgez(self, params):
		results = self.get_params('[reg],[off]', params)
		if self.register[results[1]] >= 0:
			self.j(results[2])
		
	def bgtz(self, params):
		results = self.get_params('[reg],[off]', params)
		if self.register[results[1]] > 0:
			self.j(results[2])
		
	def blez(self, params):
		results = self.get_params('[reg],[off]', params)
		if self.register[results[1]] <= 0:
			self.j(results[2])
		
	def bltz(self, params):
		results = self.get_params('[reg],[off]', params)
		if self.register[results[1]] < 0:
			self.j(results[2])
		
	def bgezal(self, params):
		self.register['$ra'] = self.register['pc']
		self.bgez(params)

	def bltzal(self, params):
		self.register['$ra'] = self.register['pc']
		self.blez(params)

	# Jump
	def j(self, params):
		if params in self.register.jumps:
			# target - 1 to offset the pc counter's pc+1
			#  ensuring the line with the target gets run
			self.register['pc'] = self.register.jumps[params] - 1

	def jal(self, params):
		self.register['$ra'] = self.register['pc']
		self.j(params)

	def jr(self, params):
		results = self.get_params('[reg]')
		self.register['pc'] = self.register['$ra']

	# Assembler Directives
	def asciiz(self, params):
		print(params)

	def data(self, param):
		pass

	# Overloads self[key] to allow easy access to MIPS functions
	def __getitem__(self, key):
		try:
			return getattr(self, key)	
		except:
			raise Exception('{} function not implemented'.format(key))
