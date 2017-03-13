import sqlite3
import csv

def load():
    #initialization
    conn = sqlite3.connect('event.db')
    c = conn.cursor()

    # Delete table if already exists
    c.execute('DROP TABLE IF EXISTS "events";')


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

    conn.commit()
    ufo_reader = csv.DictReader(open('../../data/file_ufo_lat.csv', 'r'))
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


    conn.commit()
    conn.close()
if __name__ == '__main__':
    load()
