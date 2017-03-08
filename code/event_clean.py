import csv
import re


event_file = open('../data/file_ufo.csv', 'r', encoding='utf-8')
event_reader = csv.reader(event_file)
next(event_reader, None)


event_clean_list = []
pattern_1 = re.compile(r'COLOR=#000000>.+?</TD>')
pattern_2 = re.compile(r'.html>.+?</A></TD>')
for row in event_reader:
    match_1 = pattern_1.findall(row[0])
    match_2 = pattern_2.findall(row[0])
    tmp = [match_2[0][6:-9].encode('utf-8')]
    for i in range(1,len(match_1)-1):
        tmp.append(match_1[i][14:-5].encode('utf-8'))

    event_clean_list.append(tmp)


event_clean_file = open('../data/file_ufo_clean.csv', 'w', encoding='utf-8')
event_clean_writer = csv.writer(event_clean_file)
event_clean_writer.writerow(['time'.encode('utf-8'), 'city'.encode('utf-8'), 'state'.encode('utf-8'), 'shape'.encode('utf-8'),
                             'duration'.encode('utf-8'), 'summary'.encode('utf-8')])

for item in event_clean_list:
    event_clean_writer.writerow(item)

