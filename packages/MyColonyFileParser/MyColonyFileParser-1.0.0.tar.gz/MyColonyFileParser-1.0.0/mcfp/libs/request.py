from hashlib import md5
from html.parser import HTMLParser
from pathlib import Path

from requests import Timeout, URLRequired, codes, get

from ..config import config
from ..exceptions import CacheTimeout, InvalidFileChannel, InvalidFileName
from .cache import FileCache, MemCache, get_mem_cache, update_mem_cache

cache_folder_path = Path(__file__).parent.parent / "cache" / "page"
urls = {
	"channel_version": "https://coloniae.space/static/json/mycolony_version.json",
	"game_version": "https://www.apewebapps.com/apps/my-colony/",
	"game": "https://www.apewebapps.com/apps/my-colony/{version}/game.js",
	"strings": "https://www.apewebapps.com/apps/my-colony/{version}/strings.js"
}
mem_cache = {}

def hash_md5(value: str):
	m = md5()
	m.update(value.encode("UTF-8"))
	return m.hexdigest()

def get_page(url: str):
	timeout = config["network"].getfloat("timeout")
	
	while True:
		try:
			page = get(url, timeout = timeout)
			
			if page.status_code == codes.ok:
				return page
		except Timeout:
			timeout += 1
			print(f"[mcp.libs.request.get_page]Request timeout! Increase timeout to {timeout}")
		except URLRequired:
			raise URLRequired(f"Invalid URL: {url}")

def get_channel_version(channel) -> str:
	channel_to_key = {
		'latest': 'mycolony_version',
		'stable': 'mycolony_stable_version'
	}
	
	try:
		channel_key = channel_to_key[channel]
		channel_version_page_url = urls["channel_version"]
		
		# Data has been added to mem_cache
		try:
			return get_mem_cache(mem_cache, channel_version_page_url).data[channel_key]
		# Data is not in mem_cache
		except KeyError:
			# Create FileCache to get data
			file_cache = FileCache(cache_folder_path, hash_md5(channel_version_page_url))
			
			# Cache file is created
			try:
				version_data: dict = file_cache.json()
				mem_cache[channel_version_page_url] = MemCache(version_data)
			# Cache file is not created
			except FileNotFoundError:
				version_data: dict = get_page(channel_version_page_url).json()
				file_cache.create(version_data)
				mem_cache[channel_version_page_url] = MemCache(version_data)
			# Cache file is created but timeout
			except CacheTimeout:
				version_data: dict = get_page(channel_version_page_url).json()
				file_cache.update(version_data)
				mem_cache[channel_version_page_url] = update_mem_cache(mem_cache, channel_version_page_url, version_data)
			
			return version_data[channel_key]
		# Data has been added to mem_cache but timeout
		except CacheTimeout:
			version_data: dict = get_page(channel_version_page_url).json()
			mem_cache[channel_version_page_url] = update_mem_cache(mem_cache, channel_version_page_url, version_data)
			
			return version_data[channel_key]
	except KeyError:
		raise InvalidFileChannel(channel)

def get_valid_version() -> set[str]:
	game_version_page_url = urls["game_version"]
	
	class Parser(HTMLParser):
		def __init__(self) -> None:
			super().__init__()
			self.version = set()
		
		def handle_starttag(self, tag: str, attrs) -> None:
			if tag == "a":
				for name, value in attrs:
					value: str
					if name == "href" and not value.startswith("/") and value.endswith("/"):
						self.version.add(value[:-1]) # [:-1] -> remove suffix "/"
	
	def parse_valid_version(game_version_page_url):
		parser = Parser()
		parser.feed(get_page(game_version_page_url).text)
		return parser.version
	
	# Data has been added to mem_cache
	try:
		return get_mem_cache(mem_cache, game_version_page_url).data
	# Data is not in mem_cache
	except KeyError:
		# Create FileCache to get data
		file_cache = FileCache(cache_folder_path, hash_md5(game_version_page_url))
		
		# Cache file is created
		try:
			valid_version = file_cache.json()
		# Cache file is not created
		except FileNotFoundError:
			valid_version = parse_valid_version(game_version_page_url)
			file_cache.create(valid_version)
			mem_cache[game_version_page_url] = MemCache(valid_version)
		# Cache file is created but timeout
		except CacheTimeout:
			valid_version = parse_valid_version(game_version_page_url)
			file_cache.update(valid_version)
			mem_cache[game_version_page_url] = update_mem_cache(mem_cache, game_version_page_url, valid_version)
		
		return valid_version
	# Data has been added to mem_cache but timeout
	except CacheTimeout:
		valid_version = parse_valid_version(game_version_page_url)
		mem_cache[game_version_page_url] = update_mem_cache(mem_cache, game_version_page_url, valid_version)
		
		return valid_version

def get_source(version, file) -> str:
	def get_source_data(source_page_url):
		page = get_page(source_page_url)
		page.encoding = "utf-8"
		return page.text
	
	try:
		source_page_url = urls[file].format(version=version)
		
		# Data has been added to mem_cache
		try:
			return get_mem_cache(mem_cache, source_page_url).data
		# Data is not in mem_cache
		except KeyError:
			file_cache = FileCache(cache_folder_path, hash_md5(source_page_url))
			timeout = None
			
			try:
				source_data = file_cache.get()
			except FileNotFoundError:
				source_data = get_source_data(source_page_url)
				file_cache.create(source_data, timeout)
				mem_cache[source_page_url] = MemCache(source_data, timeout)
			except CacheTimeout:
				source_data = get_source_data(source_page_url)
				file_cache.update(source_data, timeout)
				mem_cache[source_page_url] = update_mem_cache(mem_cache, source_page_url, source_data, timeout)
			
			return source_data
		except CacheTimeout:
			# Usually this does not happen
			# But it can prevent manual modification
			source_data: str = get_mem_cache(mem_cache, source_page_url).data
			mem_cache[source_page_url] = update_mem_cache(mem_cache, source_page_url, source_data, None)
			return source_data
	except KeyError:
		raise InvalidFileName(file)
	