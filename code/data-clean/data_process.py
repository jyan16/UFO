import sqlite3
import json
import re



conn = sqlite3.connect('../../data/my_ufo.db')
c = conn.cursor()

def count_by_year():
    year_count_result = {}
    for row in c.execute('''SELECT year, state, count(*)
                            FROM events
                            WHERE year>=1950 AND year<=2016
                            GROUP BY state, year'''):
        if row[0] not in year_count_result.keys():
            year_count_result[row[0]] = [[row[1], row[2]]]
        else:
            year_count_result[row[0]].append([row[1], row[2]])
    result = []
    for key, value in year_count_result.items():

        total = sum([item[1] for item in value])
        value_new = [[item[0], item[1]/total] for item in value]
        result.append({"year": key, "frequency": value_new})

    result.sort(key = lambda x : x["year"])
    with open("../../data/frequency_by_year.json", 'w') as outfile:
        json.dump(result, outfile, indent = 4)

def count_by_hour():
    hour_count_result = {}
    for row in c.execute('''SELECT time FROM events
                            WHERE year>=1950 AND year<=2016'''):
        hour = row[0].split(':')[0]
        if hour not in hour_count_result.keys():
            hour_count_result[hour] = 1
        else:
            hour_count_result[hour] += 1
    result = []
    for key, value in hour_count_result.items():
        result.append({"hour" : key, "count" : value})
    with open("../../data/count_by_hour.json", 'w') as outfile:
        json.dump(result, outfile, indent = 4)

def state_path_change():

    pattern = re.compile(r'[A-Z]')
    with open('../../data/statesPath.json', 'r') as f:
        states =json.load(f)

    state_path_new = []
    for state in states:

        tmp_points = re.split(pattern, state['d'])
        tmp_point_list = []
        tmp_chars = pattern.findall(state['d'])

        for i in range(1,len(tmp_points)-1):
            point = tmp_points[i]
            if point != '':
                tmp = point.split(',')
                tmp[0] = str(float(tmp[0]) * 0.7)[0:9]
                tmp[1] = str(float(tmp[1]) * 0.7)[0:9]
                tmp_point_list.append(','.join(tmp))
            else:
                tmp_point_list.append(point)

        path_changed = ''
        for character, point in zip(tmp_chars, tmp_point_list):
            path_changed += (character + point)

        path_changed += tmp_chars[-1]
        state['d'] = path_changed
        state_path_new.append(state)

    with open("../../data/statesPath_new.json", 'w') as outfile:
        json.dump(state_path_new, outfile, indent = 4)

def shape_count():

    shapes = {}

    for row in c.execute('''SELECT shape, count(*)
                            FROM events
                            WHERE year>=1950 AND year<=2016
                            GROUP BY shape'''):
        if row[0].lower() not in shapes.keys():
            shapes[row[0].lower()] = row[1]
        else:
            shapes[row[0]] += row[1]

    result = []
    for key, value in shapes.items():
        result.append({"shape" : key, "count" : value})

    result.sort(key = lambda x : x["count"])
    with open("../../data/shape_all.json", 'w') as outfile:
        json.dump(result, outfile, indent = 4)
if __name__ == '__main__':
    shape_count()





