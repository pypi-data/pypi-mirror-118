class UnitBase():
	def __init__(self, file, category, data) -> None:
		self.file = file
		self.category = category
		self.data = data
	
	def __str__(self) -> str:
		return self.name if hasattr(self, "name") else str(self.data)
	
	def __repr__(self) -> str:
		raise NotImplementedError("subclasses of UnitBase must provide a __repr__() method")
