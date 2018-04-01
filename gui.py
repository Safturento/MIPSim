from tkinter import *
from tkinter.ttk import *
from threading import Thread
import threading

from register import REGISTER_NICKS

class Gui():
	def __init__(self, registers, memory):
		self.root = Tk()
		self.root.geometry("500x850")
		self.registers = registers
		self.memory = memory
		self.root.title("Registers")

		self.win = Frame(self.root)

		self.init_register_section()
		self.init_text_segment()
		self.init_output_window()

		self.win.pack(fill="both", expand=True)

	def set_loop(self, loop_func):
		self.root.bind('<Return>', loop_func)

	def init_register_section(self):		
		# self.register_section = {}
		
		tv = Treeview(self.win)
		tv['columns'] = ('register', 'value')
		tv['show'] = 'headings'

		tv.heading('register', text='Reg')
		tv.column('register', anchor='e', width=50)
		
		tv.heading('value', text='Value')
		tv.column('value', anchor='w', width=80)
		
		for reg_num, reg_val in self.registers:
			tv.insert('', 'end', reg_num, values=(self.registers.get_nick(reg_num), '{:08x}'.format(reg_val)))

		tv.pack(side="left", fill="y", expand=True)
		self.register_display = tv

	def init_text_segment(self):
		# self.prev_pc_value = self.memory['pc']

		tv = Treeview(self.win)
		tv['columns'] = ('address', 'code', 'instruction')
		tv['show'] = 'headings'

		tv.heading('address', text='Address')
		tv.column('address', anchor='w', width=80)
		
		tv.heading('code', text='Code')
		tv.column('code', anchor='w', width=100)
		
		tv.heading('instruction', text='Instruction')
		tv.column('instruction', anchor='w', stretch=True)
		

		for line_num in self.memory.text_memory:
			tv.insert('', 'end', line_num, values=('{:08x}'.format(line_num), '', self.memory[line_num]['line']))

		tv.selection_set(self.registers['pc'])

		tv.pack(side="left", fill="both", expand=True)
		self.text_segment = tv

	def init_output_window(self):
		out = Text(self.root, height=8)
		out['state'] = 'disabled'
		out.pack(side='bottom', fill='y')
		self.output_window = out

	def update(self):
		self.update_register_section()
		self.update_text_segment()

	def update_register_section(self):
		changed = []
		for reg_num, reg_val in self.registers:
			# We have both of these values differently to match them because tk
			# automatically casts to int if it can..
			if str(self.register_display.item(reg_num)['values'][1]) != '{:x}'.format(reg_val):
				changed.append(reg_num)
			self.register_display.item(reg_num ,values=(self.registers.get_nick(reg_num), '{:08x}'.format(reg_val)))

		self.register_display.selection_set(changed)

	def update_text_segment(self):
		self.text_segment.selection_set(self.registers['pc'])

	def print(self, output):
		self.output_window['state'] = 'normal'
		self.output_window.insert('end', output)
		self.output_window['state'] = 'disabled'
