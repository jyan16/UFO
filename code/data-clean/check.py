import csv

#This script exstract labels of reports based on NUFORC's comment
event_file = open('../../data/processed/file_ufo_lat.csv', 'r', encoding='utf-8')
event_reader = csv.DictReader(event_file)
next(event_reader, None)

select_data = []

for row in event_reader:
	if 'nuforc' in row['summary'].lower():
		select_data.append([row['event_id'], row['summary']])

event_writer = csv.writer(open('../../data/processed/file_ufo_label.csv', 'w', encoding='utf-8'))
event_writer.writerow(['event_id', 'summary', 'label'])

for row in select_data:
	event_writer.writerow(row)