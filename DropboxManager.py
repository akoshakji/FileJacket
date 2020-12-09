import os
import sys

import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

from Filesystem import Filesystem

class DropboxManager:


    def __init__(self, access_token, root_dbx):
        self.dbx = dropbox.Dropbox(access_token)
        #root_dbx # TODO: check if the folder exists. Better to use a setter

        # check that the access token is valid
        try:
            self.dbx.users_get_current_account()
        except AuthError:
            sys.exit("ERROR: Invalid access token; try re-generating an "
                     "access token from the app console on the web.")


    def upload_on_dbx(self, localpath, backuppath):

        '''Upload files to Dropbox'''

        print("Uploading " + localpath + " in " + backuppath)

        # loop over the local directories/files
        for entry in os.scandir(localpath):
            # path to the corresponding item on dropbox
            dbx_item_path = os.path.join(backuppath, entry.name)
            # store the item's path
            self.list_of_files.append(dbx_item_path)
            # if the item is a file
            if entry.is_file():
                # upload the file
                with open(entry, 'rb') as file:
                    print("[+]", entry.name)
                    try:
                        dbx.files_upload(file.read(), dbx_item_path, mode=WriteMode.overwrite)
                    except ApiError as err:
                        if err.user_message_text:
                            print(err.user_message_text)
                            sys.exit()
                        else:
                            print(err)
                            sys.exit()
            # if the item is a directory
            if entry.is_dir():
                # check if the directory exists
                try:
                    dbx.files_list_folder(dbx_item_path)
                except ApiError:
                    # if the directory does not exist, create it
                    print("[+] Creating new directory")
                    try:
                        dbx.files_create_folder(dbx_item_path)
                    except ApiError as err:
                        if err.user_message_text:
                            print(err.user_message_text)
                            sys.exit()
                        else:
                            print(err)
                            sys.exit()
                print("[+] Folder", entry.name)
                # upload the directory
                self.upload_on_dbx(dbx, entry.path, dbx_item_path)


    def upload_file(self, file_item, dbx_item_path):
        with open(file_item.path, 'rb') as file:
            print("[+]", file_item.name)
            try:
                self.dbx.files_upload(file.read(), dbx_item_path, mode=WriteMode.overwrite)
            except ApiError as err:
                if err.user_message_text:
                    print(err.user_message_text)
                    sys.exit()
                else:
                    print(err)
                    sys.exit()
    
    
    def create_directory(self, dbx_item_path):
        print("[+] Creating new directory")
        try:
            self.dbx.files_create_folder(dbx_item_path)
        except ApiError as err:
            if err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()


    def clean(self, dbx_item_path, local_paths):
        print("Cleaning up " + dbx_item_path)
        for entry in self.dbx.files_list_folder(dbx_item_path).entries:
            print(entry.path_lower)
            if not entry.path_lower in local_paths:
                # delete the item
                print("[-] Deleting", entry.path_lower)
                try:
                    self.dbx.files_delete(entry.path_lower)
                except ApiError as err:
                    if err.user_message_text:
                        print(err.user_message_text)
                        sys.exit()
                    else:
                        print(err)
                        sys.exit()
            # if the item is a directory
            elif isinstance(entry, dropbox.files.FolderMetadata):
                # clean the directory
                self.clean(entry.path_lower, local_paths)


    def clean_up(self, backuppath):

        '''Clean up files on Dropbox'''

        print("Cleaning up " + backuppath)

        # loop over the items on dropbox
        for entry in self.dbx.files_list_folder(backuppath).entries:
            # path to the corresponding item on dropbox
            dbx_item_path = os.path.join(backuppath, entry.name)
            # if the item is not in the list of uploaded files
            if not dbx_item_path in self.list_of_files:
                # delete the item
                print("[-] Deleting", dbx_item_path)
                try:
                    self.dbx.files_delete(dbx_item_path)
                except ApiError as err:
                    if err.user_message_text:
                        print(err.user_message_text)
                        sys.exit()
                    else:
                        print(err)
                        sys.exit()
            # if the item is a directory
            elif isinstance(entry, dropbox.files.FolderMetadata):
                # clean the directory
                self.clean_up(dbx_item_path)


if __name__ == "__main__":
    ACCESS_TOKEN = ""
    dbx_root_dir = '/test'
    dbx = DropboxManager(ACCESS_TOKEN, dbx_root_dir)
