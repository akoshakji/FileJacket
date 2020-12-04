import os
import os.path as path
import re

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
        
        self.print_subdirectories(directory)
    
    def print_tree(self):
        pass
    
    def print_subdirectories(self, directory):
        print("------- " + directory.name + " /", directory.timestamp, " -------")
        for entry in directory.children:
            print(entry.name)
        self.print_files(directory)
            
    def print_files(self, directory):
        for entry in directory.files:
            print(entry.name, "\t", entry.timestamp)

if __name__ == "__main__":
    HOME = os.environ['HOME']
    f = FileManager(HOME + '/Desktop/test')
