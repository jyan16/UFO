import sqlite3
import json




conn = sqlite3.connect('../../data/my_ufo.db')
c = conn.cursor()

def count_by_year():
    year_count_result = {}
    max_count = 0
    for row in c.execute('''SELECT year, state, count(*)
                            FROM events
                            WHERE year>=1950 AND year<=2016
                            GROUP BY state, year'''):
        if row[0] not in year_count_result.keys():
            year_count_result[row[0]] = [[row[1], row[2]]]
        else:
            year_count_result[row[0]].append([row[1], row[2]])
        max_count = max(row[2], max_count)
    print(max_count)
    result = []
    for key, value in year_count_result.items():
        result.append({"year" : key, "state" : value})
    result.sort(key = lambda x : x["year"])
    with open("../../data/count_by_year.json", 'w') as outfile:
        json.dump(result, outfile, indent = 4)

def count_by_hour():
    hour_count_result = {}
    for row in c.execute('''SELECT time FROM events
                            WHERE year>=1950'''):
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


if __name__ == '__main__':
    count_by_year()





