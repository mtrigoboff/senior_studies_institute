import string

class SSI_Class:

	def __init__(self):
		self._date_time = None
		self._title = None
		self._presenter_title = None
		self._presenters = None
		self._n_presenters = None
		self._location = None
		self._description = None
		self._bios = []
		self._extra = []

	def get_date_time(self):
		return self._date_time

	def set_date_time(self, first_word, after_first):
		self._date_time = first_word + ' ' + after_first

	def get_title(self):
		return self._title

	def set_title(self, first_word, after_first):
		self._title = after_first

	def get_presenters(self):
		if self._presenter_title is None:
			return None
		else:
			return self._presenter_title + ' ' + self._presenters

	def set_presenters(self, first_word, after_first):
		if first_word == 'Tour':
			self._presenter_title = "Tour Guide:"
			self._presenters = after_first.split(' ', 1)[1].strip()
		else:
			self._presenter_title = first_word
			self._presenters = after_first

	def get_location(self):
		return self._location

	def set_location(self, first_word, after_first):
		self._location = after_first

	def get_description(self):
		return self._description

	def set_description(self, first_word, after_first):
		self._description = after_first.split(' ', 1)[1].strip()

	def get_bio(self):
		return None

	def add_bio(self, first_word, after_first):
		self._bios.append(after_first)

	def get_extra(self):
		return None

	def add_extra(self, first_word, after_first):
		self._extra.append(after_first)

	def __str__(self):
		ret_str = ''
		if self._date_time is not None:
			ret_str += self._date_time + '<br />\n'
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
			for extra in self._extra:
				ret_str += extra + '<br />\n'
		if self._bios:
			if len(self._bios) == 1:
				ret_str += '<br /><b>Bio</b>:' + ' ' + self._bios[0] + '<br />'
			else:
				ret_str += '<br /><b>Bios</b>:<br />'
				for bio in self._bios:
					ret_str += bio + '<br /><br />\n'
		return ret_str

class SSI_ClassList:

	def __init__(self):
		# self._browser = browser
		self._class_list = []

	def add(self, ssi_class):
		self._class_list.append(ssi_class)

	def __str__(self):
		ret_str = ''
		for ssi_class in self._class_list:
			if type(ssi_class) is str:
				ret_str += ssi_class + '<br /><hr />\n'
			else:
				ret_str += str(ssi_class)
				ret_str += '<hr />\n'
		return ret_str

ssi_class_attrs = {
	'title:':		(SSI_Class.get_title,			SSI_Class.set_title),
	'presenter:':	(SSI_Class.get_presenters,		SSI_Class.set_presenters),
	'presenters:':	(SSI_Class.get_presenters,		SSI_Class.set_presenters),
	'tour':			(SSI_Class.get_presenters,		SSI_Class.set_presenters),
	'location:':	(SSI_Class.get_location,		SSI_Class.set_location),
	'class':		(SSI_Class.get_description,		SSI_Class.set_description),
	'extra:':		(SSI_Class.get_extra,			SSI_Class.add_extra),
	'bio:':			(SSI_Class.get_bio,				SSI_Class.add_bio),
	'bios:':		(SSI_Class.get_bio,				SSI_Class.add_bio),
	'monday':		(SSI_Class.get_date_time,		SSI_Class.set_date_time),
	'tuesday':		(SSI_Class.get_date_time,		SSI_Class.set_date_time),
	'wednesday':	(SSI_Class.get_date_time,		SSI_Class.set_date_time),
	'thursday':		(SSI_Class.get_date_time,		SSI_Class.set_date_time),
	'friday':		(SSI_Class.get_date_time,		SSI_Class.set_date_time),
	'saturday':		(SSI_Class.get_date_time,		SSI_Class.set_date_time),
	'sunday':		(SSI_Class.get_date_time,		SSI_Class.set_date_time),
}

def main():

	class_list = SSI_ClassList()
	ssi_class = None

	with open('schedule.txt', 'r') as sched_txt:
		lines = sched_txt.readlines()

	skipped_lines_file = open('skipped_lines.txt', 'w')

	for line in lines:
		if line[0] in '?o_-\n' or ord(line[0]) == 8212 or line.startswith('NOTES:') or line.startswith('Notes:') or line.startswith('http'):
			print(line.strip(), file=skipped_lines_file)
			continue

		first_word, after_first = line.split(' ', 1)
		after_first = after_first.strip()

		if first_word.lower() == 'week':
			if ssi_class is not None:
				class_list.add(ssi_class)
			ssi_class = SSI_Class()
			class_list.add(line.strip())
			continue

		try:
			if ssi_class is None:
				ssi_class = SSI_Class()
			if ssi_class_attrs[first_word.lower()][0](ssi_class) is not None:
				class_list.add(ssi_class)
				ssi_class = SSI_Class()
			ssi_class_attrs[first_word.lower()][1](ssi_class, first_word, after_first)
		except KeyError:
			print(line.strip(), file=skipped_lines_file)
			continue

	class_list.add(ssi_class)

	with open('schedule.html', 'w') as html_file:
		print(class_list, file=html_file)

	skipped_lines_file.close()

main()