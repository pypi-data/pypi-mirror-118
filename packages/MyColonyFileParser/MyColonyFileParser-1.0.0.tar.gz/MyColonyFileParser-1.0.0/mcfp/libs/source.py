from re import sub
from json import dumps, loads, JSONDecodeError

def format_source_data(data: str) -> dict:
	for i, s in enumerate(data):
		if s == "{":
			data = data[i:]
			
			try:
				return loads(data)
			except JSONDecodeError as err:
				err_msg = err.msg
				err_pos = err.pos
				err_pos_str = data[err_pos]
				
				# may be comment
				if err_msg == "Expecting property name enclosed in double quotes":
					if err_pos_str == "/":
						comment_type_identifier = data[err_pos + 1]
						
						if comment_type_identifier == "/":
							for j, t in enumerate(data[err_pos:]):
								if t == "\n":
									comment_end_pos = err_pos + j + 1
									return format_source_data(data.replace(data[err_pos:comment_end_pos], ""))
					return format_source_data(data[err_pos:])
				if err_msg == "Extra data":
					for j, t in enumerate(data[err_pos - 1::-1]):
						if t == "}":
							return format_source_data(data[:err_pos + j])
				if err_msg == "Expecting value":
					return format_source_data(sub(r': *\.', ': 0.', data))
					
				return format_source_data(data[err_pos:])

class Source():
	def __init__(self, data: str) -> None:
		self.dict = format_source_data(data)
		self.data = dumps(self.dict, ensure_ascii=False)
	