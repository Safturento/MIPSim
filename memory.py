class Memory:

	def __init__(self):
		self.memory = {}

	def __getitem__(self, key):
		return self.memory[key]

	def __setitem__(self, key, value):
		self.memory[key] = value

	def dump(self, start, nibbles):
		string = ''
		# for i in range(nibbles):
			# line = self.memory[start + i * 4]
			# string += '{} {}\n'.format(line['inst'], ','.join(line['params']))
		return string
		# return'\n'.join([self.memory[start + i*4] for i in range(nibbles)])
			
