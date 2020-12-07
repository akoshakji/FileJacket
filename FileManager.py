import os
import os.path as path
import pickle

from Directory import Directory
from File import File

class FileManager:
    
    '''File Manager
    
    It is in charge to learn and store the structure of
    the file system
    
    root    --> root directory
    current --> current directory
    '''
    
    def __init__(self, 
                 localpath, 
                 ignore=['build', '.DS_Store', '.localized', 'builds', 'products']):
        
        name = path.basename(localpath)
        timestamp = os.stat(localpath).st_mtime
        root = Directory(name, timestamp)
        
        self.root = root
        self.current = root
        self.ignore = ignore
        
        self.build_tree(localpath, self.root)
    
    def build_tree(self, localpath, directory):
        
        print("Building tree.. (directory: ", directory.name, ")")
        for entry in os.scandir(localpath):
            if (entry.is_file() and (entry.name not in self.ignore)):
                directory.files.append(File(entry.name, os.stat(entry.path).st_mtime))
            elif (entry.is_dir() and (entry.name not in self.ignore)):
                directory.children.append(Directory(entry.name, os.stat(entry.path).st_mtime))
                self.build_tree(entry.path, directory.children[-1])
    
    def check_tree(self, tree_pickled, directory=None):
        print("Checking tree..")
        if not directory:
            assert(self.root.name == tree_pickled.root.name)
            directory = self.root
        
        for entry_file in directory.files:
            if (entry_file in tree_pickled.current.files):
                print("File Found (check timestamp)", entry_file.name)
            else:
                print("File Not Found, create it..", entry_file.name)
        
        for entry_dir in directory.children:
            if (entry_dir in tree_pickled.current.children):
                print("Dir Found", entry_dir.name)
                tree_pickled.current = entry_dir
                self.check_tree(tree_pickled, entry_dir)
            else:
                print("Dir Not Found, create it ...")
            
    def print_tree(self, directory):
        print("------- " + directory.name + " /", directory.timestamp, " -------")
        self.print_files(directory)
        for entry in directory.children:
            print(entry.name)
            self.print_tree(entry)

    def print_files(self, directory):
        for entry in directory.files:
            print(entry.name, "\t", entry.timestamp)

if __name__ == "__main__":
    HOME = os.environ['HOME']
    f = FileManager(HOME + '/Desktop/test')

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
    
    f.check_tree(f_unpickled)