import csv
import re
from porter_stemmer import PorterStemmer



stop = {'the', 'is', 'on', 'a', 'to', 'of', 's'}
def clean_duration(duration):

	pattern1 = re.compile(r'(\D?)(\d+)(\+?) (se.+)')
	pattern2 = re.compile(r'(\D?)(\d+)(\+?) (mi.+)')
	pattern3 = re.compile(r'(\D?)(\d+)(\+?) (h.+)')
	pattern4 = re.compile(r'(\d+):(\d+)')
	pattern5 = re.compile(r'^(\d+)$')
	pattern6 = re.compile(r'(\d+)(\D)(\d+) (se.+)')
	pattern7 = re.compile(r'(\d+)(\D)(\d+) (mi.+)')
	pattern8 = re.compile(r'(\d+)(\D)(\d+) (h.+)')

	match1 = pattern1.match(duration)
	match2 = pattern2.match(duration)
	match3 = pattern3.match(duration)
	match4 = pattern4.match(duration)
	match5 = pattern5.match(duration)
	match6 = pattern6.match(duration)
	match7 = pattern7.match(duration)
	match8 = pattern8.match(duration)

	if (match1):
		duration = match1.group(2)
	elif (match2):
		duration = str(int(match2.group(2)) * 60)
	elif (match3):
		duration = str(int(match3.group(2)) * 60 * 60)
	elif (match4):
		duration = str(int(match4.group(1)) * 60 + int(match4.group(2)))
	elif (match5):
		duration = match5.group(1)
	elif (match6):
		duration = str(int((int(match6.group(1)) + int(match6.group(3))) / 2))
	elif (match7):
		duration = str(int((int(match7.group(1)) + int(match7.group(3))) / 2 * 60))
	elif (match8):
		duration = str(int((int(match8.group(1)) + int(match8.group(3))) / 2 * 60 * 60))
	else:
		duration = '-1'
	return duration

def clean_summary(summary):
	label = 1
	if 'nuforc' in summary or 'hoax' in summary:
		label = 0

	summary = re.sub(r'\(\(.*\)\)', '', summary)
	summary = re.sub(r'\W', ' ', summary)
	summary_list = summary.split()
	summary_list = list(filter(lambda x: x not in stop, summary_list))
	summary_list = list(filter(lambda x: x[0] < '0' or x[0] > '9', summary_list))
	summary_list = [PorterStemmer().stem(word, 0, len(word) - 1) for word in summary_list]
	summary = ' '.join(summary_list)
	return label, summary

def clean_shape(shape):
	if shape == '<br>':
		return 'unknown'
	else:
		return shape

def check(row):
	if (len(row['time'].split(':')) != 3):
		return False
	if ('?' in row['year'] or '?' in row['month'] or '?' in row['day']):
		return False
	if (row['month'] == '' or row['day'] == '' or row['shape'] == ''):
		return False
	return True
def main():

	origin_file = open('../../data/processed/file_ufo_lat.csv', 'r', encoding='utf-8')
	origin_reader = csv.DictReader(origin_file)
	clean_file = open('../../data/processed/file_ufo_most_clean.csv', 'w', encoding='latin1')
	clean_writer = csv.writer(clean_file)

	clean_list = []
	clean_writer.writerow(['event_id', 'year', 'month', 'day', 'time', 'city', 'state', 'shape', 'duration', 'summary', 'lat', 'lng', 'label'])
	#process each row of original_reader
	for row in origin_reader:
		if check(row):
			duration = clean_duration(row['duration'][2:-1].lower())
			label, summary = clean_summary(row['summary'][2:-1].lower())
			shape = clean_shape(row['shape'][2:-1].lower())
			clean_list.append([row['event_id'], row['year'], row['month'], row['day'], row['time'], row['city'][2:-1],
							   row['state'][2:-1], shape, duration, summary, row['lat'], row['lng'], label])
			clean_writer.writerow([row['event_id'], row['year'], row['month'], row['day'], row['time'], row['city'][2:-1],
								 row['state'][2:-1], shape, duration, summary, row['lat'], row['lng'], label])


if __name__ == '__main__':
	main()