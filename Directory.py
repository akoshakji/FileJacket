class Directory:
    '''
    Class for directory

    name      --> directory name
    timestamp --> timestamp of the last modification
    path      --> local path of the directory
    children  --> subdirectories present in the directory
    files     --> files present in the directory
    '''
    def __init__(self, name, timestamp, path):
        # directory name
        self.name = name
        # timestamp of the last modification
        self.timestamp = timestamp
        # local path of the directory
        self.path = path
        # subdirectories present in the directory
        self.children = []
        # files present in the directory
        self.files = []


    def __eq__(self, other):
        '''
        Override equality operator
        '''
        if isinstance(other, Directory):
            return ((self.name == other.name) and
                    (self.timestamp == other.timestamp) and
                    (self.path == other.path))
        return False
    
    
    def __str__(self):
        '''
        Override string representation
        '''
        name = "name: " + self.name
        path = "path: " + self.path
        files = "files: " + " ".join([x.name for x in self.files])
        children = "subdirectories: " + " ".join([x.name for x in self.children])
        return "Directory:\n\t" \
                + name + "\n\t" \
                + path + "\n\t" \
                + files + "\n\t" \
                + children


if __name__ == '__main__':
    pass