import sys

import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

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


    def upload_file(self, file_item, dbx_item_path):
        print(file_item.path, dbx_item_path)
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
        print(dbx_item_path)
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
        # check if the directory exists
        try:
            self.dbx.files_list_folder(dbx_item_path)
            return True
        except ApiError:
            # if the directory does not exist, say it
            print("Directory does not exist yet")
        
        return False


    # def clean(self, dbx_item_path, local_paths):
    #     print("Cleaning up " + dbx_item_path)
    #     for entry in self.dbx.files_list_folder(dbx_item_path).entries:
    #         print(entry.path_lower)
    #         if not entry.path_lower in local_paths:
    #             # delete the item
    #             print("[-] Deleting", entry.path_lower)
    #             try:
    #                 self.dbx.files_delete(entry.path_lower)
    #             except ApiError as err:
    #                 if err.user_message_text:
    #                     print(err.user_message_text)
    #                     sys.exit()
    #                 else:
    #                     print(err)
    #                     sys.exit()
    #         # if the item is a directory
    #         elif isinstance(entry, dropbox.files.FolderMetadata):
    #             # clean the directory
    #             self.clean(entry.path_lower, local_paths)


if __name__ == "__main__":
    ACCESS_TOKEN = ""
    dbx_root_dir = '/test'
    dbx = DropboxManager(ACCESS_TOKEN, dbx_root_dir)
