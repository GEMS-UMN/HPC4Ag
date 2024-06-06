import pickle

def save_pickle(obj, filepath):
    """
    Saves the given object to a file using pickle serialization.

    Parameters:
        obj (object): The object to be serialized and saved to the file.
        filepath (str): The path to the file where the object will be saved.

    Returns:
        None
    """
    pickle.dump(obj, open(filepath, "wb"))

def load_pickle(filepath):
    """
    Loads an object from a file using pickle deserialization.

    Parameters:
        filepath (str): The path to the file from which the object will be loaded.

    Returns:
        object: The object loaded from the file.
    """
    return pickle.load(open(filepath, "rb"))