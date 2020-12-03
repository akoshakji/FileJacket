#!/usr/bin/env python3

# Documentation on Dropbox - Python API
# https://dropbox-sdk-python.readthedocs.io/en/latest/index.html

import os
import os.path as path
import sys

import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

# home directory path
HOME = os.environ['HOME']
# list of directories/files to be uploaded
#FILES = ['Desktop', 'dv', 'sim', '.profile', '.mm']
FILES = ['test']
# list of directories/files to be ignored
IGNORE = ['.DS_Store', '.localized', 'build', 'builds', 'products']
#LOCALPATH = [HOME + x for x in FILES]
# list of base paths for each file/directory to be uploaded
BASEPATH = [path.join(HOME, "Desktop")]
# list of local paths to be uploaded
LOCALPATH = [path.join(BASEPATH[0], FILES[0])]

# backup path on dropbox
DROPBOXPATH = '/test-backup'
BACKUPPATH = [path.join(DROPBOXPATH, FILES[0])]

# dropbox access token
ACCESS_TOKEN = 'HERE YOUR TOKEN'

def upload_on_dbx(dbx, localpath, backuppath):

    '''Upload files to Dropbox'''

    print("Uploading " + localpath + " in " + backuppath)

    global list_of_files

    # loop over the local directories/files
    for entry in os.scandir(localpath):
        # path to the corresponding item on dropbox
        dbx_item_path = path.join(backuppath, entry.name)
        # store the item's name
        list_of_files.append(dbx_item_path)
        # if the item is a file and is not in the ignore list
        if (entry.is_file() and (entry.name not in IGNORE)):
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
        # if the item is a directory and is not in the ignore list
        if (entry.is_dir() and (entry.name not in IGNORE)):
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
            upload_on_dbx(dbx, entry.path, dbx_item_path)

def clean_up(dbx, backuppath):

    '''Clean up files on Dropbox'''

    print("Cleaning up " + backuppath)

    # loop over the items on dropbox
    for entry in dbx.files_list_folder(backuppath).entries:
        # path to the corresponding item on dropbox
        dbx_item_path = path.join(backuppath, entry.name)
        # if the item is not in the list of uploaded files
        if not dbx_item_path in list_of_files:
            # delete the item
            print("[-] Deleting", dbx_item_path)
            try:
                dbx.files_delete(dbx_item_path)
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
            clean_up(dbx, dbx_item_path)

# create an instance of a dropbox class, which can make requests to the API.
print("Creating a Dropbox object...")
with dropbox.Dropbox(ACCESS_TOKEN) as dbx:
    # check that the access token is valid
    try:
        dbx.users_get_current_account()
    except AuthError:
        sys.exit("ERROR: Invalid access token; try re-generating an "
                     "access token from the app console on the web.")

    # container for uploaded local files names
    list_of_files = []

    # upload local files on Dropbox
    upload_on_dbx(dbx, LOCALPATH[0], BACKUPPATH[0])

    # update list of uploaded files, removing duplicates and base folder name
    list_of_files = sorted(set(list_of_files))[2:]

    # clean from dropbox all the files that are not present on the local system
    clean_up(dbx, BACKUPPATH[0])

print("all done!")
