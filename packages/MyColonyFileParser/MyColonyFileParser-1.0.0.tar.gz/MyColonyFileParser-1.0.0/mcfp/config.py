from pathlib import Path
from configparser import ConfigParser

config_file_path = Path(__file__).parent / "config.ini"
config = ConfigParser()
config.read(config_file_path)
