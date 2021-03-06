class File:
    '''
    File

    name      --> name of the file
    timestamp --> timestamp of the last modification
    path      --> local path of the file
    '''
    def __init__(self, name, timestamp, path):
        # file name
        self.name = name
        # timestamp of the last modification
        self.timestamp = timestamp
        # local path of the file
        self.path = path


    def __eq__(self, other):
        '''
        Override equality operator
        '''
        if isinstance(other, File):
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
        return "File:\n\t" \
                + name + "\n\t" \
                + path


if __name__ == '__main__':
    pass
