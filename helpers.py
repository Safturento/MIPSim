
def twos_comp(x):
	if x < 0:
		x = x & (2**32-1) 
	return '{:08x}'.format(x)

def unescape(imm):
	if type(imm) is str:
		# I haven't found a better way to do this,
		# re-escaping keys is a weird problem..
		imm = imm.replace('\\"', '\'')
		imm = imm.replace("\\'", '\"')
		imm = imm.replace('\\a', '\a')
		imm = imm.replace('\\b', '\b')
		imm = imm.replace('\\f', '\f')
		imm = imm.replace('\\n', '\n')
		imm = imm.replace('\\r', '\r')
		imm = imm.replace('\\t', '\t')
		imm = imm.replace('\\v', '\v')

		return ord(imm)
	return imm