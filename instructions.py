import re
from syscall import service_map

class Instructions:
	# Regular expression patterns to extract parameters
	def get_params(self, query, params):
		regex = query \
			.replace('[reg]', '(\\$[a-z0-9]+)') \
			.replace('[imm]', '([0-9]+)') \
			.replace('[off]', '(\\w+)')
		print(regex)

		return re.match(regex, params)

	def __init__(self, register, memory):
		self.register = register
		self.memory = memory

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

	def li(self, params):
		results = self.get_params('[reg],[imm]', params)
		self.register[results[1]] = int(results[2])

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
		if self.register[results[1]] == self.register[results[2]]:
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

	def JAL(self, params):
		pass

	def JR(self, params):
		pass



	# Overloads self[key] to allow easy access to MIPS functions
	def __getitem__(self, key):
		try:
			return getattr(self, key)	
		except:
			raise Exception('{} function not implemented'.format(key))
