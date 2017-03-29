import sqlite3
import csv
import re

#This script cleans up population and area of states

#establish us information
us_info_reader = csv.reader(open('../../data/us_states.csv', 'r', encoding='utf-8'))
us_info = {}
us_geo = []
for row in us_info_reader:
	us_info[row[0]] = row[1:]
	us_geo.append([row[1], float(re.sub(',', '', row[2]))])


#write us geo information
us_info_writer = csv.writer(open('../../data/file_us_area.csv', 'w', encoding='utf-8'))
us_info_writer.writerow(['state', 'area'])
for row in us_geo:
	us_info_writer.writerow(row)


#read population in
population_list = []



def add1(year_min, year_max):
	population_file = open('../../data/' + str(year_min) +
						   '-' + str(year_max) + '.csv', 'r', encoding='utf-8')
	population_reader = csv.reader(population_file)
	next(population_reader, None)
	for row in population_reader:
		for i in range(year_min, year_max + 1):
			population_list.append([us_info[row[0][1:]][0], i, int(re.sub(',', '', row[i - year_min + 1]))])

def add2(year_min, year_max):
	population_file = open('../../data/' + str(year_min) +
						   '-' + str(year_max) + '.csv', 'r', encoding='utf-8')
	population_reader = csv.reader(population_file)
	next(population_reader, None)
	for row in population_reader:
		for i in range(year_min, year_max + 1):
			population_list.append([us_info[row[0]][0], i, int(re.sub(',', '', row[i - year_min + 1]))])

def add3(year_min, year_max):
	population_file = open('../../data/' + str(year_min) +
						   '-' + str(year_max) + '.csv', 'r', encoding='utf-8')
	population_reader = csv.reader(population_file)
	next(population_reader, None)
	for row in population_reader:
		for i in range(year_min, year_max + 1):
			population_list.append([row[0], i, int(re.sub(',', '', row[i - year_min + 1]))])


add1(2010, 2016)
add1(2000, 2009)
add2(1990, 1999)
add3(1980, 1989)

us_info_writer = csv.writer(open('../../data/file_us_population.csv', 'w', encoding='utf-8'))
us_info_writer.writerow(['state', 'year', 'population'])
for row in population_list:
	us_info_writer.writerow(row)