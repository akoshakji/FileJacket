class File:
    
    def __init__(self, name, timestamp):
        self.name = name
        self.timestamp = timestamp
    
    def __eq__(self, other):
        if isinstance(other, File):
            return ((self.name == other.name) and 
                    (self.timestamp == other.timestamp))
        return False

if __name__ == '__main__':
    f1 = File('f1', 162076)
    f2 = File('f2', 162076)
    f3 = File('f1', 162075)
    f4 = File('f1', 162076)
    
    print(f1 == f2)
    print(f1 == f3)
    print(f1 == f4)