class POS_words:
	def __init__(self, pronoun, verb, noun, adjective):
		self.pronoun = pronoun
		self.verb = verb
		self.noun = noun
		self.adjective = adjective

	def __str__(self):
		return "(%s, %s, %s, %s)"%(self.pronoun, self.verb, self.noun, self.adjective)


class MemoryInfo:
	def __init__(self, refered_to, list_of_info):
		self.refered_to = refered_to
		self.pos_words = list_of_info

	def __str__(self):
		#return "%s, "%(self.refered_to)+self.pos_words
		return "%s, "%(self.refered_to)+"(%s, %s, %s, %s)"%(self.pos_words.pronoun, self.pos_words.verb,
			self.pos_words.noun, self.pos_words.adjective)
		# return (self.refered_to, self.pos_words)

class Memory:
	def __init__(self):
		self.memory_history = []

	def add_new_memory(self, memory):
		self.memory_history.append(memory)

	def show_all_memories(self):
		for memory in self.memory_history:
			print(memory)