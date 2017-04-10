import csv
import re

pattern1 = re.compile(r'(\D?)(\d+)(\+?) (se.+)')
pattern2 = re.compile(r'(\D?)(\d+)(\+?) (mi.+)')
pattern3 = re.compile(r'(\D?)(\d+)(\+?) (h.+)')
pattern4 = re.compile(r'(\d+):(\d+)')
pattern5 = re.compile(r'^(\d+)$')
pattern6 = re.compile(r'(\d+)(\D)(\d+) (se.+)')
pattern7 = re.compile(r'(\d+)(\D)(\d+) (mi.+)')
pattern8 = re.compile(r'(\d+)(\D)(\d+) (h.+)')

with open('../../data/raw_csv_data/duration_clean.csv', 'w', newline='', encoding='utf-8') as clean_file:
	writer = csv.writer(clean_file)
	writer.writerow(['event_id'.encode('utf-8'), 'time'.encode('utf-8'), 'city'.encode('utf-8'), 'state'.encode('utf-8'), 'shape'.encode('utf-8'), 'duration'.encode('utf-8'), 'event_id'.encode('utf-8'), 'summary'.encode('utf-8'), 'location_id'.encode('utf-8')])
	with open('../../data/raw_csv_data/file_ufo_clean.csv', 'r', encoding='utf-8') as raw_file:
		reader = csv.reader(raw_file)
		next(reader, None)
		for row in reader:
			duration = row[5][2:-1].lower()

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
				duration = str(int((int(match6.group(1)) + int(match6.group(3)))/2))
			elif (match7):
				duration = str(int((int(match7.group(1)) + int(match7.group(3)))/2 * 60))
			elif (match8):
				duration = str(int((int(match8.group(1)) + int(match8.group(3)))/2 * 60 * 60))
			else:
				duration = '-1'

			writer.writerow([row[0], row[1], row[2], row[3], row[4], duration.encode('utf-8'), row[6], row[7]])
