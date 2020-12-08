import os
import pickle

from Filesystem import Filesystem

def compare_filesystems(fs_local, fs_pickled, dir1=None, dir2=None):
    print("Checking file system..")
    assert fs_local.root.name == fs_pickled.root.name
    if (dir1 is None) and (dir2 is None):
        dir1 = fs_local.current
        dir2 = fs_pickled.current

    for entry_file in dir1.files:
        if entry_file in dir2.files:
            print("File Found (check timestamp)", entry_file.name)
            index = dir2.files.index(entry_file)
            if entry_file == dir2.files[index]:
                print("Files are equal")
                # move on
                continue
            else:
                print("Files are not equal, please upload")
                upload_file(entry_file)
        else:
            print("File Not Found, create it..", entry_file.name)

    for entry_dir in dir1.children:
        if entry_dir in dir2.children:
            print("Dir Found", entry_dir.name)
            fs_local.current = fs_pickled.current = entry_dir
            compare_filesystems(fs_local, fs_pickled, fs_local.current, fs_pickled.current)
        else:
            print("Dir Not Found, create it, and upload all of its contents...", entry_dir.name)
            upload_new_directory(entry_dir)


def upload_file(item):
    pass


def upload_new_directory(item):
    pass


def clean():
    pass


if __name__ == "__main__":
    HOME = os.environ['HOME']
    localpath = HOME + '/Desktop/test'
    fs = Filesystem(localpath)

    try:
        with open('filesystem.pickle', 'rb') as file:
            # The protocol version used is detected automatically, so we do not
            # have to specify it.
            print("Unpickling..")
            fs_pickled = pickle.load(file)
            fs_pickled.print_tree(fs_pickled.root)
    except (OSError, IOError) as err:
        print("Dumping pickle..")
        with open('filesystem.pickle', 'wb') as file: # pickle file name should be the same as principal dir
            # Pickle the 'data' dictionary using the highest protocol available.
            pickle.dump(fs, file, pickle.HIGHEST_PROTOCOL)

    try:
        compare_filesystems(fs, fs_pickled)
    except NameError:
        pass
