import re
from syscall import service_map
import string

from helpers import twos_comp, unescape

class Instructions:
	def __init__(self, register, memory):
		self.register = register
		self.memory = memory
		self.jump_instructions = ["j","jal"]
		self.branch_instructions = ["beq","bne","bgez","bgtz","blez","bltz","bgezal","bltzal"]

		# This allows for a mapping that automatically removes all whitespace
		# characters from a string using string.translate(whitespace_trans)
		self.whitespace = {ord(c):None for c in string.whitespace}
	
	def set_gui(self, gui):
		self.gui = gui

	# Arithmetic instructions
	def _addi(self, target, source, imm, return_hex=False):	
		if return_hex:
			return int('{:06b}{:05b}{:05b}{:016b}'.format(
				8,
				self.register.encode(source),
				self.register.encode(target),
				int(twos_comp(unescape(imm))[-4::],16)
				), 2)

		self.register[target] = self.register[source] + int(unescape(imm))

	def _add(self, dest, source, target, return_hex=False):
		if return_hex:
			return int('{:06b}{:05b}{:05b}{:05b}{:011b}'.format(
				0,
				self.register.encode(dest),
				self.register.encode(source),
				self.register.encode(target),
				32
				), 2)

		self.register[dest] = self.register[source] + self.register[target]

	def _sub(self, dest, source, target, return_hex=False):
		if return_hex:
			return int('{:06b}{:05b}{:05b}{:05b}{:011b}'.format(
				0,
				self.register.encode(dest),
				self.register.encode(source),
				self.register.encode(target),
				34
				), 2)

		self.register[dest] = self.register[source] - self.register[target]


	def _mult(self, source, target, return_hex=False):
		if return_hex:
			return int('{:06b}{:05b}{:05b}{:016b}'.format(
				0,
				self.register.encode(source),
				self.register.encode(target),
				24
				), 2)

		product = '{:064b}'.format((self.register[source] * self.register[target]))
		self.register['lo'] = int(product[32:],2)
		self.register['hi'] = int(product[:32],2)

	def _mflo(self, dest, return_hex=False):
		if return_hex: 
			return int('{:016b}{:05b}{:011b}'.format(
				0,
				self.register.encode(dest),
				18
				), 2)

		self.register[dest] = self.register['lo']

	def _mul(self, source, target, dest):
		self._mult(source, target)
		self.mflo(self, dest)

	def _mfhi(self, dest, return_hex=False):
		if return_hex: 
			return int('{:016b}{:05b}{:011b}'.format(
				0,
				self.register.encode(dest),
				16
				), 2)

		self.register[dest] = self.register['hi']

	# Shift instructions
	def _sll(self, dest, source, shift, return_hex=False):
		if return_hex:
			return int('{:011b}{:05b}{:05b}{:06b}'.format(
				0,
				self.register.encode(source),
				self.register.encode(dest),
				shift,
				0
				), 2)

		self.register[dest] = self.register[source] << shift

	def _srl(self, dest, source, shift, return_hex=False):
		if return_hex:
			return int('{:011b}{:05b}{:05b}{:06b}'.format(
				0,
				self.register.encode(source),
				self.register.encode(dest),
				shift,
				2
				), 2)

		self.register[dest] = self.register[source] >> shift

	# Load instructions
	def _li(self, dest, imm, return_hex=False):
		if return_hex:
			return 0

		self.register[dest] = int(unescape(imm))

	# Misc instructions
	def _move(self, dest, source, return_hex=False):
		if return_hex:
			return 0

		self.register[dest] = self.register[source]

	def _syscall(self, return_hex=False):
		if return_hex:
			return int('{:32b}'.format(12), 2)

		service_number = int(self.register['$v0'])

		output = service_map[service_number](self.register)
		if output != None:
			if hasattr(self, 'gui'):
				self.gui.print(output)
			else:
				print(output, end='')

	# Logical operators
	def _and(self, dest, source, target, return_hex=False):
		if return_hex:
			return int('{:06b}{:05b}{:05b}{:05b}{:11b}'.format(
				0,
				self.register.encode(source),
				self.register.encode(target),
				self.register.encode(dest),
				36
				), 2)

		self.register[dest] = self.register[source] & self.register[target]


	def _or(self, dest, source, target, return_hex=False):
		if return_hex:
			return int('{:06b}{:05b}{:05b}{:05b}{:11b}'.format(
				0,
				self.register.encode(source),
				self.register.encode(target),
				self.register.encode(dest),
				37
				), 2)

		self.register[dest] = self.register[source] | self.register[target]


	def _xor(self, dest, source, target, return_hex=False):
		if return_hex:
			return int('{:06b}{:05b}{:05b}{:05b}{:11b}'.format(
				0,
				self.register.encode(source),
				self.register.encode(target),
				self.register.encode(dest),
				38
				), 2)

		self.register[dest] = self.register[source] ^ self.register[target]


	def _nor(self, dest, source, target, return_hex=False):
		if return_hex:
			return int('{:06b}{:05b}{:05b}{:05b}{:11b}'.format(
				0,
				self.register.encode(source),
				self.register.encode(target),
				self.register.encode(dest),
				39
				), 2)

		self.register[dest] = ~ (self.register[source] | self.register[target])


	# Branches
	def branch(self, offset):
		self.register['pc'] += (offset) * 4

	def _beq(self, source, target, offset, return_hex=False):
		if return_hex:
			return int('{:06b}{:05b}{:05b}{:016b}'.format(
				4,
				self.register.encode(source),
				self.register.encode(target),
				int(twos_comp(offset)[-4::],16)
				), 2)

		if self.register[source] == self.register[target]:
			self.branch(offset)
		
	def _bne(self, source, target, offset, return_hex=False):
		if return_hex:
			return int('{:06b}{:05b}{:05b}{:016b}'.format(
				5,
				self.register.encode(source),
				self.register.encode(target),
				int(twos_comp(offset)[-4::],16)
				), 2)

		if self.register[source] != self.register[target]:
			self.branch(offset)

	def _bgez(self, source, offset, return_hex=False):
		if return_hex:
			return int('{:06b}{:05b}{:05b}{:016b}'.format(
				1,
				self.register.encode(source),
				1,
				int(twos_comp(offset)[-4::],16)
				), 2)

		if self.register[source] >= 0:
			self.branch(offset)
		
	def _bgtz(self, source, offset, return_hex=False):
		if return_hex:
			return int('{:06b}{:05b}{:05b}{:016b}'.format(
				7,
				self.register.encode(source),
				0,
				int(twos_comp(offset)[-4::],16)
				), 2)

		if self.register[source] > 0:
			self.branch(offset)
		
	def _blez(self, source, offset, return_hex=False):
		if return_hex:
			return int('{:06b}{:05b}{:05b}{:016b}'.format(
				6,
				self.register.encode(source),
				0,
				int(twos_comp(offset)[-4::],16)
				), 2)

		if self.register[source] <= 0:
			self.branch(offset)
		
	def _bltz(self, source, offset, return_hex=False):
		if return_hex:
			return int('{:06b}{:05b}{:05b}{:016b}'.format(
				1,
				self.register.encode(source),
				0,
				int(twos_comp(offset)[-4::],16)
				), 2)

		if self.register[source] < 0:
			self.branch(offset)
		
	def _bgezal(self, source, offset, return_hex=False):
		if return_hex:
			return int('{:06b}{:05b}{:05b}{:016b}'.format(
				1,
				self.register.encode(source),
				17,
				int(twos_comp(offset)[-4::],16)
				), 2)

		self.register['$ra'] = self.register['pc']

		self.bgez(source, offset)

	def _bltzal(self, source, offset, return_hex=False):
		if return_hex:
			return int('{:06b}{:05b}{:05b}{:016b}'.format(
				1,
				self.register.encode(source),
				16,
				int(twos_comp(offset)[-4::],16)
				), 2)

		self.register['$ra'] = self.register['pc']
		self.blez(source, offset)

	# Jump
	def _j(self, target, return_hex=False):
		if return_hex:
			return int('{:06b}{:026b}'.format(
				2, target
				), 2)
		self.register['pc'] = target - 4


	def _jal(self, target, return_hex=False):
		if return_hex:
			return int('{:06b}{:026b}'.format(
				3, target
				), 2)

		self.register['$ra'] = self.register['pc']

		self._j(target)

	def _jr(self, source, return_hex=False):
		if return_hex:
			return 0

		self.register['pc'] = self.register[source]


	def _sw(self, target, source, return_hex=False):
		word_offset, source = re.match(r'(\d+)\((\$\w+)\)', source).groups()
		if return_hex:
			return int('{:06b}{:05b}{:05b}{:016b}'.format(
				43,
				self.register.encode(source),
				self.register.encode(target),
				int(word_offset)
				), 2)

		# Offset is word offset, so we need to multiply by 4 to get actual mem address
		loc = self.register[source] + int(word_offset)
		self.memory[loc] = self.register[target]


	def _lw(self, target, source, return_hex=False):
		word_offset, source = re.match(r'(\d+)\((\$\w+)\)', source).groups()
		if return_hex:
			return int('{:06b}{:05b}{:05b}{:016b}'.format(
				35,
				self.register.encode(source),
				self.register.encode(target),
				int(word_offset)
				), 2)

		# Offset is word offset, so we need to multiply by 4 to get actual mem address
		loc = self.register[source] + int(word_offset)
		self.register[target] = self.memory[loc]


	def _nop(self, return_hex=False):
		if return_hex:
			return '{032b}'.format(0)
		pass
		
	# Assembler Directives
	
	def _ascii(self, string):
		# print(string)
		pass
	
	def _asciiz(self, string):
		
		self.register['$sp']
		self._ascii(string + "\0")

	def _globl(self, target, return_hex=False):
		pass

	def _data(self):
		pass

	def _text(self):
		pass


	# Overloads self[key] to allow easy access to MIPS functions
	def __getitem__(self, key):
		try:
			# All functions are appended with an underscore to avoid
			# issues with overwriting python functions (e.g. or)
			return getattr(self, '_' + key)	
		except:
			raise Exception('{} function not implemented'.format(key))
