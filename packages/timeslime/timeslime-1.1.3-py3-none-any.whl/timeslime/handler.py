from os import mkdir
from os.path import exists, dirname
from sqlite3 import connect
from datetime import datetime, timedelta
from sqlite3 import Connection
from .model import Timespan

class DatabaseHandler():
    def __init__(self, database_connection):
        if type(database_connection) is Connection:
            self.connection = database_connection
        else:
            if not exists(database_connection):
                directory = dirname(database_connection)
                if directory != '' and not exists(directory):
                    mkdir(directory)
            self.connection = connect(database_connection, check_same_thread=False)
        cursor = self.connection.execute('SELECT count(*) FROM sqlite_master WHERE type="table" AND name="timespans";')
        if cursor.fetchone()[0] == 0:
            self.connection.execute('CREATE TABLE timespans (id TEXT NOT NULL PRIMARY KEY, start_time DATETIME, stop_time DATETIME);')
            self.connection.commit()

    def __del__(self):
        self.connection.close()

    def get_tracked_time_in_seconds(self):
        daily_sum_in_seconds = timedelta(seconds=0)
        cursor = self.connection.execute('SELECT round(sum((julianday(stop_time) - julianday(start_time)) * 24 * 60 * 60)) as timespan FROM timespans WHERE date("now") = date(start_time);')
        response = cursor.fetchone()[0]
        if response != None:
            daily_sum_in_seconds = timedelta(seconds=response)
        self.connection.commit()
        return daily_sum_in_seconds

    def save_timespan(self, timespan):
        if type(timespan) is not Timespan:
            return

        if timespan.start_time is None:
            return

        select_statement = 'SELECT COUNT(*) FROM timespans WHERE id="%s"' % timespan.id
        cursor = self.connection.execute(select_statement)
        if cursor.fetchone()[0] > 0:
            delete_statement = 'DELETE FROM timespans WHERE id="%s"' % timespan.id
            self.connection.execute(delete_statement)
        insert_statement = 'INSERT INTO timespans VALUES ("%s", "%s", "%s")' % (timespan.id, timespan.start_time, timespan.stop_time)
        self.connection.execute(insert_statement)
        self.connection.commit()

    def get_recent_timespan(self):
        cursor = self.connection.execute('SELECT * FROM timespans WHERE stop_time = "None";')
        response = cursor.fetchone()
        timespan = Timespan()
        if response is not None:
            timespan.id = response[0]
            timespan.start_time = datetime.strptime(response[1], '%Y-%m-%d %H:%M:%S.%f')
            return timespan
        return None

class TimespanHandler():
    def __init__(self, daily_working_time, database_handler):
        self.daily_working_time = daily_working_time
        self.database_handler = database_handler
        self.timespan = self.database_handler.get_recent_timespan()
        self.on_start = None
        self.on_stop = None

    def start_time(self):
        self.stop_time()
        self.timespan = Timespan()
        self.timespan.start_time = datetime.now()
        self.database_handler.save_timespan(self.timespan)
        if self.on_start is not None:
            self.on_start()

    def stop_time(self):
        if self.timespan is not None and self.timespan.start_time is not None:
            self.timespan.stop_time = datetime.now()
            self.database_handler.save_timespan(self.timespan)
        if self.on_stop is not None:
            self.on_stop()

    def get_elapsed_time(self):
        daily_sum_in_seconds = self.database_handler.get_tracked_time_in_seconds()
        current_timedelta = timedelta(seconds=0)
        if self.timespan is not None and self.timespan.stop_time is None:
            current_timedelta = datetime.now() - self.timespan.start_time
        return self.daily_working_time - daily_sum_in_seconds - current_timedelta

    def is_running(self):
        if self.database_handler.get_recent_timespan() is not None:
            return True
        else:
            return False
