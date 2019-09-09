import time

def setup(file_location):
	global  file, print_on_console, seconds
	file = open(file_location + '/log.txt', 'w+')
	print_on_console = True
	seconds = time.time()

def start_message(input):
	message('start: ' + input)


def end_message(input):
	message('end: ' + input)


def error_message(input):
	message('error: ' + input)


def message(input):
	global print_on_console
	str = add_time_to_log_message(input)
	if print_on_console:
		output_to_console(str)
	output_to_log_txt(str)


def add_time_to_log_message(input):
	global seconds
	return time.ctime(seconds) + ' ' + input + '\n'


def output_to_log_txt(message):
	file.write(message)
	file.flush()


def output_to_console(message):
	print(message)


def close_file():
	global file
	file.close()