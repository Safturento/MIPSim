import sys

def print_int(register):
	return register['$a0']

def print_float(register):
	pass

def print_double(register):
	pass

def print_string(register):
	pass

def print_char(register):
	return chr(register['$a0'])

def read_int(register):
	pass

def read_float(register):
	pass

def read_string(register):
	pass

def exit(register):
	return '\n--- Execution finished. ---'
	# sys.exit()

service_map = {
	1: print_int,
	2: print_float,
	10: exit,
	11: print_char,
}