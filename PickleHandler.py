import os
import sys
import pickle

class PickleHandler:
    def __init__(self, pickle_file_name,
                 pickle_dir='pickles/',
                 prefix=''):
        try:
            os.makedirs(pickle_dir)
        except FileExistsError:
            # directory already exists
            pass

        pickle_file_name = pickle_file_name + ".pickle"
        
        if not prefix or os.path.isdir(prefix):
            self.pickle_path = prefix + pickle_dir + pickle_file_name
        else:
            print("PickleHandler - Error: "
                  "Please specify a regular prefix (path to pickle dir or empty string)")
            sys.exit()


    def get_pickle_path(self):
        return self.pickle_path


    def dump_pickle(self, py_object):
        '''
        Dump pickle of Python object
        '''
        print("Dumping pickle in", self.pickle_path, "..")
        with open(self.pickle_path, 'wb') as file:
            # Pickle the 'data' dictionary using the highest protocol available.
            pickle.dump(py_object, file, pickle.HIGHEST_PROTOCOL)


    def load_pickle(self):
        '''
        Unpickle Python object
        '''
        with open(self.pickle_path, 'rb') as file:
            print("Unpickling", self.pickle_path, "..")
            # The protocol version used is detected automatically, so we do not
            # have to specify it.
            return pickle.load(file)


if __name__ == "__main__":
    ph = PickleHandler('test.pickle')
    fs = ph.load_pickle()
    fs.print_tree(fs.root)