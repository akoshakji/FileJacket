import os
import pickle

from Filesystem import Filesystem

class Synchronizer:
    
    def __init__(self, fs_local, fs_pickled):
        assert fs_local.root.name == fs_pickled.root.name # what if renamed?
        self.fs_local = fs_local
        self.fs_pickled = fs_pickled
    
    def compare_filesystems(self, 
                            dir1=None, dir2=None):
        print("Checking file system..")
        if (dir1 is None) and (dir2 is None):
            dir1 = self.fs_local.current
            dir2 = self.fs_pickled.current

        for entry_file in dir1.files:
            if entry_file in dir2.files:
                index = dir2.files.index(entry_file)
                if entry_file == dir2.files[index]:
                    print(entry_file.name, entry_file.timestamp, entry_file.path)
                    print("Files are the same", entry_file.name)
                    continue
            print("File Not Found, upload it..", entry_file.name)
            # upload the file
            #self.upload_file(entry_file)

        for entry_dir in dir1.children:
            if entry_dir in dir2.children:
                print("Dir are the same", entry_dir.name)
            elif any(entry_dir.path in x.path for x in dir2.children):
                print("Dir found but are not the same, enter and upload files..", entry_dir.name)
                self.fs_local.current = entry_dir
                
                index = [i for i,x in enumerate(dir2.children) if x.path==entry_dir.path][0]
                self.fs_pickled.current = dir2.children[index]
                
                self.compare_filesystems(self.fs_local.current, self.fs_pickled.current)
            else:
                print("Dir Not Found, create it, and upload all of its contents...", entry_dir.name)
                #self.upload_directory(entry_dir)
        
    def upload_file(self, item):
        print("File", item.name, "Uploaded!")
        # with open(entry, 'rb') as file:
                #     print("[+]", entry.name)
                #     try:
                #         dbx.files_upload(file.read(), dbx_item_path, mode=WriteMode.overwrite)
                #     except ApiError as err:
                #         if err.user_message_text:
                #             print(err.user_message_text)
                #             sys.exit()
                #         else:
                #             print(err)
                #             sys.exit()
    
    def upload_directory(self, item):
        print("Creating Directory", item.name, "..")   


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
    localpath = HOME + '/Desktop/test'
    fs = Filesystem(localpath)
    pickle_file_name = os.path.basename(localpath) + ".pickle"

    try:
        fs_pickled = load_pickle(pickle_file_name)
        fs_pickled.print_tree(fs_pickled.root)
    except (OSError, IOError) as err:
        dump_pickle(fs, pickle_file_name)

    sync = Synchronizer(fs, fs_pickled)
    sync.compare_filesystems()
