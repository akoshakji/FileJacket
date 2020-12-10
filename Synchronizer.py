import os
import pickle

from Filesystem import Filesystem
from DropboxManager import DropboxManager

class Synchronizer:
    
    def __init__(self, fs_local, fs_pickled):
        assert fs_local.root.name == fs_pickled.root.name # TODO: what if renamed?
        self.fs_local = fs_local
        self.fs_pickled = fs_pickled
        self.root_base_path = os.path.dirname(fs_local.root.path)
        
        ACCESS_TOKEN = ""
        self.dbx_prefix = '/'
        dbx_root_dir = self.dbx_prefix + os.path.basename(fs_local.root.path)
        self.dbx = DropboxManager(ACCESS_TOKEN, dbx_root_dir)


    def compare_filesystems(self, dir1=None, dir2=None):
        print("Checking filesystem..")
        if (dir1 is None) and (dir2 is None):
            dir1 = self.fs_local.root
            dir2 = self.fs_pickled.root

        for entry_file in dir1.files:
            if entry_file in dir2.files:
                print("Files are the same", entry_file.name)
                continue
            print("File Not Found, uploading it..", entry_file.name)
            # upload the file
            self.upload_file(entry_file)

        for entry_dir in dir1.children:
            if entry_dir in dir2.children:
                print("Dir are the same", entry_dir.name)
            elif any(entry_dir.path in x.path for x in dir2.children):
                print("Dir found but are not the same, enter and upload files..", entry_dir.name)
                dir1 = entry_dir
                
                index = [i for i,x in enumerate(dir2.children) if x.path==entry_dir.path][0]
                dir2 = dir2.children[index]
                
                self.compare_filesystems(dir1, dir2)
            else:
                print("Dir Not Found, create it, and upload all of its contents...", entry_dir.name)
                self.upload_directory(entry_dir)


    def upload_file(self, file_item):
        dbx_item_path = self.get_remote_path(file_item.path)
        self.dbx.upload_file(file_item, dbx_item_path)
        print("File", file_item.name, "Uploaded!")


    def upload_directory(self, directory_item):
        print("Creating directory on dropbox", directory_item.name, "..")
        dbx_item_path = self.get_remote_path(directory_item.path)
        self.dbx.create_directory(dbx_item_path)
        
        for entry_file in directory_item.files:
            print("Uploading", entry_file.name, "..")
            self.upload_file(entry_file)

        for entry_dir in directory_item.children:
            print("Creating subdirectory..")
            self.upload_directory(entry_dir)
    
    
    def clean(self):
        dbx_item_path = self.get_remote_path(self.fs_local.root.path)
        dbx_local_paths = [self.get_remote_path(x) for x in self.fs_local.list_of_files_path]
        self.dbx.clean(dbx_item_path, dbx_local_paths)
    
    
    def get_remote_path(self, item_path):
        return self.dbx_prefix + os.path.relpath(item_path, self.root_base_path)


def dump_pickle(filesystem, pickle_file_name):
    print("Dumping pickle..")
    with open(pickle_file_name, 'wb') as file: # pickle file name should be the same as principal dir
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(filesystem, file, pickle.HIGHEST_PROTOCOL)


def load_pickle(pickle_file_name):
    print("Unpickling..")
    with open(pickle_file_name, 'rb') as file:
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
        return pickle.load(file)


if __name__ == "__main__":
    HOME = os.environ['HOME']
    localpath = HOME + '/Desktop/' + 'test'
    fs = Filesystem(localpath)
    pickle_file_name = os.path.basename(localpath) + ".pickle"
    # TODO: control where the pickle is created. Check also if it already exists and ask if overwrite

    try:
        # load existing pickle
        fs_pickled = load_pickle(pickle_file_name)
        sync = Synchronizer(fs, fs_pickled)
        try:
            sync.compare_filesystems() # TODO: create Exception for this case
            sync.clean()
        except:
            raise
        else:
            # update pickle
            # dump_pickle(fs, pickle_file_name)
            pass
    except (OSError, IOError) as err:
        # pickle does not exists, create it
        dump_pickle(fs, pickle_file_name)
