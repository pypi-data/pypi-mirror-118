#!/usr/bin/env python3
from datetime import timedelta
from sys import argv
from os.path import expanduser, join

from .handler import DatabaseHandler, TimespanHandler

def main():
    database = join(expanduser('~'), '.timeslime', 'data.db')
    daily_working_time = timedelta(hours=7, minutes=36)
    database_handler = DatabaseHandler(database)
    timespan_handler = TimespanHandler(daily_working_time, database_handler)
    if len(argv) == 1:
        print('start/stop/display todays working time')
        exit()
    command = argv[1]
    if command == 'start':
        timespan_handler.start_time()
    elif command == 'stop':
        timespan_handler.stop_time()
    elif command == 'display':
        print(str(timespan_handler.get_elapsed_time()))
    else:
        print('start/stop/display todays working time')

if __name__ == '__main__':
    main()
