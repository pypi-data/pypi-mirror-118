#!/usr/bin/env python3
from datetime import timedelta
from sys import argv
from os.path import expanduser, join

from .handler import DatabaseHandler, TimespanHandler

DATABASE = join(expanduser('~'), '.timeslime', 'data.db')
DAILY_WORKING_TIME = timedelta(hours=7, minutes=36)

if __name__ == '__main__':
    DATABASE_HANDLER = DatabaseHandler(DATABASE)
    TIMESPAN_HANDLER = TimespanHandler(DAILY_WORKING_TIME, DATABASE_HANDLER)
    command = argv[1]
    if command == 'start':
        TIMESPAN_HANDLER.start_time()
    elif command == 'stop':
        TIMESPAN_HANDLER.stop_time()
    elif command == 'display':
        print(str(TIMESPAN_HANDLER.get_elapsed_time()))
    else:
        print('start/stop/display todays working time')
