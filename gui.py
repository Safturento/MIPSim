from tkinter import *
from tkinter.ttk import *
import tkinter.font as tkFont
from threading import Thread
import threading

from register import REGISTER_NICKS

class Gui():
	def __init__(self, registers, memory):
		self.root = Tk()
		self.root.geometry("660x864")
		self.registers = registers
		self.memory = memory
		self.root.title("Registers")

		default_font = tkFont.nametofont("TkDefaultFont")
		default_font.configure(family="Courier New", size=10)
		self.root.option_add('*Font', default_font)

		self.win = Frame(self.root)

		self.init_register_section()
		self.init_text_segment()
		self.init_stack_segment()
		self.init_output_window()

		self.win.pack(fill="both", expand=True)

	def set_loop(self, loop_func, step):
		# if step:
		self.root.bind('<Return>', loop_func)
		# else:
		# 	while True:
		# 		loop_func(self)

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

		tv.pack(side="left", fill="y")
		self.register_display = tv

	def init_text_segment(self):
		# self.prev_pc_value = self.memory['pc']

		tv = Treeview(self.win)
		tv['columns'] = ('address', 'code', 'instruction')
		tv['show'] = 'headings'

		tv.heading('address', text='Address')
		tv.column('address', anchor='w', width=80, stretch=False)
		
		tv.heading('code', text='Code')
		tv.column('code', anchor='w', width=80, stretch=False)
		
		tv.heading('instruction', text='Instruction')
		tv.column('instruction', anchor='w', stretch=True)
		

		for line_num in self.memory.text_memory:
			tv.insert('', 'end', line_num, values=(
				'{:08x}'.format(line_num),
				'{:08x}'.format(self.memory[line_num]['code']),
				self.memory[line_num]['line']
			))

		# avoid crashing on empty program
		if len(self.memory.text_memory) > 0:
			tv.selection_set(self.registers['pc'])

		tv.pack(side="left", fill="both", expand=True)
		self.text_segment = tv

	def init_stack_segment(self):
		tv = Treeview(self.win)
		tv['columns'] = ('address', 'value')
		tv['show'] = 'headings'

		tv.heading('address', text='Address')
		tv.column('address', anchor='w', width=80)
		
		tv.heading('value', text='Value')
		tv.column('value', anchor='w', width=80)
		
		limit = 128
		for addr in range(self.registers['$sp'], self.registers['$sp'] + limit*4, 4):
			value = 0
			if addr in self.memory:
				value=self.memory[addr]
			tv.insert('', 'end', addr, values=('{:08x}'.format(addr), '{:08x}'.format(value)))

		tv.pack(side="right", fill="y")
		self.stack_segment = tv

	def init_output_window(self):
		out = Text(self.root, height=8)
		out['state'] = 'disabled'
		out.pack(side='bottom', fill='both')
		self.output_window = out

	def update(self):
		self.update_register_section()
		self.update_text_segment()
		self.update_stack_segment()

	def update_register_section(self):
		changed = []
		for reg_num, reg_val in self.registers:
			# We have both of these values differently to match them because tk
			# automatically casts to int if it can..
			if int(str(self.register_display.item(reg_num)['values'][1]),16) != reg_val:
				changed.append(reg_num)
			self.register_display.item(reg_num ,values=(self.registers.get_nick(reg_num), '{:08x}'.format(reg_val)))
		self.register_display.selection_set(changed)

	def update_stack_segment(self):
		changed = []
		# to keep things simple we'll just print the next 128 bytes like MARS does
		limit = 128
		for addr in range(self.registers['$sp'], self.registers['$sp'] + limit*4, 4):
			value = 0
			if addr in self.memory:
				value=self.memory[addr]

			if int(str(self.stack_segment.item(addr)['values'][1]),16) != value:
				changed.append(addr)

			self.stack_segment.item(addr, values=('{:08x}'.format(addr), '{:08x}'.format(value)))
		self.stack_segment.selection_set(changed)

	def update_text_segment(self):
		if self.text_segment.exists(self.registers['pc']):
			self.text_segment.selection_set(self.registers['pc'])

	def print(self, output):
		self.output_window['state'] = 'normal'
		self.output_window.insert('end', output)
		self.output_window['state'] = 'disabled'
