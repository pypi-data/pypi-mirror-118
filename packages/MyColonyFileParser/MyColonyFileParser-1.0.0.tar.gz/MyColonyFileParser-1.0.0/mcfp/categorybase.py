class CategoryBase():
	def __init__(self, file, name) -> None:
		self.file = file
		self.name = name
	
	def __eq__(self, o: object) -> bool:
		if isinstance(o, str):
			return o == self.name
		if isinstance(o, CategoryBase):
			return o == self
		return False
	
	def __getitem__(self, target):
		raise NotImplementedError("subclasses of CategoryBase must provide a __getitem__() method")
	
	def __iter__(self):
		raise NotImplementedError("subclasses of CategoryBase must provide a __iter__() method")
	
	def __repr__(self) -> str:
		return f"<File: '{self.file}', Name: '{self.name}'>"
	
	def units(self):
		raise NotImplementedError("subclasses of CategoryBase must provide a units() method")
