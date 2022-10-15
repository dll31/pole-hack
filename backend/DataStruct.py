

class DataStruct:
    def __init__(self):
        self.frame = None
        self.json_data = None

    def update(self, frame, json_data):
        self.frame = frame
        self.json_data = json_data