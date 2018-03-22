def print_int(register):
	print(int(register['$a0']))

def print_float(register):
	pass

def print_string(register):
	pass

def read_int(register):
	pass

def read_float(register):
	pass

def read_string(register):
	pass


service_map = {
	1: print_int,
	2: print_float
}