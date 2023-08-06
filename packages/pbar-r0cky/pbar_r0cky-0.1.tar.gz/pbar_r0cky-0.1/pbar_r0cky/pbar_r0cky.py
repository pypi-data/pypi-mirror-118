import threading
from os import system as sys
from os import name
from sys import stdout

class ProgressBar:
	def __init__(self, min: int = 0, max: int = 100) -> str:
		"""A simple progress bar for your software."""
		self.cur = min
		self.max = max+1
		self.clearc = "clear"
		self.Y = 90
		self.X = 5

		if name == "nt":
			self.clearc = "cls"
	
	def add(self, val: int):
		"""Adds progress"""
		self.cur += val

	def rem(self, val: int):
		"""Dunno, why'd you do that, but u can remove progress"""
		self.cur -= val

	def show(self):
		"""Shows a progress bar by starting a new thread"""
		thread = threading.Thread(target=self.draw)
		thread.start()

	def draw(self):
		"""Draws the progress bar"""
		stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (self.Y, self.X+self.max, "]"))
		stdout.flush()
		while True:
			if self.cur == self.max-1:
				sys(self.clearc)
				break
			stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (self.Y, self.X, "["+"#"*self.cur))
			stdout.flush()
		print("[DONE]")