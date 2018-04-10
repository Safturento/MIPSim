class Memory:
	def __init__(self):
		self.memory = {}

	def __getitem__(self, key):
		return self.memory[key]

	def __setitem__(self, key, value):
		self.memory[key] = value

	def __contains__(self, key):
		return key in self.memory

	def set_text_section(self, *args):
		# If only one argument is given, assume its the end
		if len(args) == 1:
			self.text_memory = range(0x00400000, args[0]+4, 4)
		else:
			self.text_memory = range(args[0], args[1]+4, 4)
			

	def dump(self, start, nibbles):
		string = ''
		# for i in range(nibbles):
			# line = self.memory[start + i * 4]
			# string += '{} {}\n'.format(line['inst'], ','.join(line['params']))
		return string
		# return'\n'.join([self.memory[start + i*4] for i in range(nibbles)])
			
