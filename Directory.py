class Directory:
    
    def __init__(self, name, timestamp):
        self.name = name
        self.timestamp = timestamp
        self.children = []
        self.files = []
