class Directory:


    '''Class for directory

    name      --> directory name
    timestamp --> timestamp of the last modification
    children  --> subdirectories present in the directory
    files     --> files present in the directory
    '''


    def __init__(self, name, timestamp):
        # directory name
        self.name = name
        # timestamp of the last modification
        self.timestamp = timestamp
        # subdirectories present in the directory
        self.children = []
        # files present in the directory
        self.files = []


    def __eq__(self, other):
                
        '''Override equality operator'''
        
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