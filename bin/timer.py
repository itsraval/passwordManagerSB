import threading
import time
import os

class logOutTimer():
	def reset(self):
		self.start = time.time()

	def run(self):
		threading.Timer(5.0, self.run).start()
		now = time.time()
		if int(now - self.start) > self.t:
			os._exit(1)

	def __init__(self, t):
		self.start = time.time()
		self.t = t
		self.run()