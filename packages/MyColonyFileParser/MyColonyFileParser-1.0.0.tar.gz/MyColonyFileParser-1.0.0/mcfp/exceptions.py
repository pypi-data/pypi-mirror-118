class MCFPError(Exception):
	def __init__(self) -> None:
		"""
		Base exception of mcfp
		"""
		pass

class FileError(MCFPError):
	def __init__(self) -> None:
		"""
		File related error
		"""
		pass

class InvalidFileChannel(FileError):
	def __init__(self, channel):
		"""
		Invalid file channel: `channel`
		"""
		self.channel = channel
	
	def __str__(self) -> str:
		return f"Invalid file channel: {self.channel}"

class InvalidFileVersion(FileError):
	def __init__(self, version) -> None:
		"""
		Invalid file version: `version`
		"""
		self.version = version
	
	def __str__(self) -> str:
		return f"Invalid file version: {self.version}"

class InvalidFileName(FileError):
	def __init__(self, name) -> None:
		"""
		Invalid file name: `file`
		"""
		self.name = name
		
	def __str__(self) -> str:
		return f"Invalid file name: {self.name}"

class CategoryError(MCFPError):
	def __init__(self) -> None:
		"""
		Category related error
		"""
		pass

class InvalidCategoryName(CategoryError):
	def __init__(self, name) -> None:
		"""
		Invalid category name: `name`
		"""
		self.name = name
	
	def __str__(self) -> str:
		return f"Invalid category name: {self.name}"

class UnitError(MCFPError):
	def __init__(self) -> None:
		"""
		Unit related error
		"""
		pass

class InvalidUnitName(UnitError):
	def __init__(self, name) -> None:
		"""
		Invalid unit name: `name`
		"""
		self.name = name
	
	def __str__(self) -> str:
		return f"Invalid unit name: {self.name}"

class CacheError(MCFPError):
	def __init__(self) -> None:
		"""
		Class Cache related error
		"""
		pass

class InvalidTimeout(CacheError):
	def __init__(self, timeout) -> None:
		"""
		Invalid timeout: `timeout`, did someone change it?
		"""
		self.timeout = timeout
	
	def __str__(self) -> str:
		return f"Invalid timeout: {self.timeout}, did someone change it?"

class CacheTimeout(CacheError):
	def __init__(self) -> None:
		"""
		This cache is timeout, please update or delete it
		"""
		pass
	
	def __str__(self) -> str:
		return "This cache is timeout, please update or delete it"
