import os

from Filesystem import Filesystem
from DropboxManager import DropboxManager
from helpers import dump_pickle, load_pickle

class Synchronizer:
    '''
    Class that synchronizes local directories with the remote server.

    The local filesystem of the target directory is compared with the
    previous state of the filesystem of the same directory, which has
    been saved in a pickle. This choice aims to limit to the minimum
    the communication with the remote server, the most time consuming part
    and connection dependent.

    Files or directories on the remote that are not present locally are cleaned
    from the remote.

    Underlying assumption: The remote filesystem is a mirror of the local filesystem.
    Therefore, directories on the remote should not be modified manually.
    If that happens, the modifications will not be reflected in the pickled filesystem
    and this could lead to errors during synchronization.
    '''


    def __init__(self, fs_local, prefix_remote='/'):
        # local filesystem
        self.fs_local = fs_local
        # previous state of the filesystem
        self.fs_pickled = None
        # base path
        self.base_path = os.path.dirname(fs_local.root.path)
        # list of paths of files or directories to delete
        self.list_to_delete = []

        #TODO move all dropbox objects and introduce abstraction
        # access token
        ACCESS_TOKEN = ""
        # prefix path to the remote root directory
        self.dbx_prefix = prefix_remote
        # root directory
        root_dir = os.path.basename(fs_local.root.path)
        # path to remote root directory
        dbx_root_dir = self.dbx_prefix + root_dir
        # start DropboxManager
        self.dbx = DropboxManager(ACCESS_TOKEN, dbx_root_dir)

        # if the remote root directory does not exist
        if not self.check_directory_exists(dbx_root_dir):
            # upload it entirely
            self.upload_directory(fs_local.root)

        pickle_file_name = root_dir + ".pickle"
        if not os.path.isfile(pickle_file_name):
            print("Pickle does not exist, creating it..")
            self.update_fs_pickle()
            self.fs_pickled = self.load_fs_pickle()
        else:
            print("Pickle found, loading it..")
            self.fs_pickled = self.load_fs_pickle()
            print("---------------------")
            print("Filesystem Pickled:")
            self.fs_pickled.print_tree(self.fs_pickled.root)


    def synchronize(self):
        # check that fs_pickle is not null
        assert self.fs_pickled is not None
        # check that the remote root directory is the same
        assert self.fs_local.root.name == self.fs_pickled.root.name # TODO: what if renamed?

        print("Checking filesystem..")
        self.sync(self.fs_local.root, self.fs_pickled.root)
        self.clean()
        self.update_fs_pickle()


    def sync(self, dir1, dir2):
        '''
        Synchronize local filesystem on the remote

        dir1 ----> directory in the local filesystem
        dir2 ----> directory in the pickled filesystem
        '''
        # loop over all local files
        for entry_file in dir1.files:
            # if the file is present in dir2
            if entry_file in dir2.files:
                print("Files are the same", entry_file.name)
                continue
            # if the file is not present in dir2, upload it
            print("Uploading File..", entry_file.name)
            # upload the file
            self.upload_file(entry_file)

        # loop over all local subdirectories
        for entry_dir in dir1.children:
            # if the path of subdirectory exists in dir2
            if any(entry_dir.path == x.path for x in dir2.children):
                print("Dir found, enter and check subfolders files..", entry_dir.name)
                #dir1 = entry_dir

                # retrieve the index of the subdirectory
                index = [i for i,x in enumerate(dir2.children) if x.path==entry_dir.path][0]
                #dir2 = dir2.children[index]

                # synchronize the subdirectory
                self.sync(entry_dir, dir2.children[index])
                #self.sync(self.fs_pickled, dir1, dir2)
            else:
                # the directory is not on the remote
                print("Dir Not Found, create it, and upload all of its contents...", entry_dir.name)
                # upload the directory
                self.upload_directory(entry_dir)


    def upload_file(self, file_item):
        '''
        Upload local file
        '''
        # path on the remote
        dbx_item_path = self.get_remote_path(file_item.path)
        # upload the file
        self.dbx.upload_file(file_item, dbx_item_path)
        print("File", file_item.name, "Uploaded!")


    def upload_directory(self, directory_item):
        '''
        Upload local directory
        '''
        print("Creating directory on dropbox", directory_item.name, "..")
        # path on the remote
        dbx_item_path = self.get_remote_path(directory_item.path)
        # create the directory on the remote
        self.dbx.create_directory(dbx_item_path)

        # upload all files
        for entry_file in directory_item.files:
            print("Uploading", entry_file.name, "..")
            self.upload_file(entry_file)

        # upload all subdirectories
        for entry_dir in directory_item.children:
            print("Creating subdirectory..")
            self.upload_directory(entry_dir)


    def check_directory_exists(self, dbx_item_path):
        '''
        Check that the directory exists on the remote
        '''
        return self.dbx.check_directory_exists(dbx_item_path)


    def clean(self):
        '''
        Clean the files on the remote that are not present locally
        '''
        # fill the list of files or directories to delete
        print("Filling delete list..")
        self.fill_delete_list(self.fs_local.root, self.fs_pickled.root)

        # if the list is not null
        if self.list_to_delete:
            print("List of files to delete:", self.list_to_delete)
            # get the corresponding path on the remote
            self.list_to_delete = map(self.get_remote_path, self.list_to_delete)
            # then clean
            self.dbx.clean(self.list_to_delete)
        else:
            print("Nothing to clean!")


    def get_remote_path(self, item_path):
        '''
        Get the path on the remote given the local path
        '''
        return self.dbx_prefix + os.path.relpath(item_path, self.base_path)


    def fill_delete_list(self, dir1, dir2):
        '''
        Fill the list of files and directories to delete

        dir1 ----> directory in the local filesystem
        dir2 ----> directory in the pickled filesystem
        '''
        # loop over the subdirectories of dir2
        for entry_dir in dir2.children:
            # if the path of the subdirectory does not exist in dir1 subdirectories
            if not any(entry_dir.path == x.path for x in dir1.children):
                # add the path to the list to delete
                self.list_to_delete.append(entry_dir.path)
            else:
                # otherwise, retrieve the index of the subdirectory
                index = [i for i,x in enumerate(dir1.children) if x.path==entry_dir.path][0]
                # check recursively if the subdirectory contains items to delete
                self.fill_delete_list(dir1.children[index], entry_dir)

        # loop over the files in dir2
        for entry_file in dir2.files:
            # if the file is not present
            if not any(entry_file.path == x.path for x in dir1.files):
                # add the path of the file to the list
                self.list_to_delete.append(entry_file.path)


    def update_fs_pickle(self):
        pickle_file_name = os.path.basename(self.fs_local.root.path) + ".pickle"
        dump_pickle(self.fs_local, pickle_file_name)


    def load_fs_pickle(self):
        pickle_file_name = os.path.basename(self.fs_local.root.path) + ".pickle"
        return load_pickle(pickle_file_name)


if __name__ == "__main__":
    HOME = os.environ['HOME']
    localpath = HOME + '/Desktop/' + 'test'
    fs = Filesystem(localpath)
    print("---------------------")
    print("Filesystem:")
    fs.print_tree(fs.root)

    sync = Synchronizer(fs)
    sync.synchronize() # TODO: create Exception for this case
