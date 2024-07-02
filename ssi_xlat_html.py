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
		self._bio = None

	def get_date_time(self):
		return self._date_time

	def get_title(self):
		return self._title

	def get_presenters(self):
		if self._presenter_title is None:
			return None
		else:
			return self._presenter_title + ' ' + self._presenters

	def get_location(self):
		return self._location

	def get_description(self):
		return self._description

	def get_bio(self):
		return self._bio

	def set_date_time(self, first_word, after_first):
		self._date_time = first_word + ' ' + after_first

	def set_title(self, first_word, after_first):
		self._title = after_first

	def set_presenters(self, first_word, after_first):
		self._presenter_title = first_word
		self._presenters = after_first

	def set_location(self, first_word, after_first):
		self._location = after_first

	def set_description(self, first_word, after_first):
		self._description = after_first.split(' ', 1)[1].strip()

	def set_bio(self, first_word, after_first):
		self._bio = after_first

	def __str__(self):
		ret_str = ''
		if self._date_time is not None:
			ret_str += self._date_time + '<br />\n'
		if self._title is not None:
			ret_str += '<b>Title</b>: ' + self._title + '<br />\n'
		if self._presenter_title is not None:
			ret_str += '<b>' + self._presenter_title + '</b>: ' + self._presenters + '<br />\n'
		if self._location is not None:
			ret_str += '<b>Location</b>: ' + self._location + '<br />\n'
		if self._description is not None:
			ret_str += '<b>Class Description</b>: ' + self._description + '<br />\n'
		if self._bio is not None:
			ret_str += '<b>Bio</b>: ' + self._bio + '<br />\n'
		return ret_str

class SSI_ClassList:

	def __init__(self):
		# self._browser = browser
		self._class_list = []

	def add(self, ssi_class):
		self._class_list.append(ssi_class)

	def __str__(self):
		ret_str = ''
		# if self._browser:
		# 	ret_str += '<html>\n'
		# 	ret_str += '<head>\n'
		# 	ret_str += '</head>\n'
		# 	ret_str += '<body>\n'
		for ssi_class in self._class_list:
			if type(ssi_class) is str:
				ret_str += ssi_class + '<br /><hr />\n'
			else:
				ret_str += str(ssi_class)
				ret_str += '<hr />\n'
		# if self._browser:
		# 	ret_str += '</body>\n'
		# 	ret_str += '</html>\n'
		return ret_str

class BadFileFormat(Exception):

	def __init__(self, line_no, msg):
		self._line_no = str(line_no)
		self._msg = msg
	
	def __str__(self):
		return 'BadFileFormat(line ' + self._line_no + '): did not find ' + self._msg + ' line.'

ssi_class_attrs = {
	# 'week':			(SSI_Class.get_week,			SSI_Class.set_week),
	'title:':		(SSI_Class.get_title,			SSI_Class.set_title),
	'presenter:':	(SSI_Class.get_presenters,		SSI_Class.set_presenters),
	'presenters:':	(SSI_Class.get_presenters,		SSI_Class.set_presenters),
	'tour':			(SSI_Class.get_presenters,		SSI_Class.set_presenters),
	'location:':	(SSI_Class.get_location,		SSI_Class.set_location),
	'class':		(SSI_Class.get_description,		SSI_Class.set_description),
	'bio"':			(SSI_Class.get_bio,				SSI_Class.set_bio),
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
	ssi_class = SSI_Class()

	with open('schedule.txt', 'r') as sched_txt:
		lines = sched_txt.readlines()

	try:		
		for line in lines:
			if line[0] in '?o_-\n' or ord(line[0]) == 8212 or line.startswith('NOTES:') or line.startswith('Notes:') or line.startswith('http'):
				continue

			first_word, after_first = line.split(' ', 1)

			if first_word.lower() == 'week':
				class_list.add(line)
				continue

			try:
				if ssi_class_attrs[first_word.lower()][0](ssi_class) is not None:
					class_list.add(ssi_class)
					ssi_class = SSI_Class()
				ssi_class_attrs[first_word.lower()][1](ssi_class, first_word, after_first.strip())
			except KeyError:
				continue

		class_list.add(ssi_class)
				
	except BadFileFormat as bfe:
		print(bfe)

	with open('schedule.html', 'w') as html_file:
		print(class_list, file=html_file)


main()