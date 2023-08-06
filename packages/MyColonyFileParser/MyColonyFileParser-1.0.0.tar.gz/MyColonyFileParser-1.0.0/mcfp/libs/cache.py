from io import TextIOWrapper
from json import JSONDecodeError, dumps, loads
from pathlib import Path
from time import time
from typing import Union

from ..exceptions import CacheTimeout, InvalidTimeout

__all__ = [
	"FileCache",
	"MemCache",
	"get_mem_cache",
	"update_mem_cache"
]

DEFAULT_TIMEOUT = 24 * 60 * 60 # 86400 seconds

# Objects in mem_cache should only be instances of FileCache
mem_cache = {}

def _data_parser(data: Union[str, list, tuple, set, dict]) -> str:
	if not isinstance(data, str):
		try:
			data = dumps(data, ensure_ascii=False)
		except TypeError:
			if isinstance(data, set):
				data = dumps(list(data))
			else:
				raise TypeError("the `data` must be `str`, `list`, `tuple`, `set` or `dict`, "
							f"not {data.__class__.__name__}")
	
	return data

def _timeout_parser(timeout: Union[int, None]):
	if timeout is None or type(timeout) is int:
		return int(time()) + timeout if timeout is not None else None
	raise TypeError("the `timeout` must be None or int, "
					f"not {timeout.__class__.__name__}")

class FileCache():
	def __init__(self, folder_path: Path, file_name: str) -> None:
		"""
		"""
		if not isinstance(folder_path, Path):
			raise TypeError("`folder_path` must be `Path` of pathlib, "
							f"not `{folder_path.__class__.__name__}`")
		
		if not isinstance(file_name, str):
			raise TypeError("`file_name` must be `str`, "
							f"not `{file_name.__class__.__name__}`")
		
		self._path = folder_path / file_name
		self._parent = folder_path
		self.timeout = None
		self.data = None
	
	def create(self, data: Union[str, list, tuple, set, dict], timeout: Union[int, None] = DEFAULT_TIMEOUT):
		"""Create file cache at path with gived data
		
		Parameter
		---------
		`timeout` (int):
			unit: second(s)
			default: 86400(1 day)
			
			How long can this cache be used, `None` for forever
		
		Raise
		-----
		TypeError:
			when `data` or `timeout` is not correct type
		"""
		# Do not create same cache twice
		if self._path in mem_cache or self.exists():
			return
		
		if not self._parent.exists():
			# parent may be multiple layer
			self._parent.mkdir(parents=True)
		
		# Convert `time()` to int to remove the decimal point and the digits after it
		# because length of digits is not fixed
		try:
			self.timeout = _timeout_parser(timeout)
			self.data = _data_parser(data)
		except TypeError as e:
			raise TypeError(e.args)
		
		with self._path.open("w", encoding="UTF-8") as f:
			# Add timeout to first line of cache file
			f.write(f"{self.timeout}\n{self.data}")
		
		# Add cache to mem_cache
		mem_cache[self._path] = MemCache(self.data, self.timeout)
	
	def get(self):
		"""Get cache data
		
		Raise
		-----
		FileNotFoundError:
			when cache is not created
		CacheTimeout:
			when cache is timeout
		"""
		# Do not open same cache file twice if it is not timeout
		try:
			return get_mem_cache(mem_cache, self._path).data
		except KeyError:
			pass
		except CacheTimeout:
			pass
		
		try:
			with self._path.open("r", encoding="UTF-8") as f:
				timeout = self._get_timeout(f)
				
				if not self._is_expired(timeout):
					f.readline() # skip the timeout and move to where the data at
					self.timeout = timeout
					self.data = f.read()
					mem_cache[self._path] = MemCache(self.data, timeout)
					return self.data
				raise CacheTimeout
		except FileNotFoundError:
			raise FileNotFoundError("You can only get cache data after created it")
	
	def update(self, data: Union[str, list, tuple, set, dict], timeout: Union[int, None] = DEFAULT_TIMEOUT):
		self.timeout = _timeout_parser(timeout)
		self.data = _data_parser(data)
		
		with self._path.open("w", encoding="utf-8") as f:
			f.write(f"{self.timeout}\n{self.data}")
		
		mem_cache[self._path] = update_mem_cache(mem_cache, self._path, self.data, self.timeout)
	
	def delete(self, *, force = False):
		try:
			self._path.unlink(missing_ok=force)
			return True
		except FileNotFoundError:
			return False
	
	def json(self):
		try:
			return loads(self.get())
		except JSONDecodeError:
			raise
		except CacheTimeout:
			raise
	
	def exists(self):
		return self._path.exists()
	
	def is_expired(self):
		try:
			timeout = self.timeout
		except AttributeError:
			with self._path.open("r", encoding="utf-8") as f:
				timeout = self._get_timeout(f)
		
		return self._is_expired(timeout)
	
	@staticmethod
	def _is_expired(timeout: Union[int, None]):
		if timeout is not None and timeout < time():
			return True
		return False
	
	def _get_timeout(self, f: TextIOWrapper):
		"""Get cache file's timeout
		"""
		# `f.readline()` will return a string end with '\n'
		# '\' will be ignore by python, so just remove 'n'
		timeout = self._timeout_converter(f.readline()[:-1])
		f.seek(0)
		return timeout
	
	@staticmethod
	def _timeout_converter(timeout: str) -> Union[int, None]:
		# `timeout` can only be None or int
		if timeout == "None":
			timeout = None
		else:
			try:
				timeout = int(timeout)
			except ValueError:
				raise InvalidTimeout(timeout)
		
		return timeout

class MemCache:
	def __init__(self, data, timeout: Union[int, None] = DEFAULT_TIMEOUT) -> None:
		self.timeout = _timeout_parser(timeout)
		self.data = data
	
	def get(self):
		if not self.is_expried():
			return self.data
		raise CacheTimeout
	
	def update(self, data, timeout: Union[int, None] = DEFAULT_TIMEOUT):
		self.timeout = _timeout_parser(timeout)
		self.data = data
	
	def is_expried(self):
		if self.timeout is not None and self.timeout < time():
			return True
		return False

def get_mem_cache(mem_cache_dict: dict[str, MemCache], key: str):
	"""Get MemCache with gived key
	
	Raise
	-----
	KeyError:
		when key not in `mem_cache_dict`
	CacheTimeout:
		when cache is timeout
	"""
	try:
		cache = mem_cache_dict[key]
		
		if not isinstance(cache, MemCache):
			raise TypeError("value in `mem_cache` must be `MemCache`, "
							f"not {cache.__class__.__name__}")
		
		if not cache.is_expried():
			return cache
	except KeyError:
		raise
	except CacheTimeout:
		raise

def update_mem_cache(mem_cache_dict: dict, key: str, data, timeout: Union[int, None] = DEFAULT_TIMEOUT):
	try:
		cache: MemCache = mem_cache_dict[key]
		cache.update(data, timeout)
	except KeyError:
		cache = MemCache(data, timeout)
	
	return cache
