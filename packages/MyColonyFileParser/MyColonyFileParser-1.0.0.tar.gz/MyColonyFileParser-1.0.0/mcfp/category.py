from typing import Generator, Union
from .base import DictBase, ListBase
from .categorybase import CategoryBase
from .exceptions import InvalidUnitName
from .unit import DictUnit, ListUnit

type_to_unit = {
	dict: DictUnit,
	list: ListUnit
}

class DictCategory(DictBase, CategoryBase):
	def __init__(self, file, name: str, data: dict) -> None:
		if type(data) is not dict:
			raise TypeError("DictCategory data must be dictionary, "
							f"not {data.__class__.__name__}")
		
		self.dict = data
		super().__init__(file, name)
	
	def __getitem__(self, name) -> Union[DictUnit, ListUnit]:
		try:
			unit_data = self.dict[name]
			unit_data_type = type(unit_data)
			
			if unit_data_type in type_to_unit:
				return type_to_unit[unit_data_type](self.file, self, unit_data, name)
			return unit_data
		except KeyError:
			raise InvalidUnitName(name)
	
	def __iter__(self):
		for key in self.dict:
			yield self[key]
	
	def units(self) -> Generator[str, None, None]:
		for key in self.dict:
			yield key

class ListCategory(ListBase, CategoryBase):
	def __init__(self, file, name, data) -> None:
		if type(data) is not list:
			raise TypeError("ListCategory data must be list, "
							f"not {data.__class__.__name__}")
		
		self.list = data
		super().__init__(file, name)
	
	def __add__(self, o: object):
		if isinstance(o, list):
			data = self.list.__add__(o)
		if isinstance(o, ListBase):
			data = self.list.__add__(o.list)
		
		try:
			return ListCategory(self.file, self.name, data)
		except NameError:
			raise TypeError(f"unsupported operand type(s) for +: 'ListCategory' and '{o.__class__.__name__}'")
	
	def __iadd__(self, o: object):
		if isinstance(o, list):
			self.list.__iadd__(o)
			return self
		if isinstance(o, ListBase):
			self.list.__iadd__(o.list)
			return self
		raise TypeError(f"unsupported operand type(s) for +: 'ListCategory' and '{o.__class__.__name__}'")
	
	def __mul__(self, o: object):
		try:
			return ListCategory(self.file, self.name, self.list.__mul__(o))
		except TypeError:
			raise TypeError(f"can't multiply sequence by non-int of type '{o.__class__.__name__}'")
	
	def __imul__(self, o: object):
		try:
			self.list.__imul__(o)
			return self
		except TypeError:
			raise TypeError(f"can't multiply sequence by non-int of type '{o.__class__.__name__}'")
	
	def __getitem__(self, target) -> Union[DictUnit, ListUnit]:
		if isinstance(target, int):
			try:
				unit_data = self.list[target]
				unit_data_type = type(unit_data)
				
				try:
					return type_to_unit[unit_data_type](self.file, self, unit_data)
				except KeyError:
					return unit_data
			except IndexError:
				raise IndexError("category index out of range")
		if isinstance(target, slice):
			return self.list[target.start:target.stop:target.step]
		raise TypeError("category indices must be integers or slices, "
						f"not {target.__class__.__name__}")
	
	def __iter__(self):
		for i in range(len(self.list)):
			yield self[i]
	
	def units(self) -> Generator[Union[dict, list], None, None]:
		for item in self.list:
			yield item
