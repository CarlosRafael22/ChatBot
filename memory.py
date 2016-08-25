class MemoryInfo:
	def __init__(self, refered_to, list_of_info):
		self.refered_to = refered_to
		self.list_of_info = list_of_info

class Memory:
	def __init__(self):
		self.memory_history = []

	def add_new_memory(self, memory):
		self.memory_history.append(memory)

	def show_all_memories(self):
		for memory in self.memory_history:
			print(memory)