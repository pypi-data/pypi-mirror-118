from .base import DictBase, ListBase
from .unitbase import UnitBase


class DictUnit(DictBase, UnitBase):
	def __init__(self, file, category, data, name=None) -> None:
		self.dict = data
		
		if name:
			self.name = name
		elif "name" in data:
			self.name = data["name"]
		elif "title" in data:
			self.name = data["title"]
		else:
			self.name = None
			
		super().__init__(file, category, data)
	
	def __getitem__(self, key):
		try:
			return self.dict[key]
		except KeyError:
			raise KeyError(key)
	
	def __repr__(self) -> str:
		return f"<File: '{self.file}', Category: '{self.category}', Name: '{self.name}'>"

class ListUnit(ListBase, UnitBase):
	def __init__(self, file, category, data) -> None:
		self.list = data
		super().__init__(file, category, data)
	
	def __getitem__(self, target):
		if isinstance(target, int):
			try:
				return self.list[target]
			except IndexError:
				raise IndexError("list index out of range")
		if isinstance(target, slice):
			return self.list[target.start:target.stop:target.step]
		raise TypeError("list indices must be integers or slices, "
						f"not {target.__class__.__name__}")
	
	def __str__(self):
		return str(self.list)
	
	def __repr__(self) -> str:
		return f"<File: '{self.file}', Category: '{self.category}'>"
