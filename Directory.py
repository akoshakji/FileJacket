class Directory:
    
    def __init__(self, name, size):
        self.name = name
        self.subfolders = []
        self.files = []
        self.size = size
