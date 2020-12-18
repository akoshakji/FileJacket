import sys

import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

class DropboxManager:
    '''
    Class that manages all the interactions with Dropbox
    '''
    def __init__(self, access_token, root_dbx):
        # dropbox object
        self.dbx = dropbox.Dropbox(access_token)
        #root_dbx # TODO: check if the folder exists. Better to use a setter

        # check that the access token is valid
        try:
            self.dbx.users_get_current_account()
        except AuthError:
            sys.exit("ERROR: Invalid access token; try re-generating an "
                     "access token from the app console on the web.")


    def upload_file(self, file_item, dbx_item_path):
        '''
        Upload file on Dropbox
        '''
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
        '''
        Create a new directory on Dropbox
        '''
        print("[+] Creating new directory", dbx_item_path)
        try:
            self.dbx.files_create_folder(dbx_item_path)
        except ApiError as err:
            if err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()


    def clean(self, list_to_delete):
        '''
        Clean files or directories on Dropbox
        '''
        for entry in list_to_delete:
            # delete the item
            print("[-] Deleting", entry)
            try:
                self.dbx.files_delete(entry)
            except ApiError as err:
                if err.user_message_text:
                    print(err.user_message_text)
                    sys.exit()
                else:
                    print(err)
                    sys.exit()


    def check_directory_exists(self, dbx_item_path):
        '''
        Check if a directory exists on Dropbox
        '''
        # check if the directory exists
        try:
            self.dbx.files_list_folder(dbx_item_path)
            return True
        except ApiError:
            # if the directory does not exist, say it
            print("Directory does not exist yet")
        
        return False


if __name__ == "__main__":
    ACCESS_TOKEN = ""
    dbx_root_dir = '/test'
    dbx = DropboxManager(ACCESS_TOKEN, dbx_root_dir)
