from uuid import uuid4

class Timespan():
    def __init__(self):
        self.id = uuid4()
        self.start_time = None
        self.stop_time = None
