import sqlite3
import csv


#This script creates database --- my_ufo.db
def load():
    #initialization
    conn = sqlite3.connect('../../data/my_ufo.db')
    c = conn.cursor()

    # Delete table if already exists
    c.execute('DROP TABLE IF EXISTS "events";')
    c.execute('DROP TABLE IF EXISTS "weathers";')
    c.execute('DROP TABLE IF EXISTS "populations";')
    c.execute('DROP TABLE IF EXISTS "areas";')


    # Create tables
    c.execute('''
            CREATE TABLE events(
                event_id    int not null,
                year        int,
                month       int,
                day         int,
                time        text,
                city        text,
                state       text,
                shape       text,
                duration    text,
                summary     text,
                lat         float,
                lng         float,
                PRIMARY KEY(event_id))
              ''')


    c.execute('''
            CREATE TABLE weathers(
                event_id            int not null,
                summary             text,
                icon                text,
                temperature         float,
                apparentTemperature float,
                dewPoint            float,
                humidity            float,
                windSpeed           float,
                windBearing         int,
                visibility          float,
                pressure            float,
                PRIMARY KEY(event_id))
              ''')

    c.execute('''
            CREATE TABLE populations(
                state       text not null,
                year        int,
                population  int)
              ''')

    c.execute('''
            CREATE TABLE areas(
                state       text not null,
                area        float,
                PRIMARY KEY(state))
              ''')
    conn.commit()
    ufo_reader = csv.DictReader(open('../../data/file_ufo_lat.csv', 'r'))
    weather_reader = csv.DictReader(open('../../data/file_ufo_weather.csv', 'r'))
    population_reader = csv.DictReader(open('../../data/file_us_population.csv', 'r'))
    area_reader = csv.DictReader(open('../../data/file_us_area.csv', 'r'))
    for row in ufo_reader:
        try:
            c.execute('''
                        INSERT INTO events
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
                      (int(row['event_id']), int(row['year']), int(row['month']), int(row['day']), row['time'],
                       row['city'][2:-1], row['state'][2:-1], row['shape'][2:-1], row['duration'][2:-1],
                       row['summary'][2:-1], float(row['lat']), float(row['lng'])))
        except:
            print('error')
    for row in weather_reader:
        try:
            c.execute('''
                        INSERT INTO weathers
                        VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
                      (int(row['event_id']), row['summary'], row['icon'], float(row['temperature']),
                       float(row['apparentTemperature']), float(row['dewPoint']), float(row['humidity']),
                       float(row['windSpeed']), int(row['windBearing']), float(row['visibility']), float(row['pressure'])))
        except:
            print('error')

    for row in population_reader:
        c.execute('''
                    INSERT INTO populations
                    VALUES (?,?,?)''',
                  (row['state'], int(row['year']), int(row['population'])))

    for row in area_reader:
        c.execute('''
                    INSERT INTO areas
                    VALUES (?,?)''',
                  (row['state'], float(row['area'])))

    conn.commit()
    conn.close()
if __name__ == '__main__':
    load()