import re
from syscall import service_map

class Instructions:

	# Regular expression patterns to extract parameters
	def get_regex(self, string):
		return string \
			.replace('[reg]', '(\\$[a-z0-9]+)') \
			.replace('[imm]', '([0-9]+)')

		return regex

	def __init__(self, register, memory):
		self.register = register
		self.memory = memory

	def addi(self, params):
		results = re.match(self.get_regex('[reg],[reg],[imm]'), params)
		self.register[results[1]] = self.register[results[2]] + int(results[3])

	def add(self, params):
		results = re.match(self.get_regex('[reg],[reg],[reg]'), params)
		self.register[results[1]] = self.register[results[2]] + self.register[results[3]]

	def mult(self, params):
		results = re.match(self.get_regex('[reg],[reg]'), params)
		product = results[1] * results[2]

		self.register['lo'] = bin(product)[34:]
		self.register['hi'] = bin(product)[2:34]

	def j(self, params):
		if params in self.register.jumps:
			# target - 1 to offset the pc counter's pc+1
			#  ensuring the line with the target gets run
			self.register['pc'] = self.register.jumps[params] - 1

	def li(self, params):
		results = re.match(self.get_regex('[reg],[imm]'), params)
		self.register[results[1]] = int(results[2])

	def move(self, params):
		results = re.match(self.get_regex('[reg],[reg]'), params)
		self.register[results[1]] = self.register[results[2]]

	def syscall(self, params):
		service_number = int(self.register['$v0'])
		service_map[service_number](self.register)


	# Overloads self[key] to allow easy access to MIPS functions
	def __getitem__(self, key):
		try:
			return getattr(self, key)	
		except:
			raise Exception('{} function not implemented'.format(key))
