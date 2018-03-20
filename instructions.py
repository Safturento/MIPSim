import re

class Instructions:
	register = None
	# Regular expression patterns to extract parameters
	PATTERNS = {
		'r_type_immediate': r'(\$[a-v0-9]+),(\$[a-v0-9]+),([\d]+)',
		'r_type':						r'(\$[a-v0-9]+),(\$[a-v0-9]+),(\$[a-v0-9]+)'
	}

	def __init__(self, register):
		self.register = register

	def addi(self, params):
		results = re.match(self.PATTERNS['r_type_immediate'], params.replace(' ', ''))

		self.register[results[1]] = self.register[results[2]] + int(results[3])

	def add(self, params):
		results = re.match(self.PATTERNS['r_type'], params.replace(' ', ''))
		self.register[results[1]] = self.register[results[2]] + self.register[results[3]]

	# Overloads self[key] to allow easy access to MIPS functions
	def __getitem__(self, key):
		try:
			return getattr(self, key)	
		except:
			raise Exception('{} function not implemented'.format(key))
