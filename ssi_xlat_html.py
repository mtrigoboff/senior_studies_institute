class SSI_Class:

	def __init__(self, date_time, title, presenter_title, presenters, n_presenters, location, description, bio):
		self._date_time = date_time
		self._title = title
		self._presenter_title = presenter_title
		self._presenters = presenters
		self._n_presenters = n_presenters
		self._location = location
		self._description = description
		self._bio = bio

	def __str__(self):
		ret_str = ''
		ret_str += self._date_time + '\n'
		ret_str += self._title + '\n'
		ret_str += self._presenter_title + ': ' + self._presenters + '\n'
		ret_str += self._location + '\n'
		ret_str += self._description + '\n'
		if self._bio is not None:
			ret_str += self._bio + '\n'
		return ret_str

class SSI_ClassList:

	def __init__(self, browser):
		self._browser = browser
		self._class_list = []

	def add(self, ssi_class):
		self._class_list.append(ssi_class)

	def __str__(self):
		ret_str = ''
		if self._browser:
			ret_str += '<html>\n'
			ret_str += '<head>\n'
			ret_str += '</head>\n'
			ret_str += '<body>\n'
		for ssi_class in self._class_list:
			ret_str += str(ssi_class)
		if self._browser:
			ret_str += '</body>\n'
			ret_str += '</html>\n'
		return ret_str

class BadFileFormat(Exception):

	def __init__(self, line_no, msg):
		self._line_no = str(line_no)
		self._msg = msg
	
	def __str__(self):
		return 'BadFileFormat(line ' + self._line_no + '): did not find ' + self._msg + ' line.'

def line_pair(line):
	pair = line.split(':')
	return (pair[0], pair[1].strip())

def main(browser):

	class_list = SSI_ClassList(browser)

	with open('schedule.txt', 'r') as sched_txt:
		lines = sched_txt.readlines()

	try:		
		for i in range(len(lines)):
			if lines[i].startswith('Title:'):
				date_time = lines[i - 1]
				title = line_pair(lines[i])[1]		# we already found Title line

				pair = line_pair(lines[i + 1])
				if pair[0] not in ('Presenter', 'Presenters', 'Tour Guide'):
					raise BadFileFormat(i, 'Instructor')
				presenter_title, presenters = pair
				if presenter_title == 'Presenters':
					n_presenters = 2
				else:
					n_presenters = 1
				
				pair = line_pair(lines[i + 2])
				if pair[0] != 'Location':
					raise BadFileFormat(i, 'Location')
				location = pair[1]
				
				pair = line_pair(lines[i + 3])
				if pair[0] != 'Class description':
					raise BadFileFormat(i, 'Description')
				description = pair[1]

				if lines[i + 5].startswith('Bio:'):
					bio = line_pair(lines[i + 5])[1]
				else:
					bio = None

				class_list.add(SSI_Class(date_time, title, presenter_title, presenters, n_presenters, location, description, bio))
				
	except BadFileFormat as bfe:
		print(bfe)

	with open('schedule.html', 'w') as html_file:
		print(class_list, file=html_file)


main(True)