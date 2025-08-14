import string

class SSI_Class:

	def __init__(self):
		self._empty = True
		self._title = None
		self._presenter_title = None
		self._presenters = None
		self._location = None
		self._description = None
		self._bios = []
		self._extra = []

	def is_empty(self):
		return self._empty
	
	def set_title(self, first_word, after_first):
		self._title = after_first
		self._empty = False

	def set_presenters(self, first_word, after_first):
		if first_word == 'Tour':
			self._presenter_title = "Tour Guide:"
			self._presenters = after_first.split(' ', 1)[1]
		else:
			self._presenter_title = first_word
			self._presenters = after_first
		self._empty = False

	def set_location(self, first_word, after_first):
		self._location = after_first
		self._empty = False

	def set_description(self, first_word, after_first):
		self._description = after_first.split(' ', 1)[1]
		self._empty = False

	def add_bio(self, first_word, after_first):
		self._bios.append(after_first)
		self._empty = False

	def add_extra(self, first_word, after_first):
		self._extra.append(after_first)
		self._empty = False

	def __str__(self):
		ret_str = ''
		if self._title is not None:
			ret_str += '<b>Title</b>: ' + self._title + '<br />\n'
		if self._presenter_title is not None:
			ret_str += '<b>' + self._presenter_title[:-1] + '</b>: ' + self._presenters + '<br />\n'
		if self._location is not None:
			ret_str += '<b>Location</b>: ' + self._location + '<br />\n'
		if self._description is not None:
			ret_str += '<b>Class Description</b>: ' + self._description + '<br />\n'
		if self._extra:
			ret_str += '<br />\n'
			if len(self._extra) == 1:
				colon = self._extra[0].find(':')
				if colon != -1:
					title = self._extra[0][0:colon]
					rest_of_line = self._extra[0][colon + 1:].strip()
					ret_str += '<b>' + title + '</b>: ' + rest_of_line
				else:
					ret_str += self._extra[0]
			else:
				for extra in self._extra:
					ret_str += extra
			ret_str += '<br />\n'
		if self._bios:
			if len(self._bios) == 1:
				ret_str += '<br /><b>Bio</b>:' + ' ' + self._bios[0] + '<br />\n'
			else:
				ret_str += '<br /><b>Bios</b>:\n'
				for bio in self._bios:
					ret_str += '<br />' + bio + '<br />\n'
		return ret_str + '<br />\n'

class SSI_ClassList:

	def __init__(self):
		self._class_list = []

	def add(self, ssi_class):
		self._class_list.append(ssi_class)

	def __str__(self):
		ret_str = ''
		for ssi_class in self._class_list:
			if type(ssi_class) is str:						# 'week of ...' or date and time of a class
				if ssi_class.lower().split(' ', 1)[0] == 'week':
					ret_str += '<b><u>' + ssi_class + '</u></b><br /><br />\n'
				else:
					ret_str += '<i><u>' + ssi_class + '</u></i><br /><br />\n'
			else:
				ret_str += str(ssi_class)
			ret_str += '\n'
		return ret_str

# dictionary for routing a line to the appropriate SSI_Class attribute
ssi_class_attrs = {
	'title:':		SSI_Class.set_title,
	'presenter:':	SSI_Class.set_presenters,
	'presenters:':	SSI_Class.set_presenters,
	'tour':			SSI_Class.set_presenters,
	'location:':	SSI_Class.set_location,
	'class':		SSI_Class.set_description,
	'extra:':		SSI_Class.add_extra,
	'bio:':			SSI_Class.add_bio,
	'bios:':		SSI_Class.add_bio,
}

def write_skipped_line(line_no, line, skipped_lines_file):
	print(f'{str(line_no + 1):>3s}: {line}', file=skipped_lines_file)

def main():

	class_list = SSI_ClassList()
	ssi_class = SSI_Class()

	with open('schedule.txt', 'r') as sched_txt:
		lines = sched_txt.readlines()

	skipped_lines_file = open('skipped_lines.txt', 'w')

	line_no = -1					# help with debugging
	for line in lines:
		line_no += 1
		line = line.strip()

		# filter lines we want to skip
		if len(line) == 0														\
				or line[0] in '?o_-\n'											\
				or line.startswith('NOTES:') or line.startswith('Notes:')		\
				or line[0] == '.' and len(line) == 1							\
				or ord(line[0]) == 8211 or ord(line[0]) == 8212:	# en, em dash
			write_skipped_line(line_no, line, skipped_lines_file)
			continue

		first_word, after_first = line.split(' ', 1)

		if first_word.lower() in ('week', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
			if not ssi_class.is_empty():
				class_list.add(ssi_class)
				ssi_class = SSI_Class()
			class_list.add(line)
			continue

		if first_word.lower() in ssi_class_attrs:
			ssi_class_attrs[first_word.lower()](ssi_class, first_word, after_first)
		else:
			write_skipped_line(line_no, line, skipped_lines_file)
			continue

	class_list.add(ssi_class)

	with open('schedule.html', 'w') as html_file:
		print(class_list, file=html_file)

	skipped_lines_file.close()

# for use as Python script -- not used from Jupyter notebook
if __name__ == '__main__':
	main()