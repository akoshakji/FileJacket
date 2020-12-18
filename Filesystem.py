import os

from Directory import Directory
from File import File

class Filesystem:
    '''
    File Manager

    Class in charge to build the structure of the filesystem

    root    --> root directory
    ignore  --> ignore list of files/directories
    '''
    def __init__(self,
                 localpath,
                 ignore=('build', '.DS_Store', '.localized', 'builds', 'products')):

        name = os.path.basename(localpath)
        timestamp = os.stat(localpath).st_mtime
        root = Directory(name, timestamp, localpath)

        # root directory
        self.root = root
        # files or directories to ignore
        self.ignore = ignore

        # build the filesystem
        self.build_tree(localpath, self.root)


    def build_tree(self, localpath, directory):
        '''
        Build the filesystem given a path to a local file/directory

        localpath --> path to a local file/directory
        directory --> Directory object
        '''
        print("Building tree.. (directory: " + directory.name + ")")
        # loop over all the items in the local directory
        for entry in os.scandir(localpath):
            # if the item is a file and it is not in the ignore list
            if (entry.is_file() and (entry.name not in self.ignore)):
                # then store it in the directory's files list
                directory.files.append(File(entry.name, 
                                            os.stat(entry.path).st_mtime,
                                            entry.path))
            # if the item is a directory and it is not in the ignore list
            elif (entry.is_dir() and (entry.name not in self.ignore)):
                # then store it in the directory's children list
                directory.children.append(Directory(entry.name, 
                                                    os.stat(entry.path).st_mtime,
                                                    entry.path))
                # build the filesystem for the subdirectory
                self.build_tree(entry.path, directory.children[-1])
    
    
    def print_tree(self, directory):
        '''
        Print the filesystem

        directory --> Directory object
        '''
        print("------- " + directory.name + " /", directory.timestamp, "/", directory.path, " -------")
        # loop over all the files
        for entry in directory.files:
            print(entry.name, "\t", entry.timestamp)
        # loop over all the subdirectories
        for entry in directory.children:
            print(entry.name)
        
        for entry in directory.children:
            # print subdirectory
            self.print_tree(entry)
        

if __name__ == "__main__":
    HOME = os.environ['HOME']
    f = Filesystem(HOME + '/Desktop/test')
