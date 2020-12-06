class Directory:
    
    def __init__(self, name, timestamp):
        self.name = name
        self.timestamp = timestamp
        self.children = []
        self.files = []

    def __eq__(self, other):
        if isinstance(other, Directory):
            return ((self.name == other.name) and 
                    (self.timestamp == other.timestamp))
        return False

if __name__ == '__main__':
    d1 = Directory('d1', 162076)
    d2 = Directory('d2', 162076)
    d3 = Directory('d1', 162075)
    d4 = Directory('d1', 162076)
    
    print(d1 == d2)
    print(d1 == d3)
    print(d1 == d4)