# Mapping of register nicknames to convert to actual register numbers
REGISTER_NICKS = {
	'$zero': '$0',
	'$at': '$1',
	'$v0': '$2',
	'$v1': '$3',
	'$a0': '$4', 
	'$a1': '$5', 
	'$a2': '$6', 
	'$a3': '$7',
	'$t0': '$8', 
	'$t1': '$9', 
	'$t2': '$10', 
	'$t3': '$11', 
	'$t4': '$12', 
	'$t5': '$13', 
	'$t6': '$14', 
	'$t7': '$15', 
	'$t8': '$16', 
	'$t9': '$17',
	'$s0': '$18', 
	'$s1': '$19', 
	'$s2': '$20', 
	'$s3': '$21', 
	'$s4': '$22', 
	'$s5': '$23', 
	'$s6': '$24', 
	'$s7': '$25',
	'$k0': '$26', 
	'$k1': '$27',
	'$gp': '$28', 
	'$sp': '$29', 
	'$fp': '$30', 
	'$ra': '$31'
}

class Register:
	def __init__(self, jumps):
		# Initialize Registers with special registers
		self.jumps = jumps
		self.registers = {
			'hi': 0,
			'lo': 0,
			'pc': 0
		}

		# Load numbered registers
		for r in range(32):
			self.registers['$' + str(r)] = 0

		self.ordered_keys = list(self.registers.keys())
		self.num_registers = len(self.registers)

	# overload indexing functions to give easy access to registers
	# ex: reg['$0'] instead of reg.registers['$0']
	def __getitem__(self, key):
		if key in REGISTER_NICKS:
			return self.registers[REGISTER_NICKS[key]]
		return self.registers[key]


	def __setitem__(self, key, value):
		if key in REGISTER_NICKS:
			self.registers[REGISTER_NICKS[key]] = value
		else:
			self.registers[key] = value

	def __str__(self):
		return '\n'.join(['{}\t: {:032b}'.format(reg,val) for reg,val in self.registers.items()])

	def __iter__(self):
		self.n = 0
		return self

	def __next__(self):
		if self.n < self.num_registers:
			key = self.ordered_keys[self.n]
			self.n += 1
			return (key, self.registers[key])
		else:
			raise StopIteration