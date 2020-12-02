import os
import os.path as path
import re

from Directory import Directory
from File import File

class FileManager:
    
    '''File Manager
    
    It is in charge to learn and store the structure of
    the file system
    
    root    --> root folder
    current --> current folder
    '''
    
    def __init__(self, 
                 localpath, 
                 ignore=['build', '.DS_Store', '.localized', 'builds', 'products']):
        
        name = path.basename(localpath)
        size = self.compute_size(localpath)
        root = Directory(name, size)
        
        self.root = root
        self.current = root
        self.ignore = ignore
        
        self.build_tree(localpath, self.root)
    
    def build_tree(self, localpath, directory):
        
        print("Building tree..")
        for entry in os.scandir(localpath):
            if (entry.is_file() and (entry.name not in self.ignore)):
                directory.files.append(File(entry.name, entry.stat().st_size))
            elif (entry.is_dir() and (entry.name not in self.ignore)):
                size = self.compute_size(entry.path)
                directory.subfolders.append(Directory(entry.name, size))
                self.build_tree(entry.path, directory.subfolders[-1])
        
        print("------- " + directory.name + " /", directory.size, " -------")
        self.print_subdirectories(directory)
    
    def print_tree(self):
        pass
    
    def print_subdirectories(self, directory):
        for entry in directory.subfolders:
            print(entry.name)
        self.print_files(directory)
            
    def print_files(self, directory):
        for entry in directory.files:
            print(entry.name, "\t", entry.size)
    
    def compute_size(self, filename):
        du_string = os.popen("du " + filename.replace(" ", "\ ")).read()[:-1]
        pattern = re.compile("^([0-9]*)")
        match = pattern.match(du_string)
        if match:
            file_size = int(match.group(0))
        return file_size

if __name__ == "__main__":
    HOME = os.environ['HOME']
    f = FileManager(HOME + '/Desktop/test')
