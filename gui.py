# from tkinter import ttk
import tkinter as tk
from threading import Thread
import threading

class Gui(threading.Thread):
	def __init__(self, registers):
		self.root = tk.Tk()
		self.registers = registers
		self.root.title("Registers")

		self.init_register_labels()

		threading.Thread.__init__(self)
		self.start()
		

	def init_register_labels(self):		
		self.register_labels = {}
		for reg in self.registers:
			self.register_labels[reg[0]] = tk.Label(self.root, text='{}\t: {:032b}'.format(*reg))
			self.register_labels[reg[0]].pack()

	def update(self):
		self.update_register_labels()

	def update_register_labels(self):
		for reg in self.registers:
				self.register_labels[reg[0]]['text'] = '{}\t: {:032b}'.format(*reg)
				self.register_labels[reg[0]].pack()
