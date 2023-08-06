from json import loads
from pathlib import Path
from typing import Generator

from .base import DictBase
from .exceptions import InvalidFileChannel, InvalidFileVersion
from .libs.cache import FileCache
from .libs.request import get_channel_version, get_source, get_valid_version
from .libs.source import Source

file_channel = {
	"stable",
	"latest"
}

mem_cache = {}

class FileBase(DictBase):
	def __init__(self, file_name: str, channel="stable", cache: bool=True, *, version=None):
		"""
		File Base, provide __init__ and basic functions
		
		Please inherit this class and run super().__init__()
		DON'T use this class directly! It won't work
		"""
		self.name = file_name
		self.channel = channel
		self._create_cache = cache
		
		# setup version
		if not version and channel in file_channel:
			self.version = get_channel_version(channel)
		elif version and version in get_valid_version():
			self.version = version
		elif not version and channel not in file_channel:
			raise InvalidFileChannel(channel)
		else:
			raise InvalidFileVersion(version)
		
		# check mem_cache
		file_identify = file_name + self.version
		
		if file_identify in mem_cache:
			file_name: FileBase = mem_cache[file_identify]
			
			for attr in dir(file_name):
				if not hasattr(self, attr):
					setattr(self, attr, getattr(file_name, attr))
			
			return
		
		# prepare cache
		cache_folder_path = Path(__file__).parent/"cache"/"source"/self.version
		cache_file = FileCache(cache_folder_path, file_name)
		
		# setup dict
		try:
			raw_dict_data = cache_file.get()
		except FileNotFoundError:
			raw_dict_data = Source(get_source(self.version, file_name)).data
		
		self.dict: dict = loads(raw_dict_data)
		
		# create cache	
		if cache:
			cache_file.create(raw_dict_data, timeout=None)
		
		mem_cache[file_name + self.version] = self
	
	def __eq__(self, o: object) -> bool:
		if isinstance(o, str):
			return o == self.name
		if isinstance(o, FileBase):
			return o == self
		return False
	
	def __getitem__(self, name):
		"""
		Return DictCategory or ListCategory
		If name not in self.dict, raise InvalidCategory
		"""
		raise NotImplementedError("subclasses of FileBase must provide a __getitem__() method")
	
	def __str__(self):
		return self.name
	
	def __repr__(self) -> str:
		return f"<File: '{self.name}', Version: '{self.version}'>"
	
	def categories(self) -> Generator[str, None, None]:
		for key in self.dict:
			yield key
	
	def copy(self):
		# `self.__class__` is FileBase subclass, so don't need to pass in `self.name`
		# because __init__() of FileBase subclass must pass in its own name when run super().__init__
		return self.__class__(self.channel, self._create_cache, version=self.version)
	
	def update(self, file):
		if not issubclass(file, FileBase):
			raise TypeError("")
		
		self.channel = file.channel
		self.version = file.version
		self.dict.update(file.dict)
	
