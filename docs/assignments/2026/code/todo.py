"""

Simple (and simplistic) implementation of a TODO list.

"""

from datetime import date
from pathlib import Path


class TodoList:

	"""Class that stores the items and actis as an interface to the items stored
	on disk."""

	# This variable stores the current number of items in the list. It's used when
	# generating the identifier of a new Item.
	count = 0

	@classmethod
	def new_id(cls):
		cls.count += 1
		return cls.count

	def __init__(self):
		self.db = 'todo.csv'
		self.items = []
		Path(self.db).touch()

	def __len__(self):
		return len(self.items)

	def __getitem__(self, i):
		return self.items[i]

	def __str__(self):
		return f'<TodoList with {TodoList.count} items>'

	def add(self, note: str, priority: int = 0, due: str = None):
		"""Add an item by handing in the description, the priority and the due
		date. Note that no identifier is needed here. Also, this only changes the
		in-memory items list.""" 
		item = TodoItem(note=note, priority=priority, due=due)
		self.items.append(item)
		return item

	def load(self):
		"""Empty the current list of items and load items from disk."""
		self.items = []
		with open(self.db) as fh:
			for line in fh:
				identifier, priority, done, created, due, note = line.strip().split('\t')
				item = TodoItem(identifier, note, priority, created, due, done)
				self.items.append(item)
		TodoList.count = len(self)

	def search(self, term: str):
		return [item.as_json() for item in self if item.matches(term)]

	def save(self):
		"""Save the items, overwriting what was on the disk previously."""
		with open(self.db, 'w') as fh:
			for item in self:
				fh.write(item.as_csv())

	def clear(self):
		self.items = []
		TodoList.count = 0

	def pp(self):
		print(self)
		for item in self:
			item.pp()


class TodoItem:

	def __init__(self, identifier: int = None, note: str = '', priority: int = 0,
				 created: str = None, due: str = None, done: bool = False):
		today = date.today()
		if identifier is None:
			identifier = TodoList.new_id()
		if due is None:
			due = date(today.year + 1, today.month, today.day)
		self.identifier = identifier
		self.priority = priority
		self.done = done
		self.created = today
		self.due = due
		self.note = note

	def __str__(self):
		return f'<TodoItem id={self.identifier} note="{self.note}">'

	def update(self, field: str, value):
		"""Update the item, does not change the item saved on disk."""
		setatr(self, field, value)

	def matches(self, term: str):
		return term in self.note

	def as_csv(self):
		return f'{self.identifier}\t{self.priority}' + \
			   f'\t{self.done}\t{self.created}\t{self.due}\t{self.note}\n'

	def as_json(self):
		return {
			'identifier': self.identifier,
			'priority': self.priority,
			'done': self.done,
			'created': self.created,
			'due': self.due,
			'note': self.note }

	def pp(self):
		print(f'<id={self.identifier:} priority={self.priority}' + \
			  f' done={self.done} created={self.created} due={self.due}' + \
			  f' note="{self.note}">')


if __name__ == '__main__':

	todo_list = TodoList()
	#todo_list.load()
	todo_list.add('do something', due='2026-10-12')
	todo_list.add('do something else', priority=3, due='2026-10-12')
	todo_list.add('and yet something else', priority=1)
	todo_list.save()
	todo_list.pp()
