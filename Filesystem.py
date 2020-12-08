import os
import os.path as path
import pickle

from Directory import Directory
from File import File

class Filesystem:
    '''File Manager

    It is in charge to build the structure of the filesystem

    root    --> root directory
    current --> current directory, used for navigation purposes
    ignore  --> ignore list of files/directories
    '''
    def __init__(self,
                 localpath,
                 ignore=('build', '.DS_Store', '.localized', 'builds', 'products')):

        name = path.basename(localpath)
        timestamp = os.stat(localpath).st_mtime
        root = Directory(name, timestamp)

        # root directory
        self.root = root
        # current directory
        self.current = root
        # files or directories to ignore
        self.ignore = ignore

        # build the filesystem
        self.build_tree(localpath, self.root)


    def build_tree(self, localpath, directory):
        '''Build the filesystem given a path to a local file/directory

        localpath --> path to a local file/directory
        directory --> Directory object
        '''
        print("Building tree.. (directory: " + directory.name + ")")
        # loop over all the items in the local directory
        for entry in os.scandir(localpath):
            # if the item is a file and it is not in the ignore list
            if (entry.is_file() and (entry.name not in self.ignore)):
                # then store it in the directory's files list
                directory.files.append(File(entry.name, os.stat(entry.path).st_mtime))
            # if the item is a directory and it is not in the ignore list
            elif (entry.is_dir() and (entry.name not in self.ignore)):
                # then store it in the directory's children list
                directory.children.append(Directory(entry.name, os.stat(entry.path).st_mtime))
                # build the filesystem for the subdirectory
                self.build_tree(entry.path, directory.children[-1])


    def print_tree(self, directory):
        '''Print the filesystem

        directory --> Directory object
        '''
        print("------- " + directory.name + " /", directory.timestamp, " -------")
        # loop over all the files
        for entry in directory.files:
            print(entry.name, "\t", entry.timestamp)
        # loop over all the subdirectories
        for entry in directory.children:
            print(entry.name)
            # print subdirectory
            self.print_tree(entry)


if __name__ == "__main__":
    HOME = os.environ['HOME']
    f = Filesystem(HOME + '/Desktop/test')

    print("Dumping pickle..")
    with open('tree.pickle', 'wb') as file: # pickle file name should be the same as principal dir
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(f, file, pickle.HIGHEST_PROTOCOL)

    print("Unpickling..")
    with open('tree.pickle', 'rb') as file:
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
        f_unpickled = pickle.load(file)

    f_unpickled.print_tree(f_unpickled.root)