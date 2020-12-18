'''
Helper functions
'''

import pickle

def dump_pickle(py_object, pickle_file_name):
    '''
    Dump pickle of Python object
    '''
    print("Dumping pickle..")
    with open(pickle_file_name, 'wb') as file:
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(py_object, file, pickle.HIGHEST_PROTOCOL)


def load_pickle(pickle_file_name):
    '''
    Unpickle Python object
    '''
    with open(pickle_file_name, 'rb') as file:
        print("Unpickling..")
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
        return pickle.load(file)